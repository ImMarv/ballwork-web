from datetime import date

from pydantic import BaseModel

from .competition import Competition
from .home_away import HomeAway


class Team(BaseModel):
    """Base Pydantic model for a team.

    Args:
        BaseModel (_type_): Team
    """

    id: int
    name: str
    competition: Competition
    table_position: int | None = None
    goals_for: HomeAway
    goals_against: HomeAway
    wins: HomeAway
    loses: HomeAway
    draws: HomeAway
