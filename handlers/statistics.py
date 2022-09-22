from aiogram import types
from loader import dp

from datetime import datetime, timedelta

from database import PostService
from database.models import Post


@dp.message_handler(commands='stats')
async def get_stats(message: types.Message):
    post_service = PostService(Post)

    if len(message.text.split()) == 2:
        name = message.text.split()[1]
        print(name)
    else:
        name = ''

    data = {
        'name': name.strip(),
        'date': datetime.now() - timedelta(weeks=1000),
    }

    statistics = post_service.select(data)

    await dp.bot.send_message(
        chat_id=message.chat.id,
        text=f'Всего постов: {statistics["count_post"]}\n'
             f'Посты с фото/видео: {statistics["posts_with_photo"]}\n'
             f'Лайки: {statistics["likes"]}\n'
             f'Комментарии: {statistics["comments"]}'
    )
