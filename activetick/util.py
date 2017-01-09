
import os
import subprocess
import multiprocessing
import pandas as pd

DATE_FORMAT = '%Y%m%d%H%M%S%f'


def split_queries(func, **kwargs):
    end_point = kwargs.get('end_point', None)
    params = kwargs.get('params', {}).copy()
    dates1, dates2 = split_date_range(pd.to_datetime(params['beginTime']), pd.to_datetime(params['endTime']))

    # Update original params dictionary with new split beginTime and endTime.
    return [
        func(end_point, dict(list(params.items()) + list(dict(zip(['beginTime', 'endTime'], dates1)).items()))),
        func(end_point, dict(list(params.items()) + list(dict(zip(['beginTime', 'endTime'], dates2)).items()))),
    ]


def dt_to_str(dt):
    return dt.strftime(DATE_FORMAT)[:-6]


def split_date_range(date_from, date_to):
    midpoint = date_from + (date_to - date_from) / 2
    return (
        tuple(map(dt_to_str, (date_from, midpoint))),
        tuple(map(dt_to_str, (midpoint, date_to)))
    )


def run_http_server():
    def activetick_http_server():
        cmd = [
            r'C:\Program Files\ActiveTick LLC\ActiveTick Feed HTTP Server\ActiveTickFeedHttpServer.exe',
            'activetick1.activetick.com',
            '127.0.0.1',
            '5000',
            os.environ['ACTIVETICK_API_KEY'],
            os.environ['ACTIVETICK_USERNAME'],
            os.environ['ACTIVETICK_PASSWORD'],
        ]
        subprocess.Popen(cmd, stdout=subprocess.PIPE)

    p = multiprocessing.Process(target=activetick_http_server)
    p.start()
