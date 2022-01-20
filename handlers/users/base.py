from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from filters import IsPrivate
from keyboards.inline.commandstart_keyboard import start_private_buttons
from keyboards.inline.menu_keyboard import get_group_menu_buttons, admin_menu
from keyboards.inline.menu_keyboard import get_my_groups
from loader import dp
from utils.db_api.db_commands import register_user, get_group


@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await register_user(user_id, full_name)
    await message.answer(f"Здравствуй {message.from_user.full_name}, я бот менеджер-ссылок.\n",
                         reply_markup=start_private_buttons)


@dp.callback_query_handler(IsPrivate(), text="groups_for_user")  # state
async def my_groups(call: types.CallbackQuery):
    markup = await get_my_groups(call.from_user.id)
    await call.answer()
    await call.message.edit_text(text="Список привязанных на ваше имя групп", reply_markup=markup)
    # await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(IsPrivate(), admin_menu.filter())
async def show_menu(call: types.CallbackQuery, callback_data: dict):
    group = await get_group(int(callback_data['group_id']))
    markup = await get_group_menu_buttons(group.chat_id)
    await call.answer()
    await call.message.edit_text(text="Настройки группы")
    await call.message.edit_reply_markup(reply_markup=markup)

