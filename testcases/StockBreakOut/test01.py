import os
from backtesting import Backtest, Strategy
from backtesting.magnus import _read_file

import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
class StockBreakOut(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        if len(self.data.Volume) > 66:
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isStockOut(prices):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0 and (TakeProfit.takeProfit(5, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(8, last_price, self.buy_price)):
                self.position.close()
                self.buy_price = 0
vn30_ticker = Ticker.getListBlueChips2020()
for ticker in vn30_ticker:
    ticker_data = _read_file(ticker+'.csv')
    bt = Backtest(ticker_data, StockBreakOut, commission=.005, exclusive_orders=False)
    stats = bt.run()
    # bt.plot()
    # print(stats)
    # print(ticker)
    # print(stats['Sharpe Ratio'])
    # # print(stats['_trades'])
    new_file = path+"/result_"+ticker+".csv"
    stats['_trades'].to_csv(new_file, index=False)
