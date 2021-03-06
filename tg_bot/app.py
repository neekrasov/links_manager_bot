from aiogram.utils import executor
from loguru import logger

# Сбор информации о хэндлерах
from handlers import dp


async def on_startup(dp):
    # Установка настроек
    from utils.misc import settings
    settings.on_startup()


    # Запускаем логирование
    from utils.misc import logging
    logging.setup()

    # Настройка фильтров
    import filters
    filters.setup(dp)

    # Настройка middlewares
    import middlewares
    middlewares.setup(dp)

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
