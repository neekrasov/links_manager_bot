import time

from environs import Env, EnvValidationError
from pathlib import Path
import os

ENV_PATH = ".env"

env = Env()
env.read_env(ENV_PATH)


def get_tg_bot_token():
    try:
        token = env.str('TG_BOT_TOKEN')
    except EnvValidationError:
        token = os.environ['TG_BOT_TOKEN']
    return token


def get_tg_bot_admins():
    try:
        admins = env.list("TG_BOT_ADMIN_USERNAMES")
    except EnvValidationError:
        admins = os.environ['TG_BOT_ADMIN_USERNAMES'].split(',')
    return [int(id) for id in admins]


def get_sheduler_prearranged_link_minutes():
    try:
        sheduler_prearranged_link_minutes = env.int("SHEDULER_PREARRANGED_LINK_MINUTES")
    except EnvValidationError:
        sheduler_prearranged_link_minutes = os.environ['SHEDULER_PREARRANGED_LINK_MINUTES'].split(',')
    return sheduler_prearranged_link_minutes


def get_db_url():
    dp_params = dict()
    for key in ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT",
                "POSTGRES_DB"]:
        try:
            value = env.str(key)
        except EnvValidationError:
            value = os.environ[key]
        dp_params[key] = value
    db_url = f"postgres://{dp_params['POSTGRES_USER']}:{dp_params['POSTGRES_PASSWORD']}@" \
             f"{dp_params['POSTGRES_HOST']}:{dp_params['POSTGRES_PORT']}/{dp_params['POSTGRES_DB']}"
    return db_url


def get_logging_level() -> list:
    try:
        logging_level = env.list("LOGGING_LEVEL")
    except EnvValidationError:
        logging_level = os.environ['LOGGING_LEVEL']
    return logging_level


def get_time_zone() -> str:
    try:
        time_zone = env.str("TIME_ZONE")
    except EnvValidationError:
        time_zone = os.environ['TIME_ZONE']
    return time_zone


TG_BOT_TOKEN = get_tg_bot_token()
TG_BOT_ADMIN_USERNAMES = get_tg_bot_admins()

SHEDULER_PREARRANGED_LINK_MINUTES=get_sheduler_prearranged_link_minutes()

DATABASE_URL = get_db_url()

LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')

LOGGING_LEVEL = get_logging_level()

TIME_ZONE = get_time_zone()
