from aiogram.dispatcher.filters.builtin import CommandHelp

from keyboards.reply.menu_keyboard import main_keyboard

from aiogram import types
from loader import dp


@dp.message_handler(CommandHelp())
async def cmd_help(message: types.Message):
    text = '<b>- Что может этот бот?</b>\n\n' \
           '<code>/parse "группа"</code> - собрать данные группы\n' \
           '<code>/stats</code> - посмотреть статистику группы за период\n' \
           '<code>/tops</code> - посмотреть топы по постам группы за период\n' \
           '<code>/autoparse "группа"</code> - назначить автоматический парсинг'
    await message.answer(text, reply_markup=await main_keyboard())
