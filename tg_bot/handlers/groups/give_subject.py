from aiogram import types
from aiogram.dispatcher.filters import Command

from filters.private import IsGroup
from keyboards.inline.get_all_links_keyboard import subjects_buttons_for_group
from keyboards.inline.menu_keyboard import links_all
from loader import dp
from utils.handlers import answer_link


@dp.message_handler(IsGroup(), Command("get_all_links"))
async def give_subject(message: types.Message):
    await message.answer('Выбери предмет', reply_markup=await subjects_buttons_for_group(message.chat.id))


@dp.callback_query_handler(IsGroup(), links_all.filter())
async def show_link(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await answer_link(int(callback_data['id']), call.message.chat.id)