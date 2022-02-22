from aiogram import Dispatcher
from loguru import logger

from .private import *


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsGroupAdmin)
    logger.info('Set filters')
    # dp.filters_factory.bind(IsChannels)
    # dp.filters_factory.bind(IsAdmin)
