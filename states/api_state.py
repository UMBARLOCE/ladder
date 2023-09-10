from aiogram.dispatcher.filters.state import State, StatesGroup


class API_State(StatesGroup):
    tg_user_id = State()
    key = State()
    secret = State()
