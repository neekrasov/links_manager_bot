from aiogram import types
from aiogram.utils.markdown import hlink

from keyboards.inline.menu_keyboard import subjects_buttons
from utils.db_api.db_commands import get_link


async def show_subjects(call: types.CallbackQuery, any_id, **kwargs):  # LEVEL = 11
    """ Вывод списка предметов """
    group_id = int(any_id)
    markup = await subjects_buttons(group_id)
    await call.answer()
    await call.message.edit_text(text='Выбери предмет', reply_markup=markup)


async def show_link(call: types.CallbackQuery, any_id, **kwargs):  # LEVEL = 12
    """ Вывод ссылок для каждого предмета """
    link = await get_link(int(any_id))
    await call.answer()
    await call.message.answer(f"{hlink(title='Ссылка', url=link['url'])} на конференцию <b>🎓{link['title']}🎓</b>\n",
                              disable_web_page_preview=True,
                              )
