"""합본 강의 — 오프닝 · Ch1 근거 · Ch2 하네스와 Skills · Ch3 데이터 · Ch4 문서와 화면 · Ch5 연결과 자동화 · 적용.

출력: docs/grounding/index.html  (python3 src/build.py)
부품은 deck.py · deck_gas.py · explain.py · intro.py 를 그대로 쓴다.
"""
from pathlib import Path

import deck
import deck_gas as g
import explain
import intro
from deck import ba, bridge, capture, cards, divider, flow, ill, lab, light
from intro import icon

deck.CAPDIR = Path(__file__).resolve().parent.parent / "docs" / "assets" / "capture"
code = explain.prompt
DATA_URL = "https://tunalee.github.io/nongshim/data/"


def dl(f):
    return f'<a class="dl" href="{DATA_URL}{f}">{f}</a>'

# 합본용 도구 ↔ 직무 지도 (위치는 그림 ⑨와 같은 시계 방향)
ROLES = [
    ("notebooklm", "Deep Research · Notebook", "리서처", "조사 · 근거 확인", (250, 255)),
    ("gemini", "Skills", "업무 매뉴얼 담당", "정제 · 판단 · 반복", (640, 215)),
    ("sheets", "Sheets", "데이터 엔지니어 · 분석가", "정리 · 저장 · 집계", (1030, 255)),
    ("docs", "Canvas", "프론트엔드 · 백엔드 개발자", "문서 · 화면 · 코드", (1030, 590)),
    ("appsscript", "Apps Script", "Ops 엔지니어", "연결 · 배포 · 운영", (640, 650)),
    ("drive", "Drive · 웹앱", "데이터 보관 · 서비스 운영", "보관 · 권한 · 공유", (250, 590)),
]


def tmap(active=None, kick="도구 지도", title="구글 도구로 꾸리는 작은 개발팀"):
    return g.team_map(active, kick, title, roles=ROLES)


def chapter(ch, title, active, map_title):
    return [divider(ch, title, ""), tmap(active, f"도구 지도 · {ch}", map_title)]


def table(head, rows, cls="dbt"):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def note(label, text):
    return f'<div class="dbnote"><span>{label}</span> {text}</div>'


def vl(*items):
    return '<div class="vl">' + "".join(f"<p>{x}</p>" for x in items) + "</div>"


# ── 오프닝 ───────────────────────────────────────────────
def opening():
    can = cards([
        ("대화", "질문 · 요약 · 초안", ["gemini"]),
        ("Deep Research", "웹을 뒤져 출처 달린 보고서", ["gemini"]),
        ("Notebook", "올린 자료 안에서만 답", ["notebooklm"]),
        ("Canvas", "문서 · 화면을 옆에 두고 수정", ["docs"]),
        ("Skills", "반복 지시를 저장해 /로 호출", ["gemini"]),
        ("Workspace 연결", "Gmail · Drive · Docs · Calendar", ["gmail", "drive", "calendar"]),
    ])
    places = cards([
        ("Gemini 앱", "대화 · Deep Research · Canvas · Skills", ["gemini"]),
        ("Workspace 사이드 패널", "Sheets · Docs · Gmail 안에서 바로", ["sheets", "docs", "gmail"]),
    ], 2)
    team = table(["담당", "맡은 일", "거래처"], [
        ["<b>김주현</b>", "편의점 담당", "A · B · C · D편의점"],
        ["<b>이지원</b>", "대형마트 담당", "A마트 · B마트"],
        ["<b>박서연</b>", "대리점 담당", "동부 · 서부 · 남부 · 북부대리점"],
    ])
    week = table(["거래처", "이번 주 일", "숫자"], [
        ["<b>A편의점</b>", "신제품 A 결품 문의", "결품률 11.5% (채널 평균 2.8%)"],
        ["<b>B편의점</b>", "스낵 C 매출 3개월 연속 감소", "5월 4,424만 → 8월 3,064만"],
        ["<b>C편의점</b>", "컵면 D 진열 확대 협의", "전월 대비 +21.0%"],
    ])
    files = table(["파일", "내용", "쓰는 장"], [
        ["01 판매실적 원본", "거래처 × SKU 월별 실적 · 일부러 넣은 오류", "Ch3"],
        ["02 미팅노트 · 03 월간 리포트", "8월 미팅 · 문의 기록, 채널별 리포트", "Ch1 · Ch4"],
        ["04 표준화 완성본", "정리된 원본 · 집계 · 이슈", "Ch3 대조 · Ch4 · Ch5"],
        ["05 카탈로그 · 06 기준표 · 07 응대 가이드", "SKU 41종, 행사 · 단가 조항, 회신 원칙", "Ch2"],
        ["08 동향 브리프 · 09 대시보드 예시", "Deep Research 예시 보고서, 완성 대시보드", "Ch1 · Ch4"],
    ])
    return [
        deck.cover(),
        intro.speaker(),
        intro.codered(),
        intro.meme(),
        light("Gemini로 할 수 있는 일", can, "오프닝"),
        light("Gemini를 쓰는 곳", places, "오프닝"),
        ill("scenes_more", "account_privacy", "top20", "개인 계정과 회사 계정",
            ["개인: 연결 데이터가 모델 개선에 쓰일 수 있음", "실습 · 업무: 회사 계정으로"]),
        deck.o_work(),
        deck.agenda(),
        tmap(),
        light("도구와 직무", table(["도구", "실제로 하는 일", "회사라면"], [
            ["<b>Deep Research · Notebook</b>", "웹 조사 보고서, 내 자료 안에서 답", '<span class="rolechip">리서처</span>'],
            ["<b>Skills</b>", "반복 지시 저장, 판단해서 정제", '<span class="rolechip">업무 매뉴얼 담당</span>'],
            ["<b>Sheets</b>", "데이터 저장 · 수식 · 피벗 집계", '<span class="rolechip">데이터 엔지니어 · 분석가</span>'],
            ["<b>Canvas</b>", "제안서 · 대시보드 화면과 동작 코드", '<span class="rolechip">프론트엔드 · 백엔드 개발자</span>'],
            ["<b>Apps Script</b>", "시트 ↔ 화면 연결, 배포, 권한", '<span class="rolechip">Ops 엔지니어</span>'],
            ["<b>Drive · 웹앱</b>", "파일 보관, 공유 범위, 팀 창구", '<span class="rolechip">데이터 보관 · 서비스 운영</span>'],
        ]), "오프닝"),
        ill("scenes_ch2", "office_map", "top20", "도구별 역할", extra=tags()),
        light("가상 시나리오", f'''<div class="scen">
  <div class="who">국내영업본부 <b>수도권영업팀</b> · 2026년 9월 첫 주 월요일 · 8월 마감 직후</div>
  {team}
</div>''', "오프닝"),
        light("이번 주에 처리할 세 건", week, "오프닝"),
        light("실습 자료", files, "오프닝"),
    ]


