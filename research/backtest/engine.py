"""
Backtrader 백테스트 엔진 설정
공통 Cerebro 구성(수수료, 슬리피지, 초기자본)을 제공.
"""
import backtrader as bt


def build_cerebro(cash: float = 10_000_000, commission: float = 0.00015) -> bt.Cerebro:
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=commission)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="timereturn")
    return cerebro
