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


@dp.message_handler(commands="tops", state=None)
@dp.message_handler(regexp="^(📈 Анализ постов)$")
async def cm_tops(message: types.Message):
    await TopsFormState.name.set()
    await message.reply(
        "⌨ Введите название группы из ссылки",
        reply_markup=await cancel_state_keyboard(),
    )


@dp.message_handler(state=TopsFormState.name, content_types=["text"])
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.reply(
        "⌨ Введите период подсчёта топов (в днях)",
        reply_markup=await cancel_state_keyboard(),
    )
    await TopsFormState.next()


@dp.message_handler(state=TopsFormState.days, content_types=["text"])
async def load_period(message: types.Message, state: FSMContext):
    analysis = Analytics(group=Group, post=Post)
    async with state.proxy() as data:
        try:
            days = timedelta(days=abs(int(message.text)))
        except (OverflowError, ValueError) as err:
            logger.warning(f"В команде /tops указан неверный параметр периода: {err}")
            await message.reply(
                "❌ Вы ввели некорректное значение, поэтому будет использоваться день, как период"
            )
            days = timedelta(days=1)

        data["date"] = str(datetime.now() - days)[:-7]

        positive_post_list = analysis.get_top_stats(data, Post.positive_comments)
        negative_post_list = analysis.get_top_stats(data, Post.negative_comments)
        popular_post_list = analysis.get_top_stats(data, Post.views)

        if (positive_post_list and negative_post_list and popular_post_list) is not None:
            popular_urls = '\n'.join(f'{hlink(pop_post["number"], pop_post["url"])}' for pop_post in popular_post_list)
            pos_urls = '\n'.join(f'{hlink(pos_post["number"], pos_post["url"])}' for pos_post in positive_post_list)
            neg_urls = '\n'.join(f'{hlink(neg_post["number"], neg_post["url"])}' for neg_post in negative_post_list)

            text = (
                f'<b>— Топ постов</b>\n\n'
                f'<b>Топ {len(popular_post_list)} самых популярных поста\n</b>' + popular_urls + '\n\n' +
                f'<b>Топ {len(positive_post_list)} самых позитивных поста\n</b>' + pos_urls + '\n\n' +
                f'<b>Топ {len(negative_post_list)} самых негативных поста\n</b>' + neg_urls + '\n\n'

                f'Период: <b>{str(datetime.now())[:-7]} — {popular_post_list[0]["to_date"]}</b>'
            )
            parse_mode = "html"
        else:
            text = (
                f'❌ Не удалось собрать статистику группы <b>{data["name"]}</b>\n\n'
                f"Добавьте группу или укажите больший период\n"
                f"Вы можете добавить группу написав <code>/parse</code>"
            )
            parse_mode = None

        await message.answer(
            text=text,
            disable_web_page_preview=True,
            parse_mode=parse_mode,
            reply_markup=await main_keyboard(),
        )
        await state.finish()
