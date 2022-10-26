from loader import dp
from loguru import logger
from aiogram import types
from database import Analytics
from .tops_state import TopsFormState
from database.models import Group, Post
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from keyboards.reply.menu_keyboard import main_keyboard
from keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from keyboards.inline.choose_date_period import choice_date_period_keyboards

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
        data["name"] = message.text.lower()

    await message.reply(
        "⌨ Укажите предпочтительный способ подсчёта статистики",
        reply_markup=await choice_date_period_keyboards(),
    )
    await TopsFormState.next()


@dp.callback_query_handler(
    state=TopsFormState.choice_date_period, text_contains="choice"
)
async def choice_data_period(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["choice"] = call.data

        if data["choice"] == "choicePeriod":
            await dp.bot.send_message(
                call.from_user.id,
                "⌨ Введите период подсчёта статистики <b>(в днях)</b>",
                reply_markup=await cancel_state_keyboard(),
            )
        else:
            await dp.bot.send_message(
                call.from_user.id,
                "⌨ Введите дату подсчёта статистики\n\n"
                "❗ Формат: <b>день.месяц.год</b>\n\n"
                "Пример: <b><i>20.10.2022</i></b>",
                reply_markup=await cancel_state_keyboard(),
            )

    await TopsFormState.next()


@dp.message_handler(state=TopsFormState.days, content_types=["text"])
async def load_period(message: types.Message, state: FSMContext):
    analysis = Analytics(group=Group, post=Post)
    async with state.proxy() as data:
        date = await get_correct_date(data["choice"], message.text)

        if date is None:
            await message.reply(
                "❗ Вы ввели некорректное значение, попробуйте ещё раз",
                reply_markup=await main_keyboard(),
            )
            await state.finish()
            return
        else:
            data["date"] = date

        positive_post_list = analysis.get_top_stats(data, Post.positive_comments)
        negative_post_list = analysis.get_top_stats(data, Post.negative_comments)
        popular_post_list = analysis.get_top_stats(data, Post.views)

        if (
            positive_post_list and negative_post_list and popular_post_list
        ) is not None:
            popular_urls = "\n".join(
                f'{hlink(pop_post["number"], pop_post["url"])}'
                for pop_post in popular_post_list
            )
            pos_urls = "\n".join(
                f'{hlink(pos_post["number"], pos_post["url"])}'
                for pos_post in positive_post_list
            )
            neg_urls = "\n".join(
                f'{hlink(neg_post["number"], neg_post["url"])}'
                for neg_post in negative_post_list
            )

            text = (
                f"<b>— Топ постов</b>\n\n"
                f"<b>Топ {len(popular_post_list)} самых популярных поста\n</b>"
                + popular_urls
                + "\n\n"
                + f"<b>Топ {len(positive_post_list)} самых позитивных поста\n</b>"
                + pos_urls
                + "\n\n"
                + f"<b>Топ {len(negative_post_list)} самых негативных поста\n</b>"
                + neg_urls
                + "\n\n"
                f'Период: <b>{popular_post_list[0]["from_date"]} — {popular_post_list[0]["to_date"]}</b>'
            )
            parse_mode = "html"
        else:
            text = (
                f'❗ Не удалось собрать статистику группы <b>{data["name"]}</b>\n\n'
                f"Добавьте группу или укажите период за который данные собраны\n\n"
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


async def get_correct_date(choice: str, message: str) -> None | str:
    if choice == "choicePeriod":
        try:
            if len(message) > 5:
                raise ValueError
            days_datetime = timedelta(days=abs(int(message)))
        except ValueError as err:
            logger.warning(f"В команде /tops указан неверный параметр периода: {err}")
            return None
        return str(datetime.now() - days_datetime)[:-7]
    else:
        try:
            date = datetime.strptime(message, "%d.%m.%Y")
        except (ValueError, OverflowError) as err:
            logger.warning(f"В команде /tops указан неверный параметр даты: {err}")
            return None
        return str(date)
