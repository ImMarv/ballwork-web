"""Subscription Repository Pattern"""
from typing import Protocol
from app.modules.digest.repository.models.subscription import Subscription

from sqlalchemy.orm import Session




class SubscriptionRepository(Protocol):
    """Protocol for subscription repository operations"""
    session: 

    def get_by_id(self, subscription_id: int) -> Subscription | None:


    def get_by_subscriber_id(self, subscriber_id: int) -> list[Subscription]:
        """Get subscriptions by subscriber ID"""
        ...

    def create(self, subscription: Subscription) -> Subscription:
        """Create a new subscription"""
        ...

    def update(self, subscription: Subscription) -> Subscription:
        """Update an existing subscription"""
        ...

    def delete(self, subscription_id: int) -> bool:
        """Delete a subscription"""
        ...