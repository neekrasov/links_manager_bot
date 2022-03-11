from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from keyboards.inline.callback_datas import make_update_date_link_cd
from utils.constant import MONTHS, LESSONS_START, LESSONS_FINISH, REPEAT, MONTHS_INDEX
from utils.db_api.db_commands import get_links_for_group
from utils.func import get_key


async def select_update_buttons(group_id) -> InlineKeyboardMarkup:
    """ Вывод списка предметов, привязанных к определённой группе"""
    CURRENT_LEVEL = 1
    links_for_group = await get_links_for_group(group_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for link in links_for_group:
        button = InlineKeyboardButton(text=link['title'],
                                      callback_data=make_update_date_link_cd(level=CURRENT_LEVEL + 1,
                                                                             link_id=link['id'],
                                                                             group_id=group_id))
        markup.insert(button)

    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL - 1, group_id=group_id))
    )
    return markup


async def edit_month_buttons(link_id: int, group_id: int):
    """ Выбор месяца """
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    month = [
        InlineKeyboardButton(text=month,
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL + 1, link_id=link_id,
                                                                    group_id=group_id, month=index))
        for month, index in MONTHS_INDEX.items()]
    buttons = [month[i: i + 3] for i in range(0, len(month), len(month) // 4)]
    for row in buttons:
        markup.add(*row)

    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL - 1, group_id=group_id))
    )
    return markup


async def edit_day_buttons(link_id: int, group_id: int, month: str):
    """ Выбор определённого дня месяца """
    CURRENT_LEVEL = 3
    number_of_days = MONTHS[get_key(MONTHS_INDEX, int(month))]
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=str(number),
                                    callback_data=make_update_date_link_cd(level=CURRENT_LEVEL + 1, link_id=link_id,
                                                                           month=month,
                                                                           group_id=group_id, day=number)) for number in
               range(1, number_of_days + 1)]

    resize_buttons = [buttons[index: index + 6] for index in range(0, len(buttons), len(buttons) // 5)]
    for row in resize_buttons:
        markup.row(*row)

    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL - 1, group_id=group_id,
                                                                    link_id=link_id))
    )
    return markup


async def edit_lessons_start_time_buttons(link_id: int, group_id: int, month: str, day: str):
    """ Выбор времени старта уведомления"""
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=time_lessons_title,
                                    callback_data=make_update_date_link_cd(level=CURRENT_LEVEL + 1, link_id=link_id,
                                                                           group_id=group_id, month=month, day=day,
                                                                           time_start=time_lessons_title))
               for time_lessons_title in LESSONS_START]

    resize_buttons = [buttons[index: index + 3] for index in range(0, len(buttons), len(buttons) // 2)]
    for row in resize_buttons:
        markup.row(*row)
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL - 1, group_id=group_id,
                                                                    link_id=link_id, month=month))
    )
    return markup


async def edit_lessons_finish_time_buttons(link_id: int, group_id: int, month: str, day: str, time_start: str):
    """ Выбор конечного времени действия уведомления """
    CURRENT_LEVEL = 5
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=time_lessons_title,
                                    callback_data=make_update_date_link_cd(level=CURRENT_LEVEL + 1, link_id=link_id,
                                                                           group_id=group_id, month=month, day=day,
                                                                           time_start=time_start,
                                                                           time_finish=time_lessons_title))
               for time_lessons_title in LESSONS_FINISH]

    resize_buttons = [buttons[index: index + 3] for index in range(0, len(buttons), len(buttons) // 2)]
    for row in resize_buttons:
        markup.row(*row)
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL - 1, group_id=group_id,
                                                                    link_id=link_id, month=month, day=day))
    )
    return markup


async def edit_repeat_buttons(link_id: int, group_id: int, month: str, day: str, time_start: str, time_finish: str):
    """ Выбор частоты повторения ссылки """
    CURRENT_LEVEL = 6
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=title,
                                    callback_data=make_update_date_link_cd(level=CURRENT_LEVEL + 1, link_id=link_id,
                                                                           group_id=group_id, month=month, day=day,
                                                                           time_start=time_start,
                                                                           time_finish=time_finish, repeat=int(degree)))
               for title, degree in REPEAT.items()]
    resize_buttons = [buttons[index: index + 2] for index in range(0, len(buttons), len(buttons) // 2)]
    for row in resize_buttons:
        markup.row(*row)
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_update_date_link_cd(level=CURRENT_LEVEL - 1, group_id=group_id,
                                                                    link_id=link_id, month=month, day=day,
                                                                    time_start=time_start))
    )
    return markup
