from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroupCallBack
from filters.private import IsGroup
from keyboards.inline.subjects_buttons import subjects
from loader import dp
from utils.db_api import session
from utils.db_api.models import Links


@dp.message_handler(IsGroup(), Command("test"))
async def give_subject(message: types.Message):
    await message.answer('Выбери предмет', reply_markup=subjects(message.chat.id))


@dp.callback_query_handler(IsGroupCallBack())
async def get_link(call: types.CallbackQuery):
    link = session.query(Links).get(call.data)
    await call.answer()
    await call.message.answer(f"Ссылка на конференцию ({link.name}):\n"
                              f"{link.url}")
