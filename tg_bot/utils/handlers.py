from aiogram.utils.markdown import hlink

from loader import dp
from utils.db_api.db_commangs import get_link


async def answer_link(link_id: int, chat_id: int):
    link = await get_link(link_id)
    await dp.bot.send_message(
        text=f"{hlink(title='Ссылка', url=link['url'])} на конференцию <b>🎓{link['title']}🎓</b>\n",
        chat_id=chat_id,
        disable_web_page_preview=True,
        )