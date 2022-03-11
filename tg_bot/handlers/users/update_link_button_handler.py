import datetime

from aiogram import types

from filters import IsPrivate
from handlers.users.menu_handler import show_admin_menu
from keyboards.inline.callback_datas import update_date_link_cd
from keyboards.inline.update_date_link_keyboard import select_update_buttons, edit_month_buttons, edit_day_buttons, \
    edit_lessons_start_time_buttons, edit_lessons_finish_time_buttons, edit_repeat_buttons
from loader import dp
from utils.constant import LESSONS_START, LESSONS_FINISH
from utils.db_api.db_commands import register_datetime_for_link
from utils.user_mailing import scheduler_add_job


@dp.callback_query_handler(IsPrivate(), update_date_link_cd.filter())
async def navigate_to_update_link_date(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    link_id = callback_data.get("link_id")
    month = callback_data.get("month")
    day = callback_data.get("day")
    time_start = callback_data.get("time_start")
    time_finish = callback_data.get("time_finish")
    group_id = callback_data.get("group_id")
    repeat = callback_data.get("repeat")
    levels = {
        '0': back_to_admin_menu,
        '1': select_update_link,
        '2': select_month_for_update_link,
        '3': select_day_of_month_for_update_link,
        '4': select_time_start_for_update_link,
        '5': select_time_finish_for_update_link,
        '6': select_repeat_for_update_link,
        '7': final_recordings_for_update_link,
    }

    current_level_function = levels[current_level]
    await current_level_function(call, link_id=link_id, group_id=group_id, month=month, day=day, time_start=time_start,
                                 time_finish=time_finish, repeat=repeat)


async def back_to_admin_menu(call: types.CallbackQuery, group_id, **kwargs):
    await show_admin_menu(message=call, any_id=group_id)


async def select_update_link(call: types.CallbackQuery, group_id, **kwargs):
    await call.message.edit_text(text="🠗Выберите предмет для редактирования🠗",
                                 reply_markup=await select_update_buttons(group_id=group_id))


async def select_month_for_update_link(call: types.CallbackQuery, link_id, group_id, **kwargs):
    await call.message.edit_text(text="🠗Выберите месяц🠗",
                                 reply_markup=await edit_month_buttons(link_id=link_id, group_id=group_id))


async def select_day_of_month_for_update_link(call: types.CallbackQuery, link_id, group_id, month, **kwargs):
    await call.message.edit_text(text="🠗Выберите дату🠗",
                                 reply_markup=await edit_day_buttons(link_id=link_id, group_id=group_id, month=month))


async def select_time_start_for_update_link(call: types.CallbackQuery, link_id, group_id, month, day, **kwargs):
    await call.message.edit_text(text="🠗Выберите время <b>начала</b>🠗",
                                 reply_markup=await edit_lessons_start_time_buttons(link_id=link_id, group_id=group_id,
                                                                                    month=month, day=day))


async def select_time_finish_for_update_link(call: types.CallbackQuery, link_id, group_id, month, day, time_start,
                                             **kwargs):
    await call.message.edit_text(text="🠗Выберите время <b>конца</b>🠗",
                                 reply_markup=await edit_lessons_finish_time_buttons(link_id=link_id, group_id=group_id,
                                                                                     month=month, day=day,
                                                                                     time_start=time_start))


async def select_repeat_for_update_link(call: types.CallbackQuery, link_id, group_id, month, day, time_start,
                                        time_finish,
                                        **kwargs):
    await call.message.edit_text(text="Сколько раз будет повторяться ссылка?",
                                 reply_markup=await edit_repeat_buttons(link_id=link_id,
                                                                        group_id=group_id,
                                                                        month=month, day=day,
                                                                        time_start=time_start,
                                                                        time_finish=time_finish))


async def final_recordings_for_update_link(call: types.CallbackQuery, link_id, group_id, month, day, time_start,
                                           time_finish, repeat):
    date = datetime.date(year=datetime.datetime.now().year, month=int(month), day=int(day))
    date_link = datetime.datetime.strptime(str(date), "%Y-%m-%d").date()
    time_start_link = datetime.datetime.strptime(LESSONS_START[time_start], "%H:%M:%S").time()
    time_finish_link = datetime.datetime.strptime(LESSONS_FINISH[time_finish], "%H:%M:%S").time()
    data = {
        "link_id": int(link_id),
        "date": date_link,
        "time_start": time_start_link,
        "time_finish": time_finish_link,
        "repeat": int(repeat),

    }

    await register_datetime_for_link(**data)
    await scheduler_add_job(data)
    await call.answer(text="Время было успешно обновлено")
    await back_to_admin_menu(call, group_id)
