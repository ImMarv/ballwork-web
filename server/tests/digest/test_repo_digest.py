"""Test cases for event repository digest functionality."""

from datetime import datetime

import pytest

from ...app.modules.digest.repository.models.notification_event_digest import (
    EntityType,
    EventType,
    NotificationEvent,
)
from .mock_repo import MockEventRepository


@pytest.fixture
def mock_repo():
    """Fixture to provide mock repository instance."""
    return MockEventRepository()


@pytest.fixture
def sample_event():
    """Fixture to provide a sample notification event."""
    return NotificationEvent(
        id=4,
        event_type=EventType.MATCH_COMPLETED,
        entity_type=EntityType.MATCH,
        entity_id=1,
        payload={"score": "3-1", "team": "PES United"},
        created_at=datetime.now(),
    )


class TestGetEventsBetween:
    """Test cases for get_events_between method."""

    def test_get_events_within_range(self, mock_repo):
        """Test retrieving events within a valid date range."""
        start = datetime(2024, 1, 15).date()
        end = datetime(2024, 1, 16).date()
        events = mock_repo.get_events_between(start, end)
        assert len(events) == 2

    def test_get_events_no_results(self, mock_repo):
        """Test retrieving events with no matches in date range."""
        start = datetime(2024, 2, 1).date()
        end = datetime(2024, 2, 28).date()
        events = mock_repo.get_events_between(start, end)
        assert len(events) == 0

    def test_get_events_single_day(self, mock_repo):
        """Test retrieving events for a single day."""
        date_filter = datetime(2024, 1, 17).date()
        events = mock_repo.get_events_between(date_filter, date_filter)
        assert len(events) == 1
        assert events[0].id == 3


class TestGetById:
    """Test cases for get_by_id method."""

    def test_get_event_by_valid_id(self, mock_repo):
        """Test retrieving an event with a valid ID."""
        event = mock_repo.get_by_id(1)
        assert event is not None
        assert event.id == 1
        assert event.event_type == EventType.PLAYER_PERFORMANCE

    def test_get_event_by_invalid_id(self, mock_repo):
        """Test retrieving an event with an invalid ID."""
        event = mock_repo.get_by_id(999)
        assert event is None

    def test_get_multiple_events_by_id(self, mock_repo):
        """Test retrieving multiple different events by ID."""
        for event_id in [1, 2, 3]:
            event = mock_repo.get_by_id(event_id)
            assert event is not None
            assert event.id == event_id


class TestAdd:
    """Test cases for add method."""

    def test_add_new_event(self, mock_repo, sample_event):
        """Test adding a new event to the repository."""
        initial_count = len(mock_repo.events)
        mock_repo.add(sample_event)
        assert len(mock_repo.events) == initial_count + 1
        assert mock_repo.events[-1].id == 4

    def test_add_event_generates_unique_id(self, mock_repo):
        """Test that added events receive unique IDs."""
        event1 = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=5,
            payload={"player": "John"},
            created_at=datetime.now(),
        )
        event2 = NotificationEvent(
            event_type=EventType.MATCH_COMPLETED,
            entity_type=EntityType.MATCH,
            entity_id=6,
            payload={"result": "draw"},
            created_at=datetime.now(),
        )
        mock_repo.add(event1)
        mock_repo.add(event2)
        assert event1.id != event2.id

    def test_add_multiple_events(self, mock_repo):
        """Test adding multiple events sequentially."""
        for i in range(3):
            event = NotificationEvent(
                event_type=EventType.MATCH_COMPLETED,
                entity_type=EntityType.MATCH,
                entity_id=10 + i,
                payload={"index": i},
                created_at=datetime.now(),
            )
            mock_repo.add(event)
        assert len(mock_repo.events) >= 6
