import asyncio

from aiogram import executor
from loader import dp

from database.models import create_tables

from loguru import logger

from modules.tasks import schedule

import handlers


async def on_startup(dispatcher):
    asyncio.create_task(schedule())
    try:
        logger.info("the bot has been successfully start")
        create_tables()
    except Exception as err:
        logger.error(f"Ошибка инициализации БД: {err}")


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
