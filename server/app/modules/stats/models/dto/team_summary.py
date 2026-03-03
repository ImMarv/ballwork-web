from pydantic import BaseModel

from .country import Country


class TeamSummary(BaseModel):
    id: int
    name: str
    code: str | None = None
    country: str | None = None 
    founded: int | None = None
    logo: str | None = None
    venue_name: str | None = None
    venue_city: str | None = None
