from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp

from datetime import datetime, timedelta

from database import Analytics
from database.models import Group, Post

from loguru import logger

from keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from keyboards.reply.menu_keyboard import main_keyboard

from .tops_state import TopsFormState
from handlers.cancel_state_handler import cancel_handler


@dp.message_handler(commands='tops', state=None)
@dp.message_handler(regexp='^(📈 Топы постов группы)$')
async def cm_tops(message: types.Message):
    await TopsFormState.name.set()
    await message.reply('Введите название группы из ссылки', reply_markup=await cancel_state_keyboard())


@dp.message_handler(state=TopsFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Введите период подсчёта топов (в днях)', reply_markup=await cancel_state_keyboard())
    await TopsFormState.next()


@dp.message_handler(state=TopsFormState.days, content_types=['text'])
async def load_period(message: types.Message, state: FSMContext):
    analysis = Analytics(group=Group, post=Post)
    async with state.proxy() as data:
        try:
            days = timedelta(days=int(message.text))
        except (OverflowError, ValueError) as err:
            logger.warning(f'В команде /tops указан неверный параметр периода: {err}')
            await message.reply('Вы ввели некорректное значение, поэтому будет использоваться неделя, как период')
            days = timedelta(days=7)

        data['date'] = str(datetime.now() - days)[:-7]

        most_positive_post = analysis.get_top_stats(data, Post.positive_comments)
        most_negative_post = analysis.get_top_stats(data, Post.negative_comments)
        most_popular_post = analysis.get_top_stats(data, Post.views)

        if (most_popular_post and most_negative_post and most_popular_post) is not None:
            text = f'{hlink("Самый популярный пост", most_popular_post)}\n' \
                   f'{hlink("Самый позитивный пост", most_positive_post)}\n' \
                   f'{hlink("Самый негативный пост", most_negative_post)}\n'
            parse_mode = 'html'
        else:
            text = f'Не удалось собрать статистику группы <b>{data["name"]}</b>\n' \
                   f'Добавьте группу или укажите больший период\n' \
                   f'Вы можете добавить группу написав <code>/parse</code>'
            parse_mode = None

        await message.answer(
            text=text, disable_web_page_preview=True, parse_mode=parse_mode, reply_markup=await main_keyboard()
        )
        await state.finish()
