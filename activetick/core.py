
from activetick.request import get_activetick_data
from activetick.util import dt_to_str


def get_option_chain(symbol, **kwargs):
    end_point = 'optionChain'
    header = ['FEEDCODE']
    args = {'symbol': symbol}
    kwargs['index_col'] = None
    return get_activetick_data(end_point, args, header, symbol, **kwargs)


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
    return get_activetick_data(end_point, args, header, symbol, ignore_cols=['RECORD'], **kwargs)


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

    return get_activetick_data(end_point, args, header, symbol, ignore_cols=['RECORD'], **kwargs)


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

    return get_activetick_data(end_point, args, header, symbol, ignore_cols=['RECORD'], **kwargs)
