from enum import Enum


class EntityType(str, Enum):
    MATCH = "match"
    PLAYER = "player"
    TEAM = "team"
    COMPETITION = "competition"
