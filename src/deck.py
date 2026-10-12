"""이론 덱 전체 구성. 실습 · 따라하기 장은 별도 덱에 있다.

장 종류
  ill      그림 장 — 장면(SVG) + 빈 구역에 제목과 3줄 이내 본문
  ba       프롬프트 장 — Before / After 두 칸
  diagram  도식 장 — 카드 · 흐름
  dark     표지 · 간지 · 생태계 지도
"""
import importlib

import explain
import intro
from intro import ICON, NAMES, coord, icon

N, G, O = "#1F3A5F", "#D9DDE3", "#F28C28"


# ── 장면 ────────────────────────────────────────────────
def scene(mod, fn):
    """장면 함수를 찾고, 아직 없으면 회색 자리 표시를 돌려준다."""
    try:
        return getattr(importlib.import_module(mod), fn)()
    except (ImportError, AttributeError):
        return (f'<rect x="560" y="200" width="660" height="460" rx="18" fill="{G}"/>'
                f'<text x="890" y="440" text-anchor="middle" font-size="22" fill="{N}">이미지 준비 중 · {fn}</text>')


PRINCIPLES = {1: "근거를 쥐여 준다", 2: "계획을 보여 줄 때 개입한다"}


def badge(n):
    return f'<div class="pbadge"><span class="pn">원칙 {"①②"[n-1]}</span>{PRINCIPLES[n]}</div>' if n else ""


# ── 장 만들기 ────────────────────────────────────────────
def ill(mod, fn, zone, title, lines=(), principle=0, extra=""):
    pos = "left" if zone == "left40" else "top"
    body = "".join(f"<li>{l}</li>" for l in lines)
    return f'''<section class="slide ill" data-title="{title}">
  <svg class="scene" viewBox="0 0 1280 720" aria-hidden="true">{scene(mod, fn)}</svg>
  {coord()}{badge(principle)}
  <div class="cap {pos}{' z25' if zone == 'top25' else ''}"><h2>{title}</h2>{'<div class="bar"></div>' if pos == 'left' else ''}{f'<ul>{body}</ul>' if body else ''}</div>
  {extra}
</section>'''


def light(title, body, ch, principle=0):
    return f'''<section class="slide lt" data-title="{title}">
  {coord()}{badge(principle)}
  <div class="eyebrow"><span class="tag">{ch}</span></div>
  <h2 class="s-title sm">{title}</h2>
  <div class="rule"></div>
  <div class="body"><div class="mid">{body}</div></div>
</section>'''


def ba(title, ch, before, after, note="", principle=0):
    def esc(t):
        return t.replace("\n", "<br/>")
    nb = f'<div class="banote">{note}</div>' if note else ""
    return light(title, f'''<div class="ba">
  <div class="b"><div class="lab">Before</div><div class="q">{esc(before)}</div></div>
  <div class="arr">→</div>
  <div class="a"><div class="lab">After</div><div class="q">{esc(after)}</div></div>
</div>{nb}''', ch, principle)


def cards(items, cols=3):
    """items: (머리, 본문, 아이콘 목록)"""
    out = []
    for h, p, ics in items:
        ic = "".join(icon(n) for n in ics)
        out.append(f'<div class="kcard">{f"<div class=icons>{ic}</div>" if ic else ""}<h4>{h}</h4><p>{p}</p></div>')
    return f'<div class="kcards c{cols}">{"".join(out)}</div>'


def flow(steps, hl=None):
    out = []
    for i, (h, p) in enumerate(steps):
        cls = " hl" if hl is not None and i == hl else ""
        out.append(f'<div class="fs{cls}"><b>{h}</b>{f"<span>{p}</span>" if p else ""}</div>')
    return '<div class="flow">' + '<div class="fa">→</div>'.join(out) + "</div>"


def bridge(title, question, ch, nxt):
    return f'''<section class="slide dk bridge" data-title="{title}">
  {coord()}
  <div class="kick">{ch} 정리</div>
  <h2>{title}</h2>
  <div class="q">{question}</div>
  <div class="nxt">{nxt}</div>
</section>'''


