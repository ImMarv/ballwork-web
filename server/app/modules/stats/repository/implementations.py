"""Concrete SQLAlchemy implementations of repository interfaces."""

from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session

from .interfaces import StatsCacheRepository
from .models.db.dbmodels import EntityCache


class SQLStatsCacheRepository(StatsCacheRepository):
    """SQLAlchemy implementation of StatsCacheRepository."""

    def __init__(self, session: Session):
        self.session = session

    def upsert(
        self,
        cache_key: str,
        entity_type: str,
        entity_id: int,
        payload: Any,
        expires_at: datetime,
    ) -> EntityCache:
        """Insert or update a cache entry by key."""
        cache_entry = (
            self.session.query(EntityCache)
            .filter(EntityCache.cache_key == cache_key)
            .first()
        )

        if cache_entry is None:
            cache_entry = EntityCache(
                cache_key=cache_key,
                entity_type=entity_type,
                entity_id=entity_id,
                payload=payload,
                expires_at=expires_at,
            )
            self.session.add(cache_entry)
        else:
            cache_entry.entity_type = entity_type
            cache_entry.entity_id = entity_id
            cache_entry.payload = payload
            cache_entry.expires_at = expires_at

        self.session.commit()
        self.session.refresh(cache_entry)
        return cache_entry

    def get(self, cache_key: str) -> Optional[EntityCache]:
        """Get a cache entry by key."""
        return (
            self.session.query(EntityCache)
            .filter(EntityCache.cache_key == cache_key)
            .first()
        )

    def delete(self, cache_key: str) -> None:
        """Delete a cache entry by key."""
        cache_entry = self.get(cache_key)
        if cache_entry:
            self.session.delete(cache_entry)
            self.session.commit()

    def clear_expired(self, now: datetime | None = None) -> int:
        """Clear expired cache entries and return number removed."""
        now = now or datetime.now(timezone.utc)
        expired_entries = (
            self.session.query(EntityCache)
            .filter(EntityCache.expires_at < now)
            .all()
        )
        removed = len(expired_entries)
        for entry in expired_entries:
            self.session.delete(entry)
        if removed:
            self.session.commit()
        return removed