from __future__ import annotations

from datetime import timedelta

from sqlalchemy.orm import Session

from app.modules.digest.repository.implementations import (
    SQLSubscriberRepository,
    SQLSubscriptionRepository,
)
from app.modules.digest.repository.models.enums.entity_type import EntityType
from app.modules.digest.repository.models.subscription import Subscription

from .helpers import (
    E2ETracker,
    build_test_email,
    build_test_entity_id,
    utc_now,
)


def test_subscribe_player_stage_persists_subscription(
    db_session: Session,
    e2e_tracker: E2ETracker,
):
    subscriber_repo = SQLSubscriberRepository(db_session)
    subscription_repo = SQLSubscriptionRepository(db_session)

    subscriber = subscriber_repo.create(email=build_test_email(), is_active=True)
    e2e_tracker.track_subscriber(subscriber.id)

    entity_id = build_test_entity_id()
    e2e_tracker.track_entity(entity_id)

    subscription = Subscription(
        subscriber_id=subscriber.id,
        entity_id=entity_id,
        entity_type=EntityType.PLAYER,
        target_type="player_performance",
        next_run=utc_now() + timedelta(minutes=1),
        day_freq=1,
    )
    created = subscription_repo.add(subscription)

    assert created.id is not None
    assert created.subscriber_id == subscriber.id
    assert created.entity_type == EntityType.PLAYER
    assert created.target_type == "player_performance"
