from typing import Union

from aiogram import types

from filters import IsPrivate
from keyboards.inline.menu_keyboard import get_my_groups, get_group_menu_buttons
from loader import dp
from utils.db_api.db_commands import get_group


@dp.callback_query_handler(IsPrivate(), text="groups_for_user")  # LEVEL = 0
async def my_groups(call: types.CallbackQuery, **kwargs):
    markup = await get_my_groups(call.from_user.id)
    await call.answer()
    await call.message.edit_text(text="Список привязанных на ваше имя групп", reply_markup=markup)


# LEVEL =  10
async def show_admin_menu(message: Union[types.CallbackQuery, types.Message], any_id, **kwargs):
    group = await get_group(int(any_id))
    markup = await get_group_menu_buttons(group['chat_id'])
    if type(message) == types.CallbackQuery:
        await message.answer()
        await message.message.edit_text(text="Настройки группы", reply_markup=markup)
    else:
        await message.answer(text="Настройки группы", reply_markup=markup)
