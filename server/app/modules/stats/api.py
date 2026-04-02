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
    query: str | None = None,
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
        "query": query,
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
async def unified_search(commons: Annotated[dict, Depends(params)], query: str):
    return await commons["service"].unified_search(query)


@router.get("/search/player")
async def search_players(
    commons: Annotated[dict, Depends(params)], query: str, limit: int
):
    """Search for players

    Args:
        query (str): Search query for player name
        commons (Annotated[dict, Depends): Value storing request parameters

    Returns:
        Search results for players
    """
    return await commons["service"].search_players(query, limit)


@router.get("/search/team")
async def search_teams(
    commons: Annotated[dict, Depends(params)], query: str, limit: int
):
    """Search for teams

    Args:
        query (str): Search query for team name
        commons (Annotated[dict, Depends): Value storing request parameters

    Returns:
        Search results for teams
    """
    return await commons["service"].search_teams(query, limit)


@router.get("/search/competition")
async def search_competitions(
    commons: Annotated[dict, Depends(params)], query: str, limit: int
):
    """Search for competitions

    Args:
        query (str): Search query for competition name
        commons (Annotated[dict, Depends): Value storing request parameters

    Returns:
        Search results for competitions
    """
    return await commons["service"].search_competitions(query, limit)


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
async def get_country(commons: Annotated[dict, Depends(params)], country_code: str):
    """Get country data from API-Football

    Args:
        commons (Annotated[dict, Depends): Value storing request parameters.

    Returns:
        Raw JSON data of country
    """
    return await commons["service"].get_country(country_code)
