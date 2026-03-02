from typing import List, Optional
from typing import Protocol

from sqlalchemy.orm import Session

from .models.subscriber import Subscriber


class SubscriberRepository(Protocol):
    session: Session

    def create(self, email: str, is_active: bool = True) -> Subscriber:
        subscriber = Subscriber(email=email, isActive=is_active)
        self.session.add(subscriber)
        self.session.commit()
        self.session.refresh(subscriber)
        return subscriber

    def get_by_id(self, subscriber_id: int) -> Optional[Subscriber]:
        return (
            self.session.query(Subscriber)
            .filter(Subscriber.id == subscriber_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[Subscriber]:
        return self.session.query(Subscriber).filter(Subscriber.email == email).first()

    def get_all_active(self) -> List[Subscriber]:
        return self.session.query(Subscriber).filter(Subscriber.isActive == True).all()

    def get_all(self) -> List[Subscriber]:
        return self.session.query(Subscriber).all()

    def update(self, subscriber_id: int, **kwargs) -> Optional[Subscriber]:
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            for key, value in kwargs.items():
                setattr(subscriber, key, value)
            self.session.commit()
            self.session.refresh(subscriber)
        return subscriber

    def delete(self, subscriber_id: int) -> bool:
        subscriber = self.get_by_id(subscriber_id)
        if subscriber:
            self.session.delete(subscriber)
            self.session.commit()
            return True
        return False
