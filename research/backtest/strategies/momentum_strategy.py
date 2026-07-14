"""모멘텀 전략: N일 이동평균 상향 돌파 시 매수, 하향 시 매도."""
import backtrader as bt


class MomentumStrategy(bt.Strategy):
    params = dict(fast=20, slow=60)

    def __init__(self):
        sma_fast = bt.ind.SMA(period=self.p.fast)
        sma_slow = bt.ind.SMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(sma_fast, sma_slow)

    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.close()
