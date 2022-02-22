from aiogram import types
from aiogram.utils.markdown import hlink

from filters import IsPrivate
from keyboards.inline.menu_keyboard import get_group_menu_buttons, subjects_buttons
from loader import dp
from utils.db_api.db_commangs import get_group, get_link


@dp.callback_query_handler(IsPrivate())  # LEVEL =  10
async def show_admin_menu(call: types.CallbackQuery, any_id, **kwargs):
    group = await get_group(int(any_id))
    markup = await get_group_menu_buttons(group['chat_id'])
    await call.answer()
    await call.message.edit_text(text="Настройки группы", reply_markup= markup)


@dp.callback_query_handler(IsPrivate())  # LEVEL = 11
async def show_subjects(call: types.CallbackQuery, any_id, **kwargs):
    group_id = int(any_id)
    markup = await subjects_buttons(group_id)
    await call.answer()
    await call.message.edit_text(text='Выбери предмет', reply_markup= markup)


@dp.callback_query_handler(IsPrivate())  # LEVEL = 12
async def show_link(call: types.CallbackQuery, any_id, **kwargs):
    link = await get_link(int(any_id))
    await call.answer()
    await call.message.answer(f"{hlink(title='Ссылка', url=link['url'])} на конференцию <b>🎓{link['title']}🎓</b>\n",
                              disable_web_page_preview=True,
                              )