from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroupCallBack
from filters.private import IsGroup
from keyboards.inline.callback_data import link_callback_data
from keyboards.inline.subjects_buttons import subjects
from loader import dp
from utils.db_api.db_commands import get_link


@dp.message_handler(IsGroup(), Command("test"))
async def give_subject(message: types.Message):
    await message.answer('Выбери предмет', reply_markup=await subjects(message.chat.id))


@dp.callback_query_handler(IsGroupCallBack(), link_callback_data.filter())
async def link(call: types.CallbackQuery, callback_data: dict):
    link = await get_link(int(callback_data['id']))
    await call.answer()
    await call.message.answer(f"Ссылка на конференцию({link.name}):\n"
                              f"{link.url}")
