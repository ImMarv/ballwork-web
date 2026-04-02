"""Tests for repository CRUD operations."""

from datetime import datetime

import pytest

from app.modules.digest.repository.models.notification_event_digest import (
    EntityType,
    EventType,
    NotificationEvent,
)
from app.modules.digest.repository.models.subscriber import Subscriber
from app.modules.digest.repository.models.subscription import Subscription
from .mock_repo import (
    MockDigestRunRepository,
    MockEventRepository,
    MockSubscriberRepository,
    MockSubscriptionRepository,
)


class TestEventRepositoryCRUD:
    """Test EventRepository CRUD operations."""

    @pytest.fixture
    def repo(self):
        """Fixture for event repository."""
        return MockEventRepository()

    def test_add_event(self, repo):
        """Test adding an event."""
        event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=1,
            payload={"message": "Goal"},
        )
        result = repo.add(event)

        assert result.id is not None
        assert result in repo.events

    def test_get_by_id(self, repo):
        """Test retrieving event by ID."""
        event = repo.get_by_id(1)

        assert event is not None
        assert event.id == 1
        assert event.entity_id == 101

    def test_get_by_id_not_found(self, repo):
        """Test retrieving non-existent event."""
        event = repo.get_by_id(999)

        assert event is None

    def test_get_events_between_dates(self, repo):
        """Test retrieving events within date range."""
        start = datetime(2024, 1, 15)
        end = datetime(2024, 1, 16, 23, 59, 59)

        events = repo.get_events_between(start, end)

        assert len(events) == 2
        assert all(start <= e.created_at <= end for e in events)

    def test_get_events_between_no_results(self, repo):
        """Test date range with no results."""
        start = datetime(2024, 3, 1)
        end = datetime(2024, 3, 31)

        events = repo.get_events_between(start, end)

        assert len(events) == 0

    def test_get_events_for_subscriptions(self, repo):
        """Test filtering events for subscriptions."""
        # Create subscriptions
        sub1 = Subscription(
            id=1, subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )
        sub2 = Subscription(
            id=2, subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=102
        )

        events = repo.get_events_for_subscriptions([sub1, sub2])

        assert len(events) == 2
        assert all(e.entity_id in [101, 102] for e in events)

    def test_get_events_for_subscriptions_empty(self, repo):
        """Test filtering with empty subscriptions."""
        events = repo.get_events_for_subscriptions([])

        assert len(events) == 0


class TestSubscriberRepositoryCRUD:
    """Test SubscriberRepository CRUD operations."""

    @pytest.fixture
    def repo(self):
        """Fixture for subscriber repository."""
        return MockSubscriberRepository()

    def test_create_subscriber(self, repo):
        """Test creating a subscriber."""
        subscriber = repo.create(email="test@example.com", is_active=True)

        assert subscriber.email == "test@example.com"
        assert subscriber.isActive is True
        assert subscriber.id is not None

    def test_get_by_id(self, repo):
        """Test retrieving subscriber by ID."""
        created = repo.create(email="test@example.com", is_active=True)
        subscriber = repo.get_by_id(created.id)

        assert subscriber is not None
        assert subscriber.email == "test@example.com"

    def test_get_by_id_not_found(self, repo):
        """Test retrieving non-existent subscriber."""
        subscriber = repo.get_by_id(999)

        assert subscriber is None

    def test_get_by_email(self, repo):
        """Test retrieving subscriber by email."""
        created = repo.create(email="test@example.com", is_active=True)
        subscriber = repo.get_by_email("test@example.com")

        assert subscriber is not None
        assert subscriber.id == created.id

    def test_get_by_email_not_found(self, repo):
        """Test retrieving non-existent email."""
        subscriber = repo.get_by_email("nonexistent@example.com")

        assert subscriber is None

    def test_get_all_active(self, repo):
        """Test retrieving all active subscribers."""
        repo.create(email="active1@example.com", is_active=True)
        repo.create(email="active2@example.com", is_active=True)
        repo.create(email="inactive@example.com", is_active=False)

        active = repo.get_all_active()

        assert len(active) == 2
        assert all(s.isActive for s in active)

    def test_get_all(self, repo):
        """Test retrieving all subscribers."""
        repo.create(email="user1@example.com", is_active=True)
        repo.create(email="user2@example.com", is_active=True)
        repo.create(email="user3@example.com", is_active=False)

        all_subs = repo.get_all()

        assert len(all_subs) == 3

    def test_update_subscriber(self, repo):
        """Test updating subscriber."""
        created = repo.create(email="test@example.com", is_active=True)
        updated = repo.update(created.id, isActive=False)

        assert updated.isActive is False

    def test_delete_subscriber(self, repo):
        """Test deleting subscriber."""
        created = repo.create(email="test@example.com", is_active=True)
        result = repo.delete(created.id)

        assert result is True
        assert repo.get_by_id(created.id) is None

    def test_delete_non_existent(self, repo):
        """Test deleting non-existent subscriber."""
        result = repo.delete(999)

        assert result is False


