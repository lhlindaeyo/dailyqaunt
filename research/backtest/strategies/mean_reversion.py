"""평균회귀 전략: RSI 과매도 매수, 과매수 매도."""
import backtrader as bt


class MeanReversionStrategy(bt.Strategy):
    params = dict(period=14, low=30, high=70)

    def __init__(self):
        self.rsi = bt.ind.RSI(period=self.p.period)

    def next(self):
        if not self.position and self.rsi < self.p.low:
            self.buy()
        elif self.position and self.rsi > self.p.high:
            self.close()
