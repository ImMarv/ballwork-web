"""Tests for DigestService - full digest flow and error handling."""

from datetime import datetime, timedelta

import pytest

from ...app.modules.digest.email.email_service import EmailSendError
from ...app.modules.digest.repository.models.enums.digest_status import DigestStatus
from ...app.modules.digest.repository.models.notification_event_digest import (
    EntityType,
    EventType,
    NotificationEvent,
)
from ...app.modules.digest.repository.models.subscriber import Subscriber
from ...app.modules.digest.repository.models.subscription import Subscription
from ...app.modules.digest.service import DigestService
from .mock_repo import (
    MockDigestRunRepository,
    MockEmailService,
    MockEventRepository,
    MockSubscriberRepository,
    MockSubscriptionRepository,
)


@pytest.fixture
def mock_event_repo():
    """Fixture for event repository."""
    return MockEventRepository()


@pytest.fixture
def mock_subscriber_repo():
    """Fixture for subscriber repository."""
    return MockSubscriberRepository()


@pytest.fixture
def mock_subscription_repo():
    """Fixture for subscription repository."""
    return MockSubscriptionRepository()


@pytest.fixture
def mock_digest_run_repo():
    """Fixture for digest run repository."""
    return MockDigestRunRepository()


@pytest.fixture
def mock_email_service():
    """Fixture for email service."""
    return MockEmailService(should_fail=False)


@pytest.fixture
def digest_service(
    mock_event_repo,
    mock_subscriber_repo,
    mock_subscription_repo,
    mock_digest_run_repo,
    mock_email_service,
):
    """Fixture for DigestService with all mocked dependencies."""
    return DigestService(
        event_repo=mock_event_repo,
        subscriber_repo=mock_subscriber_repo,
        subscription_repo=mock_subscription_repo,
        digest_run_repo=mock_digest_run_repo,
        email_service=mock_email_service,
    )


class TestDigestServiceFullFlow:
    """Test the complete digest workflow."""

    def test_full_digest_flow_single_subscriber(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
        mock_digest_run_repo,
    ):
        """Test: User subscribes to player -> digest generated -> email correct."""
        # 1. Create subscriber
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )
        assert subscriber.email == "user@example.com"

        # 2. Create subscription to player 101
        subscription = Subscription(
            subscriber_id=subscriber.id,
            entity_type=EntityType.PLAYER,
            entity_id=101,
        )
        mock_subscription_repo.add(subscription)

        # 3. Add event for player 101
        event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=101,
            payload={"message": "Scored a goal"},
        )
        mock_event_repo.add(event)

        # 4. Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # 5. Verify email was sent
        assert len(mock_email_service.sent_emails) == 1
        email = mock_email_service.sent_emails[0]
        assert email["to"] == "user@example.com"
        assert email["subject"] == "Your Football Digest"
        assert "Scored a goal" in email["body"]

        # 6. Verify digest run was recorded
        assert len(mock_digest_run_repo.runs) == 1
        run = mock_digest_run_repo.runs[0]
        assert run.subscriber_id == subscriber.id
        assert run.status == DigestStatus.PASSED

    def test_digest_flow_multiple_subscribers(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
    ):
        """Test digests sent to multiple subscribers."""
        # Create 2 subscribers with different subscriptions
        sub1 = mock_subscriber_repo.create(email="user1@example.com", is_active=True)
        sub2 = mock_subscriber_repo.create(email="user2@example.com", is_active=True)

        # Sub1 subscribes to player 101
        sub1_subscription = Subscription(
            subscriber_id=sub1.id, entity_type=EntityType.PLAYER, entity_id=101
        )
        mock_subscription_repo.add(sub1_subscription)

        # Sub2 subscribes to player 102
        sub2_subscription = Subscription(
            subscriber_id=sub2.id, entity_type=EntityType.PLAYER, entity_id=102
        )
        mock_subscription_repo.add(sub2_subscription)

        # Add events
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=101,
                payload={"message": "Player 101 scored"},
            )
        )
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=102,
                payload={"message": "Player 102 scored"},
            )
        )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # Verify both emails sent with correct content
        assert len(mock_email_service.sent_emails) == 2
        assert mock_email_service.sent_emails[0]["to"] == "user1@example.com"
        assert "Player 101 scored" in mock_email_service.sent_emails[0]["body"]
        assert mock_email_service.sent_emails[1]["to"] == "user2@example.com"
        assert "Player 102 scored" in mock_email_service.sent_emails[1]["body"]

    def test_digest_respects_date_range(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
    ):
        """Test that digest only includes events in the specified date range."""
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )
        subscription = Subscription(
            subscriber_id=subscriber.id, entity_type=EntityType.PLAYER, entity_id=101
        )
        mock_subscription_repo.add(subscription)

        # Add event OUTSIDE the digest range
        old_event = NotificationEvent(
            event_type=EventType.PLAYER_PERFORMANCE,
            entity_type=EntityType.PLAYER,
            entity_id=101,
            payload={"message": "Old event"},
            created_at=datetime(2024, 1, 1),
        )
        mock_event_repo.add(old_event)

        # Run digest for recent dates only
        start = datetime(2024, 2, 1)
        end = datetime(2024, 2, 28)
        digest_service.run_digest(start, end)

        # Verify no email sent (no events in range)
        assert len(mock_email_service.sent_emails) == 0

    def test_digest_skips_inactive_subscribers(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
    ):
        """Test that inactive subscribers don't receive digests."""
        # Create active subscriber
        active_sub = mock_subscriber_repo.create(
            email="active@example.com", is_active=True
        )
        # Create inactive subscriber
        inactive_sub = mock_subscriber_repo.create(
            email="inactive@example.com", is_active=False
        )

        # Both subscribe to player 101
        for sub in [active_sub, inactive_sub]:
            subscription = Subscription(
                subscriber_id=sub.id, entity_type=EntityType.PLAYER, entity_id=101
            )
            mock_subscription_repo.add(subscription)

        # Add event
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=101,
                payload={"message": "Goal"},
            )
        )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # Only active subscriber should receive email
        assert len(mock_email_service.sent_emails) == 1
        assert mock_email_service.sent_emails[0]["to"] == "active@example.com"


