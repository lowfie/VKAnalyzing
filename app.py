from aiogram import executor
from loader import dp

from database.models import create_tables

from loguru import logger

import handlers

logger.add(
    'logs.log',
    format='{time} : {level} : {message}',
    level='INFO',
    rotation='20 MB'
)


async def on_startup(dispatcher):
    try:
        logger.info('the bot has been successfully start')
        create_tables()
    except Exception as err:
        logger.error(f'Ошибка инициализации БД:\n{err}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
