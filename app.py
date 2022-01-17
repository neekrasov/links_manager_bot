from aiogram import executor

import filters
from handlers import dp
from utils.user_mailing import start_mailing
from utils.set_bot_commands import set_default_commands
from utils.db_api import session
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    print("Bot start")
    filters.setup(dp)

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)

    # Запускаем уведомления
    start_mailing()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)