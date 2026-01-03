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
            raw_player = await self._provider.get_player(
                player_id, year
                )
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

            results = [] # Return results

            results.append(
                {
                    "id": player_info.get("id"),
                    "name": player_info.get("name"),
                    "season": stats.get("league", {}).get("season") 
                    if int(year) == stats.get("league", {}).get("season")
                    else int(year),
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
                    "number": stats.get("games", {}).get("number")
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
            raw_team = await self._provider.get_team(
                team_id, competition_id, year
            )
        except ExternalAPIError:
            return []
        
        teams = raw_team.get("response", {})
        
        results = []

        team_info = teams.get("team", {})
        team_competition = teams.get("league", {})
        if team_info["name"] is None and team_competition["name"] is None:
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
                "wins": teams.get("fixtures, {}").get("wins", {}).get("total", {}),
                "loses": teams.get("fixtures, {}").get("loses", {}).get("total", {}),
                "draws": teams.get("fixtures, {}").get("draws", {}).get("total", {}),
                "goals_for": teams.get("goals, {}").get("for", {}).get("total", {}),
                "goals_against": teams.get("goals, {}").get("against", {}).get("total", {})
            }
        )
        return results       


    async def search_players(self, query: str):
        pass
