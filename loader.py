from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from settings.config import (
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

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher
from aiogram import types

from bot.handlers.start import bot_start
from bot.handlers.help import cmd_help
from bot.handlers.cancel_state_handler import cancel_handler
from bot.handlers.tops.get_tops_params import (
    cm_tops,
    tops_load_name,
    tops_choice_data_period,
    tops_load_period
)
from bot.handlers.statistics.get_statistics_params import (
    cm_stats,
    stats_load_name,
    stats_choice_data_period,
    stats_load_period
)
from bot.handlers.parse.parse import (
    cm_parse,
    parse_load_name
)
from bot.handlers.autoparse.autoparse import (
    cm_autoparse,
    autoparse_load_name
)

from bot.handlers.tops.tops_state import TopsFormState
from bot.handlers.statistics.statistics_state import StatisticsFormState
from bot.handlers.parse.parse_state import ParseFormState
from bot.handlers.autoparse.autoparse_state import AutoparseFormState

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

dp.register_message_handler(bot_start, commands="start")
dp.register_message_handler(cmd_help, commands="help")

dp.register_message_handler(cmd_help, regexp="^(❓ Помощь)$")
dp.register_message_handler(cancel_handler, state="*", commands=["cancel", "отмена"])

dp.register_message_handler(cm_tops, commands="tops", state=None)
dp.register_message_handler(cm_tops, regexp="^(📈 Анализ постов)$")
dp.register_message_handler(tops_load_name, state=TopsFormState.name, content_types=["text"])
dp.callback_query_handler(tops_choice_data_period, state=TopsFormState.choice_date_period, text_contains="choice")
dp.register_message_handler(tops_load_period, state=TopsFormState.days, content_types=["text"])

dp.register_message_handler(cm_stats, commands="stats", state=None)
dp.register_message_handler(cm_stats, regexp="^(📊 Статистика)$")
dp.register_message_handler(stats_load_name, state=StatisticsFormState.name, content_types=["text"])
dp.callback_query_handler(stats_choice_data_period, state=StatisticsFormState.choice_date_period, text_contains="choice")
dp.register_message_handler(stats_load_period, state=StatisticsFormState.days, content_types=["text"])

dp.register_message_handler(cm_parse, commands="parse", state=None)
dp.register_message_handler(cm_parse, regexp="^(🔨 Спарсить группу)$")
dp.register_message_handler(parse_load_name, state=ParseFormState.name, content_types=["text"])

dp.register_message_handler(cm_autoparse, commands="autoparse", state=None)
dp.register_message_handler(cm_autoparse, regexp="^(🛠 Авто-парсинг группы)$")
dp.register_message_handler(autoparse_load_name, state=AutoparseFormState.name, content_types=["text"])
