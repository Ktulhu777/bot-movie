from aiogram.fsm.state import StatesGroup, State


class Movie(StatesGroup):
    code_movie = State()
    title = State()
