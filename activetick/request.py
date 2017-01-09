
import pandas as pd
from activetick.compat import urlencode, urlopen, IO
from activetick.util import split_queries, DATE_FORMAT

# Max number of ticks received from activetick server, +1 for newline at EOF
MAX_RESPONSE = {
    'tickData': 100000 + 1,
    'barData': 20000 + 1,
    }


def get_activetick_data(end_point, args, header, symbol, **kwargs):
    data = activetick_request(end_point, args, debug=kwargs.pop('debug', False))
    if not isinstance(data, list):
        data = [data]
    return pd.concat([
        parse_activetick_response(data=d, header=header, symbol=symbol, **kwargs)
        for d in data
        ])


def activetick_request(end_point, params, host='127.0.0.1', port='5000', debug=False):
    url = (r'http://{host}:{port}/{end_point}?{parameters}'
           .format(host=host, port=port, end_point=end_point, parameters=urlencode(params)))
    if debug:
        print(url)
    data = urlopen(url).read()
    if data in [b'', b'0', b'00000000000000,0.000000,0.000000,0.000000,0.000000,0\r\n']:
        return []
    if b'ActiveTick Feed client is not connected' in data:
        raise Exception(b'ActiveTick Feed client not connected')
    if data and len(data.split(b'\r\n')) == MAX_RESPONSE.get(end_point, None):
        return split_queries(activetick_request, **{'end_point': end_point, 'params': params, 'host': host, 'port': port})
    return data


def parse_activetick_response(data, header, symbol, index_col=list(('TIMESTAMP',)), ignore_cols=list()):
    cols = [h for h in header if h not in ignore_cols]
    df = pd.read_csv(IO(data), names=header, index_col=index_col, usecols=cols)
    if index_col == ['TIMESTAMP']:
        df.index = pd.to_datetime(df.index, format=DATE_FORMAT)
    df.loc[:, 'SYMBOL'] = df.assign(SYMBOL=symbol)['SYMBOL'].astype('category')
    return df
