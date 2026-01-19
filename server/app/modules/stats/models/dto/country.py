from pydantic import BaseModel


class Country(BaseModel):
    """Base Pydantic model for the Country.

    Args:
        BaseModel (_type_): Country
    """
    code: int
    name: str
    nationality: str
