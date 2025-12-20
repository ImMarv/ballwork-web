from datetime import datetime

from pydantic import BaseModel


class player(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: int
    dob: datetime
    age: int
    name: str
    nationality: str
    season_goals: int
    season_assists: int
    season_games: int
    shirt_number: str







