import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.magnus import SMA, BID


class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumns = self.data.Volume
        if len(self.data.Volume) > 5:
            self.last_5_volumns = volumns[-5::]
            self.last_3_prices = prices[-3::]
            self.min_volumn = min(self.last_5_volumns)
            self.max_volumn = max(self.last_5_volumns)
            self.last_volumn = self.last_5_volumns[-1]
            self.mean_f = np.mean(volumns[-5:-2])
            self.last_open_price = opens[-1]
            self.last_volumn = volumns[-1]
            self.last_price = prices[-1]
        if len(self.data.Volume) > 5:
            if self.last_3_prices[0] < self.last_3_prices[1] and self.last_3_prices[0] < self.last_3_prices[
                2] and self.last_volumn > 2.5 * self.mean_f and self.last_volumn > 1000000 and self.last_open_price < \
                    self.last_3_prices[2]:
                self.buy_price = self.last_price
                self.buy()
            if self.last_price > 1.05 * self.buy_price:
                self.sell()


bt = Backtest(BID, FollowTheTrend, commission=.002,
              exclusive_orders=True)
stats = bt.run()
# bt.plot()
# print(stats)
# print(stats['_trades'])
new_file = "result.csv"
stats['_trades'].to_csv(new_file, index=True)
