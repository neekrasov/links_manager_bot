from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.db_api.db_commands import get_user_groups


async def menu_markup(user_id) -> ReplyKeyboardMarkup:
    groups = await get_user_groups(user_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        button = KeyboardButton(text=group.name)
        markup.insert(button)
    return markup
