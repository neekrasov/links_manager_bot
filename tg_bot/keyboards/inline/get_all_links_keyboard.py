from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.menu_keyboard import links_all
from utils.db_api.db_commands import get_links_for_group


async def subjects_buttons_for_group(chat_id) -> InlineKeyboardMarkup:
    links = await get_links_for_group(chat_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links:
        button = InlineKeyboardButton(text=link.name,
                                      callback_data=links_all.new(id=link.id))
        markup.insert(button)
    return markup
