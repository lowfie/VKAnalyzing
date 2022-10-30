from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from app.bot.keyboards.reply.menu_keyboard import main_keyboard


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info(f"Отмена состояния: {current_state}")
    await state.finish()
    await message.reply("Вы перешли в главное меню", reply_markup=await main_keyboard())
