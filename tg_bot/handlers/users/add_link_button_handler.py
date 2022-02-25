from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.menu_handler import show_admin_menu
from keyboards.inline.menu_keyboard import add_link_cd, menu_cd
from loader import dp
from utils.db_api.db_commands import register_link


async def back_keyboard(any_id):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Вернуться в главное меню",
                               one_time_keyboard=True,
                               callback_data=menu_cd(
                                   level=10,
                                   any_id=any_id
                               ))
            ]
        ]
    )


@dp.callback_query_handler(add_link_cd.filter())
async def add_link(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    group_id = callback_data.get("any_id")
    await state.update_data(
        group_id=group_id
    )
    await call.message.answer(text="Введите название ссылки", reply_markup=await back_keyboard(group_id))
    await state.set_state("add_link_title")


@dp.message_handler(state="add_link_title")
async def add_link_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    if message.text == "Вернуться в главное меню":
        await state.finish()
        await show_admin_menu(message, group_id)
    await state.update_data(
        link_title=message.text
    )
    await message.answer(text="Введите URL", reply_markup=await back_keyboard(group_id))
    await state.set_state("add_link_url")


@dp.message_handler(state="add_link_url")
async def add_link_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    if message.text == "Вернуться в главное меню":
        await state.finish()
        await show_admin_menu(message, group_id)
    await state.update_data(
        link_url=message.text
    )
    await message.answer(text="Ссылка должны вызваться лишь единожды?", reply_markup=await back_keyboard(group_id))
    await state.set_state("one_time_question")


@dp.message_handler(state="one_time_question")
async def add_link_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    await message.answer(text="Ссылка должны вызваться лишь единожды?", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                [
                    InlineKeyboardButton(text="Да", callback_data="yes")
                ],
                [
                    InlineKeyboardButton(text="Нет", callback_data="no")
                ]
            ],
            [
                InlineKeyboardButton(text="Вернуться в главное меню",
                                     callback_data=menu_cd(
                                         level=10,
                                         any_id=group_id))
            ]
        ]
    ))
    await state.set_state("final")


@dp.callback_query_handler(state="final", text=Union["yes", "no"])
async def final(call: types.CallbackQuery, state: FSMContext, callback_data: str):
    data = await state.get_data()
    group_id = data.get("group_id")
    link_title = data.get("link_title")
    link_url = data.get("link_url")
    one_time = True if callback_data == "yes" else False
    await register_link(group_id=group_id, title=link_title, url=link_url, one_time=one_time)
    await state.finish()
    await call.answer("Ссылка была добавлена успешно!")
