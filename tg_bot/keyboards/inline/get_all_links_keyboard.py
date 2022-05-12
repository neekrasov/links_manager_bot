from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import links_cd
from utils.db_api.db_commands import get_links_for_group


async def subjects_buttons_for_group(chat_id) -> InlineKeyboardMarkup:
    links_for_group = await get_links_for_group(chat_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link_for_group in links_for_group:
        button = InlineKeyboardButton(text=link_for_group['title'],
                                      callback_data=links_cd.new(id=link_for_group['id']))
        markup.insert(button)
    return markup
