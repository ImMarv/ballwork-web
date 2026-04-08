from datetime import date

from pydantic import BaseModel


class PlayerProfile(BaseModel):
    id: int
    name: str
    firstname: str | None = None
    lastname: str | None = None
    dob: date | None = None
    age: int | None = None
    nationality: str | None = None
    height: str | None = None
    weight: str | None = None
    position: str | None = None
    photo: str | None = None
