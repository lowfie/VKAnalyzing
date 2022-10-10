from aiogram.dispatcher.filters.state import State, StatesGroup


class StatisticsFormState(StatesGroup):
    name = State()
    days = State()
