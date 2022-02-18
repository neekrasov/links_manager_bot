from aiogram import Bot
from typing import List, Tuple

from aiohttp import web

from loguru import logger
from data import config
from loader import bot, dp


async def on_startup(app: web.Application):
    from handlers import dp

    # Настройка фильтров
    import filters
    filters.setup(dp)

    import middlewares
    middlewares.setup(dp)

    # Подключение к базе данных
    from utils.db_api import database
    await database.on_startup(dp)
    await database.db.gino.create_all()

    # Устанавливаем дефолтные команды
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    # Запускаем уведомления
    from utils.user_mailing import start_mailing
    await start_mailing()

    # Уведомляет про запуск
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    logger.info('Configure Webhook URL to: {url}', url=config.WEBHOOK_URL)
    await dp.bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(app: web.Application):
    app_bot: Bot = app['bot']
    await app_bot.close()


async def init() -> web.Application:
    from utils.misc import logging
    import web_handlers

    logging.setup()
    app = web.Application()
    subapps: List[Tuple[str, web.Application]] = [
        ('/tg/webhooks/', web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp['bot'] = bot
        subapp['dp'] = dp
        app.add_subapp(prefix, subapp)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    web.run_app(init(), port=config.TG_BOT_PUBLIC_PORT)
