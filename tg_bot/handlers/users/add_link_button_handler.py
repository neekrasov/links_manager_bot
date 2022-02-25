from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.menu_handler import show_admin_menu
from keyboards.inline.menu_keyboard import add_link_cd
from loader import dp
from utils.db_api.db_commands import register_link


async def back_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Вернуться в главное меню")
            ]
        ]
    )


@dp.callback_query_handler(add_link_cd.filter())
async def add_link(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    group_id = callback_data.get("any_id")
    await state.update_data(
        group_id=group_id
    )
    await call.message.answer(text="Введите название ссылки", reply_markup=await back_keyboard())
    await state.set_state("add_link_title")


@dp.message_handler(state="add_link_title")
async def add_link_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    if message.text == "Вернуться в главное меню":
        await state.finish()
        await show_admin_menu(message, group_id)
        await message.delete()
    else:
        await state.update_data(
            link_title=message.text
        )
        await message.answer(text="Введите URL", reply_markup=await back_keyboard())
        await state.set_state("add_link_url")


@dp.message_handler(state="add_link_url")
async def add_link_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    if message.text == "Вернуться в главное меню":
        await state.finish()
        await show_admin_menu(message, group_id)
        await message.delete()
    else:
        await state.update_data(
            link_url=message.text
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="yes")
            ],
            [
                InlineKeyboardButton(text="Нет", callback_data="no")
            ],
            [
                InlineKeyboardButton(text="Вернуться в главное меню",
                                     callback_data="back")
            ]
        ], row_width=2)
        await message.answer(text="Ссылка должны вызваться лишь единожды?",
                             reply_markup=markup)
        await state.set_state("one_time_question")


async def final_add(state: FSMContext, call: types.CallbackQuery, one_time: bool):
    data = await state.get_data()
    group_id = data.get("group_id")
    link_title = data.get("link_title")
    link_url = data.get("link_url")
    one_time = one_time
    await register_link(group_id=group_id, title=link_title, url=link_url, one_time=one_time)
    await state.finish()
    await call.answer("Ссылка была добавлена успешно!")


@dp.callback_query_handler(state="one_time_question", text="yes")
async def one_time_question_yes(call: types.CallbackQuery, state: FSMContext):
    await final_add(state=state, call=call, one_time=True)


@dp.callback_query_handler(state="one_time_question", text="no")
async def one_time_question_no(call: types.CallbackQuery, state: FSMContext):
    await final_add(state=state, call=call, one_time=False)


@dp.callback_query_handler(state="one_time_question", text="back")
async def one_time_question_back(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    group_id = data.get("group_id")
    await state.finish()
    await show_admin_menu(call, group_id)
