import aiohttp
from loguru import logger

users_url = 'users/'
user_url = users_url + '{}'
groups_for_user_url = f'{user_url}/groups'

groups_url = 'groups/'
group_url = groups_url + '{}'
links_for_group_url = f'{group_url}/links'
links_datetime_for_group_url = f'{links_for_group_url}/datetime'

links_url = 'links/'
link_url = links_url + '{}'
links_datetime = f'{links_url}datetime'
link_datetime = f'{link_url}/datetime'

HOST = 'web'


def create_url(url: str, host: str, any_id=None):
    if any_id is None:
        any_id = list()
    return f'http://{host}:8000/api/v1/{url.format(*any_id)}'


async def simple_get_request(url: str, any_id: list = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(create_url(url=url, host=HOST, any_id=any_id)) as response:
            return await response.json()


async def simple_post_request(url: str, any_id: list = None, data: dict = None):
    if data is None:
        data = dict()
    logger.debug(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=create_url(url, any_id=any_id, host=HOST),
                                data=data) as response:
            pass


async def simple_put_request(url: str, any_id: list = None, data: dict = None):
    if data is None:
        data = dict()
    async with aiohttp.ClientSession() as session:
        async with session.put(url=create_url(url, any_id=any_id, host=HOST),
                               data=data) as response:
            pass


async def get_user(user_id: int) -> dict:
    return await simple_get_request(url=user_url, any_id=[user_id])


async def get_group(group_id: int) -> dict:
    return await simple_get_request(url=group_url, any_id=[group_id])


async def get_link(link_id: int) -> dict:
    return await simple_get_request(url=link_url, any_id=[link_id])


async def get_users() -> dict:
    return await simple_get_request(url=users_url)


async def get_groups() -> dict:
    return await simple_get_request(url=groups_url)


async def get_links() -> dict:
    return await simple_get_request(url=links_url)


async def get_datetime_for_all_links() -> dict:
    return await simple_get_request(url=links_datetime)


async def get_datetime_for_link(link_id: int) -> list:
    return await simple_get_request(url=link_datetime, any_id=[link_id])


async def get_datetime_for_link_for_group(group_id: int) -> dict:
    pass


async def get_groups_for_user(user_id: int) -> dict:
    return await simple_get_request(url=groups_for_user_url, any_id=[user_id])


async def get_links_for_group(group_id: int) -> dict:
    return await simple_get_request(url=links_for_group_url, any_id=[group_id])


async def register_user(user_id: int, full_name: str, username: str) -> None:
    await simple_post_request(url=users_url, data={
        "chat_id": user_id,
        "full_name": full_name,
        "username": username,
    })


async def register_group(chat_id: int, chat_title: str) -> None:
    await simple_post_request(url=groups_url, data={
        "chat_id": chat_id,
        "title": chat_title,
    })


async def register_group_users(user_id: int, group_id: int, group_title: str) -> bool:
    user_groups = await get_groups_for_user(user_id)
    for group in user_groups:
        if group_id == group['group_id']:
            return False
    else:
        await register_group(group_id, group_title)
        await simple_post_request(url=groups_for_user_url, any_id=[user_id], data={
            "group_id": group_id,
            "user_id": user_id,
            "is_admin": True,
        })


async def update_for_link(link_id: int, **kwargs):
    await simple_put_request(url=link_datetime, any_id=[link_id], data=kwargs)
