from aiogram import types
from loader import dp
from loguru import logger


@dp.message_handler(commands='start')
async def bot_start(message: types.Message):
    logger.info('Вызван Старт')
    await dp.bot.send_message(
        chat_id=message.chat.id,
        text='<b>Аналитический бот готов к работе</b>'
    )
