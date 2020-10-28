import os
import numpy as np
from backtesting import Backtest, Strategy

from backtesting.magnus import get_pricing
import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        # self._index = self._index + 1
        # print("----------"+str(self._index)+"--------")
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
                # print("buy date:" + str(self.data.index[-1]))
                self.buy()
            if self.buy_price != 0 and (TakeProfit.takeProfit(8, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(8, last_price, self.buy_price)):
                # print("sell date:" + str(self.data.index[-1]))
                # print("buy price:" + str(self.buy_price))
                # print("sell price:" + str(self.last_price))
                # self.sell()
                self.position.close()
                self.buy_price = 0

ticker_id = 'MBB'
ticker = get_pricing(ticker_id+'.csv', '2014-01-01', '2020-05-05')
bt = Backtest(ticker, FollowTheTrend, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()
print(stats)
# # print(stats['_trades'])
new_file = path+"/result_"+ticker_id+".csv"
stats['_trades'].to_csv(new_file, index=False)
