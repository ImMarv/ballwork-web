from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Set
from uuid import uuid4


def utc_now() -> datetime:
    # SQLite often returns naive datetimes; keep test datetimes naive-UTC for safe comparisons.
    return datetime.now(UTC).replace(tzinfo=None)


@dataclass
class E2ETracker:
    subscriber_ids: Set[int] = field(default_factory=set)
    entity_ids: Set[int] = field(default_factory=set)

    def track_subscriber(self, subscriber_id: int) -> None:
        self.subscriber_ids.add(subscriber_id)

    def track_entity(self, entity_id: int) -> None:
        self.entity_ids.add(entity_id)


def build_test_email() -> str:
    marker = uuid4().hex[:10]
    return f"e2e_{marker}@example.test"


def build_test_entity_id() -> int:
    # Keep ID in signed 32-bit range to be DB-friendly across engines.
    return uuid4().int % 2_000_000_000