# ── 생태계 지도 ───────────────────────────────────────────
# 역할, 도구, 아이콘, 처음 쓰는 장. 위치는 그림 ⑨와 같은 시계 방향.
ROLES = [
    ("리서치 담당", "Deep Research", ["gemini"], "Ch1", (250, 255)),
    ("검토자", "NotebookLM", ["notebooklm"], "Ch1", (640, 215)),
    ("데이터 창고", "Sheets", ["sheets"], "Ch2", (1030, 255)),
    ("작업대", "Canvas", ["docs"], "Ch3", (1030, 590)),
    ("자동화 담당", "Apps Script · Studio", ["appsscript"], "Ch4", (640, 650)),
    ("전담 비서", "Gem", ["gemini"], "Ch5", (250, 590)),
]
ACTIVE = {
    "Ch1": {"리서치 담당", "검토자"}, "Ch2": {"데이터 창고"}, "Ch3": {"작업대"},
    "Ch4": {"작업대", "자동화 담당"}, "Ch5": {"전담 비서"},
    "Day 2": {r[0] for r in ROLES},
}
ORDER = ["Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Day 2"]


def eco(ch=None, title=None):
    hub = (640, 430)

    def state(role, first):
        if ch is None:
            return "all"
        if role in ACTIVE[ch]:
            return "on"
        return "done" if ORDER.index(first) < ORDER.index(ch) else "dim"

    lines, cards_ = [], []
    for role, tool, ics, first, (x, y) in ROLES:
        st = state(role, first)
        line = {
            "all": f'stroke="{O}" stroke-width="2.5" stroke-dasharray="6 7" opacity=".7"',
            "done": 'stroke="#fff" stroke-width="2.5" opacity=".45"',
            "dim": 'stroke="#fff" stroke-width="2" stroke-dasharray="4 8" opacity=".12"',
            "on": f'stroke="{O}" stroke-width="5" opacity=".35"',
        }[st]
        lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" {line}/>')
        if st == "on":
            lines.append(f'<line class="flow" x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="{O}" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 12"/>')
        cards_.append(f'''<div class="node {st}" style="left:{x-170}px; top:{y-44}px">
  <div class="nh"><span class="chip">{first}</span><b>{role}</b></div>
  <div class="icons">{"".join(icon(n) for n in ics)}<span class="nm">{tool}</span></div>
</div>''')
    if ch is None:
        kick, h2, dt = "구글 생태계", title or "Gemini를 중심으로 여섯 동료가 연결됩니다", "생태계 지도"
    else:
        kick, h2, dt = f"구글 생태계 · {ch}", title, f"[{ch}] 생태계 지도"
    return f'''<section class="slide dk eco{' focus' if ch else ''}" data-title="{dt}">
  {coord()}
  <div class="kick">{kick}</div>
  <h2>{h2}</h2>
  <svg class="ecosvg" viewBox="0 0 1280 720">{"".join(lines)}</svg>
  {"".join(cards_)}
  <div class="hub" style="left:{hub[0]-74}px; top:{hub[1]-74}px"><img src="{ICON.format("gemini")}" alt="Gemini"/></div>
</section>'''


def divider(ch, title, sub):
    num = ch[2:].zfill(2) if ch.startswith("Ch") else "D2"
    return f'''<section class="slide dk divider" data-title="[{ch}] {title}">
  <div class="ghost">{num}</div>
  <div class="kick">{ch}</div>
  <h2 class="big">{title}</h2>
  {f'<div class="sub">{sub}</div>' if sub else ''}
</section>'''


def chapter(ch, title, sub, map_title):
    return [divider(ch, title, sub), eco(ch, map_title)]


# ── 오프닝 ───────────────────────────────────────────────
def cover():
    strip = "".join(icon(n, "tile") for n in ["gemini", "notebooklm", "sheets", "docs", "appsscript", "gmail", "drive", "calendar"])
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">생성형 AI 중급 과정 · 국내영업</div>
  <h1>AI로 일하는 방식을<br/>바꾸는 이틀</h1>
  <div class="strip">{strip}</div>
