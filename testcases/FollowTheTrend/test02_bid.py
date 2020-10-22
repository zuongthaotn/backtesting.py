import os
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.magnus import _read_file02

import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        if len(self.data.Volume) > 5:
            last_5_volumes = volumes[-5::]
            last_3_prices = prices[-3::]
            # min_volume = min(last_5_volumes)
            max_volume = max(last_5_volumes)
            last_volume = last_5_volumes[-1]
            mean_f = np.mean(volumes[-5:-2])
            last_open_price = opens[-1]
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isFollowTrendingV2(prices, volumes, opens[-1], 2.5):
                self.buy_price = last_price
                print("buy date:" + str(self.data.index[-1]))
                self.buy()
            if self.buy_price != 0 and (TakeProfit.takeProfit(5, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(10, last_price, self.buy_price)):
                print("sell date:" + str(self.data.index[-1]))
                # print("buy price:" + str(self.buy_price))
                # print("sell price:" + str(self.last_price))
                # self.sell()
                self.position.close()
                self.buy_price = 0
path = os.getcwd()
# BID = _read_file(path+'/method/cophieu68/VHM.csv')
BID = _read_file02('BID.csv')
bt = Backtest(BID, FollowTheTrend, commission=.002,
              exclusive_orders=True)
stats = bt.run()
# bt.plot()
print(stats)
# # print(stats['_trades'])
# new_file = "result.csv"
# stats['_trades'].to_csv(new_file, index=False)
