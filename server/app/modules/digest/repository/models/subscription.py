"""Subscription DB Model"""

from __future__ import annotations

from datetime import datetime

from app.db_base.base import Base
from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class EntityType(str, Enum):
    USER = "user"
    POST = "post"
    COMMENT = "comment"


class Subscription(Base):
    __tablename__ = "subscription_digest"
    id: Mapped[int] = mapped_column(primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("subscriber_digest.id"))
    target_type: Mapped[str] = mapped_column(String(20))
    createdAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
