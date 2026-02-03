from pydantic import BaseModel

from .country import Country


class Competition(BaseModel):
    id: int
    country: Country | None = None
    season: int | None = None
    name: str | None = None
    logo: str | None = None
