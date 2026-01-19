from datetime import datetime

from country import Country
from pydantic import BaseModel


class Player(BaseModel):
    """Base pydantic model for a player

    Args:
        BaseModel (_type_): Player
    """

    id: int
    season: int
    name: str
    dob: datetime
    age: int
    position: str
    nationality: Country
    goals: int
    assists: int
    games_played: int
    shirt_number: int
