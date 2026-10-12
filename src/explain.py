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
    <div class="keymsg"><span class="k">{key_label}</span><div>{key}</div></div>
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
    return page("AI 답은 출처 · 날짜 · 숫자를 확인한 뒤에 씁니다", f'''<div class="twocol w">
  {biglist([
      ("출처", "답의 근거가 된 문서나 링크가 있는지 본다. 없으면 초안으로만 쓴다."),
      ("날짜", "자료가 언제 기준인지 본다. 법규 · 가격 · 조직 정보는 자주 바뀐다."),
      ("숫자와 이름", "금액 · 날짜 · 인명 · 법령 번호는 원문과 한 번 더 대조한다."),
  ])}
  {callout("rose", "실제 사례 — 존재하지 않는 판례 6건",
           "2023년 미국의 한 변호사가 ChatGPT가 찾아 준 판례를 확인 없이 법원에 냈다. 6건 모두 없는 판례였고, 법원은 5,000달러 제재금을 부과했다.")}
</div>''', "기준", "출처 · 날짜 · 숫자 중 하나라도 확인이 안 되면 보고서에 넣지 않는다.")


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
    return page("언어 모델은 확률이 높은 단어로 빈칸을 채웁니다", f'''<div class="twocol">
  <div class="plot">{svg}<div class="cap">다음 단어 후보와 확률 (설명용 예시 값)</div></div>
  {vlist([
      ("→", "언어 모델은 앞 문장 다음에 올 단어를 <b>확률</b>로 고른다."),
      ("→", "학습 때 본 적 없는 사실도 확률이 높은 단어로 빈칸을 채운다."),
      ("✕", "모르는 내용도 아는 내용과 같은 말투로 나온다. 이것을 <b>환각</b>(hallucination)이라 부른다."),
  ])}
</div>''', "주의", "자신 있는 말투는 정확도와 관계가 없다.")


def e3():
    return page("최신 정보는 검색으로, 사내 자료는 업로드로 채웁니다", f'''{table(
        ["모르는 것", "이유", "해결 방법"],
        [["<b>최신 정보</b>", "학습 데이터에는 기준 시점이 있어 그 뒤의 소식은 모른다", '<span class="hl">웹 검색 · Deep Research</span>'],
         ["<b>사내 자료</b>", "사내 규정 · 회의록 · 실적 자료는 공개되지 않아 학습에 들어가지 않았다", '<span class="hl">자료 올리기 · NotebookLM</span>']])}
  {callout("amber", "둘 다 해당하는 질문", "「올해 바뀐 사내 출장 규정」은 최신이면서 내부 자료다. 검색으로는 찾을 수 없어 문서를 직접 올려야 한다.")}''',
        "기준", "질문이 최신 정보인지 내부 자료인지 먼저 나누면 쓸 도구가 정해진다.")


def e4():
    return page("자료를 밖에서 모을지, 안에서 찾을지에 따라 도구가 다릅니다", table(
        ["", "Deep Research", "NotebookLM"],
        [["<b>근거를 찾는 곳</b>", "웹에 공개된 자료 수십~수백 곳", "내가 올린 문서 · 링크 · 영상"],
         ["<b>결과물</b>", "출처가 달린 조사 보고서", "출처 번호가 달린 답변 · 요약 · 오디오 개요 · 마인드맵"],
         ["<b>걸리는 시간</b>", "수 분", "바로"],
         ["<b>잘 맞는 일</b>", "시장 조사, 경쟁사 · 기술 동향", "사내 규정, 매뉴얼, 회의록 분석"],
         ["<b>주의할 점</b>", "웹 자료의 품질이 섞여 있다", "올린 자료에 없는 내용은 답하지 못한다"]]),
        "정리", "밖에서 자료를 모아야 하면 Deep Research, 가진 자료 안에서 답해야 하면 NotebookLM을 쓴다.")


