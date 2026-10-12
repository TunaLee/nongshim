"""도입부 슬라이드: 표지 · 강사 · 목차 · 코드 레드 역전 · 밈 · 생태계 · 간지.

어두운 남색 바탕에 주황 강조. 아이콘은 assets/icons/ (Wikimedia Commons, Public domain·CC0).
"""

ICON = "assets/icons/{}.svg"
NAMES = {
    "gemini": "Gemini", "notebooklm": "NotebookLM", "docs": "Docs", "sheets": "Sheets",
    "slides": "Slides", "gmail": "Gmail", "drive": "Drive", "meet": "Meet",
    "calendar": "Calendar", "vids": "Vids", "aistudio": "AI Studio", "appsscript": "Apps Script",
}

# 장 번호, 날, 제목, 설명, 아이콘
CHAPTERS = [
    ("CH1", 1, "Gemini 기본기", "프롬프트 작성법 · Gems로 나만의 비서 만들기", ["gemini"]),
    ("CH2", 1, "근거 있는 답변", "Deep Research로 자료 조사, NotebookLM으로 내 자료 분석", ["gemini", "notebooklm"]),
    ("CH3", 1, "Workspace 속 Gemini", "메일 · 문서 · 시트 · 회의에서 Gemini 활용", ["gmail", "docs", "sheets", "meet"]),
    ("CH4", 2, "콘텐츠 만들기", "Canvas · 슬라이드 · 영상 초안 제작", ["slides", "vids"]),
    ("CH5", 2, "AI Studio", "모델 비교와 프롬프트 다듬기", ["aistudio"]),
    ("CH6", 2, "자동화", "Apps Script로 시트 · 메일 · 캘린더 연동", ["appsscript", "sheets", "calendar"]),
    ("CH7", 2, "실전 과제", "내 업무 하나를 Gemini로 개선하기", ["drive"]),
]


def icon(name, cls="ic"):
    return f'<span class="{cls}"><img src="{ICON.format(name)}" alt="{NAMES[name]}"/></span>'


def coord():
    return '<div class="coord"><b></b> / <span class="tot"></span></div>'


def cover():
    strip = "".join(icon(n, "tile") for n in NAMES)
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">GOOGLE AI 실무 · 2일 과정</div>
  <h1>구글 AI로 일하는 이틀</h1>
  <div class="strip">{strip}</div>
</section>'''


def speaker():
    rows = [
        ("2026 —", "제피트", "대표", True),
        ("2025 —", "왕진연구소", "AI 엔지니어", False),
        ("2024 —", "부트캠프", "강사", False),
        ("2020 — 2023", "클레온", "AI 엔지니어", False),
    ]
    tl = "".join(
        f'<div class="row{" now" if cur else ""}"><span class="yr">{y}</span><span class="org">{o}</span><span class="role">{r}</span></div>'
        for y, o, r, cur in rows)
    return f'''<section class="slide dk" data-title="강사 소개">
  {coord()}
  <div class="speaker">
    <div class="photo"><img src="assets/speaker.jpg" alt="강사 사진"/></div>
    <div class="who">
      <div class="kick">강사 소개</div>
      <h2 class="name">이동원</h2>
      <div class="sub">AI 엔지니어 · 강사 · 창업가 · devtuna.kr</div>
      <div class="tl">{tl}</div>
    </div>
  </div>
</section>'''


def agenda():
    def col(day):
        rows = "".join(
            f'''<div class="ch"><span class="chip">{c}</span><div class="tx"><b>{t}</b><span>{d}</span></div>
<div class="icons">{"".join(icon(n) for n in ics)}</div></div>'''
            for c, dd, t, d, ics in CHAPTERS if dd == day)
        label = "첫째 날" if day == 1 else "둘째 날"
        return f'<div class="daycol"><div class="dayhead">{label}</div>{rows}</div>'
    return f'''<section class="slide dk" data-title="목차">
  {coord()}
  <div class="kick">2일 과정</div>
  <h2>목차</h2>
  <div class="days">{col(1)}{col(2)}</div>
