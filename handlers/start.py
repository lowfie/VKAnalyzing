from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.reply.main_keyboards import main_keyboard

from loader import dp
from loguru import logger


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    logger.info('Вызван Старт')
    await message.answer(text='<b>Аналитический бот готов к работе</b>', reply_markup=await main_keyboard())
