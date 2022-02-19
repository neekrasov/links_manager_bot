from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import dp
from utils.db_api.db_commands import get_datetime_for_all_links, get_link, get_datetime_for_link
from utils.db_api.models import DateTimeForLink

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


async def mailing(dp, link):
    datetime_for_link = await get_datetime_for_link(link.id)
    await datetime_for_link.update(date=datetime_for_link.date + timedelta(days=datetime_for_link.repeat)).apply()
    await dp.bot.send_message(text=f"Ссылка на конференцию ({link.name}):\n"
                                   f"{link.url}",
                              chat_id=link.group_id)


async def scheduler_add_job(dp, task):
    link = await get_link(task.link_id)
    task_datetime = datetime.combine(task.date, task.time_start)
    scheduler.add_job(mailing,
                      trigger="interval",
                      next_run_time=task_datetime,
                      seconds=task.repeat*60*60*24,
                      args=(dp, link))


async def start_mailing():
    # await add_task()
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    for task in tasks:
        await scheduler_add_job(dp, task)


# async def add_task():
#     task = DateTimeForLink(
#         link_id=3,
#         date=date(datetime.now().year, month=1, day=21),
#         time_start=time(hour=11, minute=21),
#         time_end=time(hour=11, minute=22),
#         repeat=10,
#     )
#     await task.create()
