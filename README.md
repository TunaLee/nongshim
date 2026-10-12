# AI로 일하는 방식 바꾸기

생성형 AI 중급 과정(국내영업)의 **이론 덱**. 실습 · 따라하기 장은 별도 덱에 있다.
그림은 이미지 생성 없이 인라인 SVG로 그렸고, 색은 남색 `#1F3A5F` · 밝은 회색 `#D9DDE3` · 주황 `#F28C28` 세 가지만 쓴다.

- 덱: `docs/grounding/index.html` (브라우저로 열기. ← → 로 넘기고, PDF 버튼으로 인쇄)
- 다시 만들기: `python3 src/build.py`
- 짧은 강의 「Skill과 Apps Script 실적 대시보드」: `docs/gas-dashboard/index.html` · `python3 src/build.py gas` · 구성은 `src/deck_gas.py`, 캡처는 `docs/gas-dashboard/assets/capture/` (gas-01-menu · gas-02-files · gas-03-deploy · gas-04-auth)

| 파일 | 내용 |
|---|---|
| `src/deck.py` | 전체 구성과 장별 문구 — 오프닝 · Ch1~Ch5 · 적용 |
| `src/explain.py` | Ch1 그림 장 뒤의 설명 장 8개 |
| `src/intro.py` | 강사 소개 · 코드 레드 타임라인 · 밈 장, 어두운 장 스타일 |
| `src/art.py` | 회사원 · 로봇 등 그림 공통 부품 |
| `src/scenes_ch1~5.py` | 장면 그림 |
| `src/preview.py` | 장면 하나를 PNG로 미리 보기 |

- 챕터마다 간지 다음에 생태계 지도가 나온다. 지난 장의 동료는 켜지고, 이번 장은 주황으로 강조, 남은 장은 흐리다 (`deck.ACTIVE`).
- 아이콘: `docs/grounding/assets/icons/` — Wikimedia Commons, Public domain · CC0. 상표라 참조 용도로만 쓴다.
- 밈 두 장(`meme-*.jpg`)은 출처 미확인 이미지라 저장소를 공개로 바꾸기 전에 빼야 한다.
