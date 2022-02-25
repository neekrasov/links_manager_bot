from datetime import datetime, date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from data import config
from utils.db_api.db_commands import get_link, get_datetime_for_all_links, update_for_link
from utils.func import get_datetime_from_str
from utils.handlers import answer_link

scheduler = AsyncIOScheduler(timezone=config.TIME_ZONE)


async def update_date_for_link(link_id: int, date: date, repeat: int):
    """Сдвигает дату следующей отправки мероприятия на [repeat] дней"""
    new_date = date + timedelta(days=repeat)
    logger.debug(f"Для задания link_id({link_id}) date=({date}) сменился на date=({new_date})")
    await update_for_link(link_id, date=new_date)


async def mailing(link_id: int, chat_id: int, date: date, repeat: int):
    await update_date_for_link(link_id, date, repeat)
    await answer_link(link_id, chat_id)


async def scheduler_add_job(task):
    # получаем время начала мероприятия
    link = await get_link(task['link_id'])
    task = get_datetime_from_str(task)
    task_datetime = datetime.combine(task["date"], task["time_start"])

    # обновляем дату мероприятия, если оно не одноразовое и его дата отстала от текущей даты
    if not link['one_time'] and task_datetime < datetime.now():
        await update_date_for_link(link['id'], task['date'], task["repeat"])
        task_datetime += timedelta(days=task["repeat"])

    logger.debug(f"Задание link_id({task['link_id']}) запустится в {task_datetime}")
    add_job_kwargs = {
        'trigger': "date",
        'next_run_time': task_datetime,
        'args': (link['id'], link['group_id'], task['date'], task["repeat"])
    }
    if task["repeat"] != 0:
        add_job_kwargs['seconds'] = int(task["repeat"] * 60 * 60 * 24)
        add_job_kwargs['trigger'] = 'interval'
    scheduler.add_job(mailing,
                      **add_job_kwargs)


async def start_mailing():
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    logger.info(f'Set task for mailing: count: {len(tasks)}')
    for task in tasks:
        await scheduler_add_job(task)
