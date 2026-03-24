from __future__ import annotations

import pytest
from sqlalchemy import delete
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db_base.base import Base
from app.modules.digest.repository.models.digest_run_digest import DigestRun
from app.modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)
from app.modules.digest.repository.models.subscriber import Subscriber
from app.modules.digest.repository.models.subscription import Subscription

from .helpers import E2ETracker


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
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
def e2e_tracker(db_session: Session) -> E2ETracker:
    tracker = E2ETracker()
    try:
        yield tracker
    finally:
        if tracker.subscriber_ids:
            db_session.execute(
                delete(DigestRun).where(
                    DigestRun.subscriber_id.in_(tracker.subscriber_ids)
                )
            )
            db_session.execute(
                delete(Subscription).where(
                    Subscription.subscriber_id.in_(tracker.subscriber_ids)
                )
            )
            db_session.execute(
                delete(Subscriber).where(Subscriber.id.in_(tracker.subscriber_ids))
            )

        if tracker.entity_ids:
            db_session.execute(
                delete(NotificationEvent).where(
                    NotificationEvent.entity_id.in_(tracker.entity_ids)
                )
            )

        db_session.commit()
