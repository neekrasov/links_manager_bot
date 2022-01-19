from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import link_callback_data
from utils.db_api.db_commands import get_links_for_group


async def subjects(chat_id) -> InlineKeyboardMarkup:
    links = await get_links_for_group(chat_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links:
        button = InlineKeyboardButton(text=link.name,
                                      callback_data=link_callback_data.new(id=link.group_id))
        markup.insert(button)
    return markup
