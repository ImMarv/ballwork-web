"""Service layer for the digest module"""

from datetime import datetime

from sqlalchemy import and_, or_

from server.app.modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)

from .email.email_service import EmailSendError, SMTPEmailService
from .repository.digest_run_repo import DigestRunRepository
from .repository.event_repo import EventRepository
from .repository.subscriber_repo import SubscriberRepository
from .repository.subscription_repo import SubscriptionRepository


class DigestService:
    def __init__(
        self,
        event_repo: EventRepository,
        subscriber_repo: SubscriberRepository,
        subscription_repo: SubscriptionRepository,
        digest_run_repo: DigestRunRepository,
        email_service: SMTPEmailService,
    ) -> None:
        self.email_service = email_service
        self.event_repo = event_repo
        self.subscription_repo = subscription_repo
        self.subscriber_repo = subscriber_repo
        self.digest_run_repo = digest_run_repo

    def run_digest(self, start: datetime, end: datetime) -> None:
        subscribers = self.subscriber_repo.get_all_active()

        for subscriber in subscribers:
            subscriptions = self.subscription_repo.get_subscriptions_from(subscriber.id)

            # Query events AFTER getting subscriptions
            relevant_events = self._filter_events(subscriptions)

            # Filter by date range (do this in DB too)
            relevant_events = [
                e for e in relevant_events if start <= e.created_at <= end
            ]

            if not relevant_events:
                continue  # Skip if no relevant events

            status = "PARTIAL"  # Default to PARTIAL, will update to PASSED or FAILED based on email result
            try:
                body = self._build_digest(relevant_events)
                self.email_service.send_email(
                    to=subscriber.email, subject="Your Football Digest", body=body
                )
                status = "PASSED"
            except EmailSendError as e:
                status = "FAILED"
                # Log the error for debugging
                print(f"Failed to send digest to {subscriber.email}: {e}")
            except Exception as e:
                status = "FAILED"
                # Catch unexpected errors
                print(f"Unexpected error sending digest to {subscriber.email}: {e}")
            finally:
                # Always record the digest run, whether it succeeded or failed
                self.digest_run_repo.add_run(
                    subscriber_id=subscriber.id, period_start=start, status=status
                )

    def _filter_events(self, subscriptions):
        """Get events matching subscriber's subscriptions via database join."""

        if not subscriptions:
            return []

        # Build query with OR conditions for each subscription
        conditions = [
            and_(
                NotificationEvent.entity_type == sub.entity_type,
                NotificationEvent.entity_id == sub.entity_id,
            )
            for sub in subscriptions
        ]

        return (
            self.event_repo.session.query(NotificationEvent)
            .filter(or_(*conditions))
            .all()
        )

    def _build_digest(self, events) -> str:
        lines = ["Hello,", "", "Here are your updates:", ""]

        for event in events:
            lines.append(f"- {event.payload}")

        lines.append("")
        lines.append("Regards,")
        lines.append("Ballwork")

        return "\n".join(lines)