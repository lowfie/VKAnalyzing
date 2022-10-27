import asyncio

from aiogram import executor
from loguru import logger

from database.exceptions import DBInitError
from libs.db_lib import create_tables_if_not_exist
from libs.tasks import schedule
from loader import dp, register_bot_handlers


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
    register_bot_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
