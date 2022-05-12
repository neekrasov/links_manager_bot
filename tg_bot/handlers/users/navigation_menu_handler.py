from aiogram import types

from filters import IsPrivate
from keyboards.inline.callback_datas import menu_cd

from loader import dp


@dp.callback_query_handler(IsPrivate(), menu_cd.filter())
async def navigation_to_lessons(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    any_id = callback_data.get("any_id")
    from handlers.users.menu_handler import my_groups, show_admin_menu
    from handlers.users.get_all_links_button_handler import show_subjects, show_link
    levels = {
        '0': my_groups,
        '10': show_admin_menu,
        '11': show_subjects,
        '12': show_link,
    }

    current_level_function = levels[current_level]
    await current_level_function(call, any_id=any_id)
