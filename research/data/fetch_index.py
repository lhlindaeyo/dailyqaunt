"""
대표 지수 수집 (날짜 범위 입력)
사용 예:
    python research/data/fetch_index.py --index KOSPI --start 2020-01-01 --end 2024-12-31
결과: output/index_<name>.csv
"""
import argparse
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")

# pykrx 지수 코드 / yfinance 티커 매핑
KRX_INDEX = {"KOSPI": "1001", "KOSDAQ": "2001"}
US_INDEX = {"SP500": "^GSPC", "NASDAQ": "^IXIC"}


def main():
    p = argparse.ArgumentParser(description="지수 데이터 수집")
    p.add_argument("--index", required=True)
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    args = p.parse_args()

    name = args.index.upper()
    if name in KRX_INDEX:
        from pykrx import stock
        df = stock.get_index_ohlcv(
            args.start.replace("-", ""), args.end.replace("-", ""), KRX_INDEX[name]
        )
        df = df.rename(columns={"시가": "open", "고가": "high",
                                "저가": "low", "종가": "close", "거래량": "volume"})
    elif name in US_INDEX:
        import yfinance as yf
        df = yf.download(US_INDEX[name], start=args.start, end=args.end,
                         auto_adjust=True, progress=False)
        df.columns = [c.lower() for c in df.columns]
    else:
        raise SystemExit(f"지원하지 않는 지수: {name} (지원: "
                         f"{list(KRX_INDEX) + list(US_INDEX)})")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"index_{name}.csv")
    df.to_csv(out)
    print(f"저장 완료: {out} ({len(df)} rows)")


if __name__ == "__main__":
    main()
