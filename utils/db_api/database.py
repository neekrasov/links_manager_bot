from gino import Gino
from loguru import logger

from data.config import DATABASE_URL

db = Gino()


async def on_startup(dp):
    logger.info("Setup PostgreSQL Connection")
    await db.set_bind(DATABASE_URL)


# engine = create_engine(DATABASE_URL.replace('postgres', 'postgresql'))
# base = declarative_base()
#
# base.metadata.create_all(engine)
# session = sessionmaker(bind=engine)()
