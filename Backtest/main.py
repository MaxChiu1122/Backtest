import pandas as pd
from time import sleep
import datetime
import ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from helper import get_tickers_usdt, klines, klines_extended

# Take Profit and Stop Loss. 0.03 means 3%
tp = 0.05
sl = 0.03
# Timeframe (for example, '1m', '3m', '5m', '15m', '1h', '4h')
timeframe = '4h'
begin_day = datetime.date(2021, 1, 1)
today = datetime.date.today()
# Interval in days:
interval = (today - begin_day).days


# symbols = get_tickers_usdt()

# Add indicators you want, here I just show some examples
def rsi(df, period=14):
    rsi = ta.momentum.RSIIndicator(pd.Series(df), window=period).rsi()
    return rsi

def ema(df, period=200):
    ema = ta.trend.EMAIndicator(pd.Series(df), period).ema_indicator()
    return ema

def macd(df):
    macd = ta.trend.MACD(pd.Series(df)).macd()
    return macd

def signal_h(df):
    return ta.volatility.BollingerBands(pd.Series(df)).bollinger_hband()
def signal_l(df):
    return ta.volatility.BollingerBands(pd.Series(df)).bollinger_lband()

class str(Strategy):
    # Any variables you want:
    ema_period = 200
    rsi_period = 14
    def init(self):
        # Take close prices as actual price
        price = self.data.Close
        # Declare indicators you will (or want) use in the strategy:
        self.rsi = self.I(rsi, self.data.Close, self.rsi_period)
        self.macd = self.I(macd, self.data.Close)
        self.ema = self.I(ema, self.data.Close, self.ema_period)
        self.bol_h = self.I(signal_h, self.data.Close)
        self.bol_l = self.I(signal_l, self.data.Close)

    def next(self):
        price = float(self.data.Close[-1])
        # Simple strategy example. Its RSI and EMA. Buy when RSI<30 and Close>EMA, sell when RSI>70 and Close<EMA
        if self.rsi[-2] < 30 and self.data.Close[-2] > self.ema[-2]:
            if not self.position:
                # size is % of the 'cash'
                self.buy(size=0.05, tp=(1+tp)*price, sl=(1-sl)*price)
            if self.position.is_short:
                self.position.close()
                self.buy(size=0.05, tp=(1+tp)*price, sl=(1-sl)*price)
                
        if self.rsi[-2] > 70 and self.data.Close[-2] < self.ema[-2]:
            if not self.position:
                self.sell(size=0.05, tp=(1-tp)*price, sl=(1+sl)*price)
            if self.position.is_long:
                self.position.close()
                self.sell(size=0.05, tp=(1-tp)*price, sl=(1+sl)*price)


symbol = 'BTCUSDT'
kl = klines_extended(symbol, timeframe, interval)
# cash is initial investment in USDT, margin is leverage (1/10 is x10)
# commission is about 0.1%(5bp * 2) for Binance Futures
bt = Backtest(kl, str, cash=1000000, margin=1/10, commission=0.001)
stats = bt.run()

csv_filename = "statistics.csv"
stats.to_csv(csv_filename)
print(stats)
bt.plot()
