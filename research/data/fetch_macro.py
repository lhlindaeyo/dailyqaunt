"""
매크로 데이터 수집 (금리, 환율 등)
사용 예:
    python research/data/fetch_macro.py --series USDKRW --start 2020-01-01 --end 2024-12-31
결과: output/macro_<series>.csv
TODO: 한국은행 ECOS API / FRED API 연동
"""
import argparse
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def main():
    p = argparse.ArgumentParser(description="매크로 데이터 수집")
    p.add_argument("--series", required=True, help="예: USDKRW, KR_BASE_RATE, US10Y")
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    args = p.parse_args()

    # TODO: 실제 소스 연동 (yfinance 환율/금리, FRED, ECOS)
    raise NotImplementedError("매크로 수집 소스 연동 예정")


if __name__ == "__main__":
    main()
