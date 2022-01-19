from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
def show_menu(message: types.Message):
    await message.answer(f"Здравствуй, {message.from_user.full_name}, список привязанных к тебе групп:",
                         reply_markup = admin_menu_keyboard)