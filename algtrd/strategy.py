import numpy as np
from tqdm import tqdm


def momentum(data, balance, koef_buy, koef_sell, day_steps):
    fiat_balance, ticker_balance = balance, 0
    max_balance = min_balance = balance

    avg_buy_price = 0
    ticker_price = 0

    for day in range(day_steps, len(data)):
        cur_balance = fiat_balance + ticker_balance * float(data[day][2])
        max_balance = max(cur_balance, max_balance)
        min_balance = min(cur_balance, min_balance)

        ticker_price = float(data[day][2])
        diff_n_day = float(data[day][2] - data[day-day_steps][2]) # today open price - nday before open price
        proc = abs(diff_n_day / float(data[day-day_steps][2]))

        otype = 'buy' if diff_n_day > 0 else 'sell'
        fiat_balance, ticker_balance, avg_buy_price = \
                operation(otype, proc, fiat_balance, ticker_balance,
                    ticker_price, avg_buy_price, koef_buy, koef_sell)

    return cur_balance, min_balance, max_balance


def operation(otype, proc, fiat_balance, ticker_balance, ticker_price,
        avg_buy_price, koef_buy, koef_sell):

    if otype == 'sell' and ticker_price > avg_buy_price:
        amount_trade = min(proc * koef_sell, 100) * ticker_balance / 100
        mode = 1
    elif otype == 'buy':
        amount_trade = fiat_balance * min(proc * koef_buy, 10) / 100
        mode = -1
    else: return fiat_balance, ticker_balance, avg_buy_price

    fiat_balance = fiat_balance - amount_trade \
            if mode == -1  else fiat_balance + amount_trade * ticker_price

    ticker_balance = ticker_balance + amount_trade / ticker_price \
            if mode == -1 else ticker_balance - amount_trade

    avg_buy_price = (avg_buy_price * (ticker_balance + mode * amount_trade) + \
            mode * amount_trade * ticker_price) / ticker_balance \
            if ticker_balance else 0

    return fiat_balance, ticker_balance, avg_buy_price


def koef_validation(data, balance):
    max_balance = 0
    max_day, max_koef_buy, max_koef_sell = 10, 100, 100
    min_day, min_koef_buy, min_koef_sell = 1, 1, 1
    best_koef = [0]*3

    total_iter = (max_day - min_day) * (max_koef_buy - min_koef_buy) * \
                (max_koef_sell - min_koef_sell)

    progress = tqdm(total=total_iter, desc='Progress')

    for koef_buy in range(min_koef_buy, max_koef_buy+1):
        for koef_sell in range(min_koef_sell, max_koef_sell+1):
            for day_steps in range(min_day, max_day+1):
                    result, minb, maxb = momentum(data, balance, koef_buy, koef_sell, day_steps)
                    if result > max_balance:
                        max_balance = result
                        best_koef[0], best_koef[1], best_koef[2] = koef_buy, koef_sell, day_steps

                    progress.update()
    progress.close()
    return tuple(best_koef)


def sharp_koef(data, result, balance, const_profit):
    res_profit = result/balance * 100 - 100 # in %
    return (res_profit - const_profit) / np.nanstd(data, axis=0)[2]


def profit_drawdown_koef(result, balance, min_balance):
    profit = result/balance * 100 - 100 # in %
    drawdown = 100 - min_balance / balance * 100
    return profit / drawdown
