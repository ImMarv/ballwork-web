"""Runtime mock provider for football stats endpoints."""

import asyncio
import random
from datetime import date

from .ifootball_provider import FootballDataProvider


class MockFootballProvider(FootballDataProvider):
    """Deterministic mock provider with configurable latency."""

    def __init__(self, min_latency_ms: int = 40, max_latency_ms: int = 180):
        self._min_latency_ms = max(0, min_latency_ms)
        self._max_latency_ms = max(self._min_latency_ms, max_latency_ms)

    async def _simulate_latency(self, seed: str) -> None:
        rng = random.Random(seed)
        delay_ms = rng.randint(self._min_latency_ms, self._max_latency_ms)
        await asyncio.sleep(delay_ms / 1000)

    async def get_player(self, player_id: int, year: str):
        await self._simulate_latency(f"player:{player_id}:{year}")

        return {
            "errors": [],
            "response": [
                {
                    "player": {
                        "id": player_id,
                        "name": f"Mock Player {player_id}",
                        "firstname": "Mock",
                        "lastname": f"Player {player_id}",
                        "birth": {"date": "1998-02-14"},
                        "age": max(18, date.today().year - 1998),
                        "photo": "https://images.example.test/players/mock-player.png",
                        "nationality": "Testland",
                    },
                    "statistics": [
                        {
                            "league": {
                                "id": 39,
                                "name": "Mock Premier League",
                                "season": int(year),
                                "logo": "https://images.example.test/leagues/mock-premier.png",
                            },
                            "games": {
                                "appearances": 24,
                                "position": "Attacker",
                                "number": 9,
                            },
                            "goals": {
                                "total": 11,
                                "assists": 7,
                            },
                        }
                    ],
                }
            ],
        }

    async def get_team(self, team_id: int, competition_id: int, year: str):
        await self._simulate_latency(f"team:{team_id}:{competition_id}:{year}")

        return {
            "errors": [],
            "response": [
                {
                    "team": {
                        "id": team_id,
                        "name": f"Mock FC {team_id}",
                    },
                    "league": {
                        "id": competition_id,
                        "name": "Mock Competition",
                        "season": int(year),
                        "logo": "https://images.example.test/leagues/mock-competition.png",
                    },
                    "fixtures": {
                        "wins": {"home": 10, "away": 8, "total": 18},
                        "loses": {"home": 3, "away": 4, "total": 7},
                        "draws": {"home": 2, "away": 3, "total": 5},
                    },
                    "goals": {
                        "for": {"total": {"home": 28, "away": 23, "total": 51}},
                        "against": {"total": {"home": 11, "away": 16, "total": 27}},
                    },
                }
            ],
        }

    async def search_teams(self, query: str):
        await self._simulate_latency(f"search-team:{query}")

        token = query.strip().title() or "Mock"
        return {
            "errors": [],
            "response": [
                {
                    "team": {
                        "id": 501,
                        "name": f"{token} Athletic",
                        "code": "MCK",
                        "country": "Testland",
                        "founded": 1901,
                        "logo": "https://images.example.test/teams/mock-athletic.png",
                    },
                    "venue": {
                        "city": "Mock City",
                        "name": "Mock Arena",
                    },
                }
            ],
        }

    async def search_competitions(self, query: str):
        await self._simulate_latency(f"search-competition:{query}")

        token = query.strip().title() or "Mock"
        return {
            "errors": [],
            "response": [
                {
                    "league": {
                        "id": 39,
                        "name": f"{token} League",
                        "logo": "https://images.example.test/leagues/mock-league.png",
                    },
                    "country": {
                        "code": "TL",
                        "name": "Testland",
                        "flag": "https://images.example.test/flags/tl.png",
                    },
                }
            ],
        }

    async def search_players(self, query: str):
        await self._simulate_latency(f"search-player:{query}")

        token = query.strip().title() or "Mock"
        return {
            "errors": [],
            "response": [
                {
                    "player": {
                        "id": 9001,
                        "name": f"{token} Example",
                        "firstname": token,
                        "lastname": "Example",
                        "birth": {"date": "1994-09-12"},
                        "age": max(18, date.today().year - 1994),
                        "photo": "https://images.example.test/players/mock-example.png",
                        "position": "Midfielder",
                        "height": "178 cm",
                        "weight": "72 kg",
                        "nationality": "Testland",
                    }
                }
            ],
        }

    async def get_competition(self, competition_id: int):
        await self._simulate_latency(f"competition:{competition_id}")

        return {
            "errors": [],
            "response": [
                {
                    "league": {
                        "id": competition_id,
                        "name": "Mock Competition",
                        "logo": "https://images.example.test/leagues/mock-competition.png",
                    },
                    "country": {
                        "code": "TL",
                        "name": "Testland",
                        "flag": "https://images.example.test/flags/tl.png",
                    },
                }
            ],
        }

    async def get_country(self, country_code: str):
        await self._simulate_latency(f"country:{country_code}")

        normalized = country_code.strip().upper() or "TL"
        return {
            "errors": [],
            "response": [
                {
                    "code": normalized,
                    "name": "Testland",
                    "flag": "https://images.example.test/flags/tl.png",
                }
            ],
        }
