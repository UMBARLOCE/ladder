from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from states import Order_State
from keyboards.reply.kb_reply import *
from utils.ladder import get_ladder_usdt
from utils.bf_bot import set_ladder_orders
from database.sq_db import select_api


async def open_order_(message: types.Message, state: FSMContext) -> None:
    """Открыть сделку"""
    row_from_api = await select_api(message.from_user.id)

    if row_from_api is None:
        await message.reply(
            text=f'Вы не подключили API.',
            reply_markup=kb_open_order(),
        )
        await state.finish()
        return

    async with state.proxy() as data:
        data['tg_user_id']: int = row_from_api[0]
        data['key']: str = row_from_api[1]
        data['secret']: str = row_from_api[2]
        await message.answer(
            text=f'Выбери направление.',
            reply_markup=kb_buy_sell(),
        )
        await Order_State.side.set()


async def cancel(message: types.Message, state: FSMContext) -> None:
    """Отмена состояния машины состояния."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply(
        text=f'Отмена',
        reply_markup=kb_open_order(),
    )
    await state.finish()


async def set_side(message: types.Message, state: FSMContext) -> None:
    """Ловим направление сделки."""
    if message.text == 'BUY' or message.text == 'SELL':
        async with state.proxy() as data:
            data['side']: str = message.text
        await message.reply(
            text='Какая монета?',
            reply_markup=kb_btc_eth(),
        )
        await Order_State.symbol.set()
    else:
        await message.reply(
            text='Только 2 варианта!!!',
            reply_markup=kb_buy_sell(),
        )


async def set_symbol(message: types.Message, state: FSMContext) -> None:
    """Ловим название монеты."""
    symbol = message.text.upper()

    if not symbol.endswith('USDT'):
        symbol += 'USDT'

    async with state.proxy() as data:
        data['symbol']: str = symbol

    await Order_State.price.set()
    await message.reply(
        text=f'Введите цену.',
        # reply_markup=,
    )


async def set_price(message: types.Message, state: FSMContext) -> None:
    """Ловим цену входа."""
    try:
        price = float(message.text)
        async with state.proxy() as data:
            data['entry_price']: float = price
        await message.reply(
            text=f'Отправляем ордер?',
            reply_markup=kb_yes_no(),
        )
        await Order_State.confirm.set()
    except:
        await message.reply(
            text='Введите цену. Дробную часть через точку.',
            # reply_markup=kb_3_6_9(),
        )


async def confirm_order(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний, запрос на отправку и отправка ордеров."""
    if message.text != 'ДА':
        await state.finish()  # выход из машины состояний
        await message.reply(
            text='Отмена',
            reply_markup=kb_open_order(),
        )
        return

    async with state.proxy() as data:
        data['check']: bool = True
    await message.reply(
        text=f'Проверяйте.',
        reply_markup=kb_open_order(),
    )
    order_data: dict = await state.get_data()  # берём словарик с данными
    await state.finish()  # выход из машины состояний

    try:
        ladder_data: dict = get_ladder_usdt(**order_data)
    except:
        return
    
    ladder_data |= order_data
    await set_ladder_orders(**ladder_data)

    return


def reg_order_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(open_order_, commands=['open_order'], state=None)
    dp.register_message_handler(cancel, commands=['cancel'], state='*')
    dp.register_message_handler(set_side, state=Order_State.side)
    dp.register_message_handler(set_symbol, state=Order_State.symbol)
    dp.register_message_handler(set_price, state=Order_State.price)
    dp.register_message_handler(confirm_order, state=Order_State.confirm)