
import unittest
import datetime
from activetick.core import get_option_chain, request_quote_ticks, request_bar_data, request_trade_ticks
#from activetick.http_server import run_http_server

SYMBOL = 'MSFT'


class TestActivetick(unittest.TestCase):

    date_from = datetime.datetime(2016, 1, 5, 11, 0)
    date_to_short = datetime.datetime(2016, 1, 5, 11, 1)
    date_to_long = datetime.datetime(2016, 1, 6, 11, 0)
    date_to_vlong = datetime.datetime(2016, 1, 10, 11, 0)

    def test_option_chain(self):
        data = get_option_chain(SYMBOL, debug=True)
        self.assertAlmostEquals(data.shape[0], 800, -2)

    def test_quote_ticks(self):
        data = request_quote_ticks(SYMBOL, self.date_from, self.date_to_short, debug=True)
        self.assertEqual(data.shape[0], 1117)

    def test_trade_ticks(self):
        data = request_trade_ticks(SYMBOL, self.date_from, self.date_to_short, debug=True)
        self.assertEqual(data.shape[0], 318)

    def test_bar_data(self):
        data = request_bar_data(SYMBOL, self.date_from, self.date_to_vlong, debug=True)
        self.assertEqual(data.shape[0], 4)


