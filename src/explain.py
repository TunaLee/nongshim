"""그림 장 뒤에 붙는 설명 장 8개. 템플릿 컴포넌트만 쓴다."""

N, G, O = "#1F3A5F", "#D9DDE3", "#F28C28"


def page(title, body, key_label, key, sub="근거 있는 답변", badge=""):
    return f'''<section class="slide" data-title="{title}">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="eyebrow"><span class="tag">Ch1</span><span class="dot"></span>{sub}</div>
  {badge}
  <h2 class="s-title sm">{title}</h2>
  <div class="rule"></div>
  <div class="body">
    <div class="mid">{body}</div>
    {f'<div class="keymsg"><span class="k">{key_label}</span><div>{key}</div></div>' if key else ''}
  </div>
</section>'''


def biglist(items):
    return '<div class="biglist">' + "".join(
        f'<div class="li"><div class="num">{i}</div><div class="tx"><h4>{h}</h4><p>{p}</p></div></div>'
        for i, (h, p) in enumerate(items, 1)) + "</div>"


def vlist(items):
    return '<div class="vlist">' + "".join(f'<div class="v"><span class="b">{b}</span><div>{t}</div></div>' for b, t in items) + "</div>"


def callout(kind, h, p, ic="!"):
    return f'<div class="callout {kind}"><div class="ci">{ic}</div><div class="ct"><h4>{h}</h4><p>{p}</p></div></div>'


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="ctable"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def pipe(steps):
    arrow = '<div class="arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>'
    return '<div class="pipe">' + arrow.join(
        f'<div class="step"><div class="si">{i:02d}</div><div class="sn">{n}</div><div class="sd">{d}</div></div>'
        for i, (n, d) in enumerate(steps, 1)) + "</div>"


def prompt(label, text):
    return f'<div class="code sm"><div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="fn">{label}</span></div><pre><code>{text}</code></pre></div>'


def e1():
    return page("AI 답 확인 항목", f'''<div class="twocol w">
  {biglist([
      ("출처", "근거 문서 · 링크"),
      ("날짜", "언제 기준인지"),
      ("숫자와 이름", "금액 · 날짜 · 인명은 원문 대조"),
  ])}
  {callout("rose", "존재하지 않는 판례 6건", "2023년 미국 · ChatGPT 판례를 확인 없이 제출 · 제재금 5,000달러")}
</div>''', "", "")


def e2():
    cands = [("약", .31), ("전년", .22), ("120억", .18), ("150억", .12), ("공개되지", .04)]
    bars = []
    for i, (w, p) in enumerate(cands):
        y = 70 + i * 34
        bars.append(f'<text x="96" y="{y+17}" text-anchor="end" font-size="14" fill="{N}">{w}</text>'
                    f'<rect x="106" y="{y}" width="{p*560:.0f}" height="24" rx="4" fill="{O if i == 0 else G}"/>'
                    f'<text x="{112+p*560:.0f}" y="{y+17}" font-size="13" fill="{N}">{p:.2f}</text>')
    svg = (f'<svg viewBox="0 0 420 250"><text x="10" y="34" font-size="16" font-weight="700" fill="{N}">「우리 회사의 3분기 매출은 ___」</text>'
           + "".join(bars) + "</svg>")
    return page("AI가 문장을 만드는 방식", f'''<div class="twocol">
  <div class="plot">{svg}<div class="cap">다음 단어 후보와 확률 (예시 값)</div></div>
  {vlist([
      ("→", "다음 단어를 <b>확률</b>로 선택"),
      ("✕", "모르는 내용도 같은 말투 = <b>환각</b>"),
  ])}
</div>''', "", "")


def e3():
    return page("모르는 정보별 해결 방법", f'''{table(
        ["모르는 것", "이유", "해결"],
        [["<b>최신 정보</b>", "학습 기준 시점 이후", '<span class="hl">Deep Research</span>'],
         ["<b>사내 자료</b>", "비공개라 학습에 없음", '<span class="hl">NotebookLM</span>']])}
  {callout("amber", "둘 다 해당", "올해 바뀐 사내 출장 규정 → 업로드")}''', "", "")


def e4():
    return page("Deep Research와 NotebookLM", table(
        ["", "Deep Research", "NotebookLM"],
        [["<b>근거</b>", "웹 공개 자료", "내가 올린 자료"],
         ["<b>결과물</b>", "출처 달린 보고서", "출처 번호 달린 답변 · 요약"],
         ["<b>시간</b>", "수 분", "바로"],
         ["<b>맞는 일</b>", "시장 · 경쟁사 동향", "규정 · 매뉴얼 · 회의록"],
         ["<b>주의</b>", "웹 자료 품질 편차", "자료 밖 내용은 모름"]]), "", "")


