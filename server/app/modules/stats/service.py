"""
Service layer of the application.
"""

from .providers.api_football import ExternalAPIError
from .providers.ifootball_provider import FootballDataProvider


class StatsService:
    """
    Service layer class for establishing business logic
    """

    def __init__(self, provider: FootballDataProvider):
        self._provider = provider

    async def get_player(self, player_id: int, year: str):
        """Get Player Stats

        Args:
            player_id (int): ID for the player
            year (str): Season

        Returns:
            json: Mapped response
        """
        try:
            raw_player = await self._provider.get_player(player_id, year)
        except ExternalAPIError:
            return []

        players = raw_player.get("response", [])

        results = []
        for p in players:
            player_info = p.get("player", {})
            statistics = p.get("statistics", [])
            if not statistics:
                continue
            stats = statistics[0]

            results = []  # Return results

            results.append(
                {
                    "id": player_info.get("id"),
                    "name": player_info.get("name"),
                    "season": stats.get("league", {}).get("season"),
                    "dob": player_info.get("birth", {}).get("date"),
                    "photo": player_info.get("photo"),
                    "age": player_info.get("age"),
                    "nationality": player_info.get("nationality"),
                    "team_id": stats.get("team", {}).get("id"),
                    "team_name": stats.get("team", {}).get("name"),
                    "season_goals": stats.get("goals", {}).get("total"),
                    "season_assists": stats.get("goals", {}).get("assists"),
                    "games_played": stats.get("games", {}).get("appearences"),
                    "position": stats.get("games", {}).get("position"),
                    "number": stats.get("games", {}).get("number"),
                }
            )
        return results

    async def get_team(self, team_id: int, competition_id: int, year: str):
        """Get Team Stats

        Args:
            team_id (int): ID for the team
            competition_id (int): ID for the competition
            year (str): Season
        Returns:
            json: Mapped response
        """
        # using pythonic models might be more ideal here, however we'll do this for the time being.
        try:
            raw_team = await self._provider.get_team(team_id, competition_id, year)
        except ExternalAPIError:
            return []

        teams = raw_team.get("response", {})

        results = []

        if isinstance(teams, list):
            teams = teams[0] if teams else {}

        team_info = teams.get("team", {})
        team_competition = teams.get("league", {})
        if team_info.get("name") is None and team_competition.get("name") is None:
            return []

        results.append(
            {
                "id": team_info.get("id"),
                "team_name": team_info.get("name"),
                "team_logo": team_info.get("logo"),
                "competition_id": team_competition.get("id"),
                "competition_name": team_competition.get("name"),
                "competition_logo": team_competition.get("logo"),
                "competition_region": team_competition.get("country"),
                "year": team_competition.get("season"),
                "form": teams.get("form"),
                "played": teams.get("fixtures", {}).get("played", {}).get("total", {}),
                "wins": teams.get("fixtures", {}).get("wins", {}),
                "loses": teams.get("fixtures", {}).get("loses", {}),
                "draws": teams.get("fixtures", {}).get("draws", {}),
                "goals_for": teams.get("goals", {}).get("for", {}).get("total", {}),
                "goals_against": teams.get("goals", {})
                .get("against", {})
                .get("total", {}),
            }
        )
        return results

    async def search_players(self, query: str):
        pass

    async def get_competition(self, competition_id: int):
        try:
            raw_competition = await self._provider.get_competition(competition_id)
        except ExternalAPIError:
            return []

        competitions = raw_competition.get("response", [])
        results = []

        for c in competitions:
            league_info = c.get("league", {})
            country_info = c.get("country", {})
            if not league_info or not country_info:
                continue
            results.append(
                {
                    "competition_id": league_info.get("id"),
                    "competition_name": league_info.get("name"),
                    "competition_logo": league_info.get("logo"),
                    "competition_country_code": country_info.get("code"),
                    "competition_country_name": country_info.get("name"),
                    "competition_country_logo": country_info.get("flag"),
                }
            )
        return results

    async def get_country(self, country_code: str):
        try:
            raw_country = await self._provider.get_country(country_code.capitalize())
        except ExternalAPIError:
            return []

        country = raw_country.get("response", [])
        results = []

        if isinstance(country, list):
            country = country[0] if country else {}
        results.append(
            {
                "country_code": country.get("code"),
                "country_name": country.get("name"),
                "country_logo": country.get("flag"),
            }
        )
        return results
