from sqlalchemy import Enum


class EventType(str, Enum):
    MATCH_COMPLETED = "match_completed"
    PLAYER_PERFORMANCE = "player_performance"
