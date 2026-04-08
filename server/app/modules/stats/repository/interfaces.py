"""Concerns the implementation of the StatsRepository interface."""

from typing import Optional, Protocol

from sqlalchemy.orm import Session

from .models.db.dbmodels import EntityCache


class SQLStatsCacheRepository(Protocol):
    """SQLAlchemy implementation of StatsCacheRepository."""

    class SQLStatsCacheRepository(Protocol):
        """Contract for stats cache repositories."""

        session: Session  # explicit protocol attribute

        def add(self, key: str, value: str) -> EntityCache: ...
        def get(self, key: str) -> Optional[EntityCache]: ...
        def delete(self, key: str) -> None: ...
        def clear_expired(self) -> None: ...