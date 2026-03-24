from __future__ import annotations

from datetime import timedelta

from sqlalchemy.orm import Session

from app.modules.digest.repository.implementations import (
    SQLEventRepository,
    SQLSubscriberRepository,
    SQLSubscriptionRepository,
)
from app.modules.digest.repository.models.enums.entity_type import EntityType
from app.modules.digest.repository.models.enums.event_type import EventType
from app.modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)
from app.modules.digest.repository.models.subscription import Subscription
from app.modules.digest.service import DigestService

from .helpers import (
    E2ETracker,
    build_test_email,
    build_test_entity_id,
    utc_now,
)


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


def test_digest_stage_sends_email_and_records_run(
    db_session: Session,
    e2e_tracker: E2ETracker,
):
    subscriber_repo = SQLSubscriberRepository(db_session)
    subscription_repo = SQLSubscriptionRepository(db_session)
    event_repo = SQLEventRepository(db_session)
    digest_run_repo = InMemoryDigestRunRepository()

    subscriber = subscriber_repo.create(email=build_test_email(), is_active=True)
    e2e_tracker.track_subscriber(subscriber.id)

    entity_id = build_test_entity_id()
    e2e_tracker.track_entity(entity_id)

    subscription_repo.add(
        Subscription(
            subscriber_id=subscriber.id,
            entity_id=entity_id,
            entity_type=EntityType.PLAYER,
            target_type="player_performance",
            next_run=utc_now() + timedelta(days=1),
            day_freq=1,
        )
    )

    event_repo.add(
        NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=entity_id,
            payload={"message": "player update for digest stage"},
            created_at=utc_now(),
        )
    )

    email_service = CapturingEmailService()
    digest_service = DigestService(
        event_repo=event_repo,
        subscriber_repo=subscriber_repo,
        subscription_repo=subscription_repo,
        digest_run_repo=digest_run_repo,
        email_service=email_service,
    )

    start = utc_now() - timedelta(hours=2)
    end = utc_now() + timedelta(hours=2)
    digest_service.run_digest(start=start, end=end)

    assert len(email_service.sent) == 1
    assert email_service.sent[0]["to"] == subscriber.email
    assert "player update for digest stage" in email_service.sent[0]["body"]
    assert len(digest_run_repo.runs) == 1
    assert digest_run_repo.runs[0]["subscriber_id"] == subscriber.id
