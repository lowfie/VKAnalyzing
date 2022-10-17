from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from datetime import datetime, timedelta

from database import Analytics
from database.models import Group, Post

from loguru import logger

from .statistics_state import StatisticsFormState
from handlers.cancel_state_handler import cancel_handler


@dp.message_handler(commands='stats', state=None)
async def cm_stats(message: types.Message):
    await StatisticsFormState.name.set()
    await message.reply('Введите название группы из ссылки')


@dp.message_handler(state=StatisticsFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Введите период подсчёта статистики (в днях)')
    await StatisticsFormState.next()


@dp.message_handler(state=StatisticsFormState.days, content_types=['text'])
async def load_period(message: types.Message, state: FSMContext):
    analysis = Analytics(group=Group, post=Post)
    async with state.proxy() as data:
        try:
            days = timedelta(days=int(message.text))
        except (OverflowError, ValueError) as err:
            logger.warning(f'В команде /stats указан неверный параметр периода: {err}')
            await message.reply('Вы ввели некорректное значение, поэтому будет использоваться неделя, как период')
            days = timedelta(days=7)

        data['date'] = str(datetime.now() - days)[:-7]

        statistics = analysis.get_statistic(data)

        if statistics is not None and statistics['count_post'] > 0:
            text = f'Собрано <b>{statistics["count_post"]}</b> постов за период\n' \
                   f'Посты с фото/видео: <b>{statistics["posts_with_photo"]}</b>\n' \
                   f'Лайки: <b>{statistics["likes"]}</b>\n' \
                   f'Комментарии: <b>{statistics["comments"]}</b>\n' \
                   f'Репосты: <b>{statistics["reposts"]}</b>\n' \
                   f'Всего просмотров: <b>{statistics["views"]}</b>'
        elif statistics is not None and statistics['count_post'] == 0:
            text = f'Статистику за этот период невозможно собрать\n' \
                   f'Попробуйте указать период больше'
        else:
            text = f'Группы <b>{data["name"]}</b> нету в базе\n' \
                   f'Вы можете её добавить написать <code>/parse group_name</code>'

        await message.answer(text=text)
        await state.finish()
