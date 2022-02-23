from aiogram.utils import executor
from loguru import logger
from loader import dp

# Сбор информации о хэндлерах
from handlers import dp


async def on_startup(dp):
    from utils.misc import logging, settings
    logging.setup()
    settings.on_startup()


    # Настройка фильтров
    import filters
    filters.setup(dp)

    # Настройка middlewares
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
    from utils.misc.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    logger.info(f'Bot is running')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)