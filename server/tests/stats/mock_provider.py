"""
Mock Provider for the Stats module
"""
import json
from pathlib import Path

from app.modules.stats.providers.api_football import ExternalAPIError
from app.modules.stats.providers.ifootball_provider import FootballDataProvider


class BaseMockProvider(FootballDataProvider):
    """
    The base mock provider class for the stats of a player
    """
    async def get_player(self, player_id: int, year: str):
        raise NotImplementedError

    async def get_team(self, team_id: int, competition_id: int, year: str):
        raise NotImplementedError

    async def search_players(self, query: str):
        raise NotImplementedError

    async def search_teams(self, query: str):
        raise NotImplementedError
class MockFailingProvider(BaseMockProvider):
    """
    A failing mock provider. Meant to test various external issues only
    """
    async def get_player(self, player_id: int, year: str):
        """
        Returns an external error.
        
        :param player_id: ID of the Player. 
        :type player_id: int
        :param year: Season year.
        :type year: str
        """
        raise ExternalAPIError("API unavailable")
class MockWorkingProvider(BaseMockProvider):
    """
    A working mock provider. Tests the service works as intended.
    """
    async def get_player(self, player_id: int, year: str):
        """
        Returns mock details of a player
        """
        mock_file = Path(__file__).parent / "mock_player_response.json"
        return json.loads(mock_file.read_text())
    async def get_team(self, team_id: int, competition_id: int, year: str):
        mock_file = Path(__file__).parent / "mock_team_response.json"
        return json.loads((mock_file).read_text())
