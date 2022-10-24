from aiogram import types


async def choice_date_period_keyboards():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("За период", callback_data="choicePeriod"),
        types.InlineKeyboardButton("По дате", callback_data="choiceDate"),
    )
    return keyboard
