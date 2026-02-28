from app.db_base.base import Base  # noqa: E0401
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Subscriber(Base):
    __tablename__ = "subscriber_digest"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    isActive: Mapped[bool] = mapped_column(Boolean)
    createdAt: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
