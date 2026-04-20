"""Provider that reads mock payloads from a dedicated mock API service."""

import httpx

from .ifootball_provider import FootballDataProvider


class MockAPIServiceProvider(FootballDataProvider):
    def __init__(self, base_url: str, timeout_seconds: float = 5.0):
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    async def _request(self, path: str, params: dict):
        async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
            response = await client.get(
                f"{self._base_url}/{path}",
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def get_player(self, player_id: int, year: str):
        return await self._request(
            path="players",
            params={"id": player_id, "season": year},
        )

    async def get_team(self, team_id: int, competition_id: int, year: str):
        return await self._request(
            path="teams/statistics",
            params={"team": team_id, "league": competition_id, "season": year},
        )

    async def search_players(self, query: str):
        return await self._request(path="players/profiles", params={"search": query})

    async def search_teams(self, query: str):
        return await self._request(path="teams", params={"search": query})

    async def search_competitions(self, query: str):
        return await self._request(path="leagues", params={"search": query})

    async def get_competition(self, competition_id: int):
        return await self._request(path="leagues", params={"id": competition_id})

    async def get_country(self, country_code: str):
        return await self._request(path="countries", params={"code": country_code})
