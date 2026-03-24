from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.modules.stats.service import StatsService


@pytest.mark.asyncio
async def test_search_player_stage_returns_expected_profile():
    provider = AsyncMock()
    provider.search_players.return_value = {
        "errors": [],
        "response": [
            {
                "player": {
                    "id": 12345,
                    "name": "Lionel Test",
                    "firstname": "Lionel",
                    "lastname": "Test",
                    "birth": {"date": "1987-06-24"},
                    "age": 38,
                    "photo": "https://example.test/player.png",
                    "position": "Forward",
                    "height": "170 cm",
                    "weight": "72 kg",
                    "nationality": "Argentina",
                }
            }
        ],
    }

    service = StatsService(provider)
    players = await service.search_players("Lionel", limit=1)

    assert len(players) == 1
    assert players[0].id == 12345
    assert players[0].name == "Lionel Test"
    provider.search_players.assert_awaited_once_with("Lionel")
