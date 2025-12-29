from datetime import datetime

from pydantic import BaseModel


class player(BaseModel):
    """Base pydantic model for a player

    Args:
        BaseModel (_type_): _description_
    """
    id: int
    dob: datetime
    age: int
    name: str
    nationality: str
    season_year: str
    season_goals: int
    season_assists: int
    season_games: int
    position: str