from aiogram import types
from loguru import logger

from app.bot.keyboards.reply.menu_keyboard import main_keyboard


async def bot_start(message: types.Message):
    logger.info("Вызван Старт")
    await message.answer(
        text="<b>Аналитический бот готов к работе</b>",
        reply_markup=await main_keyboard(),
    )
