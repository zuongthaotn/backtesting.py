"""Data and utilities for testing."""
import pandas as pd
from datetime import datetime

def _read_file(filename):
    from os.path import dirname, join
    file_path = join(dirname(dirname(dirname(__file__))) , 'method/cophieu68/'+filename)
    return pd.read_csv(file_path, index_col=1, parse_dates=True, infer_datetime_format=True)

# %% Get VN stocks data
def get_pricing(filename, start_date='2000-07-28', end_date=None):
    import os
    from os.path import dirname, join
    filepath = join(dirname(dirname(dirname(__file__))), 'method/cophieu68/' + filename)

    usecols = None
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')

    if os.path.isfile(filepath):
        prices = pd.read_csv(
            filepath,
            index_col='Date',
            parse_dates=['Date'],
            date_parser=date_parser,
            usecols=usecols
        )[start_date:end_date]
        prices['Date'] = prices.index
        return prices

    return None

# def _read_file02(filename):
#     from os.path import dirname, join
#     print(join(dirname(__file__), filename))
#     # return pd.read_csv(join(dirname(__file__), filename),
#     #                    index_col=0, parse_dates=True, infer_datetime_format=True)
#
# BID = _read_file02('BID.csv')
# """DataFrame of daily VNINDEX:BID stock price data from 2014 to 2020."""