TAGS = [((400, 344), "리서치 · Deep Research"), ((880, 344), "검토 · Notebook"), ((1112, 500), "데이터 · Sheets"),
        ((880, 654), "작업대 · Canvas"), ((420, 654), "연결 · 배포 · Apps Script"), ((168, 500), "업무 지침 · Skills")]


def tags():
    return "".join(f'<div class="tagl" style="left:{x-107}px; top:{y}px">{t}</div>' for (x, y), t in TAGS)


# ── Ch1 근거 ─────────────────────────────────────────────
def ch1():
    out = chapter("Ch1", "근거 있는 답을 받는 법", {"Deep Research · Notebook"}, "리서처")
    pairs = list(zip(deck.CH1_ILL, explain.SLIDES))
    for i, ((fn, zone, title, pr), ex) in enumerate(pairs):
        if fn != "s6":  # 오픈북 그림은 Ch2 「참조 파일은 참고 교재」에서 씀
            out.append(ill("scenes_ch1", fn, zone, title, principle=pr))
        out.append(ex())
        if fn == "s5":  # Deep Research 진행 순서 뒤
            out += [
                light("보고서를 받으면", vl("출처 링크 세 개는 직접 열어 보기", "숫자는 원문 표와 대조", "날짜가 오래된 자료 표시", "Docs로 내보내 Notebook 소스로"), "Ch1"),
                lab("1-1", "편의점 채널 동향 조사", "Ch1",
                    "출처가 달린 동향 보고서 한 편",
                    ["기간 · 출처 · 형식을 넣어 질문", "계획 확인 → 한 항목 고치기", "보고서 받기 → 출처 세 개 열어 확인", "Docs로 내보내기"],
                    ["출처 달린 보고서", "확인한 출처 세 개 표시"], files="웹 · 08(예시)"),
            ]
        if fn == "s6":  # NotebookLM 답변 방식 뒤
            out += [
                light("Notebook에 넣는 자료", table(["자료", "넣는 법"], [
                    ["02 미팅노트 · 03 리포트 · 08 브리프", "docx를 소스로 그대로 추가"],
                    ["Deep Research 보고서", "Docs로 내보낸 뒤 추가"],
                    ["01 · 04 같은 xlsx", "소스로 받지 않음 → Ch3 Sheets에서"],
                ]), "Ch1"),
                lab("1-2", "Notebook에 세 가지 질문", "Ch1",
                    "답마다 출처, 없으면 없다고",
                    ["02 · 03 · 08을 소스로 추가", "B편의점 스낵 C가 줄어든 이유", "A편의점 신제품 A 결품 원인", "D편의점 9월 행사 계획"],
                    ["B: 사실(감소 수치)과 가설(경쟁사 2+1) 구분", "A: 「물류 확인 전」으로 표시", "D: 자료에 없음"], files="02 · 03 · 08"),
            ]
    out.append(light("원칙 두 가지", cards([
        ("원칙 ① 근거를 쥐여 준다", "볼 자료를 정해 준다", ["notebooklm"]),
        ("원칙 ② 계획을 보여 줄 때 개입한다", "실행 전에 계획을 고친다", ["gemini"]),
    ], 2), "Ch1"))
    out.append(bridge("다음: 반복 지시를 저장하는 법", "", "Ch1", "→ Ch2 하네스와 Skills"))
    return out


