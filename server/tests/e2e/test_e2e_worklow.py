from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.orm import Session

from app.modules.digest.repository.implementations import (
    SQLEventRepository,
    SQLSubscriberRepository,
    SQLSubscriptionRepository,
)
from app.modules.digest.repository.models.enums.entity_type import EntityType
from app.modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)
from app.modules.digest.repository.models.subscription import Subscription
from app.modules.digest.service import DigestService
from app.modules.stats.service import StatsService
from app.scheduler.jobs import ingest_due_subscriptions_job
from .helpers import E2ETracker, build_test_email, build_test_entity_id, utc_now


class CapturingEmailService:
    def __init__(self) -> None:
        self.sent = []

    def send_email(self, to: str, subject: str, body: str) -> None:
        self.sent.append({"to": to, "subject": subject, "body": body})


class InMemoryDigestRunRepository:
    def __init__(self) -> None:
        self.runs = []

    def add_run(self, subscriber_id: int, period_start, status: str) -> None:
        self.runs.append(
            {
                "subscriber_id": subscriber_id,
                "period_start": period_start,
                "status": status,
            }
        )


@pytest.mark.asyncio
async def test_full_backend_workflow_search_to_email(
    db_session: Session,
    e2e_tracker: E2ETracker,
):
    # Stage 1: Search
    player_id = build_test_entity_id()
    provider = AsyncMock()
    provider.search_players.return_value = {
        "errors": [],
        "response": [
            {
                "player": {
                    "id": player_id,
                    "name": "Workflow Player",
                    "firstname": "Workflow",
                    "lastname": "Player",
                    "birth": {"date": "1990-01-01"},
                    "age": 35,
                    "photo": "https://example.test/workflow-player.png",
                    "position": "Midfielder",
                    "height": "180 cm",
                    "weight": "75 kg",
                    "nationality": "Testland",
                }
            }
        ],
    }
    stats_service = StatsService(provider)
    players = await stats_service.search_players("Workflow", limit=1)
    assert len(players) == 1
    assert players[0].id == player_id
    e2e_tracker.track_entity(player_id)

    # Stage 2: Subscribe
    subscriber_repo = SQLSubscriberRepository(db_session)
    subscription_repo = SQLSubscriptionRepository(db_session)
    event_repo = SQLEventRepository(db_session)
    digest_run_repo = InMemoryDigestRunRepository()

    subscriber = subscriber_repo.create(email=build_test_email(), is_active=True)
    e2e_tracker.track_subscriber(subscriber.id)

    now = utc_now()
    subscription = subscription_repo.add(
        Subscription(
            subscriber_id=subscriber.id,
            entity_id=player_id,
            entity_type=EntityType.PLAYER,
            target_type="player_performance",
            next_run=now - timedelta(minutes=1),
            day_freq=1,
        )
    )
    assert subscription.id is not None

    # Stage 3 + 4: Scheduler run and event creation
    scheduler_stats_service = AsyncMock()
    scheduler_stats_service.get_player.return_value = [
        {
            "player_id": player_id,
            "name": "Workflow Player",
            "event": "assist",
            "source": "e2e_workflow",
        }
    ]

    await ingest_due_subscriptions_job(
        stats_service=scheduler_stats_service,
        event_repo=event_repo,
        subscription_repo=subscription_repo,
        now=now,
    )

    events = (
        db_session.query(NotificationEvent)
        .filter(NotificationEvent.entity_id == player_id)
        .all()
    )
    assert len(events) >= 1

    # Stage 5 + 6: Digest and email
    email_service = CapturingEmailService()
    digest_service = DigestService(
        event_repo=event_repo,
        subscriber_repo=subscriber_repo,
        subscription_repo=subscription_repo,
        digest_run_repo=digest_run_repo,
        email_service=email_service,
    )

    digest_service.run_digest(
        start=now - timedelta(hours=1),
        end=utc_now() + timedelta(hours=1),
    )

    assert len(email_service.sent) == 1
    assert email_service.sent[0]["to"] == subscriber.email
    assert "assist" in email_service.sent[0]["body"]
    assert len(digest_run_repo.runs) == 1
    assert digest_run_repo.runs[0]["subscriber_id"] == subscriber.id
