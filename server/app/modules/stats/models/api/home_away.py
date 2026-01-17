from pydantic import BaseModel


class HomeAway(BaseModel):
    """Base Pydantic model for Home/Away stats

    Args:
        BaseModel (_type_): HomeAway
    """
    home: int
    away: int
    total: int