</section>'''


def o02():
    left = "".join(f"<span>{t}</span>" for t in ["질문하기", "요약하기", "초안 쓰기"])
    right = "".join(f"<span>{t}</span>" for t in ["조사 · 검증", "데이터 정리", "문서와 화면", "자동화", "전담 비서"])
    return light("초급에서는 AI에게 물었고, 이번엔 AI로 일을 잇습니다", f'''<div class="lvl">
  <div class="col"><div class="h">초급 10회</div><div class="sub">AI에게 묻는다</div><div class="chips2">{left}</div></div>
  <div class="arr">→</div>
  <div class="col hl"><div class="h">중급 이틀</div><div class="sub">AI로 일을 잇는다</div><div class="chips2">{right}</div></div>
</div>''', "오프닝")


AGENDA = [
    ("Ch1", "근거 있는 조사", "출처가 붙은 조사 보고서", ["gemini", "notebooklm"]),
    ("Ch2", "숫자 정리", "정리된 실적 시트", ["sheets"]),
    ("Ch3", "제안서", "1페이지 제안서", ["docs"]),
    ("Ch4", "화면 · 자동화", "실시간 대시보드와 주간 메일", ["appsscript", "gmail"]),
    ("Ch5", "전담 비서", "업무 전용 Gem", ["gemini"]),
]


def agenda():
    rows = "".join(f'''<div class="ch"><span class="chip">{c}</span><div class="tx"><b>{t}</b><span>{d}</span></div>
<div class="icons">{"".join(icon(n) for n in ics)}</div></div>''' for c, t, d, ics in AGENDA)
    day2 = '''<div class="ch"><span class="chip">Day 2</span><div class="tx"><b>내 업무에 적용</b><span>내 업무 결과물 하나</span></div></div>'''
    return f'''<section class="slide dk" data-title="목차">
  {coord()}
  <div class="kick">목차</div>
  <h2>첫날은 다섯 가지를 만들고, 둘째 날은 내 업무에 씁니다</h2>
  <div class="days">
    <div class="daycol"><div class="dayhead">첫째 날</div>{rows}</div>
    <div class="daycol"><div class="dayhead">둘째 날</div>{day2}</div>
  </div>
</section>'''


def o05():
    return light("이틀 동안 하나의 가상 시나리오로 진행합니다", f'''<div class="scen">
  <div class="who">가상 거래처 <b>A편의점 본부</b> · 4분기 신제품 입점 제안 준비</div>
  {flow([("조사", "Ch1"), ("숫자 정리", "Ch2"), ("제안서", "Ch3"), ("대시보드 · 주간 메일", "Ch4"), ("응대 Gem", "Ch5")])}
