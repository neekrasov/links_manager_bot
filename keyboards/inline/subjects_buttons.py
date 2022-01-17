from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

subjects = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Основы программирования", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Основы тестирования", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Формальная логика", callback_data="subject_id_"),

        ],

        [
            InlineKeyboardButton(text="Документооборот", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="ИСиТ", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Линейная алгебра", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Физкультура", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Основы ИКТ", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Английский язык", callback_data="subject_id_"),

        ],
        [
            InlineKeyboardButton(text="Коммуникации в области IT", callback_data="subject_id_"),

        ],
    ])
