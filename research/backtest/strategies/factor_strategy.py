"""팩터 전략: 팩터 스코어 상위 종목 리밸런싱 (스켈레톤)."""
import backtrader as bt


class FactorStrategy(bt.Strategy):
    params = dict(rebalance_days=20, top_n=10)

    def __init__(self):
        self.counter = 0
        # TODO: 사전 계산된 팩터 스코어를 data feed로 주입

    def next(self):
        self.counter += 1
        if self.counter % self.p.rebalance_days != 0:
            return
        # TODO: 스코어 상위 top_n 종목으로 리밸런싱
