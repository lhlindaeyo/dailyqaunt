"""
팩터 분석 결과 → JSON 변환 → site/data/factor.json
사용 예:
    python research/export/export_factor.py
TODO: factor_analysis 결과(IC 시계열, 퀀타일 수익률) 직렬화
"""
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SITE_DATA = os.path.join(ROOT, "site", "data")


def export(ic_series=None, quantile_returns=None):
    payload = {
        "ic": ic_series or [],
        "quantile_returns": quantile_returns or [],
    }
    os.makedirs(SITE_DATA, exist_ok=True)
    out = os.path.join(SITE_DATA, "factor.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print(f"저장 완료: {out}")


if __name__ == "__main__":
    export()
