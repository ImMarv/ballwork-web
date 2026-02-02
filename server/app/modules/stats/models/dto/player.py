from datetime import datetime

from pydantic import BaseModel


class Player(BaseModel):
    """Base pydantic model for a player

    Args:
        BaseModel (_type_): Player
    """

    id: int
    season: int
    name: str
    photo: str | None = None
    dob: datetime
    age: int
    position: str
    nationality: str
    goals: int | None = None
    assists: int | None = None
    games_played: int | None = None
    shirt_number: int | None = None
