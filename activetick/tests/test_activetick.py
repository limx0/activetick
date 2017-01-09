
import unittest
import os
import datetime
import subprocess
from multiprocessing import Process
from activetick.io import get_option_chain, request_quote_ticks, request_bar_data, request_trade_ticks

SYMBOL = 'MSFT'


def get_dates():
    today = datetime.datetime.now()
    last_friday = (today - datetime.timedelta(days=(today.weekday())+3))
    return last_friday.replace(hour=0, minute=0), last_friday.replace(hour=23, minute=59)


def run_http_server(*args):
    subprocess.Popen(list(args), stdout=subprocess.PIPE)


class TestBase(unittest.TestCase):
    BINARY = r'C:\Program Files\ActiveTick LLC\ActiveTick Feed HTTP Server\ActiveTickFeedHttpServer.exe'
    SERVER = 'activetick1.activetick.com'
    HOST = '127.0.0.1'
    PORT = '5000'
    API_KEY = os.environ['ACTIVETICK_API_KEY']
    USERNAME = os.environ['ACTIVETICK_USERNAME']
    PASSWORD = os.environ['ACTIVETICK_PASSWORD']

    def setUp(self):
        args = (self.BINARY, self.HOST, self.SERVER, self.PORT, self.API_KEY, self.USERNAME, self.PASSWORD)
        self.p = Process(target=run_http_server, args=args)
        self.p.start()

    def tearDown(self):
        self.p.terminate()


class TestActivetick(TestBase):

    date_from, date_to = get_dates()

    def test_option_chain(self):
        data = get_option_chain(SYMBOL, debug=True)
        print(data)
        self.assertTrue(data.shape)

    def test_quote_ticks(self):
        self.assertTrue(request_quote_ticks(SYMBOL, self.date_from, self.date_to, debug=True))
