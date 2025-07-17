import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time
from features.clearance import run_clearance_scan

async def scheduled_task(bot):
    await run_clearance_scan(bot)

def start_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone="America/Los_Angeles")

    # Schedule the task every day at 8:00 AM PT
    scheduler.add_job(scheduled_task, 'cron', hour=8, minute=0, args=[bot])
    scheduler.start()
