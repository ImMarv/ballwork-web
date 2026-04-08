"""Concrete SQLAlchemy implementations of repository interfaces."""

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .models.db.dbmodels import EntityCache


class SQLStatsCacheRepository:
    """SQLAlchemy implementation of StatsCacheRepository."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, key: str, value: str) -> EntityCache:
        """Add a new cache entry."""
        cache_entry = EntityCache(key=key, value=value)
        self.session.add(cache_entry)
        self.session.commit()
        self.session.refresh(cache_entry)
        return cache_entry

    def get(self, key: str) -> Optional[EntityCache]:
        """Get a cache entry by key."""
        return self.session.query(EntityCache).filter(EntityCache.cache_key == key).first()
    
    def delete(self, key: str) -> None:
        """Delete a cache entry by key."""
        cache_entry = self.get(key)
        if cache_entry:
            self.session.delete(cache_entry)
            self.session.commit()

    def clear_expired(self) -> None:
        """Clear expired cache entries."""
        now = date.today()
        expired_entries = self.session.query(EntityCache).filter(EntityCache.expires_at < now).all()
        for entry in expired_entries:
            self.session.delete(entry)
        self.session.commit()