from aiogram.types import CallbackQuery

from loader import dp
from utils.handlers import answer_links_for_current_datetime_for_group


@dp.callback_query_handler(text='get_link_by_date')
async def get_link_by_date(call: CallbackQuery):
    await call.answer()
    await answer_links_for_current_datetime_for_group(call.message.chat.id)
