import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.magnus import SMA, _read_file


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


BID = _read_file('BID.csv')
bt = Backtest(BID, SmaCross, commission=.002, exclusive_orders=True)
stats = bt.run()
# bt.plot()
print(stats)
#print(stats['_trades'])
