from abc import ABC, abstractmethod


class FootballDataProvider(ABC):
    """Interface for football data providers

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    async def get_player(self, player_id: int, year: str):
        pass

    @abstractmethod
    async def get_team(self, team_id: int, year: str):
        pass

    @abstractmethod
    async def search_players(self, query: str):
        pass

    @abstractmethod
    async def search_teams(self, query: str):
        pass
