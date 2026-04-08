"""Contracts for stats cache repositories."""

from datetime import datetime
from typing import Any, Optional, Protocol

from sqlalchemy.orm import Session

from .models.db.dbmodels import EntityCache


class StatsCacheRepository(Protocol):
    """Contract for stats cache repositories."""

    session: Session

    def get(self, cache_key: str) -> Optional[EntityCache]: ...

    def upsert(
        self,
        cache_key: str,
        entity_type: str,
        entity_id: int,
        payload: Any,
        expires_at: datetime,
    ) -> EntityCache: ...

    def delete(self, cache_key: str) -> None: ...

    def clear_expired(self, now: datetime | None = None) -> int: ...