# ── Ch2 하네스와 Skills ───────────────────────────────────
def ch2():
    m = "scenes_ch5"
    harness = '''<div class="hn">
  <div class="hn-out"><div class="hn-lab">하네스</div>
    <div class="hn-row"><span class="hl">지침 = Skill</span><span>참고 자료</span></div>
    <div class="hn-core">모델</div>
    <div class="hn-row"><span>도구 연결</span><span>사람 확인</span></div>
  </div>
</div>'''
    bot = '''<div class="ba">
  <div class="b"><div class="lab">2023~2024 · 봇</div><div class="q">GPTs · Gems<br/>역할마다 따로 만든 대화 상대<br/>쓰려면 그 봇으로 이동</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">2025~2026 · 스킬</div><div class="q">Skills<br/>필요할 때 꺼내 쓰는 업무 지침 묶음<br/>한 대화에서 <b>/이름</b>으로 호출 · 여러 개 조합</div></div>
</div>'''
    trend = '''<div class="tline t4">
  <div class="tl"><b>2025.10</b><span>Claude · Agent Skills</span></div>
  <div class="tl"><b>2025.12</b><span>Agent Skills 공개 표준</span></div>
  <div class="tl"><b>2026</b><span>ChatGPT · Skills (업무용 플랜)</span></div>
  <div class="tl hl"><b>2026.10</b><span>Gemini · Skills</span></div>
</div>
<div class="homework"><b>공통</b> 이름 · 설명 · 지침 · 참고 자료 한 묶음</div>'''
    move = '''<div class="tline">
  <div class="tl"><b>2026.10.13</b><span>Gemini 앱에 Skills 출시</span></div>
  <div class="tl"><b>2026.11.17</b><span>Gem은 설정 메뉴로 이동</span></div>
  <div class="tl hl"><b>2027.3.1</b><span>Workspace 계정 Gem 종료</span></div>
</div>
<div class="homework"><b>이전</b> 기존 Gem → Skill 비활성 초안 · 검토 후 활성화</div>'''
    skillmd = ("---\n"
               "name: (내가 정한 이름 · 예: 응대)\n"
               "description: 편의점 거래처 문의에 1차 회신 초안을 쓴다\n"
               "---\n"
               "목표: 기준 안에서 신뢰를 지키는 회신\n"
               "판단: 문의 유형부터 구분 (결품 · 행사 · 단가 · 제품)\n"
               "규칙: 원인 확인 전 보상 약속 금지\n"
               "모를 때: 기준표에 없으면 [확인 필요]\n"
               "참고: 05 카탈로그 · 06 기준표 · 07 응대 가이드")
    mailmd = ("---\n"
              "name: (내가 정한 이름 · 예: 메일)\n"
              "description: 받는 사람과 요점 몇 줄을 주면 내 말투로 업무 메일 초안\n"
              "---\n"
              "목표: 내가 직접 쓴 것처럼 읽히는 메일\n"
              "말투: 참고 파일의 내 메일에서 호칭 · 인사 · 문장 길이 · 맺음말을 따름\n"
              "구성: 제목 / 인사 / 용건 / 요청 · 다음 일정 / 맺음\n"
              "규칙: 요점에 없는 약속 · 숫자는 쓰지 않음, 필요하면 [확인 필요]\n"
              "모를 때: 받는 사람 · 목적이 불분명하면 먼저 질문\n"
              "참고: 내가 보낸 메일 3~5통")
    return chapter("Ch2", "하네스와 Skills", {"Skills"}, "업무 매뉴얼 담당") + [
        ill("scenes_more", "harness_rig", "left40", "하네스: 모델에 채우는 장비",
            ["모델: 답을 만드는 엔진", "하네스: 지침 · 자료 · 도구 · 확인"]),
        light("모델과 하네스", harness, "Ch2"),
        light("하네스 네 부품", cards([
            ("지침", "Skills · Ch2", ["gemini"]),
            ("참고 자료", "Notebook · 참조 파일 · Ch1", ["notebooklm"]),
            ("도구 연결", "Workspace · Apps Script · Ch5", ["appsscript"]),
            ("사람 확인", "계획 확인 · 초안 검토 · 전 과정", []),
        ], 4), "Ch2"),
        light("봇에서 스킬로", bot, "Ch2"),
        light("AI 도구 모두 Skills로", trend, "Ch2"),
        light("Gem에서 Skills로", move, "Ch2"),
        ill(m, "secretary", "left40", "Skill: 저장해 두는 업무 지침", ["/이름으로 호출", "여러 Skill 조합"]),
        light("Skill의 구조", f'<div class="twocol">{code("Skill 한 개", skillmd)}{vl("이름 · 설명: 언제 쓸지", "목표 · 판단: 어떻게 할지", "모를 때: 멈추는 기준", "참고: 무엇을 근거로")}</div>', "Ch2"),
        light("Skill 이름은 내가 정함", f'''<div class="combo"><span>/응대</span><span>/주간보고</span><span>/정제</span></div>
{note("예시", "이름은 자유 · 호출은 설명(description)을 보고 판단")}''', "Ch2"),
        light("Skill 만드는 두 가지 방법", cards([
            ("직접 쓰기", "이름 · 설명 · 지침 · 참고 자료 입력", ["gemini"]),
            ("대화에서 만들기", "잘 된 대화 → 「이 대화를 Skill로」", ["gemini"]),
        ], 2), "Ch2"),
        ba("지침은 규칙 목록이 아니라 판단 기준", "Ch2",
           "결품 문의엔 '확인 후 연락드리겠습니다'라고 써.\n행사 문의엔 '가능합니다'라고 써.\n\n→ 처음 보는 문의엔 엉뚱한 답",
           "목표: 기준 안에서 신뢰를 지키는 회신\n문의 유형부터 구분하고, 근거 조항을 찾아 답할 것.\n기준표에 없으면 지어내지 말고 [확인 필요].\n\n→ 처음 보는 문의도 같은 기준으로"),
        ill(m, "conveyor", "top20", "지침은 매번 자동 적용", ["지침 품질 = 결과 품질"]),
        ill("scenes_ch1", "s6", "top20", "참조 파일은 참고 교재", ["수치는 사용자가 준 것만"], principle=1),
        light("Skills가 아직 못 하는 것", table(["항목", "현재 (2026.10)"], [
            ["<b>Canvas · Deep Research</b>", "Skill 안에서 미지원"],
            ["<b>참조 파일</b>", "텍스트 · PDF · 이미지"],
            ["<b>Drive 첨부 · 공유</b>", "곧 추가 예정"],
            ["<b>Workspace 앱</b>", "Connected Apps로 사용"],
        ]), "Ch2"),
        light("첫 Skill은 메일 초안", vl("매일 쓰는 일이라 효과가 바로 보임", "요점 몇 줄 → 내 말투의 메일 한 통", "말투는 지침과 예시 메일로 지정"), "Ch2"),
        light("말투를 지정하는 항목", table(["항목", "예시"], [
            ["<b>호칭</b>", "담당자님 · 팀장님"],
            ["<b>첫인사</b>", "안녕하세요, 수도권영업팀 김주현입니다."],
            ["<b>문장</b>", "한 단락 두 문장 이내 · 용건 먼저"],
            ["<b>맺음</b>", "감사합니다. 김주현 드림"],
            ["<b>피할 표현</b>", "과한 사과 · 「확정」 「무조건」"],
        ]) + note("가장 쉬운 방법", "내가 보낸 메일 3~5통을 참고 파일로"), "Ch2"),
        light("예시 메일 파일", '<div class="twocol">' + code("예시 1 · 미팅 후 감사", "제목: 8/26 미팅 감사 및 후속 일정 안내\n\n담당자님, 안녕하세요. 수도권영업팀 김주현입니다.\n\n어제 미팅에 시간 내주셔서 감사합니다.\n말씀하신 내용은 아래와 같이 정리했습니다.\n\n- 육개장사발면 진열 확대: 9월 미팅에서 확정\n- 신라면 블랙 가을 진열 제안서: 9/12(금)까지 전달\n\n감사합니다.\n김주현 드림")
              + vl("예시 5통: 감사 · 결품 회신 · 제안서 송부 · 일정 조율 · 사내 요청", "끝에 「내 메일의 공통점」 정리", "내 메일로 바꿔 넣어도 됨")
              + "</div>" + note("내려받기", dl("my_emails_sample.txt") + " · " + dl("my_emails_sample.docx")), "Ch2"),
        light("메일 Skill 지침", f'<div class="twocol">{code("메일 Skill (예시)", mailmd)}{vl("말투: 예시 메일에서 배움", "구성: 매번 같은 순서", "규칙: 없는 약속은 안 씀", "모를 때: 먼저 질문")}</div>', "Ch2"),
        ba("요점 세 줄 → 메일 한 통", "Ch2",
           "/메일\n받는 사람: C편의점 담당자D\n- 8/26 미팅 감사\n- 육개장사발면 진열 확대는 9월 미팅에서 확정\n- 신라면 블랙 가을 진열 제안서 9/12까지 전달",
           "제목: 8/26 미팅 감사 및 후속 일정 안내\n\n담당자님, 안녕하세요. 수도권영업팀 김주현입니다.\n지난 8/26 미팅에 시간 내주셔서 감사합니다.\n육개장사발면 진열 확대는 9월 미팅에서 확정하겠습니다.\n신라면 블랙 가을 진열 제안서는 9/12까지 보내 드리겠습니다.\n감사합니다. 김주현 드림"),
        lab("2-1", "내 말투 메일 Skill", "Ch2",
            "요점 세 줄만 주면 내 말투의 메일 초안",
            ["내 메일 3~5통을 문서 하나로 (없으면 예시 파일 · 이름 · 연락처 가리기)", "메일 Skill 지침 쓰기 · 예시 문서 참고 파일로", "새 대화에서 /이름 + 받는 사람 · 요점 세 줄", "어색한 곳을 지침에 한 줄씩 반영 → 다시 호출"],
            ["호칭 · 인사 · 맺음말이 평소와 같음", "요점에 없는 약속 · 숫자 없음", "요점만 바꿔 두 통 더 만들어도 같은 형식"], files=dl("my_emails_sample.txt") + " · " + dl("my_emails_sample.docx") + " · 또는 내 메일"),
        light("영업관리 Skill 예시", cards([
            ("메일", "요점 → 내 말투 메일", ["gmail"]),
            ("응대", "거래처 문의 1차 회신", ["gemini"]),
            ("매출 분석", "실적 미달 거래처 정리", ["sheets"]),
            ("주간 보고", "정해진 양식의 회의 보고문", ["docs"]),
            ("판촉 기획", "목표 · 예상 성과 · 위험 요인", ["gemini"]),
        ], 5), "Ch2"),
        light("응대 Skill 지침", code("응대 Skill (예시)", skillmd), "Ch2"),
        lab("2-2", "업무 Skill: 응대", "Ch2",
            "거래처 문의에 1차 회신 초안을 쓰는 Skill",
            ["이름 정하기 (예: 응대)", "목표 · 판단 · 모를 때 지침 쓰기", "참조 파일 05 · 06 · 07 추가", "새 대화에서 /이름으로 호출"],
            ["A편의점 결품 문의 → 응대 가이드 R-6 절차대로", "금지 표현 없음 · 5문장 이내"], files="05 · 06 · 07"),
        ill("scenes_ch5", "interview", "top20", "세 가지 입력으로 테스트",
            ["정상: A편의점 결품 문의", "기준표 밖: 북부대리점 행사 물량", "기준 위반: A마트 매대 3주"]),
        light("세 입력의 정답", table(["입력", "기대하는 답", "근거"], [
            ["<b>A편의점 결품</b>", "물류 확인 후 2영업일 안 재회신", "07 R-6 · 06 S-1"],
            ["<b>북부대리점 행사 물량</b>", "[확인 필요] · 팀장 확인", "06 P-1 · 07 R-5"],
            ["<b>A마트 매대 3주</b>", "최대 2주로 안내", "06 P-5"],
        ]), "Ch2"),
        ba("지침 한 줄 추가 전후", "Ch2",
           "문의: 신제품 A 결품, 보상 가능한가요?\n\n→ 불편을 드려 죄송합니다. 보상해 드리겠습니다.",
           "지침 추가: 원인 확인 전 보상 약속 금지\n\n→ 물류팀 확인 결과를 받은 뒤\n   2영업일 안에 다시 연락드리겠습니다."),
        lab("2-3", "세 가지 입력으로 고치기", "Ch2",
            "틀린 답을 찾아 지침 보완",
            ["세 입력을 차례로 테스트", "기대와 다른 답 표시", "지침에 판단 기준 한 줄 추가", "같은 입력으로 다시 테스트"],
            ["세 답 모두 근거 조항 번호", "북부대리점 → [확인 필요]", "A마트 → 최대 2주 (P-5)"], files="02 · 06 · 07"),
        light("Skill 조합", '''<div class="combo"><span>/응대</span><b>+</b><span>/회신 형식</span><b>=</b><span class="hl">기준 지킨 회신 초안</span></div>''', "Ch2"),
        bridge("다음: 숫자를 믿을 수 있게", "", "Ch2", "→ Ch3 데이터 정리 · 분석"),
    ]


