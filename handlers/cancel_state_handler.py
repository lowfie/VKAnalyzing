from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.reply.menu_keyboard import main_keyboard

from loader import dp

from loguru import logger


@dp.message_handler(state='*', commands=['cancel', 'отмена'])
@dp.message_handler(Text(equals=['cancel', 'отмена'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info(f'Отмена состояния: {current_state}')
    await state.finish()
    await message.reply('Вы перешли в главное меню', reply_markup=await main_keyboard())
