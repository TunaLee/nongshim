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
    ("CH1", 1, "Gemini 기본기", "프롬프트 구조 · Gems로 나만의 비서 만들기", ["gemini"]),
    ("CH2", 1, "근거 있는 답", "Deep Research로 찾아오고, NotebookLM으로 가두기", ["gemini", "notebooklm"]),
    ("CH3", 1, "Workspace 속 Gemini", "메일 · 문서 · 시트 · 회의록을 한 흐름으로", ["gmail", "docs", "sheets", "meet"]),
    ("CH4", 2, "보여 주는 AI", "Canvas · 슬라이드 · 영상 초안", ["slides", "vids"]),
    ("CH5", 2, "AI Studio", "모델을 골라 시험하고 프롬프트를 다듬는 작업대", ["aistudio"]),
    ("CH6", 2, "자동화", "Apps Script로 시트 · 메일 · 캘린더 잇기", ["appsscript", "sheets", "calendar"]),
    ("CH7", 2, "실전 과제", "자기 업무 하나를 Gemini 흐름으로 바꾸기", ["drive"]),
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
      <div class="kick">SPEAKER</div>
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
    return f'''<section class="slide dk" data-title="이틀의 목차">
  {coord()}
  <div class="kick">AGENDA</div>
  <h2>이틀 동안 다루는 일곱 장</h2>
  <div class="days">{col(1)}{col(2)}</div>
</section>'''


def codered():
    # x 위치는 시간 비례 (2022.11 = 0, 2025.12 = 37개월)
    ev = [
        (0, "2022.11", "ChatGPT 공개", "OpenAI", False, "up"),
        (1, "2022.12", "구글 사내 「코드 레드」", "검색 사업 위기 경보", True, "down"),
        (3, "2023.02", "Bard 시연 오답", "알파벳 시총 하루 약 1,000억 달러 증발", False, "up"),
        (13, "2023.12", "Gemini 1.0", "Bard 뒤를 잇는 모델", False, "down"),
        (15, "2024.02", "Bard → Gemini", "이름까지 바꿔 다시 시작", False, "up"),
        (36, "2025.11", "Gemini 3 공개", "추론 · 코딩 벤치마크 선두권", False, "down"),
        (37, "2025.12", "OpenAI 사내 「코드 레드」", "ChatGPT 개선에 인력 집중", True, "up"),
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
    return f'''<section class="slide dk" data-title="3년 만에 뒤집힌 코드 레드">
  {coord()}
  <div class="kick">WHY GOOGLE, NOW</div>
  <h2>3년 만에 방향이 뒤집힌 「코드 레드」</h2>
  <div class="tlwrap"><svg viewBox="0 0 1160 420" class="tlsvg">{svg}</svg></div>
  <div class="key"><span class="k">흐름</span>2022년 경보를 울린 쪽은 구글이었고, 2025년에는 OpenAI였다.</div>
</section>'''


def meme():
    return f'''<section class="slide dk" data-title="꿈이 현실이 된 가운데 머리">
  {coord()}
  <div class="kick">MEANWHILE</div>
  <h2>꿈속의 가운데 머리가 현실이 된 Gemini</h2>
  <div class="memes">
    <figure><img src="assets/meme-dream.jpg" alt="가운데 머리가 되는 꿈을 꾸는 Gemini 밈"/><figcaption><b>그때</b> 가운데 머리는 꿈속에서만</figcaption></figure>
    <div class="arrow">→</div>
    <figure><img src="assets/meme-now.jpg" alt="가운데 머리가 된 Gemini 밈"/><figcaption><b>지금</b> 나머지 머리가 땀을 흘린다</figcaption></figure>
  </div>
</section>'''


def ecosystem():
    hub = (640, 430)
    nodes = {  # 장 → 카드 중심
        "CH1": (250, 255), "CH2": (640, 215), "CH3": (1030, 255),
        "CH6": (250, 590), "CH5": (640, 650), "CH4": (1030, 590),
    }
    lines = "".join(
        f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#F28C28" stroke-width="2.5" stroke-dasharray="6 7" opacity=".7"/>'
        for x, y in nodes.values())
    cards = []
    for c, dd, t, d, ics in CHAPTERS:
        if c not in nodes:
            continue
        x, y = nodes[c]
        cards.append(f'''<div class="node" style="left:{x-182}px; top:{y-46}px">
  <div class="nh"><span class="chip">{c}</span><b>{t}</b></div>
  <div class="icons">{"".join(icon(n) + f'<span class="nm">{NAMES[n]}</span>' for n in ics)}</div>
</div>''')
    return f'''<section class="slide dk eco" data-title="구글 생태계 지도">
  {coord()}
  <div class="kick">ECOSYSTEM</div>
  <h2>Gemini 하나에 묶인 구글 도구</h2>
  <svg class="ecosvg" viewBox="0 0 1280 720">{lines}</svg>
  {"".join(cards)}
  <div class="hub" style="left:{hub[0]-74}px; top:{hub[1]-74}px"><img src="{ICON.format("gemini")}" alt="Gemini"/></div>
  <div class="hubcap" style="left:{hub[0]-160}px; top:{hub[1]+84}px"><span class="chip">CH7</span> 실전 과제에서 전부 엮는다</div>
</section>'''


def divider():
    return '''<section class="slide dk divider" data-title="[CH2] 근거 있는 답">
  <div class="ghost">02</div>
  <div class="kick">CHAPTER 02</div>
  <h2 class="big">근거 있는 답</h2>
  <div class="agenda2"><span>Deep Research</span><span>NotebookLM</span><span>출처 확인</span></div>
</section>'''


def slides():
    return [cover(), speaker(), agenda(), codered(), meme(), ecosystem(), divider()]


CSS = '''
  /* ── 도입부: 어두운 남색 + 주황 ── */
  .slide.dk{background:radial-gradient(900px 520px at 85% -10%, #2A4C78 0%, rgba(42,76,120,0) 60%), #0F1B2D; color:#fff; border:none; padding:52px 64px 44px;}
  .dk .kick{font-family:var(--mono); font-size:13px; font-weight:700; letter-spacing:.16em; color:#F28C28; text-transform:uppercase;}
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

  .divider{justify-content:center;}
  .divider .ghost{position:absolute; right:40px; bottom:-60px; font-family:var(--mono); font-weight:700; font-size:320px; line-height:.8; color:rgba(255,255,255,.06);}
  .divider .big{font-size:56px; margin-top:16px;}
  .divider .agenda2{display:flex; gap:10px; margin-top:24px;}
  .divider .agenda2 span{font-size:14px; font-weight:600; border:1px solid rgba(255,255,255,.3); border-radius:999px; padding:6px 14px; background:rgba(255,255,255,.06);}
'''
