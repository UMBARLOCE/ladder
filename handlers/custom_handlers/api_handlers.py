from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from states import API_State
from keyboards.reply.kb_reply import *
from database.sq_db import select_api, insert_api, update_api


async def connect_api_(message: types.Message, state: FSMContext) -> None:
    """Ввести API"""
    async with state.proxy() as data:
        data['tg_user_id']: int = message.from_user.id

    await message.answer(
        text=f'Введите API KEY от binance.',
        reply_markup=kb_cancel(),
    )
    await API_State.key.set()


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


async def set_key(message: types.Message, state: FSMContext) -> None:
    """Ввод key."""
    async with state.proxy() as data:
        data['key']: str = message.text
    await message.answer(
        text=f'Введите API SECRET от binance.',
        reply_markup=kb_cancel(),
    )
    await API_State.secret.set()


async def set_secret(message: types.Message, state: FSMContext) -> None:
    """Ввод secret."""
    async with state.proxy() as data:
        data['secret']: int = message.text
    api_data: dict = await state.get_data()  # берём словарик с данными
    await state.finish()  # выход из машины состояний

    #######################################################

    row_from_api = await select_api(api_data['tg_user_id'])

    if row_from_api is None:
        await insert_api(**api_data)
    else:
        await update_api(**api_data)

    await message.answer(
        text=f'Готово.',
        reply_markup=kb_open_order(),
    )


def reg_api_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(connect_api_, commands=['connect_api'], state=None)
    dp.register_message_handler(cancel, commands=['cancel'], state='*')
    dp.register_message_handler(set_key, state=API_State.key)
    dp.register_message_handler(set_secret, state=API_State.secret)
