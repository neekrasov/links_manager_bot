from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_user_groups, get_links_for_group

# admin_menu = CallbackData("show_menu", "group_id")
links_all = CallbackData("links", "id")
# callback_datas = CallbackData("get", "group_id")
""""""
admin_menu_cd = CallbackData("menu", "level", "main_menu", "list_of_activities", "any_id")


def make_cd(level, main_menu="0", list_of_activities="0", any_id="0"):
    return admin_menu_cd.new(
        level=level,
        main_menu=main_menu,
        list_of_activities=list_of_activities,
        any_id=any_id,
    )


async def get_my_groups(user_id) -> InlineKeyboardMarkup:
    """ Список привязанных к юзеру групп """
    CURRENT_LEVEL = 0
    groups = await get_user_groups(user_id)
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        button = InlineKeyboardButton(text=str(group.name), callback_data=make_cd(level=CURRENT_LEVEL + 1,
                                                                                  any_id=group.chat_id))  # admin_menu.new(group_id=group.chat_id)
        markup.insert(button)

    return markup


async def get_group_menu_buttons(group_id):
    """ Главное меню со всеми настройками """
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text="Получить все ссылки",
                                 callback_data=make_cd(level=CURRENT_LEVEL + 1, any_id=group_id)),
            # callback_datas.new(group_id=group_id)
            InlineKeyboardButton(text="Добавить ссылку", callback_data="add_link"),
        ],
        [
            InlineKeyboardButton(text="Получить ближайшую по дате ссылку", callback_data="get_link_by_date")
        ],
        [
            InlineKeyboardButton(text="Настройки приватности", callback_data="privacy_settings"),
        ],
        [
            InlineKeyboardButton(text="Вернуться к выбору групп",
                                 callback_data=make_cd(level=CURRENT_LEVEL - 1, any_id=group_id))
        ],
    ])

    return markup


async def subjects_buttons(group_id) -> InlineKeyboardMarkup:
    """ Вывод списка предметов, привязанных к определённой группе"""
    CURRENT_LEVEL = 2
    links = await get_links_for_group(group_id)
    print(f" subjects_buttons -> links = get_links_for_group -> {links}")
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links:
        print(f" subjects_buttons -> for link in links -> link -> {link}")
        button = InlineKeyboardButton(text=link.name,
                                      callback_data=make_cd(level=CURRENT_LEVEL + 1,
                                                            any_id=link.id))  # links_all.new(id=link.id)
        markup.insert(button)

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_cd(level=CURRENT_LEVEL - 1, any_id=group_id))
    )
    return markup
