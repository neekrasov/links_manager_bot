import asyncio

import aiohttp
from loguru import logger

users_url = 'users'
groups_url = 'groups'
group_users_url = 'groups/users'
links_url = 'links'
links_for_group = 'links/group'
datetime_for_links_url = 'links/datetime'
HOST = 'web'


def create_url(url: str, host: str, any_int=""):
    return f'http://{host}:8000/api/v1/{url}/{any_int}'


async def simple_request(url: str, any_id: str = "", many: bool = False) -> dict:
    if many:
        async with aiohttp.ClientSession() as session:
            async with session.get(create_url(url=url, host=HOST)) as response:
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(create_url(url=url, host=HOST, any_int=any_id)) as response:
                return await response.json()


async def get_user(user_id: int) -> dict:
    return await simple_request(url=users_url, any_id=str(user_id))


async def get_group(group_id: int) -> dict:
    return await simple_request(url=groups_url, any_id=str(group_id))


async def get_link(link_id: int) -> dict:
    return await simple_request(url=links_url, any_id=str(link_id))


async def get_users() -> dict:
    return await simple_request(url=users_url, many=True)


async def get_groups() -> dict:
    return await simple_request(url=groups_url, many=True)


async def get_links() -> dict:
    return await simple_request(url=links_url, many=True)


async def get_datetime_for_all_links() -> dict:
    return await simple_request(url=datetime_for_links_url, many=True)


async def get_datetime_for_link(link_id: int) -> dict:
    return await simple_request(url=datetime_for_links_url, any_id=str(link_id))


async def get_user_groups(user_id: int) -> dict:
    return await simple_request(url=group_users_url, any_id=str(user_id))


async def get_links_for_group(group_id: int) -> dict:
    return await simple_request(url=links_for_group, any_id=str(group_id))


async def register_user(user_id: int, full_name: str, username: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(users_url, host=HOST), data={
            "chat_id": user_id,
            "full_name": full_name,
            "username": username,
        }) as response:
            pass


async def register_group(chat_id: int, chat_title: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(groups_url, host=HOST), data={
            "chat_id": chat_id,
            "title": chat_title,
        }) as response:
            pass


async def register_group_users(user_id: int, group_id: int, group_title: str) -> bool:
    user_groups = await get_user_groups(user_id)
    for group in user_groups:
        if group_id == group['group_id']:
            return False
    else:
        await register_group(group_id, group_title)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=create_url(group_users_url, host=HOST), data={
                "group_id": group_id,
                "user_id": user_id,
                "is_admin": True,
            }) as response:
                return True


async def register_link(group_id: int, title: str, url: str, one_time: bool) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(links_url, host=HOST), data={
            "group_id": group_id,
            "title": title,
            "url": url,
            "one_time": one_time
        }) as response:
            return True
