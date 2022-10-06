from aiogram import executor
from loader import dp

import handlers

from database.models import create_tables

import logging


logging.basicConfig(filename='logs.log', level=logging.INFO)


async def on_startup(dispatcher):
    logging.info('Bot started')
    create_tables()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
