import asyncpg
from aiogram import types
from utils.db_api.models import User, Group, DateTimeForLink, Link


async def get_user(user_id: int):
    try:
        user = await User.get(user_id)  # where(User.chat_id == chat_id).gino.first()
    except asyncpg.exceptions.UndefinedTableError:
        user = None
    return user


async def get_group(chat_id: int):
    try:
        group = await Group.query.where(Group.chat_id == chat_id).gino.first()
    except asyncpg.exceptions.UndefinedTableError:
        group = None
    return group


async def get_link(id: int):
    try:
        link = await Link.get(id)
    except asyncpg.exceptions.UndefinedTableError:
        link = None
    return link


async def get_user_groups(user_id: int):
    user = await get_user(user_id)
    groups = await Group.query.where(Group.admin_id==user.chat_id).gino.all()
    return groups


async def get_links_for_group(chat_id: int):
    group = await get_group(chat_id)
    links = await Link.query.where(Link.group_id==group.id).gino.all()
    return links


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
                             f"Пользователю: @{message.from_user.username}\n"
                             f"Для настройки перейдите в бота\n"
                             f"@mospolytech_get_links_bot")
        return

    group = Group(chat_id=message.chat.id,
                  admin_id=message.from_user.id,
                  name=message.chat.title)

    await group.create()
    await message.answer(f"Группа ({chat_title}) добавлена для настройки "
                         f"Пользователю: @{message.from_user.username}\n"
                         f"Для настройки перейдите в бота\n"
                         f"@mospolytech_get_links_bot")
