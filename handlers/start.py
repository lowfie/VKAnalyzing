from aiogram import types
from loader import dp


@dp.message_handler(commands='start')
async def bot_start(message: types.Message):
    await dp.bot.send_message(
        chat_id=message.chat.id,
        text='Аналитический бот готов к работе'
    )
