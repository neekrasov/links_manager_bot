from datetime import datetime

from aiogram.utils.markdown import hlink
from loguru import logger

from loader import dp
from utils.db_api.db_commands import get_link, get_links_for_group, get_datetime_for_link
from utils.func import get_datetime_from_str


async def answer_link(link_id: int, chat_id: int):
    link = await get_link(link_id)
    await dp.bot.send_message(
        text=f"{hlink(title='Ссылка', url=link['url'])} на конференцию <b>🎓{link['title']}🎓</b>\n",
        chat_id=chat_id,
        disable_web_page_preview=True,
    )


async def answer_links_for_current_datetime_for_group(chat_id: int):
    """Отправляет мероприятия, которые идут на текущее время для определенной группы"""

    datetime_now = datetime.now()
    links_for_group = await get_links_for_group(chat_id)
    links_id = []
    for link in links_for_group:
        link_id = link['id']
        # 1 ссылка может отправляться в разное время, получаем все времена для ссылки
        datetimes_for_link = await get_datetime_for_link(link_id)
        for datetime_for_link in datetimes_for_link:
            datetime_for_link = get_datetime_from_str(datetime_for_link)
            time_start_for_link = datetime.combine(datetime_for_link["date"],
                                                   datetime_for_link["time_start"])
            time_finish_for_link = datetime.combine(datetime_for_link["date"],
                                                    datetime_for_link["time_finish"])
            # если текущее время находятся в интервале начала и конца мероприятия, добавляем в общий
            # список ссылок
            if time_start_for_link <= datetime_now <= time_finish_for_link:
                links_id.append(link_id)
    logger.debug(links_id)
    if not links_id:
        await dp.bot.send_message(
            text='На текущее время мероприятий нет',
            chat_id=chat_id
        )
        return
    for link in links_id:
        await answer_link(link, chat_id)
