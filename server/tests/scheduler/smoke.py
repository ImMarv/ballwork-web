"""Smoke test for scheduler ingestion job end-to-end."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.orm import Session

from app.db import SessionFactory
from app.modules.digest.repository.implementations import (
    SQLEventRepository,
    SQLSubscriptionRepository,
)
from app.modules.digest.repository.models.enums.entity_type import EntityType
from app.modules.digest.repository.models.enums.event_type import EventType
from app.modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)
from app.modules.digest.repository.models.subscriber import Subscriber
from app.modules.digest.repository.models.subscription import Subscription
from app.scheduler.jobs import ingest_due_subscriptions_job


@pytest.fixture
def test_session() -> Session:
    """Create a test session using the project's SessionFactory."""
    session = SessionFactory()
    yield session
    session.rollback()
    session.close()


@pytest.mark.asyncio
async def test_ingestion_job_smoke_end_to_end(test_session: Session):
    """
    Smoke test: Verify ingestion job works end-to-end.

    Proves:
    1. Job can run without errors
    2. Writes exactly one event row for the due subscription
    3. Advances subscription scheduling fields (last_run, next_run)
    """
    # ============ SETUP ============

    # Create subscriber
    subscriber = Subscriber(
        email="test_smoke@example.com",
        isActive=True,
        createdAt=datetime.now(timezone.utc),
    )
    test_session.add(subscriber)
    test_session.commit()
    test_session.refresh(subscriber)

    # Create a due subscription (next_run in the past)
    now = datetime.now(timezone.utc)
    subscription = Subscription(
        subscriber_id=subscriber.id,
        entity_id=123,  # fake player ID
        entity_type=EntityType.PLAYER,
        target_type="player_performance",
        next_run=now - timedelta(hours=1),  # due 1 hour ago
        last_run=None,
        day_freq=1,
        createdAt=now,
    )
    test_session.add(subscription)
    test_session.commit()
    test_session.refresh(subscription)

    # Create a fake stats service that returns one player snapshot
    fake_stats_service = AsyncMock()
    fake_stats_service.get_player.return_value = [
        {
            "id": 123,
            "name": "Test Player",
            "age": 25,
            "position": "Forward",
            "goals": 10,
            "assists": 3,
        }
    ]

    # Create repository instances
    event_repo = SQLEventRepository(session=test_session)
    subscription_repo = SQLSubscriptionRepository(session=test_session)

    # ============ EXECUTE ============
    await ingest_due_subscriptions_job(
        stats_service=fake_stats_service,
        event_repo=event_repo,
        subscription_repo=subscription_repo,
        now=now,
    )

    # ============ VERIFY ============

    # Verify 1: Event was created
    events = (
        test_session.query(NotificationEvent)
        .filter(NotificationEvent.entity_id == 123)
        .all()
    )
    assert len(events) == 1, f"Expected 1 event, got {len(events)}"
    event = events[0]
    assert event.entity_type == EntityType.PLAYER
    assert event.event_type == EventType.PLAYER_PERFORMANCE
    assert event.payload.get("name") == "Test Player"

    # Verify 2: Subscription was updated
    updated_sub = test_session.query(Subscription).filter_by(id=subscription.id).first()
    assert updated_sub is not None
    assert updated_sub.last_run is not None
    assert updated_sub.next_run > now

    # Verify 3: Stats service was called with correct args
    fake_stats_service.get_player.assert_called_once()
    call_args = fake_stats_service.get_player.call_args
    assert call_args[0][0] == 123  # player_id
