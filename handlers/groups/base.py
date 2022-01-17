from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from filters import IsGroup, IsGroupAdmin
from loader import dp, bot
from utils.db_api import session
from utils.db_api.models import Users, Groups


def register_user(user_id, full_name):
    user = Users(chat_id=user_id,
                 full_name=full_name)
    session.add(user)
    session.commit()


def register_groups(message: types.Message):
    groups = Groups(chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    name=message.chat.title)
    session.add(groups)
    session.commit()


@dp.message_handler(IsGroup(), IsGroupAdmin(), CommandStart())
async def command_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user = session.query(Users).get(user_id)
    if not user:
        register_user(user_id, full_name)
        register_groups(message)
    await message.answer(f"Привет, {full_name}")


@dp.message_handler(IsGroup(), CommandHelp())
async def command_start(message: types.Message):
    await message.answer(f"<b> Стек комманд </b>\n"
                         f"/test")
