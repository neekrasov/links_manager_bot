from datetime import datetime, date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from data import config
from utils.db_api.db_commands import get_link, get_datetime_for_all_links, update_for_link
from utils.func import get_datetime_from_str
from utils.handlers import answer_link

scheduler = AsyncIOScheduler(timezone=config.TIME_ZONE)


async def update_date_for_link(task: dict):
    """Сдвигает дату следующей отправки мероприятия на [repeat] дней"""
    task_id = task['id']
    task_date = task['date']
    task_repeat = task['repeat']
    new_date = task_date + timedelta(days=task_repeat)
    link_id = task['link_id']
    logger.debug(f"Для задания link_id({link_id}) дата=({task_date}) сменилась на дату=({new_date})")
    await update_for_link(task_id, date=new_date)


async def mailing(task: dict, link_id: int, chat_id: int):
    await answer_link(link_id, chat_id)
    await scheduler_update_date_for_link(task)


async def scheduler_update_date_for_link(task: dict):
    task_datetime_finish = datetime.combine(task["date"], task["time_finish"])
    scheduler.add_job(update_date_for_link,
                      trigger='date',
                      next_run_time=task_datetime_finish,
                      args=[task])


async def scheduler_add_job(task: dict):
    prearranged_link_minutes = timedelta(minutes=config.SHEDULER_PREARRANGED_LINK_MINUTES)

    # получаем время начала мероприятия
    task = get_datetime_from_str(task)
    task_datetime_start = datetime.combine(task["date"], task["time_start"]) - prearranged_link_minutes


    link = await get_link(task['link_id'])

    datetime_now = datetime.now()
    different_time = (datetime_now - task_datetime_start)

    # обновляем дату мероприятия если его время отстало от текущего времени
    tasl_late = different_time.total_seconds() > prearranged_link_minutes.total_seconds()
    if tasl_late and task["repeat"] != 0:
        # если она одноразовая удаляем ее из БД
        if link['one_time']:
            pass
        else:
            task_datetime_start += timedelta(days=task["repeat"]) * (different_time.days // task["repeat"])
            task['date'] = task_datetime_start.date()
            await scheduler_update_date_for_link(task)

    logger.debug(f"Задание link_id({task['link_id']}) запустится в {task_datetime_start}")

    add_job_kwargs = {
        'trigger': "date",
        'next_run_time': task_datetime_start,
        'args': (task, link['id'], link['group_id'])
    }
    if task["repeat"] != 0:
        add_job_kwargs['trigger'] = 'interval'
        add_job_kwargs['seconds'] = int(task["repeat"] * 60 * 60 * 24)
    scheduler.add_job(mailing,
                      **add_job_kwargs)



async def start_mailing():
    scheduler.start()
    tasks = await get_datetime_for_all_links()
    logger.info(f'Set task for mailing: count: {len(tasks)}')
    for task in tasks:
        await scheduler_add_job(task)
