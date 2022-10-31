from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from app.bot.keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from app.bot.keyboards.reply.menu_keyboard import main_keyboard
from app.database.models import Group
from app.database.services import GroupService
from .autoparse_state import AutoparseFormState


async def cm_autoparse(message: types.Message):
    await AutoparseFormState.name.set()
    await message.reply(
        "⌨ Введите название группы из ссылки",
        reply_markup=await cancel_state_keyboard(),
    )


async def autoparse_load_name(message: types.Message, state: FSMContext):
    logger.info("Вызван Авто-парсинг")

    text = message.text.lower()

    if len(text.split()) == 1:
        group = text.split()[0]
        group_service = GroupService(Group)
        autoparsing_status = group_service.set_autoparsing_group(group)

        if autoparsing_status is None:
            text = "❗ Нельзя изменить статус не добавленной группы"
        else:
            switch = "<b>включен</b>" if autoparsing_status else "<b>выключен</b>"
            text = f"❕ Авто-парсинг данных {switch} у группы: <b>{group}</b>"
    else:
        text = "❗ Что-то пошло не так. Попробуй ещё раз"

    await message.answer(text=text, reply_markup=await main_keyboard())
    await state.finish()
