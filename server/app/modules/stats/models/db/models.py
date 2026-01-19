"""This is where all the database models are.
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(64))
    dob: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    nationality: Mapped[str] = mapped_column(String(64))
    photo: Mapped[str] = mapped_column(String(128))
    position: Mapped[str] = mapped_column(String(12))

    # Relationships
    player_seasons: Mapped[List["PlayerSeason"]] = relationship(back_populates="player")

class Team(Base):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(64))
    logo: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Relationships
    team_seasons: Mapped[List["TeamSeason"]] = relationship(back_populates="team")

class Competition(Base):
    __tablename__ = "competition"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(64))
    logo: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))

    # Relationships
    country: Mapped["Country"] = relationship(back_populates="competitions")
    competition_seasons: Mapped[List["CompetitionSeason"]] = relationship(back_populates="competition")

class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    country_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(64))
    logo: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Relationships
    competitions: Mapped[List["Competition"]] = relationship(back_populates="country")

class PlayerSeason(Base):
    __tablename__ = "player_season"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    team_season_id: Mapped[int] = mapped_column(ForeignKey("team_season.team_season_id"))
    appearances: Mapped[int] = mapped_column(Integer, default=0)
    goals: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    shirt_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    player: Mapped["Player"] = relationship()
    team_season: Mapped["TeamSeason"] = relationship(back_populates="player_seasons")

class TeamSeason(Base):
    __tablename__ = "team_season"
    team_season_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    competition_season_id: Mapped[int] = mapped_column(ForeignKey("competition_season.id"))
    played: Mapped[int] = mapped_column(Integer, default=0)
    wins_home: Mapped[int] = mapped_column(Integer, default=0)
    wins_away: Mapped[int] = mapped_column(Integer, default=0)
    losses_home: Mapped[int] = mapped_column(Integer, default=0)
    losses_away: Mapped[int] = mapped_column(Integer, default=0)
    draws_home: Mapped[int] = mapped_column(Integer, default=0)
    draws_away: Mapped[int] = mapped_column(Integer, default=0)
    goals_for_home: Mapped[int] = mapped_column(Integer, default=0)
    goals_for_away: Mapped[int] = mapped_column(Integer, default=0)
    goals_against_home: Mapped[int] = mapped_column(Integer, default=0)
    goals_against_away: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="team_seasons")
    competition_season: Mapped["CompetitionSeason"] = relationship(back_populates="team_seasons")
    player_seasons: Mapped[List["PlayerSeason"]] = relationship(back_populates="team_season")

class CompetitionSeason(Base):
    __tablename__ = "competition_season"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competition.id"))
    season_year: Mapped[int] = mapped_column(Integer)

    # Relationships
    competition: Mapped["Competition"] = relationship(back_populates="competition_seasons")
    team_seasons: Mapped[List["TeamSeason"]] = relationship(back_populates="competition_season")