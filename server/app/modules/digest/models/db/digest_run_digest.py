"""Digest run database models."""

from enum import Enum as PyEnum

from app.db_base.base import Base
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class DigestStatus(PyEnum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class DigestRun(Base):
    __tablename__ = "digest_run"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("subscriber_digest.id"))
    period_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    status: Mapped[DigestStatus] = mapped_column(Enum(DigestStatus))
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
