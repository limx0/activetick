
from io import BytesIO
import pandas as pd
from activetick.util import activetick_request, get_activetick_data, option_feedcode_to_detail, dt_to_str


def get_option_chain(underlying, **kwargs):
    data = activetick_request('optionChain', {'symbol': underlying}, **kwargs)
    df = pd.read_csv(BytesIO(data), names=['Feedcode'])
    return df['Feedcode'].apply(option_feedcode_to_detail)


def request_quote_ticks(symbol, date_from, date_to, **kwargs):
    end_point = 'tickData'
    header = ['RECORD', 'TIMESTAMP', 'BID_PRICE', 'ASK_PRICE', 'BID_SIZE',
              'ASK_SIZE', 'BID_EXCHANGE', 'ASK_EXCHANGE', 'CONDITION']
    args = {
        'symbol': symbol,
        'trades': 0,
        'quotes': 1,
        'beginTime': dt_to_str(date_from),
        'endTime': dt_to_str(date_to)
    }
    return get_activetick_data(end_point, args, header, symbol, **kwargs)


def request_trade_ticks(symbol, date_from, date_to, **kwargs):
    end_point = 'tickData'
    header = ['RECORD', 'TIMESTAMP', 'LAST_PRICE', 'LAST_SIZE', 'LAST_EXCHANGE',
              'CONDITION1', 'CONDITION2', 'CONDITION3', 'CONDITION4']
    args = {
        'symbol': symbol,
        'trades': 1,
        'quotes': 0,
        'beginTime': dt_to_str(date_from),
        'endTime': dt_to_str(date_to)
    }

    return get_activetick_data(end_point, args, header, symbol, **kwargs)


def request_bar_data(symbol, date_from, date_to, bar_size=1, **kwargs):
    end_point = 'barData'
    header = ['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
    args = {
        'symbol': symbol,
        'historyType': 1,
        'intradayMinutes': bar_size,
        'beginTime': dt_to_str(date_from),
        'endTime': dt_to_str(date_to)
    }

    return get_activetick_data(end_point, args, header, symbol, **kwargs)
