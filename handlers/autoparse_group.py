from aiogram import types
from loader import dp

from database.services import GroupService
from database.models import Group


@dp.message_handler(commands='autoparse')
async def parser_metadata_group(message: types.Message):
    group_service = GroupService(Group)

    text = message.text

    if len(text.split()) == 2:
        group = text.split()[1]
        autoparsing_status = group_service.set_autoparsing_group(group)
        if autoparsing_status is None:
            text = 'Нельзя изменить статус не добавленной группы'
        else:
            switch = '<b>включен</b>' if autoparsing_status else '<b>выключен</b>'
            text = f'Авто-парсинг данных {switch} у группы: <b>{group}</b>'
    else:
        text = 'Что-то пошло не так. Попробуй ещё раз'

    await dp.bot.send_message(
        chat_id=message.chat.id,
        text=text
    )
