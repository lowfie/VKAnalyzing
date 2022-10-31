from aiogram.dispatcher.filters.state import State, StatesGroup


class ParseFormState(StatesGroup):
    name = State()
