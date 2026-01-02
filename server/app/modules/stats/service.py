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
        """
        Get Player Stats
        
        :param self: Description
        :param player_id: Description
        :type player_id: int
        :param year: Description
        :type year: str
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
                    "id": player_info["id"],
                    "name": player_info.get("name"),
                    "season": year,
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

    async def get_team(self, team_id: int):
        pass

    async def search_players(self, query: str):
        pass
