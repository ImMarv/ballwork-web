from pydantic import BaseModel
from datetime import datetime

class Team(BaseModel):
    id: int
    founded: datetime
    name: str
    country: str
    league: str
    goals_for: int
    goals_against: int
    position: str







