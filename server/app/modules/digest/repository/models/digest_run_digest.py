"""Digest run database models."""

from enum import Enum as PyEnum
from .enums.digest_status import DigestStatus
from app.db_base.base import Base
from sqlalchemy import DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column


class DigestRun(Base):
    __tablename__ = "digest_run"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("subscriber_digest.id"))
    period_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    status: Mapped[DigestStatus] = mapped_column(
        SQLEnum(enum_class=DigestStatus, name="digest_status_enum"), nullable=False
    )
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
