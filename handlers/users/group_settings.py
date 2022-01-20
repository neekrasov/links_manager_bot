from aiogram import types
from aiogram.utils.markdown import hlink

from filters import IsPrivate
from keyboards.inline.menu_keyboard import subjects_buttons, links_all, callback_datas
from loader import dp
from utils.db_api.db_commands import get_link


@dp.callback_query_handler(IsPrivate(), callback_datas.filter())
async def give_subject(call: types.CallbackQuery, callback_data: dict):
    group_id = int(callback_data.get("group_id"))
    murcup= await subjects_buttons(group_id)
    await call.answer()
    await call.message.edit_text(text='Выбери предмет')
    await call.message.edit_reply_markup(murcup)


@dp.callback_query_handler(IsPrivate(), links_all.filter())
async def show_link(call: types.CallbackQuery, callback_data: dict):
    link = await get_link(int(callback_data['id']))
    await call.answer()
    await call.message.answer(f"{hlink(title='Ссылка', url=link.url)} на конференцию <b>🎓{link.name}🎓</b>\n",
                              disable_web_page_preview=True,
                              )
