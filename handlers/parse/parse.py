from loader import dp
from loguru import logger
from aiogram import types

from .parse_state import ParseFormState
from modules.parse_vk_group import VkParser
from aiogram.dispatcher import FSMContext

from keyboards.reply.cancel_state_keyboard import cancel_state_keyboard
from keyboards.reply.menu_keyboard import main_keyboard

from handlers.cancel_state_handler import cancel_handler


@dp.message_handler(commands="parse", state=None)
@dp.message_handler(regexp="^(🔨 Спарсить группу)$")
async def cm_stats(message: types.Message):
    await ParseFormState.name.set()
    await message.reply(
        "⌨ Введите название группы из ссылки\n\n"
        "❗ Это может занять какое-то время, ожидайте...",
        reply_markup=await cancel_state_keyboard(),
    )


@dp.message_handler(state=ParseFormState.name, content_types=["text"])
async def load_name(message: types.Message, state: FSMContext):
    text = message.text.lower()
    parser_vk = VkParser()

    if len(text.split()) == 1:
        group = text.split()[0]

        # Функция парсинга данных из группы
        is_parsing = await parser_vk.run_vk_parser(group)

        if is_parsing:
            logger.info(f"Начался парсинг группы {group}")
            await message.answer(
                text="❕ Данные были успешно собраны", reply_markup=await main_keyboard()
            )
        else:
            await message.answer(
                text=f"❗ Невозможно собрать данные группы <b>{group}</b>",
                reply_markup=await main_keyboard(),
            )
    await state.finish()
