from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime


class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        self.scheduler.start()

    def add_job(self, func, trigger, **job_kwargs):
        self.scheduler.add_job(func, trigger, **job_kwargs)

    def shutdown(self):
        self.scheduler.shutdown()