def e5():
    p = ("국내 편의점 간편식 시장의 최근 동향을 조사해 줘.\n"
         "- 기간: 2024년 이후\n"
         "- 출처: 정부 · 업계 공식 자료 우선, 개인 블로그 제외\n"
         "- 형식: 편의점 채널별 비교 표 + 한 쪽 요약")
    return page("Deep Research는 실행 전에 계획을 고칠 기회를 줍니다", f'''{pipe([
        ("질문 입력", "조사할 주제"), ("계획 제시", "조사 항목 목록"), ("계획 수정", "사람이 고치고 승인"),
        ("검색 · 읽기", "수 분간 반복"), ("보고서", "출처 링크 포함")])}
  <div class="twocol">
    {prompt("Deep Research 질문 예시", p)}
    {callout("amber", "계획 단계에서 고칠 것", "기간, 지역, 빼야 할 출처, 보고서 분량. 실행 뒤에 고치면 처음부터 다시 돌려야 한다.")}
  </div>''', "효과", "계획 단계에서 범위를 좁히면 질문에 맞는 보고서가 나온다.")


def e6():
    return page("NotebookLM은 답마다 출처 번호를 붙입니다", f'''{pipe([
        ("자료 올리기", "PDF · Docs · 웹페이지 · YouTube"), ("질문", "자료에 대해 묻기"), ("답변", "올린 자료 안에서만"),
        ("출처 번호", "문장마다 표시"), ("원문 확인", "번호를 누르면 해당 위치")])}
  <div class="twocol">
    {vlist([
        ("→", "노트북마다 자료 묶음이 따로 있다. 업무 · 프로젝트별로 나눠 만든다."),
        ("→", "자료에 없는 내용을 물으면 답하지 않거나 없다고 말한다."),
        ("✕", "같은 문서의 옛 버전과 새 버전을 함께 올리면 답이 섞인다."),
    ])}
    {callout("mint", "일반 챗봇과의 차이", "일반 챗봇은 기억으로 답하고, NotebookLM은 펼쳐 놓은 자료를 보며 답한다.", "✓")}
  </div>''', "기준", "출처 번호를 눌러 원문 문장을 확인한 답만 보고서에 쓴다.")


def e7():
    p = "올린 자료에 근거가 있는 내용만 답해 줘.\n근거가 없으면 「자료에 없음」이라고 쓰고,\n답마다 출처 위치를 붙여 줘."
    return page("「자료에 없음」도 쓸모 있는 답입니다", f'''{table(
        ["답의 유형", "모습", "대응"],
        [["<b>둘러대기</b>", "출처 없이 그럴듯한 문장", '<span class="no">쓰지 않는다.</span> 출처를 요구해 다시 묻는다'],
         ["<b>근거 제시</b>", "문서와 위치를 짚으며 답한다", '<span class="yes">원문을 열어 확인한 뒤 쓴다</span>'],
         ["<b>자료에 없음</b>", "해당 내용이 없다고 답한다", "자료를 보충하거나 담당 부서에 확인한다"]])}
  {prompt("세 번째 답을 끌어내는 지시문", p)}''',
        "기준", "「자료에 없음」은 실패한 답이 아니라 확인할 곳을 알려 주는 답이다.")


def e8():
    return page("좋은 자료를 고르는 습관이 좋은 답을 만듭니다", biglist([
        ("공식 · 최신 자료", "초안이나 개인 메모보다 확정된 문서를 올린다."),
        ("한 문서는 한 버전만", "같은 문서의 옛 버전은 노트북에서 지운다."),
        ("범위를 좁힌 질문", "기간 · 대상 · 원하는 형식을 질문에 적는다."),
        ("출처 확인", "보고서에 들어갈 문장은 원문을 직접 열어 본다."),
    ]), "정리", "좋은 자료를 고르는 것이 좋은 답을 얻는 가장 빠른 방법이다.")


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
