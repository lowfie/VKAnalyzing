from aiogram.dispatcher.filters.state import State, StatesGroup


class AutoparseFormState(StatesGroup):
    name = State()
