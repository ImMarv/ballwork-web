"""Subscription Repository Pattern"""

from typing import Protocol

from sqlalchemy.orm import Session

from .models.subscription import Subscription


class SubscriptionRepository(Protocol):
    """Protocol for subscription repository operations"""

    session: Session

    def get_by_id(self, subn_id: int, subn: Subscription) -> Subscription | None:
        return self.session.get(subn, subn_id)

    def get_by_subscriber_id(
        self, subr_id: int, subn: Subscription
    ) -> list[Subscription]:
        """Get subscriptions by subscriber ID"""
        return (
            self.session.query(subn).filter(Subscription.subscriber_id == subr_id).all()
        )

    def add(self, subn: Subscription) -> Subscription | None:
        """Create a new subscription"""
        subn = Subscription()
        return self.session.add(subn)

    def update(self, subn: Subscription, subn_id: int) -> Subscription:
        """Update an existing subscription"""
        subn = self.get_by_id(subn_id)

    def delete(self, subscription_id: int) -> bool:
        """Delete a subscription"""
        ...
