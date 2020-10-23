"""Data and utilities for testing."""
import pandas as pd

def _read_file(filename):
    from os.path import dirname, join
    file_path = join(dirname(dirname(dirname(__file__))) , 'method/cophieu68/'+filename)
    return pd.read_csv(file_path, index_col=1, parse_dates=True, infer_datetime_format=True)

def SMA(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    return pd.Series(arr).rolling(n).mean()

# def _read_file02(filename):
#     from os.path import dirname, join
#     print(join(dirname(__file__), filename))
#     # return pd.read_csv(join(dirname(__file__), filename),
#     #                    index_col=0, parse_dates=True, infer_datetime_format=True)
#
# BID = _read_file02('BID.csv')
# """DataFrame of daily VNINDEX:BID stock price data from 2014 to 2020."""