</section>'''


def codered():
    # x 위치는 시간 비례 (2022.11 = 0, 2025.12 = 37개월)
    ev = [
        (0, "2022.11", "ChatGPT 공개", "", False, "up"),
        (1, "2022.12", "구글, 코드 레드 선언", "", True, "down"),
        (3, "2023.02", "Bard 시연 중 오답", "알파벳 시총 하루 약 1,000억 달러 증발", False, "up"),
        (13, "2023.12", "Gemini 1.0 공개", "", False, "down"),
        (15, "2024.02", "Bard → Gemini 개명", "", False, "up"),
        (36, "2025.11", "Gemini 3 공개", "", False, "down"),
        (37, "2025.12", "OpenAI, 코드 레드 선언", "", True, "up"),
    ]
    x0, x1 = 110, 1150
    def X(m):
        return x0 + (x1 - x0) * m / 37
    # 37개월 끝 두 사건이 붙어 있어 라벨을 좌우로 벌린다
    nudge = {5: -70, 6: 0, 0: 0, 1: 30}
    parts = [f'<line x1="{x0-20}" y1="250" x2="{x1+30}" y2="250" stroke="rgba(255,255,255,.25)" stroke-width="3"/>']
    for yr, m in (("2023", 2), ("2024", 14), ("2025", 26)):
        parts.append(f'<line x1="{X(m)}" y1="240" x2="{X(m)}" y2="260" stroke="rgba(255,255,255,.25)" stroke-width="2"/>'
                     f'<text x="{X(m)+6}" y="276" class="yr">{yr}</text>')
    for i, (m, d, t, s, red, side) in enumerate(ev):
        x = X(m)
        lx = x + nudge.get(i, 0)
        col = "#F28C28" if red else "#FFFFFF"
        r = 11 if red else 7
        if side == "up":
            ty = 0 if i == 0 else 70
            parts.append(f'<line x1="{x}" y1="250" x2="{lx}" y2="{ty+58}" stroke="rgba(255,255,255,.3)" stroke-width="1.5"/>')
        else:
            parts.append(f'<line x1="{x}" y1="250" x2="{lx}" y2="330" stroke="rgba(255,255,255,.3)" stroke-width="1.5"/>')
            ty = 350
        anchor = "end" if lx > 1000 else "start"
        ax = lx
        parts.append(f'<circle cx="{x}" cy="250" r="{r}" fill="{col}"/>')
        parts.append(f'<text x="{ax}" y="{ty}" text-anchor="{anchor}" class="d{" red" if red else ""}">{d}</text>'
                     f'<text x="{ax}" y="{ty+26}" text-anchor="{anchor}" class="t{" red" if red else ""}">{t}</text>'
                     f'<text x="{ax}" y="{ty+48}" text-anchor="{anchor}" class="s">{s}</text>')
    svg = "".join(parts)
    return f'''<section class="slide dk" data-title="뒤바뀐 처지">
  {coord()}
  <div class="kick">왜 지금 구글인가</div>
  <h2>3년 만에 뒤바뀐 구글과 OpenAI의 처지</h2>
  <div class="tlwrap"><svg viewBox="0 0 1160 420" class="tlsvg">{svg}</svg></div>
</section>'''


def meme():
    return f'''<section class="slide dk" data-title="꿈을 이룬 Gemini">
  {coord()}
  <div class="kick">밈으로 보는 판도</div>
  <h2>꿈을 이룬 Gemini</h2>
  <div class="memes">
    <figure><img src="assets/meme-dream.jpg" alt="가운데 머리가 되는 꿈을 꾸는 Gemini 밈"/><figcaption><b>과거</b></figcaption></figure>
    <div class="arrow">→</div>
    <figure><img src="assets/meme-now.jpg" alt="가운데 머리가 된 Gemini 밈"/><figcaption><b>현재</b></figcaption></figure>
  </div>
