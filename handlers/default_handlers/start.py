from loader import bot
from aiogram import types
from keyboards.reply.kb_reply import kb_open_order


start_text = "Для того, чтобы пользоваться ботом, необходимо подключить \
API-ключи для фьючерсной торговли на Binance командой /connect_api"


async def start_(message: types.Message):
    """Запустить бота"""
    await bot.send_message(
        message.from_user.id,
        start_text,
        reply_markup=kb_open_order(),
    )
