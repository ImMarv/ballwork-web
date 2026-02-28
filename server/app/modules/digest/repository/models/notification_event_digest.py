from datetime import datetime
from enum import Enum

from app.db_base.base import Base
from sqlalchemy import JSON, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class EventType(str, Enum):
    MATCH_COMPLETED = "match_completed"
    PLAYER_PERFORMANCE = "player_performance"


class NotificationEvent(Base):
    __tablename__ = "notification_event_digest"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[EventType] = mapped_column(SQLEnum(EventType), nullable=False)
    entity_id: Mapped[int] = mapped_column(nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
