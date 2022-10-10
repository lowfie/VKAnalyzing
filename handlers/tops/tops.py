from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp

from datetime import datetime, timedelta

from database import Analytics
from database.models import Group, Post

from .tops_state import TopsFormState


@dp.message_handler(commands='tops', state=None)
async def cm_tops(message: types.Message):
    await TopsFormState.name.set()
    await message.reply('Введите название группы из ссылки')


@dp.message_handler(state=TopsFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Введите период подсчёта топов (в днях)')
    await TopsFormState.next()


@dp.message_handler(state=TopsFormState.days, content_types=['text'])
async def load_period(message: types.Message, state: FSMContext):
    analysis = Analytics(group=Group, post=Post)
    async with state.proxy() as data:
        data['date'] = str(datetime.now() - timedelta(days=int(message.text)))[:-7]

        most_positive_post = analysis.get_tops_stats(data, Post.positive_comments)
        most_negative_post = analysis.get_tops_stats(data, Post.negative_comments)
        most_popular_post = analysis.get_tops_stats(data, Post.views)

        if most_popular_post and most_negative_post and most_popular_post:
            text = f'{hlink("Самый популярный пост", most_popular_post)}\n' \
                   f'{hlink("Самый позитивный пост", most_positive_post)}\n' \
                   f'{hlink("Самый негативный пост", most_negative_post)}\n'
            parse_mode = 'html'
        else:
            text = f'К сожалению группы {data["name"]} нету в базе\n' \
                   f'Вы можете её добавить написать /parse <name>'
            parse_mode = None

        await dp.bot.send_message(
            chat_id=message.chat.id,
            text=text,
            disable_web_page_preview=True,
            parse_mode=parse_mode
        )

        await state.finish()
