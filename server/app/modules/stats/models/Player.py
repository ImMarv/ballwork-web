from pydantic import BaseModel
from datetime import datetime

class Player(BaseModel):
    id: int
    dob: datetime
    age: int
    name: str
    nationality: str
    season_goals: int
    season_assists: int
    season_games: int
    shirt_number: str







