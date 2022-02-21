import asyncpg
from aiogram import types
from utils.db_api.models import User, Group, DateTimeForLink, Link, GroupUsers


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


async def get_link(link_id: int):
    try:
        link = await Link.get(link_id)
    except asyncpg.exceptions.UndefinedTableError:
        link = None
    return link


async def get_user_groups(user_id: int):
    user = await get_user(user_id)
    groups = await Group.join(GroupUsers).select().where(GroupUsers.user_id == user.chat_id).gino.all()
    return groups


async def get_links_for_group(chat_id: int):
    group = await get_group(chat_id)
    if not group:
        return []
    links = await Link.query.where(Link.group_id == group.chat_id).gino.all()
    return links


async def get_datetime_for_all_links():
    tasks = await DateTimeForLink.query.gino.all()
    return tasks


async def get_datetime_for_link(link_id):
    datetime_for_link = await DateTimeForLink.query.where(link_id == DateTimeForLink.link_id).gino.first()
    return datetime_for_link


async def register_user(user_id, full_name):
    user = await get_user(user_id)
    if user:
        return
    user = User(chat_id=user_id,
                full_name=full_name)
    await user.create()


async def register_groups(message: types.Message):
    group = await get_group(message.chat.id)
    if not group:
        group = Group(chat_id=message.chat.id,
                      name=message.chat.title)
        await group.create()
    chat_title = message.chat.title
    user_groups = await get_user_groups(message.from_user.id)
    user_groups_id = [group.group_id for group in user_groups]
    if group.chat_id in user_groups_id:
        await message.answer(f"Группа ({chat_title}) ранее была добавлена для настройки\n"
                             f"Пользователю: @{message.from_user.username}\n"
                             f"Для настройки перейдите в бота\n"
                             f"@mospolytech_get_links_bot")
        return
    group_user = GroupUsers(group_id=message.chat.id,
                            user_id=message.from_user.id,
                            is_admin=True)
    await group_user.create()

    await message.answer(f"Группа ({chat_title}) добавлена для настройки "
                         f"Пользователю: @{message.from_user.username}\n"
                         f"Для настройки перейдите в бота\n"
                         f"@mospolytech_get_links_bot")
