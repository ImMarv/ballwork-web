import asyncio
import random

from fastapi import FastAPI, Query

app = FastAPI()


def _seeded_delay_ms(seed: str, minimum: int = 60, maximum: int = 220) -> int:
    rng = random.Random(seed)
    return rng.randint(minimum, maximum)


async def _sleep_for(seed: str) -> None:
    await asyncio.sleep(_seeded_delay_ms(seed) / 1000)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/players")
async def players(
    player_id: int = Query(..., alias="id"),
    season: str = Query(...),
):
    await _sleep_for(f"players:{player_id}:{season}")
    return {
        "errors": [],
        "response": [
            {
                "player": {
                    "id": player_id,
                    "name": f"Mock Player {player_id}",
                    "firstname": "Mock",
                    "lastname": f"Player {id}",
                    "birth": {"date": "1998-02-14"},
                    "age": 27,
                    "photo": "https://images.example.test/players/mock-player.png",
                    "nationality": "Testland",
                },
                "statistics": [
                    {
                        "league": {
                            "id": 39,
                            "name": "Mock Premier League",
                            "season": int(season),
                            "logo": "https://images.example.test/leagues/mock-premier.png",
                        },
                        "games": {"appearances": 24, "position": "Attacker", "number": 9},
                        "goals": {"total": 11, "assists": 7},
                    }
                ],
            }
        ],
    }


@app.get("/teams/statistics")
async def teams_statistics(
    team: int = Query(...), league: int = Query(...), season: str = Query(...)
):
    await _sleep_for(f"team:{team}:{league}:{season}")
    return {
        "errors": [],
        "response": [
            {
                "team": {"id": team, "name": f"Mock FC {team}"},
                "league": {
                    "id": league,
                    "name": "Mock Competition",
                    "season": int(season),
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


@app.get("/players/profiles")
async def players_profiles(search: str = Query(...)):
    await _sleep_for(f"search-player:{search}")
    token = search.strip().title() or "Mock"
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
                    "age": 31,
                    "photo": "https://images.example.test/players/mock-example.png",
                    "position": "Midfielder",
                    "height": "178 cm",
                    "weight": "72 kg",
                    "nationality": "Testland",
                }
            }
        ],
    }


@app.get("/teams")
async def teams(search: str = Query(...)):
    await _sleep_for(f"search-team:{search}")
    token = search.strip().title() or "Mock"
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
                "venue": {"city": "Mock City", "name": "Mock Arena"},
            }
        ],
    }


@app.get("/leagues")
async def leagues(
    search: str | None = Query(None),
    competition_id: int | None = Query(None, alias="id"),
):
    await _sleep_for(f"league:{search}:{competition_id}")
    league_name = (search.strip().title() if search else "Mock Competition")
    league_id = competition_id or 39
    return {
        "errors": [],
        "response": [
            {
                "league": {
                    "id": league_id,
                    "name": league_name,
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


@app.get("/countries")
async def countries(code: str = Query(...)):
    await _sleep_for(f"country:{code}")
    normalized = code.strip().upper() or "TL"
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
