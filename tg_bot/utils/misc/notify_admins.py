import logging

from aiogram import Dispatcher
from loguru import logger

from data.config import TG_BOT_ADMIN_USERNAMES


async def on_startup_notify(dp: Dispatcher):
    for admin in TG_BOT_ADMIN_USERNAMES:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
        logger.info(f'Админы {TG_BOT_ADMIN_USERNAMES} уведомлены о запуске бота')
