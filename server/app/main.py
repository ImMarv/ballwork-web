import logging
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from .core.settings import settings
from .db import SessionFactory, engine
from .modules.digest.api import router as digest_router
from .modules.digest.repository.implementations import (
    SQLEventRepository,
    SQLSubscriptionRepository,
)
from .modules.stats.api import router as stats_router
from .modules.stats.providers.api_football import ApiFootballProvider
from .modules.stats.service import StatsService
from .scheduler.jobs import ingest_due_subscriptions_job
from .scheduler.scheduler import Scheduler

LOGGER = logging.getLogger(__name__)

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


def _digest_tables_exist() -> bool:
    """Return True when required digest tables exist in the active database."""
    inspector = inspect(engine)
    required_tables = [
        "subscription_digest",
        "notification_event_digest",
    ]
    return all(inspector.has_table(table) for table in required_tables)


def get_stats_service() -> StatsService:
    return service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    if _digest_tables_exist():
        scheduler.add_job(
            run_ingest_job,
            CronTrigger(minute="*/5"),
            id="digest-ingestion-job",
            replace_existing=True,
        )
        scheduler.start()
    else:
        LOGGER.warning(
            "Digest scheduler disabled: required tables are missing. Run migrations first."
        )

    try:
        yield
    finally:
        if scheduler.scheduler.running:
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


@app.get("/health")
async def health_check():
    """Health check endpoint for readiness probes (k6, load balancers, etc.)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except SQLAlchemyError:
        LOGGER.exception("Health check failed")
        return JSONResponse(status_code=503, content={"status": "error"})


app.include_router(stats_router, prefix="/stats")
app.include_router(digest_router, prefix="/digest")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