# ── Ch3 데이터 ───────────────────────────────────────────
def ch3():
    m = "scenes_ch2"
    cols = ["기준월", "채널", "거래처", "SKU코드", "제품명", "카테고리", "발주수량", "납품수량", "단가", "매출액", "담당자"]
    row = ["2025-07", "편의점", "A편의점", "SKU-002", "스테디 B", "봉지면", "4,119", "3,995", "21,000", "83,895,000", "김주현"]
    db = ('<table class="dbt sm"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody><tr>"
          + "".join(f"<td>{c}</td>" for c in row) + "</tr><tr class=more>" + "".join("<td>⋮</td>" for _ in cols) + "</tr></tbody></table>")
    skill_md = ("---\n"
                "name: (내가 정한 이름 · 예: 정제)\n"
                "description: 판매 데이터 파일이 오면 마스터 구조로 정리\n"
                "---\n"
                "목표: 어떤 형식의 파일이든 마스터와 같은 구조로\n"
                "1. 열의 의미부터 파악 (이름 · 순서가 달라도)\n"
                "2. 거래처 · 제품은 참조 마스터에서 가장 가까운 값으로\n"
                "3. 같은 거래로 보이는 행은 하나로\n"
                "4. 수량 · 단가 · 금액이 안 맞으면 고치지 말고 표시\n"
                "5. 확신이 낮은 교정은 리포트에 따로\n"
                "참조: 거래처 마스터 · 05 제품카탈로그")
    return chapter("Ch3", "숫자를 믿을 수 있게 정리하기", {"Sheets", "Skills", "Drive · 웹앱"}, "데이터 엔지니어 · 분석가") + [
        ill(m, "tables", "top20", "AI가 잘 읽는 표", ["한 행에 한 건", "헤더는 한 줄", "병합 셀 없음"]),
        light("판매실적 원본 (01)", db + note("4,381행", "2025-07 ~ 2026-08 · 거래처 10곳 · 거래처 × SKU 월별"), "Ch3"),
        light("열 사이의 관계", cards([
            ("매출액", "납품수량 × 단가", ["sheets"]),
            ("결품률", "(발주 − 납품) ÷ 발주", ["sheets"]),
            ("전월 대비", "(이번 달 − 지난달) ÷ 지난달", ["sheets"]),
        ]), "Ch3"),
        light("원본의 흔한 오류", table(["오류", "원본", "정리 후"], [
            ["<b>띄어쓰기</b>", "B 편의점", "B편의점"],
            ["<b>오탈자</b>", "B편의졈", "B편의점"],
            ["<b>중복 행</b>", "같은 기준월 · 거래처 · SKU 2줄", "1줄"],
            ["<b>계산 불일치</b>", "매출액 ≠ 납품수량 × 단가", "표시 후 확인"],
        ]) + note("01 원본", "4,381행 → 정리 후 4,368행"), "Ch3"),
        ill("scenes_ch5", "conveyor", "top20", "규칙이 아니라 판단으로 정리", ["처음 보는 오탈자도 마스터에 맞춰 교정", "열 이름 · 순서가 달라도 처리"]),
        ba("정해진 규칙 vs Skill", "Ch3",
           "수식 · 스크립트\n\n정해 둔 규칙만 처리\n'B 편의점' → 규칙에 있으면 교정\n'B편의젬' → 규칙에 없으면 그대로\n열 순서가 바뀌면 오류",
           "Skill\n\n마스터와 비교해 판단\n'B편의젬' · 'ㅂ편의점'도 B편의점으로\n열 이름 · 순서가 달라도 읽음\n애매한 건 정제 리포트에 표시"),
        light("정제 Skill 지침", f'<div class="twocol">{code("Skill (예시)", skill_md)}{vl("목표", "판단 기준", "모를 때의 처리", "참조 마스터")}</div>', "Ch3"),
        light("외부 AI와 시트 안 Apps Script", table(["작업", "외부 AI (대화창)", "시트 안 Apps Script"], [
            ["<b>읽기</b>", "가능", "가능"],
            ["<b>새 파일 만들기</b>", "가능", "가능"],
            ["<b>기존 셀 수정</b>", "권한 거부", "가능"],
            ["<b>행 삭제 · 일괄 치환 · 행 추가</b>", "권한 거부", "가능"],
        ]) + note("이유", "Apps Script는 시트 소유자 권한으로 실행"), "Ch3"),
        light("정제 방식 두 가지", cards([
            ("A · 안전 분리형", "원본은 그대로<br/>정제본을 새 시트로 생성<br/>언제: 백업 · 변경 기록이 중요할 때", ["drive"]),
            ("B · 내부 직접 조작형", "Skill이 Apps Script 코드 생성<br/>시트에 커스텀 메뉴 · 버튼<br/>언제: 팀원이 버튼으로 품질 검사", ["appsscript"]),
        ], 2), "Ch3"),
        lab("3-1", "방식 A · 정제본 만들기", "Ch3",
            "원본은 두고 정제본 시트를 새로",
            ["정제 Skill 만들기 (이름은 자유)", "01 원본을 Drive에 올리고 대화에 첨부", "/내 Skill 이름으로 호출", "정제 리포트 확인 → 정제본 시트 생성"],
            ["정제본 4,368행 · 원본 4,381행 그대로", "편의점 8월 매출 14.21억 원"], files="01 · 04(대조용)"),
        lab("3-2", "방식 B · 시트 안 정제 메뉴", "Ch3",
            "버튼 한 번으로 시트 안에서 정제",
            ["Skill에 「이 시트용 정제 Apps Script 만들어 줘」", "확장 프로그램 → Apps Script에 붙여넣기 · 저장", "시트 새로고침 → 커스텀 메뉴 확인", "메뉴 실행 → 권한 승인(처음 한 번)"],
            ["메뉴 한 번으로 중복 · 띄어쓰기 정리", "실행 전 사본으로 백업"], files="01 사본"),
        ill(m, "navigation", "left40", "Sheets Gemini: 계획 먼저 확인", ["요청 → 계획 확인 → 실행"], principle=2),
        ba("데이터 설명 후 단계별 요청", "Ch3",
           "이 데이터 분석해 줘",
           "이 시트는 2025-07~2026-08 거래처 × SKU 월별 판매 실적이야.\n열은 기준월, 채널, 거래처, SKU코드, 제품명, 카테고리, 발주수량, 납품수량, 단가, 매출액, 담당자야.\n1단계로 2026-08 편의점 거래처별 매출과 전월 대비를 표로 만들어 줘.\n확인하고 다음 단계를 요청할게."),
        ill(m, "gauges", "top20", "값 대신 수식", ["값: 그대로", "수식: 다시 계산"]),
        ill("scenes_more", "pivot_bins", "top20", "피벗: 기준별로 묶어 합치기", ["행: 거래처 · 열: 기준월", "값: 매출액 합계"]),
        light("증감률은 수식으로", '<div class="twocol">' + code("전월 대비", "=(이번 달 매출 − 지난달 매출) / 지난달 매출\n\n14.21억 vs 13.36억 → +6.4%")
              + vl("값을 붙여 넣으면 원본이 바뀌어도 그대로", "수식이면 새 달이 들어오면 다시 계산") + "</div>", "Ch3"),
        ill(m, "two_sheets", "left40", "합계 두 개 직접 대조", ["총 매출 · 편의점 매출 SUM 대조"]),
        light("정답 숫자", table(["확인할 값", "예상 결과"], [
            ["정리 후 행 수", "4,368행"],
            ["편의점 8월 매출", "14.21억 원 (전월 대비 +6.4%)"],
            ["편의점 8월 결품률", "2.8%"],
            ["편의점 8월 SKU 매출 1위", "신제품 A 18.4%"],
        ]) + note("다르면", "대부분 정리 단계에서 빠뜨린 것"), "Ch3"),
        ill("scenes_extra", "fact_hypothesis", "left40", "사실과 가설 구분", ["사실: 시트의 숫자", "가설: 원인 추정"], principle=1),
        lab("3-3", "집계와 증감률", "Ch3",
            "정리된 시트로 8월 숫자 뽑기",
            ["사이드 패널에 데이터 설명 후 요청", "기준월 × 채널 피벗", "전월 대비 증감률 열 (수식)", "합계 두 개 SUM 대조"],
            ["증감률 셀이 수식", "정답 숫자 네 개와 일치"], files="정제본 또는 04"),
        bridge("다음: 숫자로 문서와 화면 만들기", "", "Ch3", "→ Ch4 문서 · 화면"),
    ]


