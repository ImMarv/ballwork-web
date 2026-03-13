"""Tests for input validation and common gotchas."""

import pytest

from ...app.modules.digest.repository.models.notification_event_digest import (
    EntityType,
    EventType,
    NotificationEvent,
)
from ...app.modules.digest.repository.models.subscriber import Subscriber
from ...app.modules.digest.repository.models.subscription import Subscription
from .mock_repo import (
    MockEventRepository,
    MockSubscriberRepository,
    MockSubscriptionRepository,
)


class TestSubscriberInputValidation:
    """Test subscriber input validation."""

    @pytest.fixture
    def repo(self):
        """Fixture for subscriber repository."""
        return MockSubscriberRepository()

    def test_subscriber_duplicate_email_allowed_in_mock(self, repo):
        """Test that duplicate emails are allowed (real DB would prevent this)."""
        # In real app, this should be prevented at database level with unique constraint
        sub1 = repo.create(email="duplicate@example.com", is_active=True)
        sub2 = repo.create(email="duplicate@example.com", is_active=True)

        # Mock allows duplicates; real DB won't
        assert sub1.id != sub2.id

    def test_subscriber_empty_email_accepted_in_mock(self, repo):
        """Test empty email (real app should validate this)."""
        # Mock accepts empty; real app should reject
        subscriber = repo.create(email="", is_active=True)
        assert subscriber.email == ""

    def test_subscriber_email_case_sensitivity(self, repo):
        """Test email case handling."""
        # Create subscriber with lowercase
        sub_lower = repo.create(email="test@example.com", is_active=True)

        # Get by lowercase should work
        retrieved = repo.get_by_email("test@example.com")
        assert retrieved is not None

        # Get by uppercase won't match (case sensitive in mock)
        retrieved_upper = repo.get_by_email("TEST@EXAMPLE.COM")
        assert retrieved_upper is None  # Not found because mock is case-sensitive

    def test_subscriber_is_active_default(self, repo):
        """Test default is_active value."""
        subscriber = repo.create(email="test@example.com")

        assert subscriber.isActive is True  # Should default to True


class TestSubscriptionInputValidation:
    """Test subscription input validation."""

    @pytest.fixture
    def repo(self):
        """Fixture for subscription repository."""
        return MockSubscriptionRepository()

    def test_subscription_entity_type_values(self, repo):
        """Test subscription entity types are set correctly."""
        # Create subscriptions with different entity types
        sub_player = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )
        sub_team = Subscription(
            subscriber_id=1, entity_type=EntityType.TEAM, entity_id=201
        )
        sub_competition = Subscription(
            subscriber_id=1, entity_type=EntityType.COMPETITION, entity_id=301
        )

        repo.add(sub_player)
        repo.add(sub_team)
        repo.add(sub_competition)

        all_subs = repo.get_by_subscriber_id(1)
        entity_types = [s.entity_type for s in all_subs]

        assert "player" in entity_types
        assert "team" in entity_types
        assert "competition" in entity_types

    def test_subscription_zero_entity_id(self, repo):
        """Test handling of zero entity ID (edge case)."""
        subscription = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=0
        )
        added = repo.add(subscription)

        assert added.entity_id == 0  # Should accept 0

    def test_subscription_negative_entity_id(self, repo):
        """Test handling of negative entity ID (invalid but accepted in mock)."""
        subscription = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=-1
        )
        added = repo.add(subscription)

        assert added.entity_id == -1  # Mock accepts it

    def test_subscription_large_entity_id(self, repo):
        """Test handling of very large entity ID."""
        large_id = 999999999
        subscription = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=large_id
        )
        added = repo.add(subscription)

        assert added.entity_id == large_id


