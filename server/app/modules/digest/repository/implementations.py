"""Concrete SQLAlchemy implementations of repository interfaces."""

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from .models.digest_run_digest import DigestRun
from .models.notification_event_digest import NotificationEvent
from .models.subscriber import Subscriber
from .models.subscription import Subscription


class SQLEventRepository:
    """SQLAlchemy implementation of EventRepository."""

    def __init__(self, session: Session):
        self.session = session

    def get_events_between(
        self, start: date | datetime, end: date | datetime
    ) -> List[NotificationEvent]:
        """Get events between a start and end date."""
        return (
            self.session.query(NotificationEvent)
            .filter(NotificationEvent.created_at >= start)
            .filter(NotificationEvent.created_at <= end)
            .all()
        )

    def get_by_id(self, event_id: int) -> NotificationEvent | None:
        """Get an event by its ID."""
        return self.session.get(NotificationEvent, event_id)

    def add(self, event: NotificationEvent) -> NotificationEvent:
        """Add a new event to the repository."""
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def get_events_for_subscriptions(
        self, subscriptions: List[Subscription]
    ) -> List[NotificationEvent]:
        """Get all events that match the given subscriptions."""
        if not subscriptions:
            return []

        # Build query with OR conditions for each subscription
        conditions = [
            and_(
                NotificationEvent.entity_type == sub.entity_type,
                NotificationEvent.entity_id == sub.entity_id,
            )
            for sub in subscriptions
        ]

        return self.session.query(NotificationEvent).filter(or_(*conditions)).all()


class SQLSubscriberRepository:
    """SQLAlchemy implementation of SubscriberRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, email: str, is_active: bool = True) -> Subscriber:
        """Create a new subscriber."""
        subscriber = Subscriber(email=email, isActive=is_active)
        self.session.add(subscriber)
        self.session.commit()
        self.session.refresh(subscriber)
        return subscriber

    def get_by_id(self, subscriber_id: int) -> Optional[Subscriber]:
        """Get a subscriber by ID."""
        return (
            self.session.query(Subscriber)
            .filter(Subscriber.id == subscriber_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[Subscriber]:
        """Get a subscriber by email."""
        return self.session.query(Subscriber).filter(Subscriber.email == email).first()

    def get_all_active(self) -> List[Subscriber]:
        """Get all active subscribers."""
        return self.session.query(Subscriber).filter(Subscriber.isActive).all()

    def get_all(self) -> List[Subscriber]:
        """Get all subscribers."""
        return self.session.query(Subscriber).all()

    def update(self, subscriber_id: int, **kwargs) -> Optional[Subscriber]:
        """Update a subscriber."""
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            for key, value in kwargs.items():
                setattr(subscriber, key, value)
            self.session.commit()
            self.session.refresh(subscriber)
        return subscriber

    def delete(self, subscriber_id: int) -> bool:
        """Delete a subscriber."""
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            self.session.delete(subscriber)
            self.session.commit()
            return True
        return False


class SQLSubscriptionRepository:
    """SQLAlchemy implementation of SubscriptionRepository."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, subscription_id: int) -> Subscription | None:
        """Get a subscription by ID."""
        return self.session.get(Subscription, subscription_id)

    def get_by_subscriber_id(self, subscriber_id: int) -> list[Subscription]:
        """Get all subscriptions for a subscriber."""
        return (
            self.session.query(Subscription)
            .filter(Subscription.subscriber_id == subscriber_id)
            .all()
        )

    def get_subscriptions_from(self, subscriber_id: int) -> list[Subscription]:
        """Get subscriptions from a subscriber (alias for get_by_subscriber_id)."""
        return self.get_by_subscriber_id(subscriber_id)

    def add(self, subscription: Subscription) -> Subscription:
        """Add a new subscription."""
        self.session.add(subscription)
        self.session.commit()
        self.session.refresh(subscription)
        return subscription

    def update(self, subscription: Subscription) -> Subscription:
        """Update an existing subscription."""
        self.session.merge(subscription)
        self.session.commit()
        return subscription

    def delete(self, subscription_id: int) -> bool:
        """Delete a subscription."""
        subscription = self.session.get(Subscription, subscription_id)
        if subscription:
            self.session.delete(subscription)
            self.session.commit()
            return True
        return False


class SQLDigestRunRepository:
    """SQLAlchemy implementation of DigestRunRepository."""

    def __init__(self, session: Session):
        self.session = session

    def add_run(
        self, subscriber_id: int, period_start: datetime, status: str
    ) -> DigestRun:
        """Record a digest run."""
        run = DigestRun(
            subscriber_id=subscriber_id,
            period_start=period_start,
            status=status,
            sent_at=datetime.now(),
        )
        self.session.add(run)
        self.session.commit()
        self.session.refresh(run)
        return run
