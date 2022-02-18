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


def get_tg_bot_public_port():
    try:
        port = env.str('TG_BOT_PUBLIC_PORT')
    except EnvValidationError:
        port = os.environ['TG_BOT_PUBLIC_PORT']
    return port


def get_tg_bot_admins():
    try:
        admins = env.list("TG_BOT_ADMIN_USERNAMES")
    except EnvValidationError:
        admins = os.environ['TG_BOT_ADMIN_USERNAMES'].split(',')
    return [int(id) for id in admins]


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


def get_domain_url():
    try:
        domain = env.str("DOMAIN")
    except EnvValidationError:
        domain = os.environ['DOMAIN']
    return domain


TG_BOT_TOKEN = get_tg_bot_token()
TG_BOT_PUBLIC_PORT = get_tg_bot_public_port()
TG_BOT_ADMIN_USERNAMES = get_tg_bot_admins()

DOMAIN_URL = get_domain_url()
WEBHOOK_PATH = f'/tg/webhooks/bot/{TG_BOT_TOKEN}'
WEBHOOK_URL = f'{DOMAIN_URL}{WEBHOOK_PATH}'

DATABASE_URL = get_db_url()

LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')
