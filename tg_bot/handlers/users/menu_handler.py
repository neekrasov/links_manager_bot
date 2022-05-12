from typing import Union

from aiogram import types

from filters import IsPrivate
from keyboards.inline.menu_keyboard import get_my_groups, get_group_menu_buttons
from loader import dp


@dp.callback_query_handler(IsPrivate(), text="groups_for_user")  # LEVEL = 0
async def my_groups(call: types.CallbackQuery, **kwargs):
    markup = await get_my_groups(user_id=call.from_user.id)
    await call.answer()
    await call.message.edit_text(text="Список привязанных на ваше имя групп", reply_markup=markup)


# LEVEL =  10
async def show_admin_menu(message: Union[types.CallbackQuery, types.Message], any_id, **kwargs):
    markup = await get_group_menu_buttons(any_id)
    if type(message) == types.CallbackQuery:
        await message.answer()
        await message.message.edit_text(text="Настройки группы", reply_markup=markup)
    elif type(message) == types.Message:
        await message.answer(text="Настройки группы", reply_markup=markup)