# ── Ch4 문서 · 화면 ─────────────────────────────────────
def ch4():
    m = "scenes_ch3"
    proof = table(["제안서 문장", "근거"], [
        ["컵면 D 8월 매출 +21.0%", "03 리포트 6절 · 04 집계"],
        ["신제품 A 편의점 매출 1위 18.4%", "03 리포트 5절"],
        ["C편의점 MD의 진열 확대 요청", "02 미팅노트 4절"],
        ["행사 조건", "06 기준표 조항 번호"],
    ])
    return chapter("Ch4", "근거 있는 문서와 살아 있는 화면", {"Canvas"}, "프론트엔드 · 백엔드 개발자") + [
        ill(m, "chat_vs_workbench", "top20", "채팅은 대화, Canvas는 작업대", ["채팅: 흘러가는 답", "Canvas: 한 장을 두고 수정"]),
        ill(m, "mural", "top20", "전체 재생성 대신 부분 수정", []),
        ill(m, "briefing", "left40", "신입에게 업무를 맡기듯", ["역할 · 맥락 · 작업 · 형식"]),
        ba("제안서 요청", "Ch4",
           "편의점에 낼 제안서 써 줘",
           "너는 식품회사 국내영업 담당자야.\nC편의점 MD에게 신제품 A 가을 진열 확대를 제안하려고 해.\n첨부한 03 리포트 · 02 미팅노트 · 정리된 실적 시트를 근거로 1페이지 제안서를 써 줘.\n순서는 제안 배경, 제품 강점, 기대 효과(표), 지원 조건이고 과장 표현은 쓰지 마."),
        ill(m, "audience", "top20", "거래처마다 앞에 둘 내용",
            ["A편의점: 결품 해결 먼저", "B편의점: 행사 조건 (P-3)", "C편의점: 확대 효과 숫자"]),
        light("숫자마다 출처", proof, "Ch4"),
        lab("4-1", "1페이지 제안서", "Ch4",
            "C편의점 진열 확대 또는 B편의점 9월 행사 제안서",
            ["거래처 하나 고르기", "역할 · 맥락 · 작업 · 형식으로 요청", "두 곳 이상 부분 수정", "Docs로 내보내기"],
            ["모든 숫자가 03 · 04와 일치", "행사 조건은 06 조항 안"], files="02 · 03 · 04 · 06"),
        ill(m, "photo", "left40", "공유된 Canvas는 그 순간의 사진", []),
        ill("scenes_ch4", "photo_window", "top20", "사진과 창문", ["사진: 그때 숫자", "창문: 지금 숫자"]),
        light("정적 웹: 완성된 파일을 그대로", g.static_web(), "Ch4"),
        light("동적 웹: 열 때마다 데이터를 가져와 그림", g.dynamic_web(), "Ch4"),
        ill("scenes_ch4", "menu_board", "left40", "틀은 그대로, 데이터만 교체", ["화면 틀: Index.html", "데이터: 시트에서"]),
        ba("대시보드 요청", "Ch4",
           "실적 대시보드 만들어 줘",
           "정리된 판매실적 시트로 수도권영업팀 대시보드를 만들어 줘.\n채널 선택, KPI 카드 4개(매출 · 전월 대비, 목표 달성률, 취급 SKU, 결품률),\n최근 6개월 매출 추이, SKU 매출 상위 5, 이번 주 점검 항목 표.\n화면은 render(data) 함수 하나로 그리고, 데이터는 분리해 줘."),
        light("막히면 09 예시", '<div class="twocol">' + vl("09_대시보드_예시.html을 Canvas에 올려 열기", "틀(render)과 데이터(DATA)가 나뉜 구조", "Ch5에서 시트와 연결")
              + code("09 예시의 데이터 부분", 'const DATA = {\n  month: "2026-08",\n  channels: { "편의점": { sales: 1421193000, ... } }\n};\nrender(DATA);') + "</div>", "Ch4"),
        lab("4-2", "Canvas 대시보드 시제품", "Ch4",
            "채널을 고르면 숫자가 바뀌는 화면",
            ["대시보드 요청", "채널 바꿔 보기", "숫자 대조", "코드 보기 → 복사해 두기"],
            ["편의점 8월 14.21억 · +6.4%", "달성률 103% · SKU 38종 · 결품률 2.8%"], files="04 · 09(대체)"),
        bridge("다음: 화면을 시트와 잇기", "", "Ch4", "→ Ch5 연결 · 자동화"),
    ]