</section>'''


def ecosystem(active=None):
    """active 가 없으면 전체 지도. 있으면 앞 장은 켜고, 이번 장은 강조하고, 뒤 장은 흐리게."""
    hub = (640, 430)
    nodes = {  # 장 → 카드 중심
        "CH1": (250, 255), "CH2": (640, 215), "CH3": (1030, 255),
        "CH6": (250, 590), "CH5": (640, 650), "CH4": (1030, 590),
    }

    def state(c):
        if active is None:
            return "all"
        n, k = int(c[2:]), int(active[2:])
        return "done" if n < k else "on" if n == k else "dim"

    lines = []
    for c, (x, y) in nodes.items():
        st = state(c)
        if st == "all":
            lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#F28C28" stroke-width="2.5" stroke-dasharray="6 7" opacity=".7"/>')
        elif st == "done":
            lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#FFFFFF" stroke-width="2.5" opacity=".45"/>')
        elif st == "dim":
            lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="4 8" opacity=".12"/>')
        else:
            lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#F28C28" stroke-width="5" opacity=".35"/>'
                         f'<line class="flow" x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#F28C28" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 12"/>')
    cards = []
    for c, dd, t, d, ics in CHAPTERS:
        if c not in nodes:
            continue
        x, y = nodes[c]
        cards.append(f'''<div class="node {state(c)}" style="left:{x-182}px; top:{y-46}px">
  <div class="nh"><span class="chip">{c}</span><b>{t}</b></div>
  <div class="icons">{"".join(icon(n) + f'<span class="nm">{NAMES[n]}</span>' for n in ics)}</div>
</div>''')
    if active is None:
        kick, h2, title = "구글 생태계", "Gemini로 연결되는 구글 도구", "구글 생태계 지도"
        cap = "all"
    else:
        name = next(t for c, _, t, _, _ in CHAPTERS if c == active)
        kick, h2, title = f"구글 생태계 · {active}", f"{name}에서 쓰는 도구", f"[{active}] 생태계 지도"
        cap = "on" if active == "CH7" else "dim"
    return f'''<section class="slide dk eco{' focus' if active else ''}" data-title="{title}">
  {coord()}
  <div class="kick">{kick}</div>
  <h2>{h2}</h2>
  <svg class="ecosvg" viewBox="0 0 1280 720">{"".join(lines)}</svg>
  {"".join(cards)}
  <div class="hub" style="left:{hub[0]-74}px; top:{hub[1]-74}px"><img src="{ICON.format("gemini")}" alt="Gemini"/></div>
  <div class="hubcap {cap}" style="left:{hub[0]-160}px; top:{hub[1]+84}px"><span class="chip">CH7</span> 실전 과제</div>
</section>'''


DIVIDERS = {
    "CH2": ("근거 있는 답변", ["Deep Research", "NotebookLM", "출처 확인"]),
}


def divider(ch):
    title, chips = DIVIDERS[ch]
    num = ch[2:].zfill(2)
    return f'''<section class="slide dk divider" data-title="[{ch}] {title}">
  <div class="ghost">{num}</div>
  <div class="kick">CHAPTER {num}</div>
  <h2 class="big">{title}</h2>
  <div class="agenda2">{"".join(f"<span>{c}</span>" for c in chips)}</div>
