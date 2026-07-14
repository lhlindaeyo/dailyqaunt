# 기능별 사용법

## 워크플로우 요약
```
데이터 수집 → 보조지표 → 팩터분석 → 백테스트 → JSON export → site/data → git push
```

## 1. 데이터 수집
```bash
python research/data/fetch_stock.py --ticker 005930 --market KRX --period 1y
python research/data/fetch_index.py --index KOSPI --start 2020-01-01 --end 2024-12-31
```

## 2. 보조지표 계산
```bash
python research/indicators/trend.py --ticker 005930
python research/indicators/momentum.py --ticker 005930
python research/indicators/volume.py --ticker 005930
```

## 3. 백테스트
```bash
python research/backtest/run_backtest.py --strategy momentum --ticker 005930 \
    --start 2020-01-01 --end 2024-12-31
```

## 4. 결과를 사이트로 export
```bash
python research/export/export_chart.py --ticker 005930
python research/export/export_backtest.py --strategy momentum
```

## 5. 게시
```bash
git add site/data/
git commit -m "update: 결과 갱신"
git push
```

## 대시보드 화면 구성
- `index.html` — 종합 대시보드 (시장 개요 + 지수 차트 + 워치리스트 + 백테스트/팩터 요약)
- `stock.html` — 종목 상세 차트
- `backtest.html` — 백테스트 상세 결과
- `factor.html` — 팩터 리서치

각 화면은 `site/data/*.json`을 읽어 렌더링합니다. 현재는 샘플(더미) 데이터가 들어있으며,
위 파이프라인을 돌리면 실제 데이터로 교체됩니다.
