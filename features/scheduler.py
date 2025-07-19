# features/scheduler.py

import asyncio
import logging
from datetime import datetime, timedelta
from pytz import timezone

from features.clearance import scan_and_send_clearance
from features.wishlist import check_and_notify_wishlist

PST = timezone("US/Pacific")

async def daily_schedule(bot):
    while True:
        now = datetime.now(PST)
        next_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
        next_1120pm = now.replace(hour=23, minute=20, second=0, microsecond=0)

        if now >= next_8am:
            next_8am += timedelta(days=1)
        if now >= next_1120pm:
            next_1120pm += timedelta(days=1)

        time_until_8am = (next_8am - now).total_seconds()
        time_until_1120pm = (next_1120pm - now).total_seconds()

        await asyncio.sleep(min(time_until_8am, time_until_1120pm))
        now = datetime.now(PST)

        if now.hour == 8:
            logging.info("⏰ Running 8:00AM Clearance + Wishlist Check")
            await scan_and_send_clearance(bot)
            await check_and_notify_wishlist(bot)
        elif now.hour == 23 and now.minute == 20:
            logging.info("🌙 Running 11:20PM Clearance Check")
            await scan_and_send_clearance(bot)
