from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp
from utils.db_api import session
from utils.db_api.models import DateTimeForLinks

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


def start_mailing():
    scheduler.start()
    tasks = session.query(DateTimeForLinks).all()
    for task in tasks:
        scheduler_add_job(dp, task)
