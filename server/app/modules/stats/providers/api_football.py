# check .env for api key.
# must handle any errors or issues with the tests here.
import os

import httpx
from dotenv import load_dotenv
from ifootball_provider import FootballDataProvider


class ExternalAPIError(Exception):
    pass


class ApiFootballProvider(FootballDataProvider):
    """Base class for the Api-Football data provider

    Args:
        FootballDataProvider (_type_): _description_
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
                    f"{self._base_url}/{path}",
                    headers=self._headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as timeout:
            raise ExternalAPIError("API-Football timeout") from timeout

        except httpx.HTTPStatusError as e:
            raise ExternalAPIError(
                f"API-Football returned {e.response.status_code}"
            ) from e

    async def get_player(self, player_id: int, year: str):
        """Function that gets player data from Api-Football

        Args:
            player_id (int): _description_

        Returns:
            JSON: JSON request
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/players",
                headers=self._headers,
                params={"id": player_id, "season": year},
            )
        response.raise_for_status()
        return response.json()

    async def get_team(self, team_id: int, year: str):
        """Function that gets team data from Api-Football

        Args:
            team_id (int): Team ID from Api-Football

        Returns:
            JSON: JSON request
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/teams/statistics",
                headers=self._headers,
                params={"team": team_id, "season": year},
            )
            response.raise_for_status()
            return response.json()
