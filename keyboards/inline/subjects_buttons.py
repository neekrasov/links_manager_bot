from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import get_links_for_group


async def subjects(chat_id) -> InlineKeyboardMarkup:
    links = await get_links_for_group(chat_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links:
        button = InlineKeyboardButton(text=link.name, callback_data=link.id)
        markup.insert(button)
    return markup
