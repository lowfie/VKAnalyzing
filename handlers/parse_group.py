from aiogram import types
from loader import dp

from modules.parse_vk_group import VkParser


@dp.message_handler(commands='parse')
async def parser_metadata_group(message: types.Message):
    text = message.text
    parser_vk = VkParser()

    if len(text.split()) == 2:
        group = text.split()[1]
        text = f'Парсинг группы {group} закончился'
        await parser_vk.run_vk_parser(group)
    else:
        text = 'Попробуй ещё раз.'

    await dp.bot.send_message(
        chat_id=message.chat.id,
        text=text
    )
