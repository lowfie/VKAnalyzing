from aiogram.dispatcher.filters.state import State, StatesGroup


class TopsFormState(StatesGroup):
    name = State()
    days = State()
