from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp

from .autoparse_state import AutoparseFormState

from loguru import logger

from database.services import GroupService
from database.models import Group

from handlers.cancel_state_handler import cancel_handler


@dp.message_handler(commands='autoparse', state=None)
async def cm_stats(message: types.Message):
    await AutoparseFormState.name.set()
    await message.reply('Введите название группы из ссылки')


@dp.message_handler(state=AutoparseFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    logger.info("Вызван Авто-парсинг")

    text = message.text

    if len(text.split()) == 1:
        group = text.split()[0]
        group_service = GroupService(Group)
        autoparsing_status = group_service.set_autoparsing_group(group)

        if autoparsing_status is None:
            text = 'Нельзя изменить статус не добавленной группы'
        else:
            switch = '<b>включен</b>' if autoparsing_status else '<b>выключен</b>'
            text = f'Авто-парсинг данных {switch} у группы: <b>{group}</b>'
    else:
        text = 'Что-то пошло не так. Попробуй ещё раз'

    await message.answer(text=text)
    await state.finish()
