"""
Service layer of the application.
"""
from asyncio import gather
from .mappers.mappers import (
    map_competition_response,
    map_country_response,
    map_errors,
    map_player_response,
    map_team_response,
    map_player_search,
    map_team_search
)
from .models.dto.competition import Competition
from .models.dto.country import Country
from .models.dto.player_statistics import PlayerStatistics
from .models.dto.team_stats import Team
from .models.dto.team_summary import TeamSummary
from .models.dto.player_profile import PlayerProfile
from .providers.api_football import ExternalAPIError
from .providers.ifootball_provider import FootballDataProvider


class StatsService:
    """
    Service layer class for establishing business logic.
    Talks to external providers and returns DTOs only.
    """

    def __init__(self, provider: FootballDataProvider):
        self._provider = provider

    # region - Getters
    async def get_player(self, player_id: int, year: str) -> list[PlayerStatistics]:
        """Get player statistics for a given season."""
        raw_player = await self._provider.get_player(player_id, year)

        errors = map_errors(raw_player.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)

        players = raw_player.get("response", [])
        results: list[PlayerStatistics] = []

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
        errors = map_errors(raw_team.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)

        teams = raw_team.get("response", {})

        if isinstance(teams, list):
            teams = teams[0] if teams else {}

        dto = map_team_response(teams)
        return [dto] if dto is not None else []

    async def get_competition(self, competition_id: int) -> list[Competition]:
        """Get competition metadata."""

        raw_competition = await self._provider.get_competition(competition_id)

        errors = map_errors(raw_competition.get("errors", []))
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

        errors = map_errors(raw_country.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)

        country = raw_country.get("response", [])

        if isinstance(country, list):
            country = country[0] if country else {}

        dto = map_country_response(country)
        return [dto] if dto is not None else []
    # endregion

    # region - Searchers
    async def search_players(self, query: str) -> list[PlayerProfile]:
        # Placeholder for future implementation
        raw_search = await self._provider.search_players(query)

        errors = map_errors(raw_search.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)
        
        players = raw_search.get("response", [])
        results: list[PlayerProfile] = []

        for p in players:
            dto = map_player_search(p)
            if dto is not None:
                results.append(dto)

        return results
    
    async def search_teams(self, query: str) -> list[TeamSummary]:
        raw_search = await self._provider.search_teams(query)

        errors = map_errors(raw_search.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)
        
        teams = raw_search.get("response", [])
        results: list[TeamSummary] = []

        for t in teams:
            dto = map_team_search(t)
            if dto is not None:
                results.append(dto)

        return results
    
    async def search_competitions(self, query: str) -> list[Competition]:
        raw_search = await self._provider.search_competitions(query)

        errors = map_errors(raw_search.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)
        
        competitions = raw_search.get("response", [])
        results: list[Competition] = []

        for c in competitions:
            dto = map_competition_response(c)
            if dto is not None:
                results.append(dto)

        return results
    
    async def unified_search(self, query: str):
        players_task = self.search_players(query)
        teams_task = self.search_teams(query)
        competitions_task = self.search_competitions(query)

        players, teams, competitions = await gather(
            players_task,
            teams_task,
            competitions_task
        )

        return {
            "players": players,
            "teams": teams,
            "competitions": competitions,
        }
    
    # endregion
