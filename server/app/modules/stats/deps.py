"""
In charge of wiring the local API with the provider
"""

# stats/deps.py
from app.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.settings import settings
from ..stats.providers.api_football import ApiFootballProvider
from ..stats.service import StatsService

# Create single instances (application scope)
_provider = ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)
_session = get_db()


def get_stats_service(db: Session = Depends(get_db)) -> StatsService: #noqa: B008
    """
    Gets the header data necessary to request data from the provider

    :return: The stats service credentials
    :rtype: StatsService
    """
    return StatsService(_provider)