"""
Adapter for api-football
"""

# check .env for api key.
# must handle any errors or issues with the tests here.
import os

import httpx
from dotenv import load_dotenv

from .ifootball_provider import FootballDataProvider


class ExternalAPIError(Exception):
    """Exception handler for providers

    Args:
        Exception (_type_)
    """


class ApiFootballProvider(FootballDataProvider):
    """Base class for the Api-Football data provider

    Args:
        FootballDataProvider (_type_)
    """

    def __init__(self, api_key: str):
        load_dotenv()
        self._base_url = "https://v3.football.api-sports.io/"
        self._api_key = os.environ.get("FOOTBALL_API_KEY")
        self._headers = {"x-apisports-key": api_key}

    async def _request(self, path: str, params: dict):
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(
                    f"{self._base_url}/{path}", headers=self._headers, params=params
                )
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as timeout:
            raise ExternalAPIError("API-Football timed out") from timeout

        except httpx.HTTPStatusError as err:
            raise ExternalAPIError(
                f"API-Football returned {err.response.status_code}"
            ) from err

    async def get_player(self, player_id: int, year: str):
        """Function that gets player data from Api-Football

        Args:
            player_id (int): _description_

        Returns:
            JSON: JSON request
        """
        try:
            return await self._request(
                path="players",
                params={"id": player_id, "season": year},
            )
        except ExternalAPIError:
            return {}

    async def get_team(self, team_id: int, competition_id: int, year: str):
        """Function that gets team data from Api-Football

        Args:
            team_id (int): Team ID from Api-Football

        Returns:
            JSON: JSON request
        """
        return await self._request(
            path="teams/statistics",
            params={"team": team_id, "league": competition_id, "season": year},
        )

    async def search_players(self, query: str):
        """Function that searches for a player based on a query from Api-Football

        Args:
            query (str): Lastname of the entity
        """
        return await self._request(path="players/profiles", params={"query": query})
    
    async def get_competition(self, competition_id: int):
        """Function that retrieves the league required from API-Football

        Args:
            competition_id (int): League of the ID

        Returns:
            JSON: JSON Request
        """
        return await self._request(
            path= "leagues",
            params={
                "id": competition_id
                }
        )
    async def get_country(self, country_code: str):
        """Function that retrieves the country from API-Football

        Args:
            country_code (str): Code of the Country as per ISO 3166

        Returns:
            JSON: JSON request
        """
        return await self._request(
            path= "countries",
            params={"code": country_code}
        )
