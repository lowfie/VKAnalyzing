from aiogram import executor
from loader import dp
import handlers

from database.models import create_tables


async def on_startup(dispatcher):
    print('Бот запущен')
    create_tables()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