# ── Ch5 연결 · 자동화 ───────────────────────────────────
def ch5():
    m = "scenes_ch4"
    gas_code = ("function doGet() {\n"
                "  return HtmlService.createHtmlOutputFromFile('Index');\n"
                "}\n"
                "function getCleanedSalesData() {   // 시트 → 화면\n"
                "  return SpreadsheetApp.getActive()\n"
                "    .getSheetByName('판매실적_마스터').getDataRange().getValues();\n"
                "}\n"
                "function addSalesRecord(r) {       // 화면 → 시트\n"
                "  // 검증 · 매출액 = 납품수량 × 단가\n"
                "  sheet.appendRow([...]);\n"
                "}")
    return chapter("Ch5", "한 번 만들면 계속 돌아가게", {"Apps Script", "Drive · 웹앱", "Skills"}, "Ops 엔지니어") + [
        light("전체 구조", g.pipeline(), "Ch5"),
        light("원본은 잠그고, 웹앱이 대신 접근", g.proxy(), "Ch5"),
        ill(m, "hang_window", "left40", "Apps Script로 시트와 연결", ["Code.gs: 시트 ↔ 화면", "Index.html: 화면 틀", "URL 하나로 공유"]),
        light("Code.gs의 세 함수", code("Code.gs", gas_code), "Ch5"),
        ill("scenes_extra", "forms_inlet", "top20", "입구부터 반듯하게", ["드롭다운 · 자동완성", "오탈자 원천 차단"]),
        light("등록 버튼에서 시트까지", g.save_flow(), "Ch5"),
        light("처음부터 끝까지 다섯 단계", flow([("환경 준비", ".XLSX → Google 시트"), ("코드 받기", "Skill이 Code.gs · Index.html 생성"),
                                          ("코드 넣기", "Apps Script 붙여넣기 · 메뉴"), ("웹앱 배포", "실행: 나"), ("운영", "정제 → 누적 → 새로고침")], hl=3), "Ch5"),
        light("② 코드 받기", code("Skill에 요청", "이 시트의 열 구조를 먼저 읽고\n대시보드 웹앱용 Code.gs · Index.html을 만들어 줘.\n화면은 Ch4에서 만든 대시보드 그대로,\n데이터는 시트에서 받아 오게.\n시트 이름 · 열 이름은 실제 시트에 맞춰서."), "Ch5"),
        light("코드 넣기 · 배포 · 승인", table(["단계", "누르는 곳", "확인"], [
            ["<b>코드 넣기</b>", "확장 프로그램 → Apps Script → 파일 추가(+) → HTML", "파일 이름 Index (대소문자 그대로)"],
            ["<b>웹앱 배포</b>", "배포 → 새 배포 → 톱니바퀴 → 웹 앱", "실행: 나 · 액세스: 내 조직"],
            ["<b>권한 승인</b>", "액세스 승인 → 계정 선택", "경고 창: 고급 → 이동 → 허용"],
        ]) + note(".XLSX 파일", "Apps Script 메뉴가 안 보이면 파일 → Google 스프레드시트로 저장"), "Ch5"),
        light("자주 막히는 곳", table(["증상", "원인", "해결"], [
            ["<b>빈 화면</b>", "시트 이름 한 글자 차이", "getSheetByName 이름 확인"],
            ["<b>실행 안 됨</b>", "권한 승인 안 함", "메뉴 한 번 실행 → 승인"],
            ["<b>주소가 바뀜</b>", "고친 뒤 「새 배포」", "배포 관리 → 새 버전"],
        ]), "Ch5"),
        lab("5-1", "웹앱 대시보드", "Ch5",
            "시트와 연결된 대시보드 주소 받기",
            ["판매실적_마스터에서 Apps Script 열기", "Code.gs · Index.html 붙여넣기", "웹앱 배포 → 권한 승인", "웹 화면에서 한 건 등록"],
            ["옆 사람이 URL로 접속", "등록한 한 건이 시트와 화면에 반영"], files="판매실적_마스터 · 09(화면 틀)"),
        light("⑤ 운영: 매달 반복", flow([("새 원본 도착", ""), ("정제 Skill 실행", "검출 · 정제"), ("마스터에 누적", "append"), ("팀원 새로고침", "URL 그대로")], hl=1), "Ch5"),
        light("결과물의 연결", flow([("조사", "Ch1"), ("Skill", "Ch2"), ("숫자", "Ch3"), ("제안서 · 화면", "Ch4"), ("웹앱", "Ch5")]), "Ch5"),
    ]



