from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData("menu", "level", "any_id")
update_date_link_cd = CallbackData("update_link", "level", "link_id", "group_id", "month", "day", "time_start",
                                   "time_finish",
                                   "repeat")
add_link_cd = CallbackData("add_link", 'any_id')
links_cd = CallbackData("links", "id")


def make_menu_cd(level, any_id="0"):
    return menu_cd.new(
        level=level,
        any_id=any_id,
    )


def make_update_date_link_cd(level, link_id="0", group_id="0", month="0", day="0", time_start="0", time_finish="0",
                             repeat="0"):
    return update_date_link_cd.new(
        level=level,
        link_id=link_id,
        month=month,
        day=day,
        time_start=time_start,
        time_finish=time_finish,
        group_id=group_id,
        repeat=repeat,
    )
