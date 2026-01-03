"""Tests for the stats module"""
import pytest
from app.modules.stats.service import StatsService

from .mock_provider import MockFailingProvider, MockWorkingProvider


@pytest.mark.asyncio
async def test_get_player_handles_external_api_error():
    """
    Checks if the service correctly handles external errors.
    """
    _provider = MockFailingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.get_player(player_id=1, year="2021")

    assert result == []

@pytest.mark.asyncio
async def test_get_player_maps_data_properly():
    """
    Passes if the raw data is correctly mapped.
    """
    _provider = MockWorkingProvider()
    _service = StatsService(provider=_provider)

    result = await _service.get_player(player_id=276, year="2022")

    assert result == [
  {
    "id": 276,
    "name": "Neymar",
    "season": 2022,
    "dob": "1992-02-05",
    "photo": "https://media.api-sports.io/football/players/276.png",
    "age": 33,
    "nationality": "Brazil",
    "team_id": 85,
    "team_name": "Paris Saint Germain",
    "season_goals": 13,
    "season_assists": 11,
    "games_played": 20,
    "position": "Attacker",
    "number": None
  }
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
  {
    "id": 33,
    "team_name": "Manchester United",
    "team_logo": "https://media.api-sports.io/football/teams/33.png",
    "competition_id": 39,
    "competition_name": "Premier League",
    "competition_logo": "https://media.api-sports.io/football/leagues/39.png",
    "competition_region": "England",
    "year": 2022,
    "form": "LLWWWWLWDWDWLWWWWWDLWDWWLDLWWWDWLLWWWW",
    "played": 38,
    "wins": {
      "home": 15,
      "away": 8,
      "total": 23
    },
    "loses": {
      "home": 1,
      "away": 8,
      "total": 9
    },
    "draws": {
      "home": 3,
      "away": 3,
      "total": 6
    },
    "goals_for": {
      "home": 36,
      "away": 22,
      "total": 58
    },
    "goals_against": {
      "home": 10,
      "away": 33,
      "total": 43
    }
  }
]
