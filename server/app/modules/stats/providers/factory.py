"""Provider factory for stats module."""

from ....core.settings import settings
from .api_football import ApiFootballProvider
from .ifootball_provider import FootballDataProvider
from .mock_api_service import MockAPIServiceProvider
from .mock_football import MockFootballProvider


def create_stats_provider() -> FootballDataProvider:
    provider_name = settings.STATS_PROVIDER.strip().lower()

    if provider_name == "mock":
        return MockFootballProvider(
            min_latency_ms=settings.MOCK_STATS_LATENCY_MIN_MS,
            max_latency_ms=settings.MOCK_STATS_LATENCY_MAX_MS,
        )

    if provider_name == "mock_remote":
        return MockAPIServiceProvider(base_url=settings.MOCK_API_BASE_URL)

    if provider_name == "api_football":
        if not settings.API_FOOTBALL_KEY.strip():
            raise ValueError(
                "API_FOOTBALL_KEY must be set when STATS_PROVIDER=api_football"
            )
        return ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)

    raise ValueError(
        "Invalid STATS_PROVIDER value. Use 'api_football', 'mock', or 'mock_remote'."
    )
