from aiogram.types import ReplyKeyboardMarkup


def kb_open_order() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row('/open_order')
    return kb


def kb_buy_sell() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('BUY', 'SELL')
    kb.row('/cancel')
    return kb


def kb_btc_eth() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('BTCUSDT', 'ETHUSDT')
    kb.row('/cancel')
    return kb


def kb_yes_no() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('ДА', 'НЕТ')
    return kb


def kb_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('/cancel')
    return kb