"""Subscriber DB Model"""

from __future__ import annotations

from datetime import date, datetime

from app.db_base.base import Base
from sqlalchemy import Date, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(64))
    photo_url: Mapped[str | None] = mapped_column(String(128), nullable=True)
    position: Mapped[str | None] = mapped_column(String(32), nullable=True)

    player_seasons: Mapped[list["PlayerSeason"]] = relationship(back_populates="player")


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    logo_url: Mapped[str | None] = mapped_column(String(128), nullable=True)

    player_seasons: Mapped[list["PlayerSeason"]] = relationship(back_populates="team")


class Competition(Base):
    __tablename__ = "competition"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    logo_url: Mapped[str | None] = mapped_column(String(128), nullable=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))

    country: Mapped["Country"] = relationship(back_populates="competitions")
    player_seasons: Mapped[list["PlayerSeason"]] = relationship(
        back_populates="competition"
    )


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    logo_url: Mapped[str | None] = mapped_column(String(128), nullable=True)

    competitions: Mapped[list["Competition"]] = relationship(back_populates="country")


class PlayerSeason(Base):
    __tablename__ = "player_season"

    id: Mapped[int] = mapped_column(primary_key=True)

    season_year: Mapped[int]

    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    competition_id: Mapped[int] = mapped_column(ForeignKey("competition.id"))

    appearances: Mapped[int] = mapped_column(Integer, default=0)
    goals: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    shirt_number: Mapped[int | None] = mapped_column(Integer, nullable=True)

    player: Mapped["Player"] = relationship(back_populates="player_seasons")
    team: Mapped["Team"] = relationship(back_populates="player_seasons")
    competition: Mapped["Competition"] = relationship(back_populates="player_seasons")

class EntityCache(Base):
    __tablename__ = "entity_cache"

    id: Mapped[int] = mapped_column(primary_key=True)
    cache_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)  # e.g., "PLAYER_12345"
    entity_type: Mapped[str] = mapped_column(String(32)) # e.g., "PLAYER", "TEAM"
    entity_id: Mapped[int] = mapped_column(Integer) # External ID
    payload: Mapped[dict] = mapped_column(JSON)  # Store as JSON string
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)