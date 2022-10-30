from aiogram.dispatcher.filters.state import State, StatesGroup


class StatisticsFormState(StatesGroup):
    name = State()
    choice_date_period = State()
    days = State()
