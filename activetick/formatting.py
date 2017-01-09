
import datetime


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
