"""
Docstring for server.app.modules.stats.api
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from .deps import get_stats_service
from .service import StatsService

router = APIRouter()


async def params(
    player_id: int | None = None,
    team_id: int | None = None,
    year: str | None = None,
    competition_id: int | None = None,
    country_code: str | None = None,
    service: StatsService = Depends(get_stats_service),  # noqa: B008
):
    """Common Parameters for the API commands

    Args:
        player_id (int): The ID of the player
        year (str | None, optional): Year of the season. Defaults to None.
        competition_id (int | None, optional): ID for the competition.
        service (_type_, optional): Service singleton. Dependant on StatsService.

    Returns:
        dict: A dictionary with the request values.
    """
    return {
        "player_id": player_id,
        "team_id": team_id,
        "year": year,
        "competition_id": competition_id,
        "country_code": country_code,
        "service": service,
    }


@router.get("/player/{player_id}")
async def get_player(commons: Annotated[dict, Depends(params)]):
    """Gets player data from API-Football

    Args:
        commons (Annotated[dict, Depends): Value storing request parameters

    Returns:
        Raw JSON data of player
    """
    return await commons["service"].get_player(
        commons["player_id"],
        commons["year"],
    )


@router.get("/team/{team_id}")
async def get_team(commons: Annotated[dict, Depends(params)]):
    """Gets team stats data from API-Football

    Args:
        commons (Annotated[dict, Depends): Value storing request parameters

    Returns:
        Raw JSON data of team
    """
    return await commons["service"].get_team(
        commons["team_id"], commons["competition_id"], commons["year"]
    )


@router.get("/search")
async def search_players(query: str):
    return {"team_id": query}


@router.get("/competition")
async def get_competition(commons: Annotated[dict, Depends(params)]):
    """Get competition data from API-Football

    Args:
        commons (Annotated[dict, Depends): Value storing request parameters.

    Returns:
        Raw JSON data of competition
    """
    return await commons["service"].get_competition(commons["competition_id"])


@router.get("/country")
async def get_country(commons: Annotated[dict, Depends(params)]):
    """Get country data from API-Football

    Args:
        commons (Annotated[dict, Depends): Value storing request parameters.

    Returns:
        Raw JSON data of country
    """
    return await commons["service"].get_country(commons["country_code"])
