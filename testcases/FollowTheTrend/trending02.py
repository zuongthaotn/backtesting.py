import os
from backtesting import Backtest, Strategy

from backtesting.magnus import get_pricing
import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
STOPLOSS = 0.08
class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self.trailing_price = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        if len(self.data.Volume) > 5:
            last_price = prices[-1]
            # price is increased
            if last_price > self.trailing_price:
                self.trailing_price = last_price

            if self.buy_price == 0 and Ticker.isFollowTrendingV2(prices, volumes, opens[-1], 2.5):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0:
                # print(self.buy_price * (1 - STOPLOSS))
                # print(last_price)
                # print(self.trailing_price * (1 - STOPLOSS))
                # print('------------------------')
                if TakeProfit.takeProfit(15, last_price, self.buy_price) or last_price < self.buy_price * (1 - STOPLOSS) or last_price < self.trailing_price * (1 - STOPLOSS):
                    print(self.data.Date[-1])
                    self.position.close()
                    self.buy_price = 0
                    self.trailing_price = 0

ticker_id = 'PNJ'
ticker = get_pricing(ticker_id+'.csv', '2018-01-01', '2020-10-05')
bt = Backtest(ticker, FollowTheTrend, commission=.005, exclusive_orders=False)
stats = bt.run()
# bt.plot()
print(stats)
# print(stats['_trades'])
# new_file = path+"/result_"+ticker_id+".csv"
# stats['_trades'].to_csv(new_file, index=False)
