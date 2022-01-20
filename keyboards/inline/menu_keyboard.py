from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_user_groups, get_links_for_group

admin_menu = CallbackData("show_menu", "group_id")
links_all = CallbackData("links", "id")
callback_datas = CallbackData("get", "group_id")
# back = CallbackData("back", "command_start", "show_menu", "id")

#
# def make_callback_data(command_start="0", show_menu="0", id="0"):
#     return back.new(
#         command_start=command_start,
#         show_menu=show_menu,
#         id=id,
#     )


async def get_my_groups(user_id) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    groups = await get_user_groups(user_id)
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        button = InlineKeyboardButton(text=str(group.name), callback_data=admin_menu.new(group_id=group.chat_id))
        markup.insert(button)

    return markup


async def get_group_menu_buttons(group_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text="Получить все ссылки", callback_data=callback_datas.new(group_id=group_id)),
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
                                 callback_data="/")
        ],
    ])

    return markup


async def subjects_buttons(chat_id) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2
    links = await get_links_for_group(chat_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links:
        button = InlineKeyboardButton(text=link.name,
                                      callback_data=links_all.new(id=link.id))
        markup.insert(button)

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data="/")
    )
    return markup
