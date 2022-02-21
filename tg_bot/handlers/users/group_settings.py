from aiogram import types
from aiogram.utils.markdown import hlink

from filters import IsPrivate
from keyboards.inline.menu_keyboard import subjects_buttons, get_my_groups, \
    get_group_menu_buttons, admin_menu_cd
from loader import dp
from utils.db_api.db_commands import get_link, get_group


@dp.callback_query_handler(IsPrivate(), admin_menu_cd.filter())
async def navigation_to_lessons(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    main_menu = callback_data.get("main_menu")
    list_of_activities = callback_data.get("list_of_activities")
    any_id = callback_data.get("any_id")

    levels = {
        "0": my_groups,
        "1": show_admin_menu,
        "2": show_subjects,
        "3": show_link,
    }

    current_level_function = levels[current_level]
    await current_level_function(call, main_menu=main_menu, list_of_activities=list_of_activities, any_id=any_id)


@dp.callback_query_handler(IsPrivate(), text="groups_for_user")  # state ; LEVEL = 0
async def my_groups(call: types.CallbackQuery, **kwargs):
    markup = await get_my_groups(call.from_user.id)
    await call.answer()
    await call.message.edit_text(text="Список привязанных на ваше имя групп", reply_markup=markup)
    # await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(IsPrivate())  # admin_menu.filter(); LEVEL =  1
async def show_admin_menu(call: types.CallbackQuery, any_id, **kwargs):  # callback_data: dict
    group = await get_group(int(any_id))  # callback_data['group_id']
    markup = await get_group_menu_buttons(group.chat_id)
    await call.answer()
    await call.message.edit_text(text="Настройки группы")
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(IsPrivate())  # callback_datas.filter(); # LEVEL = 2
async def show_subjects(call: types.CallbackQuery, any_id, **kwargs):  # callback_data: dict
    group_id = int(any_id)  # callback_data.get("group_id")
    print(f" hadler -> show_subjects-> group_id -> {group_id}")
    murcup = await subjects_buttons(group_id)
    await call.answer()
    await call.message.edit_text(text='Выбери предмет')
    await call.message.edit_reply_markup(murcup)


@dp.callback_query_handler(IsPrivate())  # links_all.filter()
async def show_link(call: types.CallbackQuery, any_id, **kwargs):  # callback_data: dict
    print(f"show link - > {await get_link(int(any_id))}")
    link = await get_link(int(any_id))  # callback_data['id']
    await call.answer()
    await call.message.answer(f"{hlink(title='Ссылка', url=link.url)} на конференцию <b>🎓{link.name}🎓</b>\n",
                              disable_web_page_preview=True,
                              )
