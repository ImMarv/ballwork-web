from contextlib import asynccontextmanager

import uvicorn
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .core.settings import settings
from .db import SessionFactory, engine
from .modules.digest.repository.implementations import (
    SQLEventRepository,
    SQLSubscriptionRepository,
)
from .modules.stats.api import router as stats_router
from .modules.stats.providers.api_football import ApiFootballProvider
from .modules.stats.service import StatsService
from .scheduler.jobs import ingest_due_subscriptions_job
from .scheduler.scheduler import Scheduler

provider = ApiFootballProvider(api_key=settings.API_FOOTBALL_KEY)
service = StatsService(provider=provider)
scheduler = Scheduler()


async def run_ingest_job():
    db = SessionFactory()
    try:
        event_repo = SQLEventRepository(session=db)
        subscription_repo = SQLSubscriptionRepository(session=db)
        await ingest_due_subscriptions_job(
            stats_service=service,
            event_repo=event_repo,
            subscription_repo=subscription_repo,
        )
    finally:
        db.close()


def get_stats_service() -> StatsService:
    return service


@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    scheduler.add_job(
        run_ingest_job, CronTrigger(minute="*/5")
    )  # every 5 minutes for testing
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()
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
