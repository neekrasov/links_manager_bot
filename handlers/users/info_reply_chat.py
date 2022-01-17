from aiogram import types

from filters import IsPrivate, IsForwarded
from loader import dp


@dp.message_handler(IsPrivate(), IsForwarded(), content_types=types.ContentTypes.ANY)
async def get_info(message: types.Message):
    await message.answer(message.forward_from_chat.id)
