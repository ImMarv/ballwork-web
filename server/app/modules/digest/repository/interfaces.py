"""Repository interfaces (Protocols) for the digest module."""

from datetime import date, datetime
from typing import List, Optional, Protocol

from .models.digest_run_digest import DigestRun
from .models.notification_event_digest import NotificationEvent
from .models.subscriber import Subscriber
from .models.subscription import Subscription


class EventRepository(Protocol):
    """Interface for event data access operations."""

    def get_events_between(
        self, start: date | datetime, end: date | datetime
    ) -> List[NotificationEvent]:
        """Get events between a start and end date.

        Args:
            start: Start date/datetime
            end: End date/datetime

        Returns:
            List of notification events within the date range
        """
        ...

    def get_by_id(self, event_id: int) -> NotificationEvent | None:
        """Get an event by its ID.

        Args:
            event_id: The event ID

        Returns:
            NotificationEvent or None if not found
        """
        ...

    def add(self, event: NotificationEvent) -> NotificationEvent:
        """Add a new event to the repository.

        Args:
            event: The notification event to add

        Returns:
            The created event
        """
        ...

    def get_events_for_subscriptions(
        self, subscriptions: List[Subscription]
    ) -> List[NotificationEvent]:
        """Get all events that match the given subscriptions.

        Args:
            subscriptions: List of subscriptions to filter by

        Returns:
            List of events matching any of the subscriptions
        """
        ...


class SubscriberRepository(Protocol):
    """Interface for subscriber data access operations."""

    def create(self, email: str, is_active: bool = True) -> Subscriber:
        """Create a new subscriber.

        Args:
            email: Subscriber email address
            is_active: Whether the subscriber is active

        Returns:
            The created subscriber
        """
        ...

    def get_by_id(self, subscriber_id: int) -> Optional[Subscriber]:
        """Get a subscriber by ID.

        Args:
            subscriber_id: The subscriber ID

        Returns:
            Subscriber or None if not found
        """
        ...

    def get_by_email(self, email: str) -> Optional[Subscriber]:
        """Get a subscriber by email.

        Args:
            email: The subscriber's email address

        Returns:
            Subscriber or None if not found
        """
        ...

    def get_all_active(self) -> List[Subscriber]:
        """Get all active subscribers.

        Returns:
            List of active subscribers
        """
        ...

    def get_all(self) -> List[Subscriber]:
        """Get all subscribers.

        Returns:
            List of all subscribers
        """
        ...

    def update(self, subscriber_id: int, **kwargs) -> Optional[Subscriber]:
        """Update a subscriber.

        Args:
            subscriber_id: The subscriber ID
            **kwargs: Fields to update

        Returns:
            Updated subscriber or None if not found
        """
        ...

    def delete(self, subscriber_id: int) -> bool:
        """Delete a subscriber.

        Args:
            subscriber_id: The subscriber ID

        Returns:
            True if deleted, False if not found
        """
        ...


class SubscriptionRepository(Protocol):
    """Interface for subscription data access operations."""

    def get_by_id(self, subscription_id: int) -> Subscription | None:
        """Get a subscription by ID.

        Args:
            subscription_id: The subscription ID

        Returns:
            Subscription or None if not found
        """
        ...

    def get_by_subscriber_id(self, subscriber_id: int) -> list[Subscription]:
        """Get all subscriptions for a subscriber.

        Args:
            subscriber_id: The subscriber ID

        Returns:
            List of subscriptions for the subscriber
        """
        ...

    def get_subscriptions_from(self, subscriber_id: int) -> list[Subscription]:
        """Get subscriptions from a subscriber (alias for get_by_subscriber_id).

        Args:
            subscriber_id: The subscriber ID

        Returns:
            List of subscriptions for the subscriber
        """
        ...

    def add(self, subscription: Subscription) -> Subscription:
        """Add a new subscription.

        Args:
            subscription: The subscription to add

        Returns:
            The created subscription
        """
        ...

    def update(self, subscription: Subscription) -> Subscription:
        """Update an existing subscription.

        Args:
            subscription: The subscription to update

        Returns:
            The updated subscription
        """
        ...

    def delete(self, subscription_id: int) -> bool:
        """Delete a subscription.

        Args:
            subscription_id: The subscription ID

        Returns:
            True if deleted, False if not found
        """
        ...


class DigestRunRepository(Protocol):
    """Interface for digest run data access operations."""

    def add_run(
        self, subscriber_id: int, period_start: datetime, status: str
    ) -> DigestRun:
        """Record a digest run.

        Args:
            subscriber_id: ID of the subscriber
            period_start: Start of the digest period
            status: Status of the digest run

        Returns:
            The created digest run
        """
        ...
