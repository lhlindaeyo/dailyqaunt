"""
백테스트 결과를 site/data/로 복사.
사용 예:
    python research/export/export_backtest.py --strategy momentum
"""
import argparse
import os
import shutil

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUTPUT_DIR = os.path.join(ROOT, "output")
SITE_DATA = os.path.join(ROOT, "site", "data")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--strategy", required=True)
    args = p.parse_args()
    src = os.path.join(OUTPUT_DIR, f"backtest_{args.strategy}.json")
    os.makedirs(SITE_DATA, exist_ok=True)
    dst = os.path.join(SITE_DATA, f"backtest_{args.strategy}.json")
    shutil.copy(src, dst)
    print(f"복사 완료: {dst}")


if __name__ == "__main__":
    main()
