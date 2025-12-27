from .providers.ifootball_provider import FootballDataProvider


class StatsService:

    def __init__(self, provider: FootballDataProvider):
        self._provider = provider

    async def get_player(self, player_id: int, year: str):
        raw_player = await self._provider.get_player(
            player_id, year
            )
        players = raw_player.get("response", [])

        results = []
        for p in players:
            stats = p["statistics"][0]

            results.append(
                {
                "id": p["player"]["id"],
                "name": p["player"]["name"],
                "season_goals": stats["statistics"]["goals"]["total"],
                "season_assists": stats["statistics"]["goals"]["assists"],
                "season_games": stats["statistics"]["games"]["appearences"],
                "position": stats["statistics"]["games"]["position"],
            }
            )
        return results

    async def get_team(self, team_id: int):
        pass

    async def search_players(self, query: str):
        pass
