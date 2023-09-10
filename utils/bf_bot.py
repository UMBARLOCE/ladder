from binance.um_futures import UMFutures
import asyncio


async def set_ladder_orders(symbol, side, key, secret, **kwargs) -> None:
    """Установка плеча, типа маржи, ордеров."""
    bf_bot = UMFutures(key=key, secret=secret)
    
    try:
        bf_bot.change_leverage(symbol=symbol, leverage=12)
        bf_bot.change_margin_type(symbol=symbol, marginType='CROSSED')
    except:
        pass

    for i in range(4):
        try:
            bf_bot.new_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=kwargs[str(i)]['quantity'],
                price=kwargs[str(i)]['price'],
                timeInForce='GTC',
            )
            await asyncio.sleep(5)
        except:
            return
