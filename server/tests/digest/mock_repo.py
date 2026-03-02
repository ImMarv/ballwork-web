"""Mock event repository for testing."""

from datetime import date
from typing import List

from ...app.modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)


class MockEventRepository:
    """Mock repository that returns fake notification events for testing."""

    def __init__(self):
        """Initialize mock repository with sample data."""
        self.events = [
            NotificationEvent(
                id=1,
                created_at=date(2024, 1, 15),
                event_type="player_performance",
                entity_id=101,
                payload={"message": "Minanda scored a goal"},
            ),
            NotificationEvent(
                id=2,
                created_at=date(2024, 1, 16),
                event_type="match_completed",
                entity_id=102,
                payload={"message": "PES United vs Team B ended 2-0"},
            ),
            NotificationEvent(
                id=3,
                created_at=date(2024, 1, 17),
                event_type="player_performance",
                entity_id=103,
                payload={"message": "Ximelez scored a hatrick"},
            ),
        ]

    def get_events_between(self, start: date, end: date) -> List[NotificationEvent]:
        """Return mock events between start and end dates."""
        return [e for e in self.events if start <= e.created_at <= end]

    def get_by_id(self, selected_id: int) -> NotificationEvent | None:
        """Return mock event by id or None."""
        for e in self.events:
            if e.id == selected_id:
                return e
        return None

    def add(self, event: NotificationEvent) -> None:
        """Add mock event to the repository."""
        event.id = max((e.id for e in self.events), default=0) + 1
        self.events.append(event)
