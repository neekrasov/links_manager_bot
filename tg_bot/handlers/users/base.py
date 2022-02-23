from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from filters import IsPrivate
from keyboards.inline.commandstart_keyboard import start_private_buttons
from loader import dp
from utils.db_api.db_commands import register_user


@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    await register_user(user_id, full_name, username)
    await message.answer(f"Здравствуй {full_name}, я бот менеджер-ссылок.\n",
                         reply_markup=start_private_buttons)
