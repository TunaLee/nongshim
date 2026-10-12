# AI로 일하는 방식 바꾸기

생성형 AI 중급 과정(국내영업)의 **이론 덱**. 실습 · 따라하기 장은 별도 덱에 있다.
그림은 이미지 생성 없이 인라인 SVG로 그렸고, 색은 남색 `#1F3A5F` · 밝은 회색 `#D9DDE3` · 주황 `#F28C28` 세 가지만 쓴다.

- 덱: `docs/index.html` (브라우저로 열기. ← → 로 넘기고, PDF 버튼으로 인쇄)
- 다시 만들기: `python3 src/build.py`

| 파일 | 내용 |
|---|---|
| `src/course.py` | **합본 강의 구성** — 오프닝 · Ch1 근거 · Ch2 하네스와 Skills · Ch3 데이터 · Ch4 문서와 화면 · Ch5 연결과 자동화 · 적용 |
| `src/deck.py` · `src/deck_gas.py` | 장 부품(그림 장 · 실습 장 · 캡처 장 · 직무 지도 · 웹 도해) |
| `src/explain.py` | Ch1 그림 장 뒤의 설명 장 8개 |
| `src/intro.py` | 강사 소개 · 코드 레드 타임라인 · 밈 장, 어두운 장 스타일 |
| `src/art.py` | 회사원 · 로봇 등 그림 공통 부품 |
| `src/scenes_ch1~5.py` | 장면 그림 |
| `src/preview.py` | 장면 하나를 PNG로 미리 보기 |

- 챕터마다 간지 다음에 생태계 지도가 나온다. 지난 장의 동료는 켜지고, 이번 장은 주황으로 강조, 남은 장은 흐리다 (`deck.ACTIVE`).
- 아이콘: `docs/assets/icons/` — Wikimedia Commons, Public domain · CC0. 상표라 참조 용도로만 쓴다.
- 밈 두 장(`meme-*.jpg`)은 출처 미확인 이미지라 저장소를 공개로 바꾸기 전에 빼야 한다.

## 배포 · 데이터
- GitHub Actions(`.github/workflows/pages.yml`)가 main에 push될 때마다 슬라이드를 빌드해 GitHub Pages에 올린다.
  - 강의: https://tunalee.github.io/nongshim/
- 핸즈온 데이터: `python3 src/make_data.py` (openpyxl 필요)로 `docs/data/`에 만든다.
  - https://tunalee.github.io/nongshim/data/store_check_raw.xlsx — 정제 전 점검 기록
  - https://tunalee.github.io/nongshim/data/store_check_clean.xlsx — 정답 정제본
  - https://tunalee.github.io/nongshim/data/my_emails_sample.txt · .docx — 메일 Skill 실습용 「내가 보낸 메일」 예시 5통 (`python3 src/make_emails.py`)
  - `docs/data/answer.json` — 정답 숫자 (슬라이드 「정답 숫자」 장이 읽어 씀)