# ── 최종 핸즈온 ─────────────────────────────────────────
ANSWER = Path(__file__).resolve().parent.parent / "docs" / "data" / "answer.json"


def final():
    import json
    a = json.loads(ANSWER.read_text()) if ANSWER.exists() else {}
    link = dl
    files = table(["파일", "내용"], [
        [link("store_check_raw.xlsx"), "정제 전 점검 기록 · 점포 / 제품 마스터 포함"],
        [link("store_check_clean.xlsx"), "정답 정제본 · 막혔을 때 다음 단계로"],
    ]) + note("가상 데이터", "제품명은 공개 제품명 · 점포 · 사람 · 수치는 모두 가상")
    cols = ["점검일", "지역", "점포코드", "점포명", "채널", "제품코드", "제품명", "카테고리", "진열면수", "적정재고", "실재고", "결품", "자사행사", "경쟁사행사", "점검자"]
    row = ["2026-08-10", "경기 남부", "S02", "A편의점 판교점", "편의점", "P01", "신라면", "봉지면", "4", "40", "0", "Y", "N", "N", "김주현"]
    db = ('<table class="dbt sm"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody><tr>"
          + "".join(f"<td>{c}</td>" for c in row) + "</tr><tr class=more>" + "".join("<td>⋮</td>" for _ in cols) + "</tr></tbody></table>")
    region = a.get("8월 지역별 결품률(%)", {})
    face = a.get("편의점 스낵 평균 진열면수(경쟁사 행사 有/無)", ["", ""])
    ans = table(["확인할 값", "정답"], [
        ["원본 → 정제 후 행 수", f'{a.get("원본 데이터 행 수(빈 행 제외)", "")}행 → {a.get("정제 후 행 수", "")}행'],
        ["8월 결품률", f'{a.get("8월 결품률(%)", "")}%'],
        ["8월 결품률 1위 제품", a.get("8월 결품률 1위 제품", "")],
        ["8월 결품률 가장 높은 지역", " · ".join(f"{k} {v}%" for k, v in sorted(region.items(), key=lambda x: -x[1])[:2])],
        ["편의점 스낵 진열면수 (경쟁사 행사 있음 / 없음)", f"{face[0]} / {face[1]}"],
        ["평균 재고충족률", f'{a.get("평균 재고충족률(%)", "")}%'],
    ])
    return chapter("최종", "핸즈온: 점포 점검 대시보드", {r[1] for r in ROLES}, "세 역할을 한 번에") + [
        light("만들 것", flow([("데이터 엔지니어링", "원본 정제"), ("데이터 분석", "결품 · 재고 · 진열"), ("웹앱 개발", "대시보드 · 현장 입력")], hl=2), "최종"),
        light("실습 데이터", files, "최종"),
        light("점검 기록의 구조", db + note("1,768건", "2026-07-06 ~ 09-28 · 주 1회 · 점포 14곳 · 제품 10종"), "최종"),
        light("열 사이의 관계", cards([
            ("결품", "실재고 = 0", ["sheets"]),
            ("재고충족률", "실재고 ÷ 적정재고", ["sheets"]),
            ("적정재고", "제품 기준 × 채널 배수", ["sheets"]),
        ]), "최종"),
        light("원본에 숨어 있는 문제", table(["문제", "예"], [
            ["<b>표 위의 제목 · 빈 행</b>", "1~2행 제목, 중간중간 빈 행"],
            ["<b>점포 · 제품 표기</b>", "B편의졈 홍대점 · 신 라면 · 辛라면 · 신라면블랙"],
            ["<b>날짜 형식</b>", "2026.08.10 · 8/10 · 26년 8월 10일"],
            ["<b>Y/N 표기</b>", "O · 예 · 있음 · X · 아니오 · 빈칸"],
            ["<b>숫자가 문자</b>", "12박스"],
            ["<b>중복 · 이상값</b>", "같은 점검 두 번 입력 · 자릿수 실수 (37 → 374)"],
        ]), "최종"),
        lab("F-1", "데이터 엔지니어링: 원본 정제", "최종",
            "점검 기록을 분석할 수 있는 표로",
            ["원본 내려받기 → Drive → Google 스프레드시트로 저장", "정제 Skill 만들기 (점포 · 제품 마스터를 기준으로)", "정제본 시트 새로 만들기 (원본은 그대로)", "이상값은 고치지 말고 표시 → 리포트 확인"],
            [f'정제 후 {a.get("정제 후 행 수", "")}행', "점포명 · 제품명이 마스터와 일치", "Y/N · 날짜 형식 통일"], files=link("store_check_raw.xlsx")),
        light("분석 질문", cards([
            ("어디서 비었나", "지역 × 제품 결품률", ["sheets"]),
            ("왜 비었나", "사실과 가설 구분", ["gemini"]),
            ("경쟁사 행사의 영향", "행사 유무별 진열면수", ["sheets"]),
            ("재고는 충분한가", "재고충족률", ["sheets"]),
        ], 4), "최종"),
        ill("scenes_more", "pivot_bins", "top20", "피벗으로 묶어 보기", ["행: 지역 · 열: 제품", "값: 결품 비율"]),
        lab("F-2", "데이터 분석: 결품과 진열", "최종",
            "8월 결품의 위치와 원인 후보 찾기",
            ["사이드 패널에 데이터 설명 후 단계별 요청", "지역 × 제품 결품률 피벗 (수식)", "경쟁사 행사 유무별 평균 진열면수", "사실과 가설을 나눠 세 줄 요약"],
            ["정답 숫자와 일치", "가설에는 「확인 필요」 표시"], files="F-1 정제본 · 막히면 " + link("store_check_clean.xlsx")),
        light("정답 숫자", ans, "최종"),
        light("대시보드 화면 구성", cards([
            ("KPI 카드", "점검 수 · 결품률 · 재고충족률", ["sheets"]),
            ("지역 × 제품 결품", "색으로 보는 표", ["docs"]),
            ("경쟁사 행사와 진열", "막대 비교", ["docs"]),
            ("현장 입력 폼", "점포 · 제품 드롭다운", ["appsscript"]),
        ], 4), "최종"),
        ba("대시보드 요청", "최종",
           "점검 대시보드 만들어 줘",
           "정제된 점검 기록 시트로 영업팀 대시보드를 만들어 줘.\n위: 기간 · 지역 선택, KPI 카드 3개(점검 수, 결품률, 재고충족률)\n가운데: 지역 × 제품 결품률 표(높을수록 진하게), 경쟁사 행사 유무별 진열면수 막대\n아래: 현장 점검 입력 폼(점포 · 제품은 마스터 드롭다운)\n화면은 render(data) 하나로 그리고 데이터는 분리해 줘."),
        lab("F-3", "웹앱 개발: 대시보드 배포", "최종",
            "팀원이 URL로 보고 입력하는 대시보드",
            ["Canvas로 화면 시제품 → 숫자 대조", "Skill에 「이 시트용 Code.gs · Index.html」 요청", "Apps Script 붙여넣기 → 웹앱 배포 (실행: 나)", "폼으로 점검 1건 입력 → 화면에 반영 확인"],
            ["옆 사람이 URL로 접속", "입력한 1건이 시트와 화면에 반영", "원본 시트는 공유 「제한됨」 그대로"], files="F-1 정제본 · 막히면 " + link("store_check_clean.xlsx")),
        bridge("원본 → 정제 → 분석 → 웹앱", "", "최종", "데이터 엔지니어 · 분석가 · 개발자 · Ops의 일을 한 흐름으로"),
    ]


