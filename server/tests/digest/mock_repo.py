"""Mock repositories for testing digest module."""

from datetime import date, datetime
from typing import List, Optional

from app.modules.digest.email.email_service import SMTPEmailService
from app.modules.digest.repository.models.digest_run_digest import DigestRun
from app.modules.digest.repository.models.notification_event_digest import (
    EntityType,
    EventType,
    NotificationEvent,
)
from app.modules.digest.repository.models.subscriber import Subscriber
from app.modules.digest.repository.models.subscription import Subscription


class MockEventRepository:
    """Mock implementation of EventRepository for testing."""

    def __init__(self):
        """Initialize mock repository with sample data."""
        self.events = [
            NotificationEvent(
                id=1,
                created_at=datetime(2024, 1, 15),
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=101,
                payload={"message": "Minanda scored a goal"},
            ),
            NotificationEvent(
                id=2,
                created_at=datetime(2024, 1, 16),
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=102,
                payload={"message": "Another player scored"},
            ),
            NotificationEvent(
                id=3,
                created_at=datetime(2024, 1, 17),
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=103,
                payload={"message": "Ximelez scored a hatrick"},
            ),
        ]

    def get_events_between(
        self, start: date | datetime, end: date | datetime
    ) -> List[NotificationEvent]:
        """Get events between start and end dates."""
        # Convert dates to datetime for consistent comparison
        if isinstance(start, date) and not isinstance(start, datetime):
            start = datetime.combine(start, datetime.min.time())
        if isinstance(end, date) and not isinstance(end, datetime):
            end = datetime.combine(end, datetime.max.time())

        return [e for e in self.events if e.created_at and start <= e.created_at <= end]

    def get_by_id(self, event_id: int) -> NotificationEvent | None:
        """Get event by ID."""
        for e in self.events:
            if e.id == event_id:
                return e
        return None

    def add(self, event: NotificationEvent) -> NotificationEvent:
        """Add event to repository."""
        if not event.id:
            event.id = max((e.id for e in self.events), default=0) + 1
        if not event.created_at:
            event.created_at = datetime.now()
        self.events.append(event)
        return event

    def get_events_for_subscriptions(
        self, subscriptions: List[Subscription]
    ) -> List[NotificationEvent]:
        """Get events matching subscriptions."""
        if not subscriptions:
            return []

        filtered = []
        for event in self.events:
            for sub in subscriptions:
                if (
                    event.entity_type == sub.entity_type
                    and event.entity_id == sub.entity_id
                ):
                    filtered.append(event)
                    break  # Avoid duplicates

        return filtered


class MockSubscriberRepository:
    """Mock implementation of SubscriberRepository for testing."""

    def __init__(self):
        """Initialize with sample subscribers."""
        self.subscribers = []
        self._id_counter = 0

    def create(self, email: str, is_active: bool = True) -> Subscriber:
        """Create a new subscriber."""
        self._id_counter += 1
        sub = Subscriber(id=self._id_counter, email=email, isActive=is_active)
        self.subscribers.append(sub)
        return sub

    def get_by_id(self, subscriber_id: int) -> Optional[Subscriber]:
        """Get subscriber by ID."""
        for s in self.subscribers:
            if s.id == subscriber_id:
                return s
        return None

    def get_by_email(self, email: str) -> Optional[Subscriber]:
        """Get subscriber by email."""
        for s in self.subscribers:
            if s.email == email:
                return s
        return None

    def get_all_active(self) -> List[Subscriber]:
        """Get all active subscribers."""
        return [s for s in self.subscribers if s.isActive]

    def get_all(self) -> List[Subscriber]:
        """Get all subscribers."""
        return self.subscribers.copy()

    def update(self, subscriber_id: int, **kwargs) -> Optional[Subscriber]:
        """Update subscriber."""
        sub = self.get_by_id(subscriber_id)
        if sub:
            for key, value in kwargs.items():
                setattr(sub, key, value)
        return sub

    def delete(self, subscriber_id: int) -> bool:
        """Delete subscriber."""
        sub = self.get_by_id(subscriber_id)
        if sub:
            self.subscribers.remove(sub)
            return True
        return False


class MockSubscriptionRepository:
    """Mock implementation of SubscriptionRepository for testing."""

    def __init__(self):
        """Initialize with no subscriptions."""
        self.subscriptions = []
        self._id_counter = 0

    def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Get subscription by ID."""
        for s in self.subscriptions:
            if s.id == subscription_id:
                return s
        return None

    def get_by_subscriber_id(self, subscriber_id: int) -> List[Subscription]:
        """Get subscriptions by subscriber ID."""
        return [s for s in self.subscriptions if s.subscriber_id == subscriber_id]

    def get_subscriptions_from(self, subscriber_id: int) -> List[Subscription]:
        """Get subscriptions from subscriber (alias)."""
        return self.get_by_subscriber_id(subscriber_id)

    def add(self, subscription: Subscription) -> Subscription:
        """Add subscription."""
        if not subscription.id:
            self._id_counter += 1
            subscription.id = self._id_counter
        self.subscriptions.append(subscription)
        return subscription

    def update(self, subscription: Subscription) -> Subscription:
        """Update subscription."""
        # Just return the subscription as-is for mock
        return subscription

    def delete(self, subscription_id: int) -> bool:
        """Delete subscription."""
        sub = self.get_by_id(subscription_id)
        if sub:
            self.subscriptions.remove(sub)
            return True
        return False


class MockDigestRunRepository:
    """Mock implementation of DigestRunRepository for testing."""

    def __init__(self):
        """Initialize with no digest runs."""
        self.runs = []
        self._id_counter = 0

    def add_run(
        self, subscriber_id: int, period_start: datetime, status: str
    ) -> DigestRun:
        """Add digest run."""
        self._id_counter += 1
        run = DigestRun(
            id=self._id_counter,
            subscriber_id=subscriber_id,
            period_start=period_start,
            status=status,
            sent_at=datetime.now(),
        )
        self.runs.append(run)
        return run


class MockEmailService(SMTPEmailService):
    """Mock email service for testing."""

    def __init__(self, should_fail: bool = False):
        """Initialize mock email service."""
        self.sent_emails = []
        self.should_fail = should_fail

    def send_email(self, to: str, subject: str, body: str) -> None:
        """Mock sending email."""
        if self.should_fail:
            from app.modules.digest.email.email_service import EmailSendError

            raise EmailSendError(f"Failed to send email to {to}")

        self.sent_emails.append(
            {
                "to": to,
                "subject": subject,
                "body": body,
                "timestamp": datetime.now(),
            }
        )
