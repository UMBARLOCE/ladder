from loader import bot
from aiogram import types
from keyboards.reply.kb_reply import kb_open_order


help_text = "Бот отправляет лимитный ордер с заданными параметрами \
на бирже Binance через API. \nТоргуемая монета настраивается на КРОСС-маржу \
с кредитным плечом х12 и начальной маржой $4. \
\nДалее бот отправляет 3 ордера (при наличии средств) с докупкой \
х2 от текущей маржи каждые -100%.\
\nРекомендуемый балланс $110."

async def help_(message: types.Message):
    """Вызвать справку"""
    await bot.send_message(
        chat_id=message.from_user.id,
        text=help_text,
        reply_markup=kb_open_order(),
    )
