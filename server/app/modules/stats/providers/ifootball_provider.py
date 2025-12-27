"""Module providing abstract methods"""
from abc import ABC, abstractmethod
from typing import Any, Mapping


class FootballDataProvider(ABC):
    """Interface for football data providers

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    async def get_player(self, player_id: int, year: str) -> Mapping[str, Any]:
        pass

    @abstractmethod
    async def get_team(self, team_id: int, year: str) -> Mapping[str, Any]:
        pass

    @abstractmethod
    async def search_players(self, query: str) -> Mapping[str, Any]:
        pass
