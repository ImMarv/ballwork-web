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

    async def search_teams(self, query: str):
        raise NotImplementedError

    async def search_players(self, query: str):
        raise NotImplementedError

    async def search_competitions(self, query: str):
        raise NotImplementedError

    async def get_competition(self, competition_id: int):
        raise NotImplementedError

    async def get_country(self, country_code: str):
        raise NotImplementedError


class MockFailingProvider(BaseMockProvider):
    """
    A failing mock provider. Meant to test various external issues only
    """

    async def get_500(self, player_id: int, year: int):
        """
        Returns an external error.

        :param player_id: ID of the Player.
        :type player_id: int
        :param year: Season year.
        :type year: str
        """
        mock_file = Path(__file__).parent / "mock_500_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def get_204(self, id: int, year: int):
        mock_file = Path(__file__).parent / "mock_204_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def search_teams(self, query: str):
        return {"response": [], "errors": []}

    async def search_players(self, query: str):
        return {"response": [], "errors": []}

    async def search_competitions(self, query: str):
        return {"response": [], "errors": []}


class MockWorkingProvider(BaseMockProvider):
    """
    A working mock provider. Tests the service works as intended.
    """

    async def get_player(self, player_id: int, year: str):
        """
        Returns mock details of a player
        """
        mock_file = Path(__file__).parent / "mock_player_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def get_team(self, team_id: int, competition_id: int, year: str):
        mock_file = Path(__file__).parent / "mock_team_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def get_competition(self, competition_id: int):
        """
        Returns mock details of a competition
        """
        mock_file = Path(__file__).parent / "mock_competition_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def get_country(self, country_code: str):
        """
        Returns mock details of a country
        """
        mock_file = Path(__file__).parent / "mock_country_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def search_teams(self, query: str):
        """
        Returns mock details of a team search
        """
        mock_file = Path(__file__).parent / "mock_search_teams_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def search_players(self, query: str):
        """Returns mock details of a player search"""
        mock_file = Path(__file__).parent / "mock_search_players_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def search_competitions(self, query: str):
        """Returns mock details of a competition search"""
        mock_file = Path(__file__).parent / "mock_search_competitions_response.json"
        return json.loads(mock_file.read_text(encoding="utf-8"))

    async def unified_search(self, query: str):
        """Returns mock details of a unified search"""
        # I'll implement this when I have the time, but for now, it's nothing
        return {"response": [], "errors": []}
