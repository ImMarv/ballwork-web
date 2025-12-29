"""
Docstring for server.app.modules.stats.api
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from .deps import get_stats_service
from .service import StatsService

router = APIRouter()
async def params(
    player_id: int,
    year: str | None = None,
    service: StatsService = Depends(get_stats_service)
    ):
    return {
        "id": player_id,
        "year": year,
        "service": service,
    }

@router.get("/player/{player_id}")
async def get_player(commons: Annotated[dict, Depends(params)]):
    return await commons["service"].get_player(
        commons["id"],
        commons["year"],
    )

@router.get("/team/{team_id}")
async def get_team(team_id: int):
    return {"team_id": team_id}

@router.get("/search")
async def search_players(query: str):
    return {"team_id": query}
