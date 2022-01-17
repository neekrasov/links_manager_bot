from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api import session
from utils.db_api.models import Groups


def subjects(chat_id) -> InlineKeyboardMarkup:
    links = session.query(Groups).get(chat_id).links
    keyboard = InlineKeyboardMarkup(row_width=1)
    for link in links:
        button = InlineKeyboardButton(text=link.name, callback_data=link.id)
        keyboard.add(button)
    return keyboard
