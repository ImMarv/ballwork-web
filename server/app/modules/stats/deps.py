"""
In charge of wiring the local API with the provider
"""

# stats/deps.py
from app.core.settings import settings

from ..stats.providers.api_football import ApiFootballProvider
from ..stats.service import StatsService

# Create single instances (application scope)
_provider = ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)
_stats_service = StatsService(_provider)


def get_stats_service() -> StatsService:
    """
    Gets the header data necessary to request data from the provider

    :return: The stats service credentials
    :rtype: StatsService
    """
    return _stats_service
