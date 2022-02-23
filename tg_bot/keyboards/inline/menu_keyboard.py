from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commangs import get_user_groups, get_group, get_links_for_group

links_cd = CallbackData("links", "id")
""""""
menu_cd = CallbackData("menu", "level", "any_id")


def make_cd(level, any_id="0"):
    return menu_cd.new(
        level=level,
        any_id=any_id,
    )


async def get_my_groups(user_id) -> InlineKeyboardMarkup:
    """ Список привязанных к юзеру групп """
    CURRENT_LEVEL = 0
    user_groups = await get_user_groups(user_id)
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    for user_group in user_groups:
        group = await get_group(user_group['group_id'])
        button = InlineKeyboardButton(text=str(group['title']), callback_data=make_cd(level=CURRENT_LEVEL + 10,
                                                                                      any_id=group[
                                                                                          'chat_id']))
        markup.insert(button)

    return markup


async def get_group_menu_buttons(group_id):
    """ Главное меню со всеми настройками """
    CURRENT_LEVEL = 10
    markup = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text="Получить все ссылки",
                                 callback_data=make_cd(level=CURRENT_LEVEL + 1, any_id=group_id)),
            InlineKeyboardButton(text="Добавить ссылку",
                                 callback_data=make_cd(level=CURRENT_LEVEL + 10, any_id=group_id)),
        ],
        [
            InlineKeyboardButton(text="Получить ближайшую по дате ссылку", callback_data="get_link_by_date")
        ],
        [
            InlineKeyboardButton(text="Настройки приватности", callback_data="privacy_settings"),
        ],
        [
            InlineKeyboardButton(text="Вернуться к выбору групп",
                                 callback_data=make_cd(level=CURRENT_LEVEL - 10, any_id=group_id))
        ],
    ])

    return markup


async def subjects_buttons(group_id) -> InlineKeyboardMarkup:
    """ Вывод списка предметов, привязанных к определённой группе"""
    CURRENT_LEVEL = 11
    links_for_group = await get_links_for_group(group_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links_for_group:
        button = InlineKeyboardButton(text=link['title'],
                                      callback_data=make_cd(level=CURRENT_LEVEL + 1,
                                                            any_id=link['id']))
        markup.insert(button)

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_cd(level=CURRENT_LEVEL - 1, any_id=group_id))
    )
    return markup
