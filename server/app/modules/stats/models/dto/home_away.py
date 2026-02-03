from pydantic import BaseModel


class HomeAway(BaseModel):
    """Base Pydantic model for Home/Away stats

    Args:
        BaseModel (_type_): HomeAway
    """

    home: int | None = None
    away: int | None = None
    total: int | None = None