</div>''', "오프닝")


def o06():
    return light("이틀 동안 세 가지만 약속합니다", cards([
        ("실제 데이터는 넣지 않기", "회사 · 거래처 실제 자료 대신 가상 예시만 씁니다", []),
        ("막히면 바로 손들기", "혼자 붙잡고 있는 10분이 가장 아깝습니다", []),
        ("먼저 끝나면 옆 사람 돕기", "설명해 보면 내 것도 한 번 더 정리됩니다", []),
    ]), "오프닝")


# ── Ch1 ─────────────────────────────────────────────────
CH1_ILL = [
    ("s1", "left40", "AI 답, 그대로 써도 될까요?", 0),
    ("s2", "top25", "AI는 모를 때도 문장을 완성한다", 0),
    ("s3", "top20", "AI가 모르는 두 가지: 최신 정보, 우리 회사", 0),
    ("s4", "top20", "근거를 찾아오게 하거나, 근거 안에 가두거나", 0),
    ("s5", "left40", "Deep Research는 계획부터 세운다", 2),
    ("s6", "top20", "노트북은 오픈북 시험이다", 1),
    ("s7", "top20", "같은 질문, 세 가지 답", 0),
    ("s8", "left40", "AI 답의 품질은 근거의 품질이다", 1),
]


def ch1():
    out = chapter("Ch1", "근거 있는 답을 받는 법", "Deep Research와 NotebookLM", "Ch1에서는 리서치 담당과 검토자를 만납니다")
    for (fn, zone, title, pr), ex in zip(CH1_ILL, explain.SLIDES):
        out.append(ill("scenes_ch1", fn, zone, title, principle=pr))
        out.append(ex())
    out.append(light("이틀 동안 지킬 원칙 두 가지가 여기서 나옵니다", cards([
        ("원칙 ① 근거를 쥐여 준다", "오픈북 시험처럼 볼 자료를 정해 주면 답이 자료를 벗어나지 않습니다", ["notebooklm"]),
        ("원칙 ② 계획을 보여 줄 때 개입한다", "실행 전에 계획을 고치는 것이 결과를 고치는 것보다 쉽습니다", ["gemini"]),
    ], 2), "Ch1"))
    return out


# ── Ch2 ─────────────────────────────────────────────────
def ch2():
    m = "scenes_ch2"
    return chapter("Ch2", "숫자를 믿을 수 있게 정리하기", "확인한 숫자를 다음 챕터의 재료로", "Ch2에서는 데이터 창고를 정리합니다") + [
        ill(m, "tables", "top20", "AI가 잘 읽는 표는 사람이 보기 좋은 표와 다릅니다",
            ["한 행에 한 건", "헤더는 한 줄", "병합 셀 없음"]),
        ba("데이터를 먼저 설명하고, 한 단계씩 요청합니다", "Ch2",
           "이 데이터 정리해 줘",
           "이 시트는 거래처별 월 매출이야.\n열은 월, 지역, 거래처 유형, 품목, 매출액이야.\n1단계로 거래처명 표기만 통일해 줘.\n확인하고 다음 단계를 요청할게."),
        ill(m, "navigation", "left40", "Sheets의 Gemini도 계획을 먼저 보여 줍니다",
            ["요청 → 계획 확인 → 실행", "계획 확인은 사람이 합니다", "Ch1과 같은 원칙입니다"], principle=2),
        ill(m, "gauges", "top20", "값이 아니라 수식으로 받아야 합니다",
            ["값: 원본이 바뀌어도 그대로", "수식: 원본이 바뀌면 다시 계산", "수식이어야 Ch4 자동화가 됩니다"]),
        ill(m, "two_sheets", "left40", "AI 집계는 두 개만 직접 대조합니다",
            ["전부 다시 계산할 필요는 없습니다", "합계 두 개를 SUM으로 맞춰 봅니다", "오류가 나면 Gemini의 수정 제안을 씁니다"]),
        bridge("정리된 숫자가 다음 세 챕터의 재료입니다", "이 숫자로 제안서를 어떻게 빠르게 쓸까요?", "Ch2", "→ Ch3 제안서 · Ch4 대시보드 · Ch5 Gem"),
    ]


# ── Ch3 ─────────────────────────────────────────────────
def ch3():
    m = "scenes_ch3"
    return chapter("Ch3", "근거 있는 제안서를 빠르게", "검증한 내용과 정리한 숫자로 쓰는 1페이지", "Ch3에서는 작업대를 씁니다") + [
        ill(m, "chat_vs_workbench", "top20", "채팅은 대화, Canvas는 작업대입니다",
            ["채팅: 주고받으며 답이 흘러갑니다", "Canvas: 결과물 한 장을 두고 고칩니다"]),
        ill(m, "mural", "top20", "전체를 다시 만들면 좋은 부분까지 바뀝니다",
            ["전체 재생성: 좋던 문장도 바뀝니다", "부분 수정: 고칠 곳만 골라 요청합니다"]),
        ill(m, "briefing", "left40", "제안서 요청은 신입에게 일을 맡기는 것과 같습니다",
            ["역할 · 맥락 · 작업 · 형식", "네 가지를 알려 주면", "한 번에 쓸 만한 초안이 나옵니다"]),
        ba("역할, 맥락, 작업, 형식을 갖추면 초안이 달라집니다", "Ch3",
           "편의점에 낼 제안서 써 줘",
           "너는 식품회사 국내영업 담당자야.\nA편의점 본부 바이어에게 신제품 입점을 제안하려고 해.\n첨부한 검증 완료 보고서와 실적 시트 숫자를 근거로 1페이지 제안서를 써 줘.\n순서는 제안 배경, 제품 강점, 기대 효과(표), 지원 조건이고 과장 표현은 쓰지 마.",
           "역할 · 맥락 · 작업 · 형식"),
        ill(m, "audience", "top20", "받는 사람의 상황에 따라 앞에 둘 내용이 다릅니다",
            ["신규: 브랜드 신뢰와 초기 지원", "기존: 지난 실적과 확대 효과", "이탈 위험: 문제 해결과 조건 개선"]),
        ill(m, "photo", "left40", "공유된 Canvas는 그 순간의 사진입니다",
            ["공유하면 그 시점 모습이 전달됩니다", "문서라면 이걸로 충분합니다", "숫자가 바뀌는 화면이라면?"]),
    ]


# ── Ch4 ─────────────────────────────────────────────────
def ch4():
    m = "scenes_ch4"
    sc = '<div class="capbox">캡처: Sheets canvas 화면</div>'
    return chapter("Ch4", "한 번 만들면 계속 돌아가게", "화면은 살아 있게, 반복은 자동으로", "Ch4에서는 작업대와 자동화 담당이 함께 일합니다") + [
        ill(m, "photo_window", "top20", "붙여 넣은 화면은 사진, 연결된 화면은 창문입니다",
            ["사진: 붙여 넣은 그때의 숫자", "창문: 시트와 연결된 지금 숫자"]),
        ill(m, "hang_window", "left40", "Apps Script가 대시보드를 시트와 연결해 걸어 줍니다",
            ["Canvas 대시보드는 아직 사진입니다", "Apps Script가 시트와 이어 줍니다", "주소 하나로 팀에 공유합니다"]),
        ill(m, "menu_board", "left40", "화면은 그대로 두고 데이터만 갈아 끼웁니다",
            ["메뉴판 틀은 그대로, 가격표만 교체", "화면은 render(rows) 하나로 요청"]),
        ba("대시보드는 화면과 데이터를 나눠 달라고 요청합니다", "Ch4",
           "실적 대시보드 만들어 줘",
           "'실적' 시트의 지역, 월, 매출액으로\n지역별 월 매출 막대그래프와 전월 대비 증감률 표가 있는 대시보드를 만들어 줘.\n화면은 render(rows) 함수 하나로 그리고,\n데이터는 나중에 시트에서 받을 수 있게 분리해 줘."),
        light("곧 시트 안에서 바로 대시보드를 만들게 됩니다", f'''<div class="twocol">
  <div class="vl"><p>시트 안에서 만드는 실시간 대시보드</p><p>지금은 영어로 설정된 계정에서만 쓸 수 있습니다</p></div>
  {sc}
