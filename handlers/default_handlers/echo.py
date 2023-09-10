from loader import bot
from aiogram import types
from keyboards.reply.kb_reply import kb_open_order


async def echo(message: types.Message):
    """Удаляет лишнюю переписку."""
    await message.delete()
