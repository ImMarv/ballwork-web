from fastapi import FastAPI

from app.core.settings import settings
from app.modules.stats.api import router as stats_router
from app.modules.stats.providers.api_football import ApiFootballProvider
from app.modules.stats.service import StatsService

app = FastAPI()

provider = ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)
service = StatsService(provider=provider)

app.include_router(stats_router)
