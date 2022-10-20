from aiogram.dispatcher.filters.builtin import CommandHelp

from keyboards.reply.menu_keyboard import main_keyboard

from aiogram import types
from loader import dp


@dp.message_handler(CommandHelp())
@dp.message_handler(regexp="^(❓ Помощь)$")
async def cmd_help(message: types.Message):
    text = (
        "<b>— Что может этот бот?</b>\n\n"
        "<code>/parse</code> - собрать данные\n"
        "<code>/stats</code> - посмотреть статистику\n"
        "<code>/tops</code> - посмотреть топы по постам группы\n"
        "<code>/autoparse</code> - назначить автоматический сбор данных\n\n"
        "<b>— FAQ?</b>\n\n"
        "<b>● Парсинг</b> – это процесс сбора данных с последующей их обработкой и анализом\n"
        "<b>● Парсинг</b> групп собирает 60 последних постов (ВК установил лимит 100)\n"
        "<b>● Авто-парсинг групп</b> собирает 2 раза в день по 60 постов"
    )
    await message.answer(text, reply_markup=await main_keyboard())