</div>''', "Ch4"),
        ill(m, "alarm", "left40", "자동화는 '언제'와 '무엇을'로 나뉩니다",
            ["언제: 매주 월요일 8시, 메일 도착 시", "무엇을: 읽고, 요약하고, 보내기"]),
        ill(m, "two_tools", "top20", "자동화 도구에는 맞춤 제작형과 주문형이 있습니다",
            ["Apps Script: 코드로 만드는 맞춤 제작", "Workspace Studio: 말로 하는 주문"]),
        ba("언제, 어디서, 무엇을 정확히 말합니다", "Ch4",
           "매주 실적 메일 자동으로 보내 줘",
           "'실적' 시트의 A~E열을 읽어서\n매주 월요일 오전 8시에\n지난주 지역별 매출 합계를 표로 만들어\n내 메일로 보내 줘.",
           "언제 · 어디서 · 무엇을"),
        ill(m, "domino", "top20", "말로 설명하면 Studio가 흐름을 만들어 줍니다",
            ["할 일을 말하면 단계가 만들어집니다", "단계 검토는 사람이 합니다"], principle=2),
        ill(m, "envelope_fly", "left40", "테스트 실행도 진짜로 보냅니다",
            ["테스트도 실제로 메일을 보냅니다", "파일도 실제로 바뀝니다", "실습 수신자는 반드시 본인"]),
        bridge("매번 같은 지시를 반복하고 있지 않나요?", "긴 설명을 매번 다시 쓰고 있다면, 저장해 둘 때입니다", "Ch4", "→ Ch5 전담 비서 Gem"),
    ]


# ── Ch5 ─────────────────────────────────────────────────
def ch5():
    m = "scenes_ch5"
    return chapter("Ch5", "반복되는 지시를 저장하는 나만의 비서", "", "Ch5에서는 전담 비서를 둡니다") + [
        ill(m, "secretary", "left40", "Gem은 업무 매뉴얼을 숙지한 전담 비서입니다",
            ["긴 설명을 한 번만 저장합니다", "말을 걸면 바로 그 역할로 일합니다"]),
        ill(m, "conveyor", "top20", "지침은 매 대화 앞에 자동으로 붙는 프롬프트입니다",
            ["짧은 요청 앞에 지침이 붙습니다", "지침의 품질이 곧 Gem의 품질입니다"]),
        ill("scenes_ch1", "s6", "top20", "지식 파일은 Gem이 펴 놓는 교재입니다",
            ["오픈북 시험, 다시", "규칙: 수치는 사용자가 준 것만"], principle=1),
        ba("지침은 역할, 입력, 출력, 규칙, 예시로 씁니다", "Ch5",
           "너는 방문일지 정리 도우미야",
           "역할: 방문일지 정리 도우미\n입력: 방문 메모\n출력: 일시, 거래처, 논의, 요청, 후속 조치\n규칙: 메모에 없는 내용은 지어내지 않기, 불분명하면 [확인 필요]\n예시: 첨부 파일 형식 따르기",
           "역할 · 입력 · 출력 · 규칙 · 예시"),
        ill(m, "interview", "top20", "Gem 테스트는 세 종류 질문으로 보는 면접입니다",
            ["정상 입력 → 형식대로 정리", "정보 부족 → [확인 필요] 표시", "금지 문의 → 정중히 거절 · 안내"]),
        ba("지침 한 줄이 답을 바꿉니다", "Ch5",
           "메모: 3/12 A편의점 본부, 신제품 3종 소개. 반응 괜찮음.\n\n→ 신제품 3종 입점 확정, 다음 달 첫 발주 예정",
           "지침 추가: 메모에 없는 내용은 지어내지 마\n\n→ 논의: 신제품 3종 소개\n→ 요청: [확인 필요]\n→ 후속 조치: [확인 필요]",
           "같은 메모, 지침 한 줄 차이"),
        ill(m, "agent_morning", "top20", "Gem과 Studio를 합치면 에이전트가 됩니다",
            ["Gem은 전문성, Studio는 언제와 무엇을", "문의 도착 → 답장 초안 → 담당자 알림", "자동 발송은 하지 않고 사람이 확인"]),
        light("오늘 만든 다섯 가지는 하나로 이어집니다", f'''{flow([("조사", "Ch1"), ("숫자", "Ch2"), ("제안서", "Ch3"), ("대시보드 · 메일", "Ch4"), ("Gem", "Ch5")])}
