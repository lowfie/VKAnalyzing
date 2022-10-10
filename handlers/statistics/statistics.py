from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from datetime import datetime, timedelta

from database import Analytics
from database.models import Group, Post

from loguru import logger

from .statistics_state import StatisticsFormState


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

        if statistics:
            text = f'Собрано {statistics["count_post"]} постов за период\n' \
                   f'Посты с фото/видео: {statistics["posts_with_photo"]}\n' \
                   f'Лайки: {statistics["likes"]}\n' \
                   f'Комментарии: {statistics["comments"]}\n' \
                   f'Репосты: {statistics["reposts"]}\n' \
                   f'Всего просмотров: {statistics["views"]}'
        else:
            text = f'К сожалению группы {data["name"]} нету в базе\n' \
                   f'Вы можете её добавить написать /parse <name>'

        await dp.bot.send_message(
            chat_id=message.chat.id,
            text=text,
            disable_web_page_preview=True,
        )

        await state.finish()
