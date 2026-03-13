"""Tests for email service."""

import pytest

from ...app.modules.digest.email.email_service import EmailSendError
from .mock_repo import MockEmailService


class TestEmailService:
    """Test email service functionality."""

    def test_successful_send(self):
        """Test successful email sending."""
        service = MockEmailService(should_fail=False)

        service.send_email(
            to="user@example.com",
            subject="Test Subject",
            body="Test Body",
        )

        assert len(service.sent_emails) == 1
        email = service.sent_emails[0]
        assert email["to"] == "user@example.com"
        assert email["subject"] == "Test Subject"
        assert email["body"] == "Test Body"

    def test_send_failure_raises_error(self):
        """Test that email send failure raises EmailSendError."""
        service = MockEmailService(should_fail=True)

        with pytest.raises(EmailSendError):
            service.send_email(
                to="user@example.com",
                subject="Test Subject",
                body="Test Body",
            )

    def test_multiple_emails(self):
        """Test sending multiple emails."""
        service = MockEmailService(should_fail=False)

        for i in range(3):
            service.send_email(
                to=f"user{i}@example.com",
                subject=f"Subject {i}",
                body=f"Body {i}",
            )

        assert len(service.sent_emails) == 3

    def test_email_timestamp_recorded(self):
        """Test that email timestamp is recorded."""
        service = MockEmailService(should_fail=False)

        service.send_email(
            to="user@example.com",
            subject="Test",
            body="Test",
        )

        email = service.sent_emails[0]
        assert "timestamp" in email
        assert email["timestamp"] is not None

    def test_email_content_validation(self):
        """Test email content is preserved correctly."""
        service = MockEmailService(should_fail=False)

        body = "Line 1\nLine 2\nLine 3"
        service.send_email(
            to="user@example.com",
            subject="Multi-line Test",
            body=body,
        )

        email = service.sent_emails[0]
        assert email["body"] == body
