import asyncio

from aiogram import Bot, Dispatcher
from aiogram import executor
from aiogram import types
from loguru import logger

from database.exceptions import DBInitError
from libs.db_lib import create_tables_if_not_exist
from libs.tasks import schedule
from loader import redis_storage, register_bot_handlers
from settings.config import BOT_TOKEN


async def on_startup(dispatcher):
    asyncio.create_task(schedule())
    try:
        logger.info("the bot has been successfully start")
        create_tables_if_not_exist()
        register_bot_handlers(dispatcher)
    except DBInitError as err:
        logger.error(f"Ошибка инициализации БД: {err}")


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=redis_storage)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