class TestSubscriptionRepositoryCRUD:
    """Test SubscriptionRepository CRUD operations."""

    @pytest.fixture
    def repo(self):
        """Fixture for subscription repository."""
        return MockSubscriptionRepository()

    def test_add_subscription(self, repo):
        """Test adding a subscription."""
        subscription = Subscription(
            subscriber_id=1, entity_type="player", entity_id=101
        )
        result = repo.add(subscription)

        assert result.id is not None
        assert result in repo.subscriptions

    def test_get_by_id(self, repo):
        """Test retrieving subscription by ID."""
        subscription = Subscription(
            subscriber_id=1, entity_type="player", entity_id=101
        )
        added = repo.add(subscription)
        retrieved = repo.get_by_id(added.id)

        assert retrieved is not None
        assert retrieved.id == added.id

    def test_get_by_subscriber_id(self, repo):
        """Test retrieving subscriptions by subscriber."""
        sub1 = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )
        sub2 = Subscription(subscriber_id=1, entity_type=EntityType.TEAM, entity_id=201)
        sub3 = Subscription(
            subscriber_id=2, entity_type=EntityType.PLAYER, entity_id=102
        )

        repo.add(sub1)
        repo.add(sub2)
        repo.add(sub3)

        subs = repo.get_by_subscriber_id(1)

        assert len(subs) == 2
        assert all(s.subscriber_id == 1 for s in subs)

    def test_get_subscriptions_from_alias(self, repo):
        """Test get_subscriptions_from alias."""
        sub1 = Subscription(
            subscriber_id=1, entity_type=EntityType.PLAYER, entity_id=101
        )
        repo.add(sub1)

        subs = repo.get_subscriptions_from(1)

        assert len(subs) == 1
        assert subs[0].subscriber_id == 1

    def test_delete_subscription(self, repo):
        """Test deleting subscription."""
        subscription = Subscription(
            subscriber_id=1, entity_type="player", entity_id=101
        )
        added = repo.add(subscription)
        result = repo.delete(added.id)

        assert result is True
        assert repo.get_by_id(added.id) is None

    def test_delete_non_existent(self, repo):
        """Test deleting non-existent subscription."""
        result = repo.delete(999)

        assert result is False


class TestDigestRunRepositoryCRUD:
    """Test DigestRunRepository CRUD operations."""

    @pytest.fixture
    def repo(self):
        """Fixture for digest run repository."""
        return MockDigestRunRepository()

    def test_add_run_passed(self, repo):
        """Test adding a PASSED digest run."""
        period_start = datetime.now()
        run = repo.add_run(subscriber_id=1, period_start=period_start, status="PASSED")

        assert run.id is not None
        assert run.subscriber_id == 1
        assert run.status == "PASSED"
        assert run in repo.runs

    def test_add_run_failed(self, repo):
        """Test adding a FAILED digest run."""
        period_start = datetime.now()
        run = repo.add_run(subscriber_id=1, period_start=period_start, status="FAILED")

        assert run.status == "FAILED"

    def test_add_run_partial(self, repo):
        """Test adding a PARTIAL digest run."""
        period_start = datetime.now()
        run = repo.add_run(subscriber_id=1, period_start=period_start, status="PARTIAL")

        assert run.status == "PARTIAL"

    def test_multiple_runs_tracked(self, repo):
        """Test tracking multiple digest runs."""
        for i in range(3):
            repo.add_run(
                subscriber_id=i + 1,
                period_start=datetime.now(),
                status="PASSED",
            )

        assert len(repo.runs) == 3