class TestDigestErrorHandling:
    """Test error handling in digest service."""

    def test_email_send_failure_records_failed_status(
        self,
        mock_event_repo,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_digest_run_repo,
        mock_email_service,
    ):
        """Test that email failures are recorded as FAILED status."""
        # Setup failing email service
        failing_email_service = MockEmailService(should_fail=True)
        digest_service = DigestService(
            event_repo=mock_event_repo,
            subscriber_repo=mock_subscriber_repo,
            subscription_repo=mock_subscription_repo,
            digest_run_repo=mock_digest_run_repo,
            email_service=failing_email_service,
        )

        # Create subscriber with subscription and event
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )
        subscription = Subscription(
            subscriber_id=subscriber.id, entity_type=EntityType.PLAYER, entity_id=101
        )
        mock_subscription_repo.add(subscription)
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=101,
                payload={"message": "Goal"},
            )
        )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # Verify run was recorded as FAILED
        assert len(mock_digest_run_repo.runs) == 1
        assert mock_digest_run_repo.runs[0].status == "FAILED"

    def test_subscriber_with_no_subscriptions_skipped(
        self, digest_service, mock_subscriber_repo, mock_event_repo, mock_email_service
    ):
        """Test that subscribers with no subscriptions don't get emails."""
        # Create subscriber but NO subscription
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )

        # Add event
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=101,
                payload={"message": "Goal"},
            )
        )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # No email should be sent
        assert len(mock_email_service.sent_emails) == 0

    def test_no_matching_events_skipped(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
    ):
        """Test that subscribers get no email when no events match their subscriptions."""
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )

        # Subscribe to player 101
        subscription = Subscription(
            subscriber_id=subscriber.id, entity_type=EntityType.PLAYER, entity_id=101
        )
        mock_subscription_repo.add(subscription)

        # Add event for player 102 (doesn't match)
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=102,
                payload={"message": "Goal"},
            )
        )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # No email should be sent
        assert len(mock_email_service.sent_emails) == 0


class TestDigestEmailContent:
    """Test the content of generated digest emails."""

    def test_digest_email_format(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
    ):
        """Test that digest email has correct format and structure."""
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )
        subscription = Subscription(
            subscriber_id=subscriber.id, entity_type=EntityType.PLAYER, entity_id=101
        )
        mock_subscription_repo.add(subscription)

        # Add multiple events
        for i in range(3):
            mock_event_repo.add(
                NotificationEvent(
                    event_type=EventType.PLAYER_PERFORMANCE,
                    entity_type=EntityType.PLAYER,
                    entity_id=101,
                    payload={"message": f"Event {i + 1}"},
                )
            )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # Verify email content
        email = mock_email_service.sent_emails[0]
        assert "Hello" in email["body"]
        assert "Here are your updates:" in email["body"]
        assert "Event 1" in email["body"]
        assert "Event 2" in email["body"]
        assert "Event 3" in email["body"]
        assert "Regards," in email["body"]
        assert "Ballwork" in email["body"]

    def test_digest_email_subject(
        self,
        digest_service,
        mock_subscriber_repo,
        mock_subscription_repo,
        mock_event_repo,
        mock_email_service,
    ):
        """Test that digest email has correct subject."""
        subscriber = mock_subscriber_repo.create(
            email="user@example.com", is_active=True
        )
        subscription = Subscription(
            subscriber_id=subscriber.id, entity_type=EntityType.PLAYER, entity_id=101
        )
        mock_subscription_repo.add(subscription)
        mock_event_repo.add(
            NotificationEvent(
                event_type=EventType.PLAYER_PERFORMANCE,
                entity_type=EntityType.PLAYER,
                entity_id=101,
                payload={"message": "Goal"},
            )
        )

        # Run digest
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        digest_service.run_digest(start, end)

        # Verify subject
        email = mock_email_service.sent_emails[0]
        assert email["subject"] == "Your Football Digest"
