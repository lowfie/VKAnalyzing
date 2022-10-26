import asyncio

from loader import dp
from loguru import logger
from aiogram import executor
from libs.tasks import schedule
from database.exceptions import DBInitError
from database.services import create_tables_if_not_exist


async def on_startup(dispatcher):
    asyncio.create_task(schedule())
    try:
        logger.info("the bot has been successfully start")
        create_tables_if_not_exist()
    except DBInitError as err:
        logger.error(f"Ошибка инициализации БД: {err}")


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
