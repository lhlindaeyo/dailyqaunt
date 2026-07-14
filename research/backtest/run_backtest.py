"""
백테스트 실행 → JSON 저장
사용 예:
    python research/backtest/run_backtest.py --strategy momentum --ticker 005930 \
        --start 2020-01-01 --end 2024-12-31
결과: output/backtest_<strategy>.json (수익률 곡선, MDD, 샤프비율 등)
"""
import argparse
import json
import os
import backtrader as bt

from engine import build_cerebro
from strategies import STRATEGIES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def main():
    p = argparse.ArgumentParser(description="백테스트 실행")
    p.add_argument("--strategy", required=True, choices=list(STRATEGIES))
    p.add_argument("--ticker", required=True)
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    args = p.parse_args()

    src = os.path.join(OUTPUT_DIR, f"stock_{args.ticker}.csv")
    data = bt.feeds.GenericCSVData(
        dataname=src, dtformat="%Y-%m-%d",
        fromdate=None, todate=None, headers=True,
    )

    cerebro = build_cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(STRATEGIES[args.strategy])
    start_value = cerebro.broker.getvalue()
    result = cerebro.run()[0]
    end_value = cerebro.broker.getvalue()

    dd = result.analyzers.drawdown.get_analysis()
    sharpe = result.analyzers.sharpe.get_analysis()
    timereturn = result.analyzers.timereturn.get_analysis()

    equity, cum = [], 1.0
    for dt, r in timereturn.items():
        cum *= (1 + r)
        equity.append({"date": dt.strftime("%Y-%m-%d"), "value": round(cum, 4)})

    payload = {
        "strategy": args.strategy,
        "ticker": args.ticker,
        "period": {"start": args.start, "end": args.end},
        "summary": {
            "total_return_pct": round((end_value / start_value - 1) * 100, 2),
            "mdd_pct": round(dd.get("max", {}).get("drawdown", 0), 2),
            "sharpe": round(sharpe.get("sharperatio") or 0, 2),
        },
        "equity_curve": equity,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"backtest_{args.strategy}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"저장 완료: {out}")


if __name__ == "__main__":
    main()
