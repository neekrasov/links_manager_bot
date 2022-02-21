from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from data.config import TIME_ZONE
from utils.db_api.db_commands import get_datetime_for_all_links, get_link, get_datetime_for_link
from utils.handlers import answer_link

scheduler = AsyncIOScheduler(timezone=TIME_ZONE)


async def mailing(link_id, chat_id):
    datetime_for_link = await get_datetime_for_link(link_id)
    await datetime_for_link.update(date=datetime_for_link.date + timedelta(days=datetime_for_link.repeat)).apply()
    await answer_link(link_id, chat_id)


async def scheduler_add_job(task):
    link = await get_link(task.link_id)
    task_datetime = datetime.combine(task.date, task.time_start)
    if not link.one_time and task_datetime < datetime.now():
        await task.update(date=task.date + timedelta(days=task.repeat)).apply()
        task_datetime = datetime.combine(task.date, task.time_start)
    logger.debug(f"Задание {task} запустится в {task_datetime}")
    scheduler.add_job(mailing,
                      trigger="interval",
                      next_run_time=task_datetime,
                      seconds=int(task.repeat*60*60*24),
                      args=(link.id, link.group_id))


async def start_mailing():
    # await add_task()
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    logger.info(f'Set task for mailing: count: {len(tasks)}')
    for task in tasks:
        await scheduler_add_job(task)



# async def add_task():
#     task = DateTimeForLink(
#         link_id=3,
#         date=date(datetime.now().year, month=1, day=21),
#         time_start=time(hour=11, minute=21),
#         time_end=time(hour=11, minute=22),
#         repeat=10,
#     )
#     await task.create()