<div class="homework"><b>숙제</b> 내 업무에서 만들 것 하나 떠올려 오기</div>''', "Ch5"),
    ]


# ── Day 2 ───────────────────────────────────────────────
def day2():
    return chapter("Day 2", "내 업무에 적용하기", "", "둘째 날은 여섯 동료를 모두 씁니다") + [
        light("어제를 관통한 원칙은 두 가지입니다", cards([
            ("원칙 ① 근거를 쥐여 준다", "Ch1 오픈북 · Ch5 지식 파일", ["notebooklm", "gemini"]),
            ("원칙 ② 계획을 보여 줄 때 개입한다", "Ch1 Deep Research · Ch2 Sheets · Ch4 Studio", ["gemini", "sheets", "appsscript"]),
        ], 2), "Day 2"),
        ill("scenes_ch5", "construction", "top20", "작게 끝내는 쪽이 이깁니다",
            ["Before: 팀 전체 영업 관리 시스템", "After: 내 방문 메모 저녁 정리 흐름"]),
        light("세 가지 트랙 중 하나를 고릅니다", cards([
            ("문서 · 제안", "Canvas + Gem", ["docs", "gemini"]),
            ("대시보드", "Sheets + Canvas + Apps Script", ["sheets", "docs", "appsscript"]),
            ("자동화", "Workspace Studio + Gem", ["appsscript", "gemini"]),
        ]), "Day 2"),
        light("발표는 2분, 문제와 데모와 전후 비교입니다", flow([("문제", "무엇이 불편했나"), ("데모", "직접 보여 주기"), ("전후 비교", "얼마나 달라졌나")], hl=1), "Day 2"),
    ]


# ── 오프닝 이어 붙이기 ─────────────────────────────────────
# 그림 ⑨ 이름표 자리 (scenes_ch2.office_map 의 label 위치와 같다)
TAGS = [((400, 344), "리서치 · Deep Research"), ((880, 344), "검토자 · NotebookLM"), ((1112, 500), "데이터 창고 · Sheets"),
        ((880, 654), "작업대 · Canvas"), ((420, 654), "자동화 · Apps Script · Studio"), ((168, 500), "전담 비서 · Gem")]


def tags():
    return "".join(f'<div class="tagl" style="left:{x-107}px; top:{y}px">{t}</div>' for (x, y), t in TAGS)


def opening():
    return [
        cover(),
        intro.speaker(),
        intro.codered(),
        intro.meme(),
        o02(),
        ill("scenes_ch2", "desk_outputs", "top25", "첫날이 끝나면 책상 위에 결과물 다섯 가지가 남습니다"),
        agenda(),
        ill("scenes_ch2", "office_map", "top20", "오늘 쓰는 도구는 역할이 다른 동료입니다", extra=tags()),
        eco(None),
        o05(),
        o06(),
    ]


def slides():
    return opening() + ch1() + ch2() + ch3() + ch4() + ch5() + day2()


CSS = '''
  /* ── 그림 장 ── */
  .slide.ill{padding:0; background:#fff; border:none;}
  .slide.ill svg.scene{position:absolute; inset:0; width:1280px; height:720px;}
  .ill .cap{position:absolute; z-index:2; color:#1F3A5F;}
  .ill .cap h2{margin:0; font-weight:800; letter-spacing:-.03em; word-break:keep-all;}
  .ill .cap ul{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:8px;}
  .ill .cap li{position:relative; padding-left:16px; color:#1F3A5F; word-break:keep-all;}
  .ill .cap li::before{content:""; position:absolute; left:0; top:.62em; width:7px; height:7px; border-radius:50%; background:#F28C28;}
  .ill .cap.left{left:72px; top:0; bottom:0; width:410px; display:flex; flex-direction:column; justify-content:center;}
  .ill .cap.left h2{font-size:40px; line-height:1.22;}
  .ill .cap.left .bar{width:56px; height:5px; border-radius:3px; background:#F28C28; margin:22px 0 20px;}
  .ill .cap.left li{font-size:19px; line-height:1.5;}
  .ill .cap.top{left:72px; right:150px; top:34px; display:grid; grid-template-columns:1.35fr 1fr; gap:36px; align-items:start;}
  .ill .cap.top h2{font-size:31px; line-height:1.25;}
  .ill .cap.top ul{padding-top:4px; gap:5px;}
  .ill .cap.top li{font-size:16px; line-height:1.45;}
  .ill .cap.top.z25 h2{font-size:34px;}
  .ill .coord{z-index:3;}
  .ill .tagl{position:absolute; z-index:2; width:214px; height:24px; line-height:24px; text-align:center; font-size:12.5px; font-weight:700; color:#1F3A5F; letter-spacing:-.02em;}
  .pbadge{position:absolute; right:40px; top:56px; z-index:3; display:flex; align-items:center; gap:8px; font-size:12.5px; font-weight:700; color:#1F3A5F; background:#FFF3E6; border:1px solid #F7C99A; border-radius:999px; padding:5px 12px 5px 6px;}
  .pbadge .pn{background:#F28C28; color:#fff; border-radius:999px; padding:2px 8px; font-size:11.5px;}
  .slide.dk .pbadge{top:56px;}

  /* ── 밝은 본문 장 ── */
  .slide.lt .eyebrow .tag{font-family:var(--serif);}
  .ba{display:grid; grid-template-columns:1fr 56px 1.5fr; align-items:stretch;}
  .ba .b, .ba .a{border-radius:16px; padding:24px 26px; display:flex; flex-direction:column; gap:14px;}
  .ba .b{background:#EEF1F5; border:1px solid #DDE2E9;}
  .ba .a{background:#fff; border:2px solid #F28C28; box-shadow:0 18px 40px -26px rgba(242,140,40,.6);}
  .ba .lab{font-family:var(--mono); font-size:13px; font-weight:700; letter-spacing:.08em; color:#8A94A6; text-transform:uppercase;}
  .ba .a .lab{color:#F28C28;}
  .ba .q{font-size:18.5px; line-height:1.65; color:#16233A; word-break:keep-all;}
  .ba .b .q{color:#44506A;}
  .ba .arr{display:grid; place-items:center; font-size:30px; color:#F28C28; font-weight:800;}
  .banote{margin-top:4px; font-size:15px; color:#44506A;}
  .banote::before{content:"구성  "; font-weight:800; color:#F28C28;}
  .kcards{display:grid; gap:18px;} .kcards.c2{grid-template-columns:1fr 1fr;} .kcards.c3{grid-template-columns:repeat(3,1fr);}
  .kcard{background:#fff; border:1px solid #E1E5EB; border-top:4px solid #1F3A5F; border-radius:10px; padding:24px 24px 26px; display:flex; flex-direction:column; gap:10px;}
  .kcard h4{margin:0; font-size:22px; font-weight:800; color:#16233A; word-break:keep-all;}
  .kcard p{margin:0; font-size:16.5px; line-height:1.55; color:#44506A; word-break:keep-all;}
  .kcard .icons{display:flex; gap:8px; margin-bottom:4px;}
  .kcard .ic, .lt .ic{width:38px; height:38px; border-radius:10px; background:#F6F8FA; border:1px solid #E1E5EB; display:inline-grid; place-items:center;}
  .kcard .ic img{width:24px; height:24px;}
  .flow{display:flex; align-items:stretch; gap:0;}
  .flow .fs{flex:1; background:#fff; border:1px solid #E1E5EB; border-top:4px solid #1F3A5F; border-radius:10px; padding:18px 14px; text-align:center; display:flex; flex-direction:column; gap:6px; justify-content:center;}
  .flow .fs b{font-size:19px; color:#16233A;} .flow .fs span{font-size:14px; color:#8A94A6;}
  .flow .fs.hl{border-top-color:#F28C28; box-shadow:0 18px 40px -26px rgba(242,140,40,.6);}
  .flow .fa{display:grid; place-items:center; padding:0 8px; color:#F28C28; font-weight:800; font-size:22px;}
  .lvl{display:grid; grid-template-columns:1fr 70px 1.4fr; align-items:stretch;}
  .lvl .col{background:#EEF1F5; border-radius:16px; padding:26px 28px; display:flex; flex-direction:column; gap:8px;}
  .lvl .col.hl{background:#fff; border:2px solid #F28C28;}
  .lvl .h{font-size:24px; font-weight:800; color:#16233A;} .lvl .sub{font-size:15px; color:#8A94A6; margin-bottom:10px;}
  .lvl .arr{display:grid; place-items:center; font-size:34px; color:#F28C28; font-weight:800;}
  .chips2{display:flex; flex-wrap:wrap; gap:10px;}
  .chips2 span{font-size:17px; font-weight:700; color:#1F3A5F; background:#fff; border:1px solid #D9DDE3; border-radius:999px; padding:8px 16px;}
  .lvl .col.hl .chips2 span{background:#FFF3E6; border-color:#F7C99A;}
  .scen{display:flex; flex-direction:column; gap:28px;}
  .scen .who{font-size:21px; color:#16233A; background:#EEF1F5; border-radius:12px; padding:18px 22px;}
  .scen .who b{color:#F28C28;}
  .homework{margin-top:30px; font-size:20px; color:#16233A; border-left:4px solid #F28C28; padding:8px 0 8px 18px;}
  .homework b{color:#F28C28; margin-right:12px;}
  .capbox{background:#D9DDE3; border-radius:14px; height:300px; display:grid; place-items:center; font-size:18px; font-weight:700; color:#1F3A5F;}
  .vl p{font-size:20px; color:#16233A; margin:0 0 12px; padding-left:16px; border-left:4px solid #F28C28;}

  /* ── 어두운 정리 장 ── */
  .bridge{justify-content:center;}
  .bridge h2{font-size:44px; max-width:24ch; word-break:keep-all;}
  .dk h2, .s-title{word-break:keep-all;}
  .bridge .q{margin-top:30px; font-size:22px; color:rgba(255,255,255,.85); border-left:4px solid #F28C28; padding:6px 0 6px 18px;}
  .bridge .nxt{margin-top:26px; font-size:16px; color:#F28C28; font-weight:700;}
  .divider .sub{font-size:20px; color:rgba(255,255,255,.7); margin-top:16px;}
  .eco .node{width:340px;}
  .eco .nm{font-size:13px;}
'''
