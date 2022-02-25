from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command

from filters import IsGroup, IsGroupAdmin
from keyboards.inline.commandstart_keyboard import start_group_buttons
from loader import dp
from utils.db_api.db_commands import register_user, register_group_users


@dp.message_handler(IsGroup(), CommandStart())
async def command_start(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"Привет, {full_name}, я помогу тебе добраться до ссылок твоих предметов!\n",
                         reply_markup=start_group_buttons)


@dp.callback_query_handler(IsGroup(), text='help')
async def show_help(call: types.CallbackQuery):
    await command_help(call.message)


@dp.message_handler(IsGroup(), CommandHelp())
async def command_help(message: types.Message):
    await message.answer(f"<b> Стек комманд </b>\n"
                         f"/get_all_links - получить ссылки по всем предметам.\n"
                         f"/get_link - получить ссылку на текущее время.\n"
                         f"/get_group - прикрепить группу.<b>( Для администраторов )</b>"
                         )


@dp.message_handler(IsGroup(), IsGroupAdmin(), Command("get_group"))
async def get_group_for_user(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    usename = message.from_user.username
    await register_user(user_id, full_name, usename)
    is_register = await register_group_users(user_id, message.chat.id, message.chat.title)
    if is_register:
        await message.answer(f"Группа <b>{message.chat.title}</b> добавлена для настройки\n"
                             f"Пользователю: @{message.from_user.username}\n"
                             f"Для настройки перейдите в бота\n"
                             f"@{(await dp.bot.get_me())['username']}")
    else:
        await message.answer(f"Группа <b>{message.chat.title}</b> уже была добавлена для настройки "
                             f"Пользователю: @{message.from_user.username}\n"
                             f"Для настройки перейдите в бота\n"
                             f"@{(await dp.bot.get_me())['username']}")
