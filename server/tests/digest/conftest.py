"""Fixtures for digest module tests."""

import os
from datetime import datetime, timedelta
from typing import Tuple

# Set env vars BEFORE importing app modules (which instantiate Settings at import time)
os.environ.setdefault("API_FOOTBALL_KEY", "test_key_12345")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("ENV", "test")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db_base.base import Base
from app.modules.digest.repository.models.notification_event_digest import (
    EntityType,
    EventType,
    NotificationEvent,
)
from app.modules.digest.repository.models.subscriber import Subscriber
from app.modules.digest.repository.models.subscription import Subscription

# Import DigestRun to ensure it's registered with Base
from app.modules.digest.repository.models.digest_run_digest import DigestRun


@pytest.fixture
def db_session() -> Session:
    """Create an in-memory SQLite database session for testing."""
    # Use check_same_thread=False to avoid threading issues with TestClient
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use StaticPool for in-memory databases
    )
    SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def subscriber_with_events(
    db_session, request
) -> Tuple[Subscriber, Subscription, list]:
    """
    Create a test subscriber with subscription and 3 mock events.

    Returns:
        tuple: (subscriber, subscription, events)
    """
    # Use unique email based on test name
    unique_email = f"test-{request.node.name}@example.com"

    # 1. Create test subscriber
    subscriber = Subscriber(email=unique_email, isActive=True)
    db_session.add(subscriber)
    db_session.flush()

    # 2. Create subscription (watching Team #1 for injuries)
    subscription = Subscription(
        subscriber_id=subscriber.id,
        entity_id=1,
        entity_type=EntityType.TEAM,
        target_type="INJURIES",
    )
    db_session.add(subscription)
    db_session.flush()

    # 3. Create 3 mock events in the past 24 hours
    now = datetime.utcnow()
    events = [
        NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.TEAM,
            entity_id=1,
            payload={
                "player": "John Doe",
                "performance": "Excellent",
                "status": "Available",
            },
            created_at=now - timedelta(hours=12),
        ),
        NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.TEAM,
            entity_id=1,
            payload={
                "player": "Jane Smith",
                "performance": "Good",
                "status": "Available",
            },
            created_at=now - timedelta(hours=6),
        ),
        NotificationEvent(
            event_type=EventType.MATCH_COMPLETED,
            entity_type=EntityType.TEAM,
            entity_id=1,
            payload={"result": "Win", "score": "3-1", "opponent": "Team B"},
            created_at=now - timedelta(hours=2),
        ),
    ]
    db_session.add_all(events)
    db_session.commit()

    return subscriber, subscription, events
