"""Subscription DB Model"""

from __future__ import annotations

from datetime import datetime

from app.db_base.base import Base
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .enums.entity_type import EntityType


class Subscription(Base):
    __tablename__ = "subscription_digest"
    id: Mapped[int] = mapped_column(primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("subscriber_digest.id"))
    entity_id: Mapped[int] = mapped_column(index=True)
    entity_type: Mapped[EntityType] = mapped_column()
    target_type: Mapped[str] = mapped_column(String(20))
    createdAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