# ── 적용 ────────────────────────────────────────────────
def apply_():
    kit = table(["구성", "내용"], [
        ["<b>필수 · Skill 세트</b>", "매출 분석 · 주간 보고 · 응대 (이름은 자유)"],
        ["<b>필수 · 근거 자료</b>", "정리된 시트 · 조사 보고서를 참조로"],
        ["<b>선택 · 화면</b>", "시트와 연결된 웹앱 대시보드"],
    ])
    return chapter("적용", "내 업무에 적용하기", {r[1] for r in ROLES}, "전체 도구") + [
        light("두 가지 원칙", cards([
            ("원칙 ① 근거를 쥐여 준다", "Ch1 오픈북 · Ch2 참조 파일", ["notebooklm", "gemini"]),
            ("원칙 ② 계획을 보여 줄 때 개입한다", "Ch1 Deep Research · Ch3 Sheets 계획 확인", ["gemini", "sheets", "appsscript"]),
        ], 2), "적용"),
        ill("scenes_ch5", "construction", "top20", "작게 끝내기",
            ["Before: 팀 전체 영업 관리 시스템", "After: 내 방문 메모 정리 Skill"]),
        light("월요일 아침 브리핑 키트", kit, "적용"),
        light("트랙 선택", cards([
            ("문서 · 제안", "Canvas + Skill<br/>예: 판촉 성과 비교", ["docs", "gemini"]),
            ("대시보드", "Sheets + Canvas + Apps Script<br/>예: 담당 채널 대시보드", ["sheets", "docs", "appsscript"]),
            ("현장 입력", "Sheets + Apps Script<br/>예: 점검 입력 웹앱", ["sheets", "appsscript"]),
        ]), "적용"),
        light("평가 기준", f'''<div class="score">
  <div class="sc"><b>30</b><span>실제 업무 적합성</span></div><div class="sc"><b>30</b><span>계산 · 분석 정확도</span></div>
  <div class="sc"><b>25</b><span>실행 완성도</span></div><div class="sc"><b>15</b><span>사용성 · 확장성</span></div>
</div>
<div class="homework"><b>완료</b> 분석 1 + 계산 1 + 자동화 시연 1</div>''', "적용"),
        lab("6-1", "내 업무 Skill 세트", "적용",
            "월요일 아침 업무를 Skill로",
            ["반복 업무 세 개 고르기", "Skill 만들기 · 이름 정하기", "새 대화에서 차례로 호출", "손으로 할 때와 시간 비교"],
            ["옆 사람이 불러도 같은 형식", "숫자는 시트와 일치"], files="04 · 내 업무 자료"),
        light("발표 구성", flow([("문제", ""), ("데모", ""), ("전후 비교", "")], hl=1), "적용"),
        bridge("작은 자동화부터 2주 시범 운영", "", "적용", "운영 계정 · 데이터 정책 → 2주 파일럿 → 개선"),
    ]


def slides():
    return opening() + ch1() + ch2() + ch3() + ch4() + ch5() + final()


CSS = g.CSS + '''
  .dl{color:#F28C28; font-weight:800; font-family:var(--mono); text-decoration:none;}
  .kcards.c5{grid-template-columns:repeat(5,1fr);}
  .dbt.sm{font-size:13px;} .dbt.sm th, .dbt.sm td{padding:9px 7px;}
'''
