from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp

from loguru import logger

from .parse_state import ParseFormState
from modules.parse_vk_group import VkParser

from keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from keyboards.reply.menu_keyboard import main_keyboard
from handlers.cancel_state_handler import cancel_handler


@dp.message_handler(commands='parse', state=None)
@dp.message_handler(regexp='^(🔨 Спарсить группу)$')
async def cm_stats(message: types.Message):
    await ParseFormState.name.set()
    await message.reply('Введите название группы из ссылки', reply_markup=await cancel_state_keyboard())


@dp.message_handler(state=ParseFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    text = message.text
    parser_vk = VkParser()

    if len(text.split()) == 1:
        group = text.split()[0]
        text = f'Парсинг группы <b>{group}</b> закончился'
        logger.info(f'Начался парсинг группы {group}')
        await message.answer('Начался сбор данных, пожалуйста ожидайте...')
        await parser_vk.run_vk_parser(group)
        logger.info(f'Парсинг группы {group} закончен')
    else:
        text = 'Что-то пошло не так. Попробуй ещё раз.'

    await message.answer(text=text, reply_markup=await main_keyboard())
    await state.finish()
