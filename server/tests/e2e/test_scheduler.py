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
from app.scheduler.jobs import ingest_due_subscriptions_job

from .helpers import (
    E2ETracker,
    build_test_email,
    build_test_entity_id,
    utc_now,
)


@pytest.mark.asyncio
async def test_scheduler_stage_creates_events_for_due_subscriptions(
    db_session: Session,
    e2e_tracker: E2ETracker,
):
    subscriber_repo = SQLSubscriberRepository(db_session)
    subscription_repo = SQLSubscriptionRepository(db_session)
    event_repo = SQLEventRepository(db_session)

    subscriber = subscriber_repo.create(email=build_test_email(), is_active=True)
    e2e_tracker.track_subscriber(subscriber.id)

    entity_id = build_test_entity_id()
    e2e_tracker.track_entity(entity_id)
    now = utc_now()

    due_subscription = Subscription(
        subscriber_id=subscriber.id,
        entity_id=entity_id,
        entity_type=EntityType.PLAYER,
        target_type="player_performance",
        next_run=now - timedelta(minutes=5),
        day_freq=1,
    )
    created_subscription = subscription_repo.add(due_subscription)

    fake_stats_service = AsyncMock()
    fake_stats_service.get_player.return_value = [
        {"player_id": entity_id, "summary": "scored in test fixture"}
    ]

    await ingest_due_subscriptions_job(
        stats_service=fake_stats_service,
        event_repo=event_repo,
        subscription_repo=subscription_repo,
        now=now,
    )

    events = (
        db_session.query(NotificationEvent)
        .filter(NotificationEvent.entity_id == entity_id)
        .all()
    )

    assert len(events) >= 1
    assert events[0].entity_type == EntityType.PLAYER

    updated = subscription_repo.get_by_id(created_subscription.id)
    assert updated is not None
    assert updated.last_run is not None
    assert updated.next_run > now
