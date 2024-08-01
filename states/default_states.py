from aiogram.fsm.state import StatesGroup, State


class MovieState(StatesGroup):
    code_movie = State()
    title = State()


class AdminState(StatesGroup):
    password = State()
