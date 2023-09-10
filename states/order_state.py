from aiogram.dispatcher.filters.state import State, StatesGroup


class Order_State(StatesGroup):
    side = State()
    symbol = State()
    price = State()
    key = State()
    secret = State()
    confirm = State()
