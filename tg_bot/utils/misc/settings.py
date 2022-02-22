import time
import os
from data import config


def set_time_zone():
    os.environ['TZ'] = config.TIME_ZONE
    time.tzset()


def on_startup():
    set_time_zone()
