from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from filters import IsPrivate
from keyboards.default.menu import menu_markup
from loader import dp
from utils.db_api.db_commands import register_user


@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await register_user(user_id, full_name)
    await message.answer(
        f"Здравствуй, {message.from_user.full_name}, список привязанных к тебе групп:",
        reply_markup=await menu_markup(message.from_user.id))
