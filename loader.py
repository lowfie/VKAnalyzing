from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from data.config import USER_POSTGRES, PASSWORD_POSTGRES, HOST_POSTGRES, PORT_POSTGRES, DATABASE_POSTGRES, BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Создание сессии для коммуникации с бд
engine = create_engine(
    f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@{HOST_POSTGRES}:{PORT_POSTGRES}/{DATABASE_POSTGRES}")
session = scoped_session(sessionmaker(bind=engine))

# Создание моделей в бд
Base = declarative_base()
Base.query = session.query_property()

# Работа с машиной состояния
storage = MemoryStorage()

# Подключение к апи телеграмм бота
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

