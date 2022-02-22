from aiogram import types

from filters import IsPrivate
from keyboards.inline.menu_keyboard import menu_cd, get_my_groups
from loader import dp


@dp.callback_query_handler(IsPrivate(), menu_cd.filter())
async def navigation_to_lessons(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    any_id = callback_data.get("any_id")
    from handlers.users.get_all_links_button_handler import show_admin_menu, show_subjects, show_link
    levels = {
        '0': my_groups,
        '10': show_admin_menu,
        '11': show_subjects,
        '12': show_link,
    }

    current_level_function = levels[current_level]
    await current_level_function(call, any_id=any_id)


@dp.callback_query_handler(IsPrivate(), text="groups_for_user")  # LEVEL = 0
async def my_groups(call: types.CallbackQuery, **kwargs):
    markup = await get_my_groups(call.from_user.id)
    await call.answer()
    await call.message.edit_text(text="Список привязанных на ваше имя групп", reply_markup=markup)
