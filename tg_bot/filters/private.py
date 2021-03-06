from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import TG_BOT_ADMIN_USERNAMES
from loader import bot

is_admin = lambda id: id in TG_BOT_ADMIN_USERNAMES


class IsGroup(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.SUPERGROUP
        if isinstance(message, types.CallbackQuery):
            return message.message.chat.type == types.ChatType.SUPERGROUP


class IsPrivate(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.PRIVATE
        if isinstance(message, types.CallbackQuery):
            return message.message.chat.type == types.ChatType.PRIVATE


class IsForwarded(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.forward_from_chat:
            return message.forward_from_chat.type == types.ChatType.CHANNEL


class IsGroupAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()
