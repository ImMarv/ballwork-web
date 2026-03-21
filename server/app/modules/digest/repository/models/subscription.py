"""Subscription DB Model"""

from __future__ import annotations

from datetime import datetime

from app.db_base.base import Base
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text

from .enums.entity_type import EntityType


class Subscription(Base):
    __tablename__ = "subscription_digest"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(
        ForeignKey("subscriber_digest.id"), index=True
    )

    entity_id: Mapped[int] = mapped_column(index=True)
    entity_type: Mapped[EntityType] = mapped_column(
        Enum(EntityType, name="entity_type_enum"), nullable=False
    )
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)

    # Scheduler fields
    next_run: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        index=True,
    )
    last_run: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    day_freq: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="1",
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
