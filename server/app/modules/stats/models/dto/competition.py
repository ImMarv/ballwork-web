from country import Country
from pydantic import BaseModel


class Competition(BaseModel):
    id: int
    country: Country
    season: int
    name: str
    logo: str
