"""
Service layer of the application.
"""

import hashlib
from asyncio import gather
from datetime import datetime, timedelta, timezone
from typing import Any, TypeVar, cast

from .mappers.mappers import (
    map_competition_response,
    map_country_response,
    map_errors,
    map_player_response,
    map_player_search,
    map_team_response,
    map_team_search,
)
from .providers.api_football import ExternalAPIError
from .providers.ifootball_provider import FootballDataProvider
from .repository.interfaces import StatsCacheRepository
from .repository.models.dto.competition import Competition
from .repository.models.dto.country import Country
from .repository.models.dto.player_profile import PlayerProfile
from .repository.models.dto.player_statistics import PlayerStatistics
from .repository.models.dto.team_stats import Team
from .repository.models.dto.team_summary import TeamSummary

DEFAULT_SEARCH_LIMIT = 10
MAX_SEARCH_LIMIT = 50
DEFAULT_CACHE_TTL_SECONDS = 300
TDto = TypeVar("TDto")


class StatsService:
    """
    Service layer class for establishing business logic.
    Talks to external providers and returns DTOs only.
    """

    def __init__(
        self,
        provider: FootballDataProvider,
        cache_repo: StatsCacheRepository | None = None,
        cache_ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
    ) -> None:
        self._provider = provider
        self._cache_repo = cache_repo
        self._cache_ttl_seconds = cache_ttl_seconds

    # region - Getters
    async def get_player(self, player_id: int, year: str) -> list[PlayerStatistics]:
        """Get player statistics for a given season."""
        cache_key = self._hash_cache_key("player", player_id=player_id, year=year)
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, PlayerStatistics)

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

        self._write_cache(cache_key, "PLAYER", player_id, results)
        return results

    async def get_team(
        self, team_id: int, competition_id: int, year: str
    ) -> list[Team]:
        """Get team statistics for a competition and season."""
        cache_key = self._hash_cache_key(
            "team",
            team_id=team_id,
            competition_id=competition_id,
            year=year,
        )
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, Team)

        raw_team = await self._provider.get_team(team_id, competition_id, year)
        errors = map_errors(raw_team.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)

        teams = raw_team.get("response", {})

        if isinstance(teams, list):
            teams = teams[0] if teams else {}

        dto = map_team_response(teams)
        results = [dto] if dto is not None else []
        self._write_cache(cache_key, "TEAM", team_id, results)
        return results

    async def get_competition(self, competition_id: int) -> list[Competition]:
        """Get competition metadata."""
        cache_key = self._hash_cache_key("competition", competition_id=competition_id)
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, Competition)

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

        self._write_cache(cache_key, "COMPETITION", competition_id, results)
        return results

    async def get_country(self, country_code: str) -> list[Country]:
        """Get country metadata."""
        normalized_country = country_code.capitalize()
        cache_key = self._hash_cache_key("country", country_code=normalized_country)
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, Country)

        raw_country = await self._provider.get_country(normalized_country)

        errors = map_errors(raw_country.get("errors", []))
        if errors:
            raise ExternalAPIError(errors)

        country = raw_country.get("response", [])

        if isinstance(country, list):
            country = country[0] if country else {}

        dto = map_country_response(country)
        results = [dto] if dto is not None else []
        self._write_cache(cache_key, "COUNTRY", 0, results)
        return results

    # endregion

    # region - Searchers
    async def search_players(
        self, query: str, limit: int = DEFAULT_SEARCH_LIMIT
    ) -> list[PlayerProfile]:
        cache_key = self._hash_cache_key("search_players", query=query, limit=limit)
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, PlayerProfile)

        limit = min(limit, MAX_SEARCH_LIMIT)
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

        final_results = results[:limit]
        self._write_cache(cache_key, "SEARCH_PLAYERS", 0, final_results)
        return final_results

    async def search_teams(
        self, query: str, limit: int = DEFAULT_SEARCH_LIMIT
    ) -> list[TeamSummary]:
        cache_key = self._hash_cache_key("search_teams", query=query, limit=limit)
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, TeamSummary)

        limit = min(limit, MAX_SEARCH_LIMIT)
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

        final_results = results[:limit]
        self._write_cache(cache_key, "SEARCH_TEAMS", 0, final_results)
        return final_results

    async def search_competitions(
        self, query: str, limit: int = DEFAULT_SEARCH_LIMIT
    ) -> list[Competition]:
        cache_key = self._hash_cache_key(
            "search_competitions",
            query=query,
            limit=limit,
        )
        cached_payload = self._read_cache(cache_key)
        if cached_payload is not None:
            return self._rehydrate_list(cached_payload, Competition)

        limit = min(limit, MAX_SEARCH_LIMIT)
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

        final_results = results[:limit]
        self._write_cache(cache_key, "SEARCH_COMPETITIONS", 0, final_results)
        return final_results

    async def unified_search(self, query: str):
        players_task = self.search_players(query)
        teams_task = self.search_teams(query)
        competitions_task = self.search_competitions(query)

        players, teams, competitions = await gather(
            players_task, teams_task, competitions_task
        )

        return {
            "players": players,
            "teams": teams,
            "competitions": competitions,
        }

    # endregion

    # region - Helpers
    def _hash_cache_key(self, operation: str, **params: object) -> str:
        """Generate a deterministic cache key from operation and sorted params."""
        canonical = ":".join(
            [
                f"stats:{operation}",
                *[f"{k}={params[k]}" for k in sorted(params)],
            ]
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _read_cache(self, cache_key: str) -> Any | None:
        if self._cache_repo is None:
            return None

        cache_entry = self._cache_repo.get(cache_key)
        if cache_entry is None:
            return None

        now = datetime.now(timezone.utc)
        expires_at = cache_entry.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= now:
            return None

        return cache_entry.payload

    def _write_cache(
        self,
        cache_key: str,
        entity_type: str,
        entity_id: int,
        data: Any,
    ) -> None:
        if self._cache_repo is None:
            return

        payload = self._to_cache_payload(data)
        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=self._cache_ttl_seconds
        )
        self._cache_repo.upsert(
            cache_key=cache_key,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
            expires_at=expires_at,
        )

    def _to_cache_payload(self, data: Any) -> Any:
        """Convert DTOs and nested structures into JSON-compatible objects."""
        if hasattr(data, "model_dump"):
            return data.model_dump(mode="json")
        if isinstance(data, list):
            return [self._to_cache_payload(item) for item in data]
        if isinstance(data, dict):
            return {key: self._to_cache_payload(value) for key, value in data.items()}
        if isinstance(data, datetime):
            return data.isoformat()
        return data

    def _rehydrate_list(self, data: Any, dto_type: type[TDto]) -> list[TDto]:
        """Rebuild DTO instances from cached JSON payloads."""
        if not isinstance(data, list):
            return []

        results: list[TDto] = []
        for item in data:
            if isinstance(item, dto_type):
                results.append(item)
                continue

            model_validate = getattr(dto_type, "model_validate", None)
            if callable(model_validate):
                results.append(cast(TDto, model_validate(item)))
                continue

            parse_obj = getattr(dto_type, "parse_obj", None)
            if callable(parse_obj):
                results.append(cast(TDto, parse_obj(item)))

        return results
    # endregion
