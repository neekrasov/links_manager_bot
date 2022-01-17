from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS
from loader import bot

is_admin = lambda id: id in ADMINS


class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.SUPERGROUP


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE


class IsForwarded(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.forward_from_chat:
            return message.forward_from_chat.type == types.ChatType.CHANNEL


class IsGroupCallBack(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        return call.message.chat.type == types.ChatType.SUPERGROUP


class IsGroupAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()