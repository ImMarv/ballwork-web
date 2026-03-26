"""Mappers for converting API responses to domain models."""

from datetime import date

from ..models.dto.api_error import APIError
from ..models.dto.competition import Competition
from ..models.dto.country import Country
from ..models.dto.home_away import HomeAway
from ..models.dto.player_profile import PlayerProfile
from ..models.dto.player_statistics import PlayerStatistics
from ..models.dto.team_stats import Team
from ..models.dto.team_summary import TeamSummary


def _normalize_birth_date(value: str | None) -> date | None:
    """Normalize provider date strings such as '1984-9-1' into date objects."""
    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        parts = value.split("-")
        if len(parts) != 3:
            return None

        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return None

        try:
            return date(int(year), int(month), int(day))
        except ValueError:
            return None


def map_errors(errors: list | dict) -> list[APIError]:
    """
    Normalizes API error responses into a list of APIError objects.

    Handles both list format (empty or with error strings) and dict format
    (error_key -> message) from the API response.
    """

    if not errors:
        return []

    result: list[APIError] = []

    # Handle dict format: error_key -> message
    if isinstance(errors, dict):
        for key, value in errors.items():
            result.append(APIError(message=str(value), bug=str(key)))
    # Handle list format: list of error strings
    else:
        for err in errors:
            result.append(APIError(message=str(err), bug=str(err)))

    return result


def map_player_response(p: dict) -> PlayerStatistics | None:
    """
    Maps a player data dictionary to a Player object.

    :param p: Dictionary containing player information and statistics data.
    :return: Player object with mapped attributes, or None if statistics data is missing.
    """
    player_info = p.get("player", {})
    stats = p.get("statistics", [])

    if not stats or not player_info:
        return None  # TODO: Handle missing stats appropriately

    stats = stats[0]
    dob = _normalize_birth_date(player_info.get("birth", {}).get("date"))
    if dob is None:
        return None

    return PlayerStatistics(
        id=player_info.get("id"),
        name=player_info.get("name"),
        season=stats.get("league", {}).get("season"),
        dob=dob,
        photo=player_info.get("photo"),
        age=player_info.get("age"),
        nationality=player_info.get("nationality"),
        games_played=stats.get("games", {}).get("appearances"),
        position=stats.get("games", {}).get("position"),
        goals=stats.get("goals", {}).get("total"),
        assists=stats.get("goals", {}).get("assists"),
        shirt_number=stats.get("games", {}).get("number"),
    )


def map_team_response(t: dict) -> Team | None:
    """
    Maps a team data dictionary to a Team object.

    :param t: Dictionary containing team information and statistics data.
    :return: Team object with mapped attributes, or None if required data is missing.
    """
    team_info = t.get("team", {})
    league_info = t.get("league", {})
    fixture_info = t.get("fixtures", {})
    goal_info = t.get("goals", {})

    wins = fixture_info.get("wins")
    loses = fixture_info.get("loses")
    draws = fixture_info.get("draws")

    goal_for = goal_info.get("for", {}).get("total", {})
    goal_against = goal_info.get("against", {}).get("total", {})

    if not team_info.get("id") or not league_info.get("id"):
        return None

    return Team(
        id=team_info.get("id"),
        name=team_info.get("name"),
        table_position=t.get("position"),
        competition=Competition(
            id=league_info.get("id"),
            name=league_info.get("name"),
            season=league_info.get("season"),
            logo=league_info.get("logo"),
        ),
        goals_for=HomeAway(
            home=goal_for.get("home"),
            away=goal_for.get("away"),
            total=goal_for.get("total"),
        ),
        goals_against=HomeAway(
            home=goal_against.get("home"),
            away=goal_against.get("away"),
            total=goal_against.get("total"),
        ),
        wins=HomeAway(
            home=wins.get("home"), away=wins.get("away"), total=wins.get("total")
        ),
        loses=HomeAway(
            home=loses.get("home"), away=loses.get("away"), total=loses.get("total")
        ),
        draws=HomeAway(
            home=draws.get("home"), away=draws.get("away"), total=draws.get("total")
        ),
    )


def map_team_search(t: dict) -> TeamSummary | None:
    """Maps a team summary (obtained from a simpler endpoint) to a TeamSummary

    Args:
        t (dict): Dictionary containing team information and venue data.

    Returns:
        TeamSummary | None: Team object with mapped attributes, or None if required data is missing.
    """
    team_info = t.get("team", {})
    venue_info = t.get("venue", {})

    if not team_info or not venue_info:
        return None

    return TeamSummary(
        id=team_info.get("id"),
        name=team_info.get("name"),
        code=team_info.get("code"),
        country=team_info.get("country"),
        founded=team_info.get("founded"),
        logo=team_info.get("logo"),
        venue_city=venue_info.get("city"),
        venue_name=venue_info.get("name"),
    )


def map_player_search(p: dict) -> PlayerProfile | None:
    player_info = p.get("player", {})

    if not player_info:
        return None

    return PlayerProfile(
        id=player_info.get("id"),
        name=player_info.get("name"),
        firstname=player_info.get("firstname"),
        lastname=player_info.get("lastname"),
        dob=_normalize_birth_date(player_info.get("birth", {}).get("date")),
        age=player_info.get("age"),
        photo=player_info.get("photo"),
        position=player_info.get("position"),
        height=player_info.get("height"),
        weight=player_info.get("weight"),
        nationality=player_info.get("nationality"),
    )


def map_competition_response(c: dict) -> Competition | None:
    """
    Maps a competition data dictionary to a Competition object.

    :param c: Dictionary containing competition information and country data.
    :return: Competition object with mapped attributes, or None if required data is missing.
    """
    league_info = c.get("league", {})
    country_info = c.get("country", {})

    if not league_info or not country_info:
        return None

    return Competition(
        id=league_info.get("id"),
        season=None,  # this needs to change later.
        name=league_info.get("name"),
        logo=league_info.get("logo"),
        country=Country(
            code=country_info.get("code"),
            name=country_info.get("name"),
            logo=country_info.get("flag"),
        ),
    )


def map_country_response(c: dict) -> Country | None:
    """
    Maps a country data dictionary to a Country object.

    :param c: Dictionary containing country information.
    :return: Country object with mapped attributes, or None if required data is missing.
    """
    code = c.get("code")
    name = c.get("name")
    logo = c.get("flag")

    if not code or not name:
        return None

    return Country(code=code, name=name, logo=logo)
