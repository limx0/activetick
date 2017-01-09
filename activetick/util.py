
from io import BytesIO
import datetime
import logging
import requests
import pandas as pd
from activetick.compat import urlencode


logging.getLogger("requests").setLevel(logging.WARNING)

#  Max number of ticks received from activetick server, +1 for newline at EOF
MAX_RESPONSE = {
    'tickData': 100000 + 1,
    'barData': 20000 + 1,
    }


dt_fmt = '%Y%m%d%H%M%S%f'


def empty_df_on_fail(func):
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return pd.DataFrame()
    return function_wrapper


def split_queries(func, **kwargs):
    end_point = kwargs.get('end_point', None)
    params = kwargs.get('params', {}).copy()
    dates1, dates2 = split_date_range(pd.to_datetime(params['beginTime']), pd.to_datetime(params['endTime']))

    # Update original params dictionary with new split beginTime and endTime.
    return [
        func(end_point, dict(list(params.items()) + list(dict(zip(['beginTime', 'endTime'], dates1)).items()))),
        func(end_point, dict(list(params.items()) + list(dict(zip(['beginTime', 'endTime'], dates2)).items()))),
    ]


def get_activetick_data(end_point, args, header, symbol, **kwargs):
    data = activetick_request(end_point, args, **kwargs)
    if not isinstance(data, list):
        data = [data]
    return pd.concat([
        parse_activetick_response(data=BytesIO(d), header=header, symbol=symbol, ignore_cols=['RECORD'], **kwargs)
        for d in data
        ])


def activetick_request(end_point, params, host='127.0.0.1', port='5000', debug=False):
    url = (r'http://{host}:{port}/{end_point}?{parameters}'
           .format(host=host, port=port, end_point=end_point, parameters=urlencode(params)))
    if debug:
        print(url)
    data = requests.get(url).content
    if data in [b'', b'0', b'00000000000000,0.000000,0.000000,0.000000,0.000000,0\r\n']:
        return []
    if b'ActiveTick Feed client is not connected' in data:
        raise Exception(b'ActiveTick Feed client not connected')
    if data and len(data.split(b'\r\n')) == MAX_RESPONSE.get(end_point, None):
        return split_queries(activetick_request, **{'end_point': end_point, 'params': params, 'host': host, 'port': port})
    return data


@empty_df_on_fail
def parse_activetick_response(data, header, symbol, ignore_cols=list()):
    cols = [h for h in header if h not in ignore_cols]
    df = pd.read_csv(data, names=header, index_col=['TIMESTAMP'], usecols=cols)
    df.index = pd.to_datetime(df.index, format=dt_fmt)
    df.loc[:, 'SYMBOL'] = df.assign(SYMBOL=symbol)['SYMBOL'].astype('category')
    return df


def generate_option_feedcode(symbol, expiry, kind, strike):
    from math import modf
    d, i = modf(strike)
    return 'OPTION:{s}{e}{k}{i}{d}'.format(
        s=symbol.ljust(6, '-').upper(),
        e=expiry.strftime('%y%m%d'),
        k=kind,
        i=str(int(i)).rjust(5, '0'),
        d=str(int(d * 100)).ljust(3, '0')
    )


def option_feedcode_to_detail(feedcode):
    symbol = feedcode[7:13].replace('-', '')
    expiry = datetime.datetime.strptime(feedcode[13:19], '%y%m%d')
    kind = feedcode[19]
    strike = float('{0}.{1}'.format(feedcode[20:25].lstrip('0'), feedcode[25:28].lstrip('0')))
    return pd.Series({'SYMBOL': symbol, 'EXPIRY': expiry, 'KIND': kind, 'STRIKE': strike, 'FEEDCODE': feedcode})


def dt_to_str(dt):
    return dt.strftime(dt_fmt)[:-6]


def split_date_range(date_from, date_to):
    midpoint = date_from + (date_to - date_from) / 2
    return (
        tuple(map(dt_to_str, (date_from, midpoint))),
        tuple(map(dt_to_str, (midpoint, date_to)))
    )