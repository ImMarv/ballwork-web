from sqlalchemy import Enum


class EntityType(str, Enum):
    PLAYER = "player"
    TEAM = "team"
    COMPETITION = "competition"
