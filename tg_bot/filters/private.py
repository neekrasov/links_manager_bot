from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from data.config import TG_BOT_ADMIN_USERNAMES
from loader import bot

is_admin = lambda id: id in TG_BOT_ADMIN_USERNAMES


class IsPrivate(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.PRIVATE
        if isinstance(message, types.CallbackQuery):
            if hasattr(message, 'chat_instance'):
                return True
            return message.message.chat.type == types.ChatType.PRIVATE


class IsGroup(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.SUPERGROUP
        elif isinstance(message, types.CallbackQuery):
            logger.debug(message)
            if hasattr(message, 'chat_instance'):
                return True
            return message.message.chat.type == types.ChatType.SUPERGROUP


class IsForwarded(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.forward_from_chat:
            return message.forward_from_chat.type == types.ChatType.CHANNEL


class IsGroupAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()
