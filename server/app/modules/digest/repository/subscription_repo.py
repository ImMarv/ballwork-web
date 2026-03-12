"""Subscription Repository Pattern"""

from sqlalchemy.orm import Session

from .models.subscription import Subscription


class SubscriptionRepository:
    """Repository for subscription database operations"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, subn_id: int) -> Subscription | None:
        """Get subscription by ID"""
        return self.session.get(Subscription, subn_id)

    def get_by_subscriber_id(self, subr_id: int) -> list[Subscription]:
        """Get subscriptions by subscriber ID"""
        return (
            self.session.query(Subscription)
            .filter(Subscription.subscriber_id == subr_id)
            .all()
        )

    def add(self, subn: Subscription) -> Subscription:
        """Create a new subscription"""
        self.session.add(subn)
        self.session.commit()
        return subn

    def update(self, subn: Subscription) -> Subscription:
        """Update an existing subscription"""
        self.session.merge(subn)
        self.session.commit()
        return subn

    def delete(self, subscription_id: int) -> bool:
        """Delete a subscription by ID"""
        subscription = self.session.get(Subscription, subscription_id)
        if subscription:
            self.session.delete(subscription)
            self.session.commit()
            return True
        return False

    def get_subscriptions_from(self, subscriber_id: int):
        subscriptions = (
            self.session.query(Subscription)
            .filter(Subscription.subscriber_id == subscriber_id)
            .all()
        )
        return subscriptions
