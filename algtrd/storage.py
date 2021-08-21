import argparse
import json


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker')
    parser.add_argument('balance', help='Объем средств инвестирования',
            nargs='?', default=1000)
    parser.add_argument('-upd', '--update', help='forced update parameters',  
            action="store_true")
    return parser.parse_args()


def read_data(storage_name):
    with open(storage_name, 'r') as file:
        raw_data = file.read()
        if raw_data: return json.loads(raw_data)
        else: return {}


def write_data(storage_name, data):
    with open(storage_name, 'w') as file:
        file.write(json.dumps(data))


def put(storage_name, ticker, new_param):
    param = read_data(storage_name)
    param[ticker] = param.get(ticker, list())
    if list(new_param) not in param[ticker]:
        param[ticker].append(new_param)
    write_data(storage_name, param)


def get(storage_name, ticker):
    param = read_data(storage_name)
    return param.get(ticker, list())


def get_parameters(storage_name):
    args = parse()
    return args.ticker, args.balance, get(storage_name, args.ticker), args.update
