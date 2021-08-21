def momentum(data, balance, koef_buy, koef_sell, day_steps):
    usd_balance = balance
    eth_balance = 0

    avg_buy_price = 0
    eth_price = 0

    for day in range(day_steps, len(data)):
        cur_balance = usd_balance + eth_balance * data[day][2]
        eth_price = data[day][2]
        diff_n_day = sum(data[day-day_steps:day])[6]
        if diff_n_day > 0:
            proc = diff_n_day / data[day-day_steps][2]
            amount_buy = usd_balance * min(proc * koef_buy, 10) / 100
            if usd_balance - amount_buy > 0:
                usd_balance -= amount_buy
                eth_amount = amount_buy / eth_price
                eth_balance += eth_amount

                avg_buy_price = (avg_buy_price * (eth_balance - eth_amount) + eth_amount * eth_price) / eth_balance

        else:
            proc = -(diff_n_day / data[day-day_steps][2])
            if eth_price > avg_buy_price:
                amount_cell = min(proc * koef_sell, 100) * eth_balance / 100
                usd_balance += amount_cell * eth_price
                eth_balance -= amount_cell
                if eth_balance != 0:
                    avg_buy_price = (avg_buy_price * (eth_balance + amount_cell) - amount_cell * eth_price) / eth_balance
                else:
                    avg_buy_price = 0

    return cur_balance   


def koef_validation(data, balance):
    max_balance = 0

    best_koef = [0]*3
    for day_steps in range(1, 10):
        for koef_buy in range(1, 100):
            for koef_sell in range(1, 100):
                result = momentum(data, balance, koef_buy, koef_sell, day_steps)
                if result > max_balance:
                    max_balance = result
                    best_koef[0], best_koef[1], best_koef[2] = koef_buy, koef_sell, day_steps
    
    return best_koef
