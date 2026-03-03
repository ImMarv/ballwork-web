"""Tests for the stats module"""

from datetime import date

import pytest
from app.modules.stats.models.dto.competition import Competition
from app.modules.stats.models.dto.country import Country
from app.modules.stats.models.dto.home_away import HomeAway
from server.app.modules.stats.models.dto.player_statistics import PlayerStatistics
from server.app.modules.stats.models.dto.team_stats import Team
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
