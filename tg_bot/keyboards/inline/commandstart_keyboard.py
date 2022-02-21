from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_group_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Получить справку", callback_data="help")
    ]
])

start_private_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мои группы", callback_data="groups_for_user")
    ]
])
