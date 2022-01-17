from aiogram import types
from aiogram.dispatcher.filters import Command

from filters.private import IsGroup
from keyboards.inline.subjects_buttons import subjects
from loader import dp


@dp.message_handler(IsGroup(), Command("test"))
async def give_subject(message: types.Message):
    await message.answer('Выбери предмет', reply_markup=subjects)
