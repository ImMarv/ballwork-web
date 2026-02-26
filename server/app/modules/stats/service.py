"""
Service layer of the application.
"""

from .mappers.mappers import (
    map_competition_response,
    map_country_response,
    map_errors,
    map_player_response,
    map_team_response,
)
from .models.dto.competition import Competition
from .models.dto.country import Country
from .models.dto.player import Player
from .models.dto.team import Team
from .providers.api_football import ExternalAPIError
from .providers.ifootball_provider import FootballDataProvider


class StatsService:
    """
    Service layer class for establishing business logic.
    Talks to external providers and returns DTOs only.
    """

    def __init__(self, provider: FootballDataProvider):
        self._provider = provider

    async def get_player(self, player_id: int, year: str) -> list[Player]:
        """Get player statistics for a given season."""
        raw_player = await self._provider.get_player(player_id, year)

        errors = map_errors(raw_player.get("errors", {}))
        if errors:
            raise ExternalAPIError(errors)

        players = raw_player.get("response", [])
        results: list[Player] = []

        for p in players:
            dto = map_player_response(p)
            if dto is not None:
                results.append(dto)

        return results

    async def get_team(
        self, team_id: int, competition_id: int, year: str
    ) -> list[Team]:
        """Get team statistics for a competition and season."""

        raw_team = await self._provider.get_team(team_id, competition_id, year)
        errors = map_errors(raw_team.get("errors", {}))
        if errors:
            raise ExternalAPIError(errors)

        teams = raw_team.get("response", {})

        if isinstance(teams, list):
            teams = teams[0] if teams else {}

        dto = map_team_response(teams)
        return [dto] if dto is not None else []

    async def search_players(self, query: str) -> list[Player]:
        # Placeholder for future implementation
        return []

    async def get_competition(self, competition_id: int) -> list[Competition]:
        """Get competition metadata."""

        raw_competition = await self._provider.get_competition(competition_id)

        errors = map_errors(raw_competition.get("errors", {}))
        if errors:
            raise ExternalAPIError(errors)

        competitions = raw_competition.get("response", [])
        results: list[Competition] = []

        for c in competitions:
            dto = map_competition_response(c)
            if dto is not None:
                results.append(dto)

        return results

    async def get_country(self, country_code: str) -> list[Country]:
        """Get country metadata."""
        raw_country = await self._provider.get_country(country_code.capitalize())

        errors = map_errors(raw_country.get("errors"))
        if errors:
            raise ExternalAPIError(errors)

        country = raw_country.get("response", [])

        if isinstance(country, list):
            country = country[0] if country else {}

        dto = map_country_response(country)
        return [dto] if dto is not None else []