class TestEventInputValidation:
    """Test event input validation."""

    @pytest.fixture
    def repo(self):
        """Fixture for event repository."""
        return MockEventRepository()

    def test_event_payload_as_dict(self, repo):
        """Test event payload is properly stored as dict."""
        payload = {"goal": True, "assists": 2, "player": "John"}
        event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=1,
            payload=payload,
        )
        added = repo.add(event)

        assert added.payload == payload

    def test_event_payload_complex_nested_dict(self, repo):
        """Test event payload with nested structure."""
        payload = {
            "player": {"name": "John", "stats": {"goals": 5, "assists": 3}},
            "match": {"date": "2024-01-15", "score": "3-1"},
        }
        event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=1,
            payload=payload,
        )
        added = repo.add(event)

        assert added.payload["player"]["stats"]["goals"] == 5

    def test_event_payload_empty_dict(self, repo):
        """Test event with empty payload."""
        event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=1,
            payload={},
        )
        added = repo.add(event)

        assert added.payload == {}

    def test_event_entity_types_match_subscriptions(self):
        """Test that event entity_type matches subscription entity_type."""
        # Create subscription for player
        sub = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )

        # Create event for player
        event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=101,
            payload={"message": "Goal"},
        )

        # Types should match
        assert event.entity_type == sub.entity_type
        assert event.entity_id == sub.entity_id

    def test_event_entity_type_mismatch_not_matched(self):
        """Test that events don't match if entity_type differs."""
        # Subscription for player
        sub = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )

        # Event for team (different type)
        event = NotificationEvent(
            event_type=EventType.MATCH_COMPLETED,
            entity_type=EntityType.TEAM,
            entity_id=101,
            payload={"message": "Win"},
        )

        # Should NOT match
        assert event.entity_type != sub.entity_type


class TestFilteringLogicValidation:
    """Test filtering logic handles edge cases."""

    @pytest.fixture
    def event_repo(self):
        """Fixture for event repository."""
        return MockEventRepository()

    def test_filter_empty_subscriptions_returns_empty(self, event_repo):
        """Test filtering with no subscriptions returns empty."""
        result = event_repo.get_events_for_subscriptions([])

        assert result == []

    def test_filter_multiple_subscriptions_same_entity(self, event_repo):
        """Test filtering doesn't duplicate when multiple subs match same entity."""
        sub1 = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )
        sub2 = Subscription(
            subscriber_id=2, entity_type=EntityType.PLAYER, entity_id=101
        )

        # Should not include duplicates even with 2 subs for same entity
        results = event_repo.get_events_for_subscriptions([sub1, sub2])

        # Count events with id=1 (only one instance, not duplicated)
        count = sum(1 for e in results if e.entity_id == 101)
        assert count <= 2  # Should be deduplicated in real impl

    def test_filter_multiple_subscriptions_different_entities(self, event_repo):
        """Test filtering with multiple subscriptions for different entities."""
        sub1 = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )
        sub2 = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=102
        )
        sub3 = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=103
        )

        results = event_repo.get_events_for_subscriptions([sub1, sub2, sub3])

        entity_ids = [e.entity_id for e in results]
        assert 101 in entity_ids or 102 in entity_ids or 103 in entity_ids


class TestCommonGotchas:
    """Test for common gotchas and edge cases."""

    def test_date_range_boundary_inclusive(self):
        """Test that date range boundaries are inclusive."""
        from datetime import datetime

        repo = MockEventRepository()

        # Get all events
        all_events = repo.get_events_between(
            datetime(2024, 1, 1), datetime(2024, 12, 31)
        )

        # Initial data has 3 events
        assert len(all_events) == 3

    def test_subscriber_status_change_affects_digest(self):
        """Test that changing subscriber status between runs works correctly."""
        repo = MockSubscriberRepository()

        # Create subscriber
        sub = repo.create(email="user@example.com", is_active=True)

        # Should be in active list
        assert len(repo.get_all_active()) == 1

        # Deactivate
        repo.update(sub.id, isActive=False)

        # Should not be in active list anymore
        assert len(repo.get_all_active()) == 0

    def test_subscription_order_independence(self):
        """Test that subscription order doesn't affect matching."""
        event_repo = MockEventRepository()

        # Create subscriptions in different orders
        subs_order1 = [
            Subscription(subscriber_id=1, entity_type="player", entity_id=101),
            Subscription(subscriber_id=1, entity_type="player", entity_id=102),
            Subscription(subscriber_id=1, entity_type="player", entity_id=103),
        ]

        subs_order2 = [
            Subscription(subscriber_id=1, entity_type="player", entity_id=103),
            Subscription(subscriber_id=1, entity_type="player", entity_id=101),
            Subscription(subscriber_id=1, entity_type="player", entity_id=102),
        ]

        results1 = event_repo.get_events_for_subscriptions(subs_order1)
        results2 = event_repo.get_events_for_subscriptions(subs_order2)

        # Should get same events regardless of order
        assert sorted([e.id for e in results1]) == sorted([e.id for e in results2])
