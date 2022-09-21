from aiogram import types
from loader import dp

from modules.parse_vk_group import VkParser


@dp.message_handler(commands='group')
async def parser_metadata_group(message: types.Message):
    text = message.text
    parser_vk = VkParser()

    if len(text.split()) == 2:
        group = text.split()[1]
        await parser_vk.get_posts(group)
        await parser_vk.get_wall_comments()
    else:
        group = 'Попробуй ещё раз.'

    await dp.bot.send_message(
        chat_id=message.chat.id,
        text='Парсинг группы {0} закончился.'.format(group)
    )
