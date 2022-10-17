from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp

from loguru import logger

from .parse_state import ParseFormState
from modules.parse_vk_group import VkParser

from handlers.cancel_state_handler import cancel_handler


@dp.message_handler(commands='parse', state=None)
async def cm_stats(message: types.Message):
    await ParseFormState.name.set()
    await message.reply('Введите название группы из ссылки')


@dp.message_handler(state=ParseFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    text = message.text
    parser_vk = VkParser()

    if len(text.split()) == 1:
        group = text.split()[0]
        text = f'Парсинг группы <b>{group}</b> закончился'
        logger.info(f'Начался парсинг группы {group}')
        await parser_vk.run_vk_parser(group)
        logger.info(f'Парсинг группы {group} закончен')
    else:
        text = 'Что-то пошло не так. Попробуй ещё раз.'

    await message.answer(text=text)
    await state.finish()
