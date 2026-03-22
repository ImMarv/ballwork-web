"""Scheduler jobs for digest ingestion workflows."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from ..modules.digest.repository.models.enums.entity_type import EntityType
from ..modules.digest.repository.models.enums.event_type import EventType
from ..modules.digest.repository.models.notification_event_digest import (
    NotificationEvent,
)
from ..modules.digest.repository.models.subscription import Subscription

LOGGER = logging.getLogger(__name__)

MIN_SUPPORTED_SEASON = 2022
MAX_SUPPORTED_SEASON = 2024


def _select_supported_season(now: datetime) -> str:
    """Clamp season year to provider-supported range."""
    season = max(MIN_SUPPORTED_SEASON, min(MAX_SUPPORTED_SEASON, now.year))
    return str(season)


def _serialize_payload(value: Any) -> dict[str, Any]:
    """Normalize provider DTOs for JSON storage."""
    if isinstance(value, dict):
        return value

    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")

    if hasattr(value, "dict"):
        return value.dict()

    return {"value": str(value)}


def _resolve_event_type(subscription: Subscription) -> EventType | None:
    """Map subscription metadata to a digest event type."""
    target_type = (subscription.target_type or "").strip().lower()

    if subscription.entity_type == EntityType.PLAYER:
        return EventType.PLAYER_PERFORMANCE

    if subscription.entity_type == EntityType.MATCH:
        return EventType.MATCH_COMPLETED

    if "player" in target_type and "performance" in target_type:
        return EventType.PLAYER_PERFORMANCE

    return None


def _get_due_subscriptions(subscription_repo: Any, now: datetime) -> list[Subscription]:
    """Get due subscriptions from repository API."""
    return list(subscription_repo.get_due_subscriptions(now))


def _save_events(event_repo: Any, events: list[NotificationEvent]) -> None:
    """Persist events using batch method if available."""
    add_many = getattr(event_repo, "add_many", None)
    if callable(add_many):
        add_many(events)
        return

    for event in events:
        event_repo.add(event)


def _subscription_window_start(subscription: Subscription) -> datetime:
    """Compute idempotency window start for a subscription run."""
    if subscription.last_run is not None:
        return subscription.last_run
    return subscription.createdAt


def _event_exists_for_window(
    event_repo: Any,
    subscription: Subscription,
    event_type: EventType,
    start: datetime,
    end: datetime,
) -> bool:
    """Check if this subscription already produced events in the current run window."""
    exists_event = getattr(event_repo, "exists_event_in_window", None)
    if not callable(exists_event):
        return False

    return bool(
        exists_event(
            entity_type=subscription.entity_type,
            entity_id=subscription.entity_id,
            event_type=event_type,
            start=start,
            end=end,
        )
    )


def _dedupe_snapshots(snapshots: list[Any]) -> list[Any]:
    """Drop duplicate snapshots before insert to avoid duplicated payload rows."""
    seen: set[str] = set()
    deduped: list[Any] = []

    for snapshot in snapshots:
        payload = _serialize_payload(snapshot)
        key = json.dumps(payload, sort_keys=True, default=str)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(snapshot)

    return deduped


def _mark_subscription_ran(
    subscription_repo: Any,
    subscription: Subscription,
    now: datetime,
) -> None:
    """Update last and next run timestamps after a processing attempt."""
    freq_days = max(1, int(subscription.day_freq or 1))
    subscription.last_run = now
    subscription.next_run = now + timedelta(days=freq_days)

    mark_run = getattr(subscription_repo, "mark_subscription_run", None)
    if callable(mark_run):
        mark_run(
            subscription_id=subscription.id,
            last_run=subscription.last_run,
            next_run=subscription.next_run,
        )
        return

    update = getattr(subscription_repo, "update", None)
    if callable(update):
        update(subscription)
        return

    raise AttributeError(
        "Subscription repository must expose mark_subscription_run(...) or update(subscription)"
    )


async def _fetch_subscription_snapshot(
    stats_service: Any,
    subscription: Subscription,
    season: str,
) -> list[Any]:
    """Fetch entity data from provider based on subscription scope."""
    if subscription.entity_type == EntityType.PLAYER:
        return await stats_service.get_player(subscription.entity_id, season)

    LOGGER.warning(
        "Skipping subscription %s: unsupported entity_type=%s",
        subscription.id,
        subscription.entity_type,
    )
    return []


async def ingest_due_subscriptions_job(
    stats_service: Any,
    event_repo: Any,
    subscription_repo: Any,
    now: datetime | None = None,
) -> None:
    """Ingest due subscriptions and persist entity snapshots as digest events."""
    current = now or datetime.now(timezone.utc)
    season = _select_supported_season(current)

    subscriptions = _get_due_subscriptions(subscription_repo, current)
    if not subscriptions:
        LOGGER.info("Ingestion job: no subscriptions due at %s", current.isoformat())
        return

    LOGGER.info("Ingestion job: processing %s due subscriptions", len(subscriptions))

    for subscription in subscriptions:
        try:
            event_type = _resolve_event_type(subscription)
            if event_type is None:
                LOGGER.warning(
                    "Skipping subscription %s: unsupported target_type=%s",
                    subscription.id,
                    subscription.target_type,
                )
                _mark_subscription_ran(subscription_repo, subscription, current)
                continue

            window_start = _subscription_window_start(subscription)
            if _event_exists_for_window(
                event_repo=event_repo,
                subscription=subscription,
                event_type=event_type,
                start=window_start,
                end=current,
            ):
                LOGGER.info(
                    "Skipping subscription %s: duplicate window already ingested",
                    subscription.id,
                )
                _mark_subscription_ran(subscription_repo, subscription, current)
                continue

            snapshots = await _fetch_subscription_snapshot(
                stats_service=stats_service,
                subscription=subscription,
                season=season,
            )

            snapshots = _dedupe_snapshots(snapshots)

            events = [
                NotificationEvent(
                    event_type=event_type,
                    entity_type=subscription.entity_type,
                    entity_id=subscription.entity_id,
                    payload=_serialize_payload(snapshot),
                    created_at=current,
                )
                for snapshot in snapshots
            ]

            if events:
                _save_events(event_repo, events)
                LOGGER.info(
                    "Created %s events for subscription %s",
                    len(events),
                    subscription.id,
                )

            _mark_subscription_ran(subscription_repo, subscription, current)
        except (TypeError, ValueError, RuntimeError, AttributeError):
            LOGGER.exception(
                "Failed to process subscription %s", getattr(subscription, "id", None)
            )
