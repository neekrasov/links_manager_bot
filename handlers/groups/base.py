from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), CommandStart())
async def command_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}")


@dp.message_handler(IsGroup(), CommandHelp())
async def command_start(message: types.Message):
    await message.answer(f"<b> Стек комманд </b>\n"
                         f"/test")
