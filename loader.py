from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from data.config import (
    BOT_TOKEN,
    USER_POSTGRES,
    PASSWORD_POSTGRES,
    HOST_POSTGRES,
    PORT_POSTGRES,
    DATABASE_POSTGRES,
    PREFIX_REDIS,
    PASSWORD_REDIS,
    HOST_REDIS,
    PORT_REDIS,
    DATABASE_REDIS,
)

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import types

from loguru import logger

# Создание сессии для коммуникации с бд
engine = create_engine(
    f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@{HOST_POSTGRES}:{PORT_POSTGRES}/{DATABASE_POSTGRES}"
)
session = scoped_session(sessionmaker(bind=engine))

# Создание моделей в бд
Base = declarative_base()
Base.query = session.query_property()

# Работа с машиной состояния
redis_storage = RedisStorage2(
    host=HOST_REDIS,
    port=PORT_REDIS,
    db=DATABASE_REDIS,
    pool_size=10,
    password=PASSWORD_REDIS,
    prefix=PREFIX_REDIS,
)

# Подключение к апи телеграмм бота
bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=redis_storage)

# Базовые настройки логирования
logger.add(
    "logs/{time:YYYY-MM-DD} logs.log",
    format="{time} : {level} : {message}",
    level="INFO",
    rotation="1 day",
)
