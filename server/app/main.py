from contextlib import asynccontextmanager

from sqlalchemy import text
import uvicorn
from app.core.settings import settings
from app.db import engine
from app.modules.stats.api import router as stats_router
from app.modules.stats.providers.api_football import ApiFootballProvider
from app.modules.stats.service import StatsService
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

provider = ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)
service = StatsService(provider=provider)


def get_stats_service() -> StatsService:
    return service


@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats_router, prefix="/stats")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
