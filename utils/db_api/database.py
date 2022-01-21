from gino import Gino
from loguru import logger

from data.config import DATABASE_URL

db = Gino()


async def on_startup(dp):
    logger.info("Setup PostgreSQL Connection")
    await db.set_bind(DATABASE_URL)
