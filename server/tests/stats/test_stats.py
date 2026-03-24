"""Tests for the stats module"""

from datetime import date

import pytest
from app.modules.stats.models.dto.competition import Competition
from app.modules.stats.models.dto.country import Country
from app.modules.stats.models.dto.home_away import HomeAway
from app.modules.stats.models.dto.player_profile import PlayerProfile
from app.modules.stats.models.dto.player_statistics import PlayerStatistics
from app.modules.stats.models.dto.team_stats import Team
from app.modules.stats.models.dto.team_summary import TeamSummary
from app.modules.stats.service import StatsService

from .mock_provider import MockFailingProvider, MockWorkingProvider


@pytest.mark.asyncio
async def test_get_player_maps_data_properly():
    """
    Passes if the raw data is correctly mapped.
    """
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.get_player(player_id=276, year="2022")

    assert result == [
        PlayerStatistics(
            id=276,
            name="Neymar",
            season=2022,
            dob=date(year=1992, month=2, day=5),  # 1992-02-05
            photo="https://media.api-sports.io/football/players/276.png",
            age=33,
            nationality="Brazil",
            goals=13,
            assists=11,
            games_played=None,
            position="Attacker",
            shirt_number=None,
        )
    ]


@pytest.mark.asyncio
async def test_get_team_maps_data_properly():
    """
    Passes if the raw data is correctly mapped.
    """
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.get_team(team_id=1, competition_id=1, year="2021")

    assert result == [
        Team(
            id=33,
            name="Manchester United",
            competition=Competition(
                id=39,
                country=None,
                season=2022,
                name="Premier League",
                logo="https://media.api-sports.io/football/leagues/39.png",
            ),
            wins=HomeAway(home=15, away=8, total=23),
            loses=HomeAway(home=1, away=8, total=9),
            draws=HomeAway(home=3, away=3, total=6),
            goals_for=HomeAway(home=36, away=22, total=58),
            goals_against=HomeAway(home=10, away=33, total=43),
        )
    ]


@pytest.mark.asyncio
async def test_get_competition_maps_data_properly():
    """
    Passes if the raw data is correctly mapped.
    """
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.get_competition(competition_id=39)

    assert result == [
        Competition(
            id=39,
            country=Country(
                code="GB",
                name="England",
                logo="https://media.api-sports.io/flags/gb.svg",
            ),
            season=None,
            name="Premier League",
            logo="https://media.api-sports.io/football/leagues/2.png",
        )
    ]


@pytest.mark.asyncio
async def test_get_country_maps_data_properly():
    """
    Passes if the raw data is correctly mapped.
    """
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.get_country(country_code="BR")

    assert result == [
        Country(
            code="GB", name="England", logo="https://media.api-sports.io/flags/gb.svg"
        )
    ]


@pytest.mark.asyncio
async def test_error_is_mapped_on_499_500_iseandtimeout():
    _provider = MockFailingProvider()

    result = await _provider.get_500(player_id=1, year=2022)

    assert result == {
        "message": "Something went wrong while fetching details. Try again later."
    }


@pytest.mark.asyncio
async def test_error_is_mapped_204_nocontent():
    _provider = MockFailingProvider()

    result = await _provider.get_204(id=1, year=2022)

    assert result == {
        "errors": {
            "bug": "This is on our side, please report us this bug on "
            "https://dashboard.api-football.com",
            "report": "players",
            "time": "2019-11-26T00:00:00+00:00",
        },
        "get": "players",
        "paging": {
            "current": 1,
            "total": 1,
        },
        "parameters": [],
        "response": [],
        "results": 0,
    }


@pytest.mark.asyncio
async def test_search_players_maps_data_properly():
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.search_players(query="neymar")

    assert result == [
        PlayerProfile(
            id=276,
            name="Neymar",
            firstname="Neymar",
            lastname="da Silva Santos Júnior",
            dob=date(year=1992, month=2, day=5),
            age=32,
            nationality="Brazil",
            height="175 cm",
            weight="68 kg",
            position="Attacker",
            photo="https://media.api-sports.io/football/players/276.png",
        )
    ]


@pytest.mark.asyncio
async def test_search_players_respects_limit():
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.search_players(query="player", limit=1)

    assert len(result) == 1
    assert result[0].id == 276


@pytest.mark.asyncio
async def test_search_teams_maps_data_properly():
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.search_teams(query="manchester")

    assert result == [
        TeamSummary(
            id=33,
            name="Manchester United",
            code="MUN",
            country="England",
            founded=1878,
            logo="https://media.api-sports.io/football/teams/33.png",
            venue_name="Old Trafford",
            venue_city="Manchester",
        ),
        TeamSummary(
            id=34,
            name="Asscastle United",
            code="MUN",
            country="England",
            founded=1878,
            logo="https://media.api-sports.io/football/teams/34.png",
            venue_name="Somththing Park",
            venue_city="Asscastle",
        ),
    ]


@pytest.mark.asyncio
async def test_search_teams_respects_limit():
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.search_teams(query="team", limit=1)

    assert len(result) == 1
    assert result[0].id == 33


@pytest.mark.asyncio
async def test_search_competitions_maps_data_properly():
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.search_competitions(query="premier")

    assert result == [
        Competition(
            id=39,
            season=None,
            name="Premier League",
            logo="https://media.api-sports.io/football/leagues/2.png",
            country=Country(
                code="GB",
                name="England",
                logo="https://media.api-sports.io/flags/gb.svg",
            ),
        )
    ]


@pytest.mark.asyncio
async def test_unified_search_aggregates_results():
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    async def _search_players(_query: str):
        return {
            "errors": [],
            "response": [{"player": {"id": 7, "name": "Cristiano Ronaldo"}}],
        }

    async def _search_teams(_query: str):
        return {
            "errors": [],
            "response": [
                {
                    "team": {"id": 40, "name": "Liverpool"},
                    "venue": {"name": "Anfield", "city": "Liverpool"},
                }
            ],
        }

    async def _search_competitions(_query: str):
        return {
            "errors": [],
            "response": [
                {
                    "league": {
                        "id": 140,
                        "name": "La Liga",
                        "logo": "https://media.api-sports.io/football/leagues/140.png",
                    },
                    "country": {
                        "code": "ES",
                        "name": "Spain",
                        "flag": "https://media.api-sports.io/flags/es.svg",
                    },
                }
            ],
        }

    _provider.search_players = _search_players
    _provider.search_teams = _search_teams
    _provider.search_competitions = _search_competitions

    result = await _service.unified_search(query="liverpool")

    assert set(result.keys()) == {"players", "teams", "competitions"}
    assert len(result["players"]) == 1
    assert len(result["teams"]) == 1
    assert len(result["competitions"]) == 1
