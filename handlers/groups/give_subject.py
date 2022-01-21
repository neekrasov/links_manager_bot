from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink

from filters.private import IsGroup
from keyboards.inline.get_all_links_keyboard import subjects_buttons_for_group
from keyboards.inline.menu_keyboard import links_all
from loader import dp
from utils.db_api.db_commands import get_link


@dp.message_handler(IsGroup(), Command("get_all_links"))
async def give_subject(message: types.Message):
    print(f"message.chat.id -> {message.chat.id}")
    await message.answer('Выбери предмет', reply_markup=await subjects_buttons_for_group(message.chat.id))


@dp.callback_query_handler(IsGroup(), links_all.filter())  # вынести эту хуету
async def show_link(call: types.CallbackQuery, callback_data: dict):
    link = await get_link(int(callback_data['id']))
    await call.answer()
    await call.message.answer(f"{hlink(title='Ссылка', url=link.url)} на конференцию <b>🎓{link.name}🎓</b>\n",
                              disable_web_page_preview=True,
                              )
