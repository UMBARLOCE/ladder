from requests import request


def request_tick_and_step_for_symbol(symbol) -> tuple[int, int]:
    base_url: str = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    exchange_info: dict = request('GET', base_url).json()
    filters_symbol: list[dict] = [
        i['filters']
        for i in exchange_info['symbols']
        if i['symbol'] == symbol
    ][0]
    
    tick_size: str = filters_symbol[0]['tickSize']
    tick_round: int = 0 if float(tick_size) >= 1 \
        else len(tick_size.split('.')[1].split('1')[0]) + 1
    
    step_size: str = filters_symbol[1]['stepSize']
    step_round: int = 0 if float(step_size) >= 1 \
        else len(step_size.split('.')[1].split('1')[0]) + 1
    
    return tick_round, step_round


def get_ladder_usdt(symbol: str, side: str, entry_price: float, **kwargs: dict) -> dict:
    tick, step = request_tick_and_step_for_symbol(symbol)
    leverage = 12
    ladder = {}
    coeff = 0.923 if side == 'BUY' else 1.091
    full_usdt = cur_usdt = 4
    cur_quantity = full_quantity = round(
        int(cur_usdt * leverage / entry_price * 10 ** step) / 10 ** step,
        step,
    )
    real_cur_usdt = real_full_usdt = round(entry_price * cur_quantity / leverage, 2)
    ladder['0'] = {'quantity': cur_quantity, 'price': entry_price}

    for i in range(1, 4):
        cur_usdt = full_usdt * 2
        liq_price = round(entry_price * coeff, tick)
        cur_quantity = round(int(cur_usdt * leverage / liq_price * 10 ** step) / 10 ** step, step)
        real_cur_usdt = round(liq_price * cur_quantity / leverage, 2)
        real_full_usdt = round(real_full_usdt + real_cur_usdt, 2)
        entry_price = round(
            (entry_price * full_quantity + liq_price * cur_quantity) / (full_quantity + cur_quantity),
            tick,
        )
        full_quantity = round(full_quantity + cur_quantity, step)
        full_usdt += cur_usdt
        ladder[str(i)] = {'quantity': cur_quantity, 'price': liq_price}
    print(ladder)
    return ladder


def get_ladder_coin(symbol: str, side: str, entry_price: float, **kwargs: dict) -> dict:
    tick, step = request_tick_and_step_for_symbol(symbol)
    leverage = 12
    ladder = {}
    coeff = 0.923 if side == 'BUY' else 1.091
    cur_usdt = 4
    full_quantity = round(
        int(cur_usdt * leverage / entry_price * 10 ** step) / 10 ** step,
        step,
    )
    full_usdt = round(entry_price * full_quantity / leverage, 2)
    ladder['0'] = {'quantity': full_quantity, 'price': entry_price}

    for i in range(1, 4):
        cur_quantity = full_quantity * 2
        liq_price = round(entry_price * coeff, tick)
        ladder[str(i)] = {'quantity': cur_quantity, 'price': liq_price}
        entry_price = round(
            (entry_price * full_quantity + liq_price * cur_quantity) / (full_quantity + cur_quantity),
            tick,
        )
        cur_usdt = round(liq_price * cur_quantity / leverage, 2)
        full_quantity = round(full_quantity + cur_quantity, step)
        full_usdt = round(full_usdt + cur_usdt, 2)
    
    return ladder


if __name__ == "__main__":
    get_ladder_usdt('BTCUSDT', 'SELL', 29140)
