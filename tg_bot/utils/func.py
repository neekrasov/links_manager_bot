from datetime import datetime


def get_datetime_from_str(datetime_for_link: dict):
    datetime_for_link['date'] = datetime.strptime(datetime_for_link['date'], "%Y-%m-%d").date()
    datetime_for_link['time_start'] = datetime.strptime(datetime_for_link['time_start'], "%H:%M:%S").time()
    datetime_for_link['time_finish'] = datetime.strptime(datetime_for_link['time_finish'], "%H:%M:%S").time()
    return datetime_for_link


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
