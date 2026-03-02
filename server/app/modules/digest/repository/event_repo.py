"""Event repository module for managing notification event digests."""

from datetime import date
from typing import List, Protocol

from sqlalchemy.orm import Session

from .models.notification_event_digest import NotificationEvent


class EventRepository(Protocol):
    """Class dealing with DOA for events

    Args:
        Protocol (_type_)

    Returns:
        _type_: _description_
    """

    session: Session

    def get_events_between(
        self, event: NotificationEvent, start: date, end: date
    ) -> List[NotificationEvent]:
        """Get a list of events between a start date and an end date.

        Args:
            event (NotificationEvent): Notification event object
            start (date): Date start
            end (date): Date end

        Returns:
            list[NotificationEvent]: A list of all notification events between the end and start
        """
        return (
            self.session.query(event)
            .filter(NotificationEvent.created_at >= start)
            .filter(NotificationEvent.created_at <= end)
            .all()
        )

    def get_by_id(
        self, event: NotificationEvent, selected_id: int
    ) -> NotificationEvent | None:
        """Get the event by id.

        Args:
            event (NotificationEvent): Notification event object
            selected_id (int): The PK ID of the object in the DB

        Returns:
            NotificationEvent | None: _description_
        """
        return self.session.get(event, selected_id)

    def add(self, event: NotificationEvent):
        """Adds Notification Event to DB

        Args:
            event (NotificationEvent): _description_
        """
        return self.session.add(event)
