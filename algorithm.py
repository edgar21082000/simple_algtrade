import algtrd

if __name__ == '__main__':
    ticker, balance, param_list, upd_status = algtrd.get_parameters(algtrd.storage_name)
    #print(ticker, balance, param_list, upd_status)

    if not upd_status: param_tuple = algtrd.choose_param(param_list)
    else: print('Будет выполнено обучение параметров:\n')
    
    if upd_status or not param_tuple or param_tuple == -1:
        data_train = algtrd.get_finance(ticker, 'train')
        if not algtrd.check_data(data_train):
            exit("Wrong ticker")
        param_tuple = algtrd.koef_validation(data_train, balance)
        algtrd.put(algtrd.storage_name, ticker, param_tuple)

    data_final = algtrd.get_finance(ticker, 'final_test')
    if not algtrd.check_data(data_final):
        exit('Wrong ticker')
    result, min_balance, max_balance = algtrd.momentum(data_final, balance, 
            param_tuple[0], param_tuple[1], param_tuple[2])
    print()
    print('result: {0: .3f}\nmin: {1: .3f}\nmax: {2: .3f}'.format(
            result, min_balance, max_balance))
    
    const_profit = 0.0659 # USA 1 year bond
    print('sharp: {0: .3f}\nprof/drdwn: {1: .3f}'.format(
            algtrd.sharp_koef(data_final, result, balance, const_profit),
            algtrd.profit_drawdown_koef(result, balance, min_balance)
    ))
