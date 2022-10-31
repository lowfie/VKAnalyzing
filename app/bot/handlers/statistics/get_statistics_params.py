from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from app.loader import dp

from app.analytics.statistics import Analytics
from app.bot.keyboards.inline.choose_date_period import choice_date_period_keyboards
from app.bot.keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from app.bot.keyboards.reply.menu_keyboard import main_keyboard
from app.database.models import Group, Post
from .statistics_state import StatisticsFormState


async def cm_stats(message: types.Message):
    await StatisticsFormState.name.set()
    await message.reply(
        "⌨ Введите название группы из ссылки",
        reply_markup=await cancel_state_keyboard(),
    )


async def stats_load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text.lower()

    await message.reply(
        "⌨ Укажите предпочтительный способ подсчёта статистики",
        reply_markup=await choice_date_period_keyboards(),
    )
    await StatisticsFormState.next()


async def stats_choice_data_period(call: types.CallbackQuery, state: FSMContext):
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

    await StatisticsFormState.next()


async def stats_load_period(message: types.Message, state: FSMContext):
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

        try:
            statistics = analysis.get_statistic(data)
        except TypeError as err:
            logger.warning(f"Невозможно собрать статистику за эту дату: {err}")
            await message.reply(
                "❗ Невозможно собрать статистику за эту дату",
                reply_markup=await main_keyboard(),
            )
            await state.finish()
            return

        if statistics is not None and statistics["count_post"] > 0:
            text = (
                f"<b>— Статистика</b>\n\n"
                f'<b>{statistics["group_name"]}: {statistics["group_members"]}</b>\n\n'
                f'Собрано <b>{statistics["count_post"]}</b> поста\n'
                f'Посты с фото/видео: <b>{statistics["posts_with_photo"]}</b>\n'
                f'Лайки: <b>{statistics["likes"]}</b>\n'
                f'Комментарии: <b>{statistics["comments"]}</b>\n'
                f'Репосты: <b>{statistics["reposts"]}</b>\n'
                f'Всего просмотров: <b>{statistics["views"]}</b>\n\n'
                f'Вовлеченность: <b>{statistics["er_users"]}</b> пользователей <b>(+{statistics["engagement_rate"]}%)</b>\n\n'
                f'Период: <b>{statistics["from_date"]} — {statistics["to_date"]}</b>'
            )
        elif statistics is not None and statistics["count_post"] == 0:
            text = f"❗ Невозможно собрать статистику за этот период\n\n" f"Попробуйте указать период больше"
        else:
            text = (
                f'❗ Группы <b>{data["name"]}</b> нету в базе\n\n' f"Вы можете её добавить написать <code>/parse</code>"
            )

        await message.answer(text=text, reply_markup=await main_keyboard())
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
