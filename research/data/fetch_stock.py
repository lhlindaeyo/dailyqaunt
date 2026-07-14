"""
종목 주가 / 거래량 수집
사용 예:
    python research/data/fetch_stock.py --ticker 005930 --market KRX --period 1y
    python research/data/fetch_stock.py --ticker AAPL --market US --period 1y
결과: output/stock_<ticker>.csv (OHLCV)
"""
import argparse
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def fetch_krx(ticker: str, period: str):
    """pykrx로 KRX 종목 OHLCV 수집."""
    from datetime import datetime, timedelta
    from pykrx import stock

    days = {"1m": 30, "3m": 90, "6m": 180, "1y": 365, "3y": 1095}.get(period, 365)
    end = datetime.today()
    start = end - timedelta(days=days)
    df = stock.get_market_ohlcv(
        start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), ticker
    )
    df = df.rename(
        columns={"시가": "open", "고가": "high", "저가": "low",
                 "종가": "close", "거래량": "volume"}
    )
    return df[["open", "high", "low", "close", "volume"]]


def fetch_us(ticker: str, period: str):
    """yfinance로 미국 종목 OHLCV 수집."""
    import yfinance as yf

    df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    df = df.rename(
        columns={"Open": "open", "High": "high", "Low": "low",
                 "Close": "close", "Volume": "volume"}
    )
    return df[["open", "high", "low", "close", "volume"]]


def main():
    p = argparse.ArgumentParser(description="종목 주가/거래량 수집")
    p.add_argument("--ticker", required=True)
    p.add_argument("--market", choices=["KRX", "US"], default="KRX")
    p.add_argument("--period", default="1y")
    args = p.parse_args()

    df = fetch_krx(args.ticker, args.period) if args.market == "KRX" \
        else fetch_us(args.ticker, args.period)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"stock_{args.ticker}.csv")
    df.to_csv(out)
    print(f"저장 완료: {out} ({len(df)} rows)")


if __name__ == "__main__":
    main()
