import datetime
import functools
import pandas as pd
import pandas_datareader as pdr


def validate_input(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            print('>>>', type(err), err, "\nНекорректные данные, повторите ввод\n")
            return None
        return result               
    return wrapped


@validate_input
def get_finance(ticker, mode):
    if mode == 'train':
        data = pdr.get_data_yahoo(ticker, 
                start=datetime.datetime(2016, 1, 1), 
                end=datetime.datetime(2020, 12, 31))
    
    elif mode == 'final_test':
        data = pdr.get_data_yahoo(ticker, 
            start=datetime.datetime(2021, 1, 1), 
            end=datetime.datetime(2021, 8, 13))

    return data.values


def param_input(param_list):
    param_tuple = None

    @validate_input
    def idx_input(param_list):
        if(param_list):
            idx = int(input('Введите номер параметров: '))
            return param_list[idx-1]
        else:
            print('Для данного иснтрумента в базе еще нет параметров\nБудет выполнено обучение\n') 
            return -1

    @validate_input
    def user_input():
        return tuple(map(int, 
                input('Введите параметры через пробел (koef_buy, koef_sell, day_steps): ').split()))

    cmd = input('Введите \'p\' для выбора параметров или \'u\' для пользовательского ввода: ')
    while not param_tuple:
        param_tuple = user_input() if cmd == 'u' else idx_input(param_list)
    
    return param_tuple


def choose_param(param_list):
    for idx, param in enumerate(param_list):
        print('{}: {}'.format(idx+1, param))

    return param_input(param_list)


def check_data(data):
    try: len(data)
    except Exception: return False
    else: return True