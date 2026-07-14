# 환경 세팅 가이드

## 1. 사전 준비
- Python 3.10+ (권장 3.12)
- Git

## 2. 클론 & 가상환경
```bash
git clone https://github.com/lhlindaeyo/dailyqaunt.git
cd dailyqaunt
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

## 3. API 키
```bash
copy .env.example .env     # Windows (cp on mac/linux)
```
`.env`에 한국투자증권 키 입력. 이 파일은 `.gitignore`에 포함되어 커밋되지 않습니다.

## 4. 대시보드 로컬 미리보기
`site/` 폴더는 정적 사이트입니다. 로컬에서 열려면:
```bash
cd site
python -m http.server 8000
```
브라우저에서 http://localhost:8000 접속.

> `file://`로 직접 열면 JSON fetch가 CORS로 막힐 수 있으니 반드시 로컬 서버로 여세요.

## 5. GitHub Pages 배포
저장소 Settings → Pages → Source를 `main` 브랜치 `/site` 폴더로 지정.
