from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp
from utils.db_api.db_commands import get_datetime_for_all_links

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
                      seconds=604800,
                      args=(dp, task.link))


async def start_mailing():
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    for task in tasks:
        scheduler_add_job(dp, task)
