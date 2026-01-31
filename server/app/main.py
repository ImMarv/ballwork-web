from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import settings
from app.db import create_db_and_tables, engine
from app.modules.stats.api import router as stats_router
from app.modules.stats.providers.api_football import ApiFootballProvider
from app.modules.stats.service import StatsService

provider = ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)
service = StatsService(provider=provider)


def get_stats_service() -> StatsService:
    return stats_service

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(stats_router, prefix="/stats")
