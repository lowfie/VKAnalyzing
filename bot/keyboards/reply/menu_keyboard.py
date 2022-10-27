from aiogram import types


async def main_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("🔨 Спарсить группу"),
        types.KeyboardButton("🛠 Авто-парсинг группы"),
    )
    keyboard.add(types.KeyboardButton("📊 Статистика"), types.KeyboardButton("📈 Анализ постов"))
    keyboard.add(types.KeyboardButton("❓ Помощь"))
    return keyboard
