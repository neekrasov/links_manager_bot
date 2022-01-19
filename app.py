from aiogram import executor

import filters
from handlers import dp
from utils.db_api import database
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.user_mailing import start_mailing


async def on_startup(dispatcher):
    print("Bot start")
    filters.setup(dp)
    await database.on_startup(dp)
    await database.db.gino.create_all()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    # Запускаем уведомления
    await start_mailing()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
