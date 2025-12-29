from .providers.ifootball_provider import FootballDataProvider


class StatsService:

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
        raw_player = await self._provider.get_player(
            player_id, year
            )
        players = raw_player.get("response", [])

        results = []
        for p in players:
            player_info = p.get("player", {})
            statistics = p.get("statistics", [])
            if not statistics:
                continue
            stats = statistics[0]
            results = []
            results.append(
                {
                    "id": player_info["id"],
                    "name": player_info.get("name"),
                    "season_goals": stats.get("goals", {}).get("total"),
                    "season_assists": stats.get("goals", {}).get("assists")
            }
            )
        return results

    async def get_team(self, team_id: int):
        pass

    async def search_players(self, query: str):
        pass
