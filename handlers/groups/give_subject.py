from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroupCallBack
from filters.private import IsGroup
from keyboards.inline.subjects_buttons import subjects
from loader import dp
from utils.db_api.db_commands import get_links_for_group


@dp.message_handler(IsGroup(), Command("test"))
async def give_subject(message: types.Message):
    await message.answer('Выбери предмет', reply_markup=await subjects(message.chat.id))


@dp.callback_query_handler(IsGroupCallBack())
async def get_link(call: types.CallbackQuery):
    link = await get_links_for_group(call.data)
    await call.answer()
    await call.message.answer("Ссылка на конференцию:\n"
                              f"{link.url}")
