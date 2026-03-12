from datetime import datetime
from enum import Enum

from app.db_base.base import Base
from sqlalchemy import JSON, DateTime, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .enums.entity_type import EntityType
from .enums.event_type import EventType


class NotificationEvent(Base):
    __tablename__ = "notification_event_digest"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[EventType] = mapped_column(String(50))  # "goal", "assist", etc.
    entity_type: Mapped[EntityType] = mapped_column()  # PLAYER, TEAM, COMPETITION
    entity_id: Mapped[int] = mapped_column(nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column()
