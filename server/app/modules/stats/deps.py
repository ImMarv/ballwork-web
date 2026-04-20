"""
In charge of wiring the local API with the provider
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from ...db import get_db
from .providers.factory import create_stats_provider
from .repository.implementations import SQLStatsCacheRepository
from .service import StatsService

# Create single instances (application scope)
_provider = create_stats_provider()


def get_stats_service(db: Session = Depends(get_db)) -> StatsService:  # noqa: B008
    """
    Gets the header data necessary to request data from the provider

    :return: The stats service credentials
    :rtype: StatsService
    """
    return StatsService(
        provider=_provider,
        cache_repo=SQLStatsCacheRepository(db),
    )