</section>'''


def chapter_open(ch):
    """챕터 시작마다 간지 + 그 장이 켜진 생태계 지도."""
    return [divider(ch), ecosystem(ch)]


def slides():
    return [cover(), speaker(), agenda(), codered(), meme(), ecosystem()] + chapter_open("CH2")


CSS = '''
  /* ── 도입부: 어두운 남색 + 주황 ── */
  .slide.dk{background:radial-gradient(900px 520px at 85% -10%, #2A4C78 0%, rgba(42,76,120,0) 60%), #0F1B2D; color:#fff; border:none; padding:52px 64px 44px;}
  .dk .kick{font-family:var(--serif); font-size:15px; font-weight:700; letter-spacing:.02em; color:#F28C28; text-transform:uppercase;}
  .dk h2{font-size:40px; line-height:1.15; letter-spacing:-.03em; font-weight:800; margin:12px 0 0;}
  .dk .sub{font-size:17px; color:rgba(255,255,255,.7); margin-top:10px;}
  .dk .coord{color:rgba(255,255,255,.45);} .dk .coord b{color:#fff;}
  .dk .chip{display:inline-block; font-family:var(--mono); font-size:12px; font-weight:700; color:#0F1B2D; background:#F28C28; border-radius:6px; padding:3px 8px; flex:none;}
  .dk .ic{width:34px; height:34px; border-radius:9px; background:#fff; display:inline-grid; place-items:center; flex:none;}
  .dk .ic img{width:22px; height:22px; object-fit:contain;}
  .dk .key{margin-top:auto; border-left:4px solid #F28C28; padding:6px 0 6px 16px; font-size:18px; color:rgba(255,255,255,.92);}
  .dk .key .k{font-family:var(--mono); font-size:12px; letter-spacing:.12em; color:#F28C28; margin-right:12px;}

  .cover-dk{justify-content:center; padding:0 80px;}
  .cover-dk .glow{position:absolute; right:-160px; top:-160px; width:560px; height:560px; border-radius:50%; background:radial-gradient(circle, rgba(242,140,40,.28), rgba(242,140,40,0) 65%);}
  .cover-dk h1{font-size:68px; line-height:1.08; letter-spacing:-.035em; font-weight:800; margin:22px 0 0; position:relative;}
  .cover-dk .strip{display:flex; gap:12px; margin-top:56px; position:relative;}
  .cover-dk .tile{width:58px; height:58px; border-radius:15px; background:#fff; display:grid; place-items:center; box-shadow:0 10px 24px -12px rgba(0,0,0,.6);}
  .cover-dk .tile img{width:34px; height:34px; object-fit:contain;}

  .speaker{display:grid; grid-template-columns:330px 1fr; gap:60px; align-items:center; height:100%;}
  .speaker .photo{width:330px; height:440px; border-radius:22px; overflow:hidden; background:#fff; box-shadow:0 30px 60px -30px rgba(0,0,0,.7);}
  .speaker .photo img{width:100%; height:100%; object-fit:cover; object-position:50% 30%;}
  .speaker .name{font-size:56px; margin-top:14px;}
  .speaker .tl{margin-top:34px; display:flex; flex-direction:column; gap:4px; border-left:2px solid rgba(255,255,255,.18); padding-left:22px;}
  .speaker .row{display:grid; grid-template-columns:150px 140px 1fr; align-items:baseline; padding:9px 0; font-size:18px;}
  .speaker .yr{font-family:var(--mono); font-size:14px; color:rgba(255,255,255,.5);}
  .speaker .org{font-weight:800;}
  .speaker .role{color:rgba(255,255,255,.72);}
  .speaker .row.now .yr{color:#F28C28;}

  .days{display:grid; grid-template-columns:1fr 1fr; gap:28px; margin-top:28px; flex:1; min-height:0;}
  .daycol{display:flex; flex-direction:column; gap:12px;}
  .dayhead{font-size:15px; font-weight:800; color:#F28C28; letter-spacing:.04em; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,.15);}
  .ch{display:flex; align-items:center; gap:14px; background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1); border-radius:12px; padding:14px 16px;}
  .ch .tx{flex:1; display:flex; flex-direction:column; gap:3px; min-width:0;}
  .ch .tx b{font-size:19px;} .ch .tx span{font-size:14px; color:rgba(255,255,255,.65);}
  .ch .icons{display:flex; gap:6px;}

  .tlwrap{flex:1; min-height:0; display:flex; align-items:center; margin-top:10px;}
  .tlsvg{width:100%; height:auto; overflow:visible;}
  .tlsvg text{font-family:var(--serif); fill:#fff;}
  .tlsvg .yr{font-family:var(--mono); font-size:13px; fill:rgba(255,255,255,.45);}
  .tlsvg .d{font-family:var(--mono); font-size:14px; fill:rgba(255,255,255,.55);}
  .tlsvg .t{font-size:19px; font-weight:800;}
  .tlsvg .s{font-size:13.5px; fill:rgba(255,255,255,.62);}
  .tlsvg .red{fill:#F28C28;}

  .memes{flex:1; min-height:0; display:flex; align-items:center; justify-content:center; gap:26px; margin-top:16px;}
  .memes figure{margin:0; display:flex; flex-direction:column; gap:12px; align-items:center;}
  .memes img{height:430px; width:auto; border-radius:14px; box-shadow:0 30px 60px -30px rgba(0,0,0,.8);}
  .memes figure:first-child img{height:auto; width:470px;}
  .memes figcaption{font-size:16px; color:rgba(255,255,255,.75);}
  .memes figcaption b{color:#F28C28; margin-right:8px;}
  .memes .arrow{font-size:44px; color:#F28C28; font-weight:800;}

  .eco .ecosvg{position:absolute; inset:0; width:1280px; height:720px;}
  .eco .node{position:absolute; width:364px; background:#16263D; border:1px solid rgba(255,255,255,.14); border-radius:14px; padding:12px 14px; display:flex; flex-direction:column; gap:10px; z-index:2;}
  .eco .nh{display:flex; align-items:center; gap:10px; font-size:17px;}
  .eco .icons{display:flex; align-items:center; gap:6px; flex-wrap:wrap;}
  .eco .nm{font-size:12px; color:rgba(255,255,255,.7); margin-right:3px;}
  .eco .hub{position:absolute; width:148px; height:148px; border-radius:50%; background:#fff; display:grid; place-items:center; z-index:2; box-shadow:0 0 0 10px rgba(242,140,40,.18), 0 0 60px 10px rgba(242,140,40,.35);}
  .eco .hub img{width:84px; height:84px;}
  .eco .hubcap{position:absolute; width:320px; text-align:center; font-size:15px; color:rgba(255,255,255,.8); z-index:2;} .eco .hubcap{background:#0F1B2D; padding:4px 0;}

  .eco .node{transition:none;}
  .eco .node.done > *{opacity:.85;}
  .eco .node.dim{background:#111D30; border-color:rgba(255,255,255,.06);}
  .eco .node.dim > *{opacity:.28; filter:grayscale(1);}
  .eco .node.on{border:2px solid #F28C28; background:#22344F; box-shadow:0 0 0 6px rgba(242,140,40,.15), 0 0 40px 4px rgba(242,140,40,.35); transform:scale(1.06);}
  .eco .node.done .chip{background:rgba(255,255,255,.75);}
  .eco .hubcap.dim{opacity:.3;}
  .eco .flow{animation:flow 1.1s linear infinite;}
  @keyframes flow{to{stroke-dashoffset:-52;}}
  @media print{ .eco .flow{animation:none;} }
  .divider{justify-content:center;}
  .divider .ghost{position:absolute; right:40px; bottom:-60px; font-family:var(--mono); font-weight:700; font-size:320px; line-height:.8; color:rgba(255,255,255,.06);}
  .divider .big{font-size:56px; margin-top:16px;}
  .divider .agenda2{display:flex; gap:10px; margin-top:24px;}
  .divider .agenda2 span{font-size:14px; font-weight:600; border:1px solid rgba(255,255,255,.3); border-radius:999px; padding:6px 14px; background:rgba(255,255,255,.06);}
'''
