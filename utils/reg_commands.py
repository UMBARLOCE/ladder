from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from handlers.default_handlers import start, help, echo
from handlers.custom_handlers import api_handlers, order_handlers


def reg_handlers(dp: Dispatcher):
    """Регистрация хендлеров."""
    order_handlers.reg_order_handlers(dp)
    api_handlers.reg_api_handlers(dp)
    # start.start_(dp)
    # help.help_(dp)
    dp.register_message_handler(start.start_, commands=['start'])
    dp.register_message_handler(help.help_, commands=['help'])
    dp.register_message_handler(echo.echo)  # эхо последнее


async def set_commands(dp: Dispatcher):
    """Регистрация команд с подсказками в меню бота."""
    all_commands = [
        start.start_,
        api_handlers.connect_api_,
        order_handlers.open_order_,
        help.help_,
    ]

    await dp.bot.set_my_commands([
        BotCommand(command=f"/{func.__name__[:-1]}", description=func.__doc__)
        for func in all_commands
    ])