def e5():
    p = ("국내 편의점 간편식 시장의 최근 동향을 조사해 줘.\n"
         "- 기간: 2024년 이후\n"
         "- 출처: 정부 · 업계 공식 자료 우선, 개인 블로그 제외\n"
         "- 형식: 편의점 채널별 비교 표 + 한 쪽 요약")
    return page("Deep Research 진행 순서", f'''{pipe([
        ("질문", ""), ("계획 제시", ""), ("계획 수정", "사람"), ("검색 · 읽기", "수 분"), ("보고서", "출처 포함")])}
  <div class="twocol">
    {prompt("질문 예시", p)}
    {callout("amber", "계획에서 고칠 것", "기간 · 지역 · 제외 출처 · 분량")}
  </div>''', "", "")


def e6():
    return page("NotebookLM 답변 방식", f'''{pipe([
        ("자료 올리기", "PDF · Docs · 웹 · YouTube"), ("질문", ""), ("답변", "자료 안에서만"),
        ("출처 번호", "문장마다"), ("원문 확인", "번호 클릭")])}
  <div class="twocol">
    {vlist([
        ("→", "업무 · 프로젝트별 노트북"),
        ("✕", "옛 버전과 새 버전을 함께 올리면 답이 섞임"),
    ])}
    {callout("mint", "일반 챗봇과의 차이", "기억으로 답하기 vs 펼친 자료로 답하기", "✓")}
  </div>''', "", "")


def e7():
    p = "올린 자료에 근거가 있는 내용만 답해 줘.\n근거가 없으면 「자료에 없음」이라고 쓰고,\n답마다 출처 위치를 붙여 줘."
    return page("답의 유형별 대응", f'''{table(
        ["유형", "모습", "대응"],
        [["<b>둘러대기</b>", "출처 없는 그럴듯한 문장", '<span class="no">쓰지 않음</span>'],
         ["<b>근거 제시</b>", "문서 · 위치 표시", '<span class="yes">원문 확인 후 사용</span>'],
         ["<b>자료에 없음</b>", "없다고 답함", "자료 보충 · 담당 부서 확인"]])}
  {prompt("지시문", p)}''', "", "")


def e8():
    return page("근거 자료 관리", biglist([
        ("공식 · 최신 자료", "확정본만"),
        ("한 문서는 한 버전", "옛 버전 삭제"),
        ("좁은 질문", "기간 · 대상 · 형식"),
        ("출처 확인", "원문 열어 보기"),
    ]), "", "")


SLIDES = [e1, e2, e3, e4, e5, e6, e7, e8]

# 템플릿의 보라 계열 변수를 덱 색(남색 · 주황)으로 덮는다
CSS = '''
  :root{ --violet:#1F3A5F; --violet-700:#14263F; --violet-300:#F5B06A; --wash:#EEF1F5; --wash-2:#F6F8FA; --line:#E1E5EB; --ink:#16233A; --ink-soft:#44506A; --mut:#8A94A6; --amber:#F28C28; }
  body{background:#E6E9EE;}
  .plot svg{width:100%; height:auto;}
  .mid{flex:1; min-height:0; display:flex; flex-direction:column; justify-content:center; gap:22px; padding-bottom:18px;}
  .mid .biglist{gap:22px;} .mid .biglist .li .num{width:42px; height:42px; font-size:17px;}
  .mid .biglist .li .tx h4{font-size:23px;} .mid .biglist .li .tx p{font-size:17px;}
  .mid .vlist{gap:16px;} .mid .vlist .v{font-size:18.5px;} .mid .vlist .v .b{width:28px; height:28px;}
  .mid .ctable{font-size:17px;} .mid .ctable thead th{font-size:13px;} .mid .ctable th, .mid .ctable td{padding:16px 20px;}
  .mid .callout{padding:20px 22px;} .mid .callout .ct h4{font-size:19px; margin-bottom:6px;} .mid .callout .ct p{font-size:16px; line-height:1.6;}
  .mid .pipe{margin-bottom:0;} .mid .pipe .step{padding:16px 10px;} .mid .pipe .step .sn{font-size:18px;} .mid .pipe .step .sd{font-size:13px;}
  .mid .code code{font-size:15.5px; line-height:1.75;}
  .mid .twocol{align-items:center;}
'''
