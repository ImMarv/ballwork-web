from datetime import datetime

from pydantic import BaseModel


class team(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    id: int
    founded: datetime
    name: str
    country: str
    league: str
    goals_for: int
    goals_against: int
    position: str
