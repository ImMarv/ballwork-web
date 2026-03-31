from datetime import datetime
from enum import Enum

from app.db_base.base import Base
from sqlalchemy import JSON, DateTime, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text

from .enums.entity_type import EntityType
from .enums.event_type import EventType


class NotificationEvent(Base):
    __tablename__ = "notification_event_digest"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_type_enum"), nullable=False
    )
    entity_type: Mapped[EntityType] = mapped_column(
        SQLEnum(EntityType, name="entity_type_enum"), nullable=False
    )
    entity_id: Mapped[int] = mapped_column(nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=func.now,
        nullable=False,
    )
