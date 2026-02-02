from ..models.dto.api_error import APIError
from ..models.dto.competition import Competition
from ..models.dto.country import Country
from ..models.dto.home_away import HomeAway
from ..models.dto.player import Player
from ..models.dto.team import Team


def map_error(e: dict) -> APIError | None:
    pass
def map_player_response(p: dict) -> Player | None:
    """
    Maps a player data dictionary to a Player object.

    :param p: Dictionary containing player information and statistics data.
    :return: Player object with mapped attributes, or None if statistics data is missing.
    """
    player_info = p.get("player", {})
    stats = p.get("statistics", [])

    if not stats:
        return None # TODO: Handle missing stats appropriately

    stats = stats[0]

    return Player(
        id=player_info.get("id"),
        name=player_info.get("name"),
        season=stats.get("league", {}).get("season"),
        dob=player_info.get("birth", {}).get("date"),
        photo=player_info.get("photo"),
        age=player_info.get("age"),
        nationality=player_info.get("nationality"),
        games_played=stats.get("games", {}).get("appearances"),
        position=stats.get("games", {}).get("position"),
        goals=stats.get("goals", {}).get("total"),
        assists=stats.get("goals", {}).get("assists"),
        shirt_number=stats.get("games", {}).get("number")
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
            id = league_info.get("id"),
            name = league_info.get("name"),
            season = league_info.get("season"),
            logo = league_info.get("logo")
            ),
        goals_for = HomeAway(
            home= goal_for.get("home"),
            away= goal_for.get("away"),
            total= goal_for.get("total")
        ),
        goals_against=HomeAway(
            home=goal_against.get("home"),
            away=goal_against.get("away"),
            total=goal_against.get("total")
        ),
        wins= HomeAway(
            home = wins.get("home"),
            away = wins.get("away"),
            total = wins.get("total")
            ),
        loses=HomeAway(
            home = loses.get("home"),
            away = loses.get("away"),
            total = loses.get("total")
        ),
        draws=HomeAway(
            home = draws.get("home"),
            away = draws.get("away"),
            total = draws.get("total")
        )
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
        season=None, # this needs to change later.
        name=league_info.get("name"),
        logo=league_info.get("logo"),
        country=Country(
            code=country_info.get("code"),
            name=country_info.get("name"),
            logo=country_info.get("flag")
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

    return Country(
        code=code,
        name=name,
        logo=logo
    )
