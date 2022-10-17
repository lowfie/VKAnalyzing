from aiogram import types


async def cancel_state_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Отмена'))
    return keyboard
