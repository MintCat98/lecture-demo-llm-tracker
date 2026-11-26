# 할인 소식 트래커 데모

뽐뿌 핫딜과 Google 뉴스 키워드 검색 결과를 함께 모으고, Chrome 내장 AI로 관심사에 맞는 것만 골라 보는 가능성 확인용 데모.

## 파일
- `collect.py`: 수집 (Python 표준 라이브러리만 사용, 설치할 것 없음)
- `config.json`: 뉴스 검색어, 보관 기간 (뽐뿌 목록 페이지는 스크립트 접근이 막혀 있어 0으로 둠)
- `index.html`: 화면 + 내장 AI 필터
- `.github/workflows/collect.yml`: 15분마다 자동 수집 (뽐뿌 RSS는 최근 15건만 제공)
- `data.json`: 지금은 샘플 데이터. `collect.py`를 실행하면 실제 데이터로 바뀜

## 내 컴퓨터에서 바로 테스트
```bash
python3 collect.py              # 실제 수집 → data.json
python3 -m http.server 8000     # 그다음 Chrome에서 http://localhost:8000 열기
```
- `file://`로 직접 열면 data.json을 못 읽어요. 꼭 위처럼 서버로 열어주세요.
- "AI로 거르기"가 "쓸 수 없어요"라고 나오면 `chrome://flags`에서 Prompt API 관련 항목을 켜고 Chrome을 다시 시작하세요.

## GitHub Pages로 올릴 때
1. 이 폴더를 public repo로 push
2. Settings → Pages → `main` / `(root)`
3. Settings → Actions → General → Workflow permissions → **Read and write** 선택
4. Actions 탭 → collect → Run workflow (첫 수집)

## 오프라인 테스트
```bash
FIXTURE_DIR=tests/fixtures python3 collect.py
```
