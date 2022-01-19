import asyncpg
from aiogram import types
from utils.db_api.models import User, Group, DateTimeForLink


async def get_user(chat_id: int):
    try:
        user = await User.get(chat_id)  # where(User.chat_id == chat_id).gino.first()
    except asyncpg.exceptions.UndefinedTableError:
        user = None
    return user


async def get_group(chat_id: int):
    try:
        group = await Group.get(chat_id)  # where(User.chat_id == chat_id).gino.first()
    except asyncpg.exceptions.UndefinedTableError:
        group = None
    return group


async def get_links_for_group(chat_id: int):
    group = await get_group(chat_id)
    return group.links


async def get_datetime_for_all_links():
    tasks = await DateTimeForLink.query.gino.all()
    return tasks


async def register_user(chat_id, full_name):
    user = await get_user(chat_id)
    if user:
        return False
    user = User(chat_id=chat_id,
                full_name=full_name)
    await user.create()
    return True


async def register_groups(message: types.Message):
    group = await get_group(message.chat.id)
    chat_title = message.chat.title
    if group:
        await message.answer(f"Группа ({chat_title}) уже была добавлена для настройки\n"
                             f"Для настройки перейдите в бота\n"
                             f"@mospolytech_get_links_bot")
        return

    group = Group(chat_id=message.chat.id,
                  admin_id=message.from_user.id,
                  name=message.chat.title)
    print(group)

    await group.create()
    await message.answer(f"Группа ({chat_title}) добавлена для настройки\n"
                         f"Для настройки перейдите в бота\n"
                         f"@mospolytech_get_links_bot")
