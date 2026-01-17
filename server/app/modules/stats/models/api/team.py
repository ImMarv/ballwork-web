from datetime import datetime

from country import Country
from home_away import HomeAway
from pydantic import BaseModel


class Team(BaseModel):
    """Base Pydantic model for a team.

    Args:
        BaseModel (_type_): Team
    """

    id: int
    founded: datetime
    name: str
    country: Country
    league: str
    goals_for: int
    goals_against: int
    table_position: str
    wins: HomeAway
    loses: HomeAway
    draws: HomeAway
    goals: HomeAway
