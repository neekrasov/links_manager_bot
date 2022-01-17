from aiogram import types

from filters import IsPrivate, IsForwarded
from loader import dp


@dp.message_handler(IsPrivate(), content_types=types.ContentTypes.ANY)
async def i_dont_death(message: types.Message):
    await message.answer("Я ЖИВОЙ СУКА!")