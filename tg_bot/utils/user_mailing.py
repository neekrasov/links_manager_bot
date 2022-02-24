from datetime import datetime, date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from utils.db_api.db_commands import get_link, get_datetime_for_all_links
from utils.handlers import answer_link

scheduler = AsyncIOScheduler()


async def update_date_for_link(date: date, repeat: int):
    """Сдвигает дату следующей отправки мероприятия на [repeat] дней"""
    # datetime_for_link.update(date=date + timedelta(days=repeat))
    pass


async def mailing(link_id: int, chat_id: int, date: date, repeat: int):
    await update_date_for_link(date, repeat)
    await answer_link(link_id, chat_id)


async def scheduler_add_job(task):
    # получаем время начала мероприятия
    link = await get_link(task['link_id'])
    task_datetime = datetime.combine(task["date"], task["time_start"])

    # обновляем дату мероприятия, если оно не одноразовое и его дата отстала от текущей даты
    if not link['one_time'] and task_datetime < datetime.now():
        await update_date_for_link(task["date"], task["repeat"])
        task_datetime += timedelta(days=task["repeat"])

    logger.debug(f"Задание {task} запустится в {task_datetime}")

    scheduler.add_job(mailing,
                      trigger="interval",
                      next_run_time=task_datetime,
                      seconds=int(task.repeat * 60 * 60 * 24),
                      args=(link['id'], link['group_id']))


async def start_mailing():
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    logger.info(f'Set task for mailing: count: {len(tasks)}')
    for task in tasks:
        await scheduler_add_job(task)
