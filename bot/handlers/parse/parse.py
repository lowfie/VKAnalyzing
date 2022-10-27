from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from bot.keyboards.reply.menu_keyboard import main_keyboard
from libs.vk_parser import VkParser
from .parse_state import ParseFormState


async def cm_parse(message: types.Message):
    await ParseFormState.name.set()
    await message.reply(
        "⌨ Введите название группы из ссылки\n",
        reply_markup=await cancel_state_keyboard(),
    )


async def parse_load_name(message: types.Message, state: FSMContext):
    text = message.text.lower()
    parser_vk = VkParser()

    if len(text.split()) == 1:
        group = text.split()[0]

        await message.answer("❗ Это может занять какое-то время, ожидайте...")

        # Функция парсинга данных из группы
        is_parsing = await parser_vk.run_vk_parser(group)

        if is_parsing:
            logger.info(f"Начался парсинг группы {group}")
            await message.answer(text="❕ Данные были успешно собраны", reply_markup=await main_keyboard())
        else:
            await message.answer(
                text=f"❗ Невозможно собрать данные группы <b>{group}</b>",
                reply_markup=await main_keyboard(),
            )
    await state.finish()
