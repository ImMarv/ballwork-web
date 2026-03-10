"""Service layer for the digest module"""
from datetime import datetime

from .email.email_service import SMTPEmailService
from .repository.digest_run_repo import DigestRunRepository
from .repository.event_repo import EventRepository
from .repository.models.enums import DigestStatus
from .repository.subscriber_repo import SubscriberRepository
from .repository.subscription_repo import SubscriptionRepository


class DigestService:
    def __init__(self, 
                 event_repo: EventRepository,
                 subscriber_repo: SubscriberRepository,
                 subscription_repo: SubscriptionRepository,
                 digest_run_repo: DigestRunRepository,
                 email_service: SMTPEmailService) -> None:
        self.email_service = email_service
        self.event_repo = event_repo
        self.subscription_repo = subscription_repo
        self.subscriber_repo = subscriber_repo
        self.digest_run_repo = digest_run_repo

    def run_digest(self, start: datetime, end: datetime) -> None:

        events = self.event_repo.get_events_between(start, end)

        subscribers = self.subscriber_repo.get_all_active()

        for subscriber in subscribers:

            subscriptions = self.subscription_repo.get_subscriptions_from(subscriber.id)

            relevant_events = self._filter_events(events, subscriptions)

            if not relevant_events:
                continue

            body = self._build_digest(relevant_events)

            self.email_service.send_email(
                to=subscriber.email,
                subject="Your Football Digest",
                body=body
            )

            self.digest_run_repo.add_run(
                subscriber_id = subscriber.id,
                period_start = start,
                status = "PASSED"
            )
    
    def _filter_events(self, events, subscriptions):

        filtered = []

        for event in events:
            for sub in subscriptions:

                if (
                    event.entity_type == sub.entity_type
                    and event.entity_id == sub.entity_id
                ):
                    filtered.append(event)

        return filtered
    
    def _build_digest(self, events) -> str:

        lines = ["Hello,", "", "Here are your updates:", ""]

        for event in events:
            lines.append(f"- {event.payload}")

        lines.append("")
        lines.append("Regards,")
        lines.append("Ballwork")

        return "\n".join(lines)