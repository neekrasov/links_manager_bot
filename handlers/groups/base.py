from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command

from filters import IsGroup, IsGroupAdmin
from loader import dp
from utils.db_api.db_commands import register_user, register_groups


@dp.message_handler(IsGroup(), IsGroupAdmin(), CommandStart())
async def command_start(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"Привет, {full_name}")


@dp.message_handler(IsGroup(), CommandHelp())
async def command_help(message: types.Message):
    await message.answer(f"<b> Стек комманд </b>\n"
                         f"/test")


@dp.message_handler(IsGroup(), IsGroupAdmin(), Command("get_group"))
async def get_group_for_user(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await register_user(user_id, full_name)
    await register_groups(message)
