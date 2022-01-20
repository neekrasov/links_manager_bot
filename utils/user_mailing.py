from datetime import datetime, date, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp
from utils.db_api.db_commands import get_datetime_for_all_links
from utils.db_api.models import DateTimeForLink

scheduler = AsyncIOScheduler()


async def mailing(dp, link):
    await dp.bot.send_message(text=f"Ссылка на конференцию ({link.name}):\n"
                                   f"{link.url}",
                              chat_id=link.groups_id)


def scheduler_add_job(dp, task):
    task_datetime = datetime.combine(task.date, task.time)
    scheduler.add_job(mailing,
                      trigger="interval",
                      next_run_time=task_datetime,
                      # seconds=604800,
                      hour=100,
                      args=(dp, task.link))


async def start_mailing():
    await add_task()
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    for task in tasks:
        scheduler_add_job(dp, task)


async def add_task():
    task = DateTimeForLink(
        links_id=1,
        date=date(datetime.now().year, month=1, day=20),
        time_start=time(hour=18, minute=0),
        time_end=time(hour=20, minute=0),
        repeat=10,
    )
    await task.create()
