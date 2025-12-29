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
    service: StatsService = Depends(get_stats_service)  # noqa: B008
    ):
    """Common Parameters for the API commands

    Args:
        player_id (int): The ID of the player
        year (str | None, optional): Year of the season. Defaults to None.
        service (_type_, optional): Service singleton. Dependant on StatsService.

    Returns:
        dict: A dictionary with the request values.
    """
    return {
        "id": player_id,
        "year": year,
        "service": service,
    }

@router.get("/player/{player_id}")
async def get_player(commons: Annotated[dict, Depends(params)]):
    """Gets player data from API-Football

    Args:
        commons (Annotated[dict, Depends): Value storing parameters used in the request

    Returns:
        Player data as specified by the id and year.
    """
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
