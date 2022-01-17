from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from filters import IsPrivate
from filters.private import is_admin
from loader import dp


@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer(f"Пошёл нахуй челл")
        return
    await message.answer(f"Привет, {message.from_user.full_name}")