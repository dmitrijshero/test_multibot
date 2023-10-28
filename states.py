from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    Normal = State()
    InputToken = State()
