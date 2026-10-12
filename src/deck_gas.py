"""짧은 강의: Skill 정제 + Apps Script 웹앱 대시보드.

출력: docs/gas-dashboard/index.html  (python3 src/build.py gas)
기존 덱의 부품 · 장면을 그대로 쓴다.
"""
from pathlib import Path

import deck
import explain
from deck import ba, bridge, capture, divider, flow, ill, lab, light
from intro import coord, icon

N, G, O, W = "#1F3A5F", "#D9DDE3", "#F28C28", "#FFFFFF"
deck.CAPDIR = Path(__file__).resolve().parent.parent / "docs" / "gas-dashboard" / "assets" / "capture"
code = explain.prompt


# ── 도식 ────────────────────────────────────────────────
def box(x, y, w, h, title, sub="", fill=W, stroke=N, tcolor=N, rx=14):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
    s += f'<text x="{x+w/2}" y="{y+(h/2 if not sub else h/2-8)}" text-anchor="middle" dominant-baseline="middle" class="bt" fill="{tcolor}">{title}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" dominant-baseline="middle" class="bs">{sub}</text>'
    return s


_P = ["a"]  # 그림마다 화살표 머리 id 를 다르게 쓴다 (숨은 장의 id 를 참조하면 안 보인다)


def arrow(x1, y1, x2, y2, color=N, dash="", w=3, mid="ah"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d} marker-end="url(#{_P[0]}{mid})"/>'


def markers(prefix):
    _P[0] = prefix
    return _MARKERS.replace('id="ah"', f'id="{prefix}ah"').replace('id="aho"', f'id="{prefix}aho"')


_MARKERS = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path d="M0 0 L10 5 L0 10 Z" fill="{N}"/></marker>'
           f'<marker id="aho" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path d="M0 0 L10 5 L0 10 Z" fill="{O}"/></marker></defs>')


def browser(x, y, w, h, inner):
    """브라우저 창: 위 막대 + 안쪽 내용."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{G}"/><rect x="{x}" y="{y+14}" width="{w}" height="12" fill="{G}"/>'
            + "".join(f'<circle cx="{x+16+i*14}" cy="{y+13}" r="4" fill="{N}"/>' for i in range(3))
            + inner)


def bars(x, y, hs, color=N, bw=22, gap=12):
    base = y
    return "".join(f'<rect x="{x+i*(bw+gap)}" y="{base-h}" width="{bw}" height="{h}" rx="3" fill="{color}"/>' for i, h in enumerate(hs))


def db(x, y, w=120, h=130, label="시트"):
    """데이터베이스 원통."""
    ry = 16
    return (f'<path d="M{x} {y+ry} L{x} {y+h-ry} A{w/2} {ry} 0 0 0 {x+w} {y+h-ry} L{x+w} {y+ry}" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+ry}" rx="{w/2}" ry="{ry}" fill="{W}" stroke="{N}" stroke-width="3"/>'
            f'<path d="M{x} {y+h*0.45} A{w/2} {ry} 0 0 0 {x+w} {y+h*0.45}" fill="none" stroke="{N}" stroke-width="2"/>'
            f'<path d="M{x} {y+h*0.7} A{w/2} {ry} 0 0 0 {x+w} {y+h*0.7}" fill="none" stroke="{N}" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{y+h+30}" text-anchor="middle" class="bt" fill="{N}">{label}</text>')


def static_web():
    mk = markers("st")
    page = browser(760, 70, 330, 250, bars(800, 290, [90, 140, 70, 170, 120], G))
    file_ = (f'<path d="M140 90 L250 90 L290 130 L290 300 L140 300 Z" fill="{W}" stroke="{N}" stroke-width="3"/>'
             f'<path d="M250 90 L250 130 L290 130" fill="none" stroke="{N}" stroke-width="3"/>'
             + "".join(f'<rect x="160" y="{150+i*26}" width="{100 - (i%2)*30}" height="9" rx="4" fill="{G}"/>' for i in range(5))
             + f'<text x="215" y="340" text-anchor="middle" class="bt" fill="{N}">완성된 HTML 파일</text>'
             + f'<text x="215" y="366" text-anchor="middle" class="bs">숫자가 파일 안에 고정</text>')
    flowline = (arrow(310, 195, 740, 195, N, w=4)
                + f'<text x="525" y="178" text-anchor="middle" class="bs">그대로 전달</text>')
    return f'''<svg viewBox="0 0 1180 400" class="websvg">{mk}{file_}{flowline}{page}
<text x="925" y="352" text-anchor="middle" class="bt" fill="{N}">브라우저</text>
<text x="925" y="378" text-anchor="middle" class="bs">숫자를 바꾸려면 파일을 다시 만들어 올림</text></svg>'''


def dynamic_web():
    # 브라우저(왼쪽) · Apps Script 서버(가운데) · 시트(오른쪽). 위 줄은 요청, 아래 줄은 데이터가 흐른다.
    mk = markers("dy")
    page = browser(40, 80, 300, 230, bars(80, 280, [80, 120, 150, 100, 170], O))
    server = box(470, 120, 220, 150, "Apps Script", "틀(HTML) + 데이터", fill="#EEF1F5")
    sheet = db(880, 110)
    req = (arrow(345, 130, 465, 130, N, "7 6") + f'<text x="405" y="112" text-anchor="middle" class="bs">① 요청</text>'
           + arrow(695, 150, 875, 150, N, "7 6") + f'<text x="785" y="132" text-anchor="middle" class="bs">② 조회</text>')
    res = (arrow(875, 250, 695, 250, O, w=4, mid="aho") + f'<text x="785" y="282" text-anchor="middle" class="bso">③ 최신 데이터</text>'
           + arrow(465, 270, 345, 270, O, w=4, mid="aho") + f'<text x="405" y="302" text-anchor="middle" class="bso">④ 화면 그리기</text>')
    # 흐르는 데이터 점
    dots = "".join(
        f'<circle r="8" fill="{O}"><animateMotion dur="2.4s" begin="{d}s" repeatCount="indefinite" path="M875 250 L695 250 L580 260 L465 270 L345 270"/></circle>'
        for d in (0, .8, 1.6))
    return f'''<svg viewBox="0 0 1180 400" class="websvg">{mk}{page}{server}{sheet}{req}{res}{dots}
<text x="190" y="350" text-anchor="middle" class="bt" fill="{N}">브라우저</text>
<text x="190" y="376" text-anchor="middle" class="bs">열 때마다 지금 숫자</text></svg>'''


def pipeline():
    """전체 구조 — 입력 A · B → 시트 마스터 → 웹앱 대시보드."""
    s = markers("pl")
    s += box(40, 30, 300, 92, "입력 A · 대량 엑셀 원본", "오탈자 · 중복 · 공백")
    s += box(840, 30, 300, 92, "입력 B · 웹 화면 건별 입력", "드롭다운 · 자동완성")
    s += box(40, 170, 300, 92, "Skill  sales-data-cleaner", "교정 · 중복 제거 · 검증", fill="#FFF3E6", stroke=O)
    s += box(840, 170, 300, 92, "GAS  addSalesRecord", "검증 · 금액 계산 · 저장", fill="#EEF1F5")
    s += db(530, 250, 120, 110, "")
    s += f'<text x="590" y="395" text-anchor="middle" class="bt" fill="{N}">시트 마스터 · 클린 데이터</text>'
    s += box(440, 440, 300, 80, "GAS 웹앱 대시보드", "KPI · 차트 · 새로고침", fill=N, stroke=N, tcolor=W)
    s += arrow(190, 124, 190, 166) + arrow(990, 124, 990, 166)
    s += arrow(340, 216, 525, 290) + arrow(840, 216, 655, 290)
    s += arrow(590, 405, 590, 436, O, w=4, mid="aho")
    s = s.replace('class="bs">KPI', 'class="bsw">KPI')
    return f'<svg viewBox="0 0 1180 530" class="websvg pipe2">{s}</svg>'


def save_flow():
    return flow([("등록 버튼", "웹 화면"), ("google.script.run", "브라우저 → 서버"),
                 ("addSalesRecord", "검증 · 금액 계산"), ("appendRow", "시트에 한 행 추가")], hl=3)


# ── 장 ──────────────────────────────────────────────────
def cover():
    strip = "".join(icon(n, "tile") for n in ["gemini", "sheets", "appsscript", "drive"])
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">실습 · 영업 데이터 파이프라인</div>
  <h1>Skill과 Apps Script로<br/>만드는 실적 대시보드</h1>
  <div class="strip">{strip}</div>
</section>'''


def slides():
    skill_md = ("---\n"
                "name: sales-data-cleaner\n"
                "description: 판매 데이터 파일이 오면 마스터 구조로 정리\n"
                "---\n"
                "목표: 어떤 형식의 파일이든 마스터와 같은 구조로\n"
                "1. 열의 의미부터 파악 (이름 · 순서가 달라도)\n"
                "2. 거래처 · 제품은 참조 마스터에서 가장 가까운 값으로\n"
                "3. 같은 거래로 보이는 행은 하나로\n"
                "4. 수량 · 단가 · 금액이 안 맞으면 고치지 말고 표시\n"
                "5. 확신이 낮은 교정은 리포트에 따로\n"
                "참조: 거래처 마스터 · 05 제품카탈로그")
    static_code = ("const DATA = {\n"
                   "  month: \"2026-08\",\n"
                   "  channels: { \"편의점\": { sales: 1421193000, ... } }\n"
                   "};\n"
                   "render(DATA);   // 숫자가 파일 안에 고정")
    dynamic_code = ("google.script.run\n"
                    "  .withSuccessHandler(render)   // 받은 데이터로 그리기\n"
                    "  .getCleanedSalesData();       // 시트에서 최신 데이터")
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
    return [
        cover(),
        light("전체 구조", pipeline(), "개요"),
        light("단계별 역할", f'''<table class="dbt">
<thead><tr><th>단계</th><th>하는 일</th><th>도구</th></tr></thead><tbody>
<tr><td><b>정리</b></td><td>오탈자 · 중복 · 공백 정리</td><td>Skill · sales-data-cleaner</td></tr>
<tr><td><b>입력</b></td><td>건별 거래를 바로 기록</td><td>웹 화면 + GAS addSalesRecord</td></tr>
<tr><td><b>저장</b></td><td>깨끗한 데이터 한 곳</td><td>시트 마스터</td></tr>
<tr><td><b>보여주기</b></td><td>지금 숫자를 화면에</td><td>GAS 웹앱 대시보드</td></tr>
</tbody></table>''', "개요"),

        divider("01", "정적 웹과 동적 웹", ""),
        ill("scenes_ch4", "photo_window", "top20", "사진과 창문", ["사진: 그때 숫자", "창문: 지금 숫자"]),
        light("정적 웹: 완성된 파일을 그대로", static_web(), "01"),
        light("동적 웹: 열 때마다 데이터를 가져와 그림", dynamic_web(), "01"),
        ill("scenes_ch4", "menu_board", "left40", "틀은 그대로, 데이터만 교체", ["화면 틀: Index.html", "데이터: 시트에서"]),
        light("같은 대시보드, 데이터 위치만 다름", f'''<div class="twocol">
  {code("정적 · 09_대시보드_예시.html", static_code)}
  {code("동적 · Apps Script 웹앱", dynamic_code)}
</div>''', "01"),

        divider("02", "Skill로 원본 정리", ""),
        light("원본의 흔한 오류", f'''<table class="dbt">
<thead><tr><th>오류</th><th>원본</th><th>정리 후</th></tr></thead><tbody>
<tr><td><b>띄어쓰기</b></td><td>B 편의점</td><td>B편의점</td></tr>
<tr><td><b>오탈자</b></td><td>B편의졈</td><td>B편의점</td></tr>
<tr><td><b>중복 행</b></td><td>같은 기준월 · 거래처 · SKU 2줄</td><td>1줄</td></tr>
<tr><td><b>계산 불일치</b></td><td>매출액 ≠ 납품수량 × 단가</td><td>표시 후 확인</td></tr>
</tbody></table>
<div class="dbnote"><span>01 원본</span> 4,381행 → 정리 후 4,368행</div>''', "02"),
        ill("scenes_ch5", "conveyor", "top20", "규칙이 아니라 판단으로 정리", ["처음 보는 오탈자도 마스터에 맞춰 교정", "열 이름 · 순서가 달라도 처리"]),
        ba("정해진 규칙 vs Skill", "02",
           "수식 · 스크립트\n\n정해 둔 규칙만 처리\n'B 편의점' → 규칙에 있으면 교정\n'B편의젬' → 규칙에 없으면 그대로\n열 순서가 바뀌면 오류",
           "Skill\n\n마스터와 비교해 판단\n'B편의젬' · 'ㅂ편의점'도 B편의점으로\n열 이름 · 순서가 달라도 읽음\n애매한 건 정제 리포트에 표시"),
        ba("지침은 규칙 목록이 아니라 판단 기준", "02",
           "'B 편의점'을 'B편의점'으로 바꿔 줘.\nC열과 D열을 기준으로 중복을 지워 줘.\n2~4381행만 처리해 줘.\n\n→ 다음 달 파일에서는 안 맞음",
           "목표: 어떤 파일이든 마스터 구조로\n열 의미부터 파악하고, 거래처는 마스터에서 가장 가까운 값으로.\n안 맞는 숫자는 고치지 말고 표시, 애매한 건 리포트에.\n\n→ 파일이 바뀌어도 그대로 사용"),
        light("sales-data-cleaner", f'<div class="twocol">{code("Skill", skill_md)}<div class="vl"><p>목표</p><p>판단 기준</p><p>모를 때의 처리</p><p>참조 마스터</p></div></div>', "02"),
        lab("1", "원본 정리 Skill", "02",
            "01 원본을 Skill 한 줄로 마스터 시트에",
            ["sales-data-cleaner Skill 만들기", "01 원본을 Drive에 올리고 대화에 첨부", "/sales-data-cleaner 호출", "정제 리포트 확인 → 마스터 시트 기록"],
            ["판매실적_마스터 4,368행", "편의점 8월 매출 14.21억 원"],
            20, "01 · 04(대조용)"),

        divider("03", "웹 화면에서 바로 입력", ""),
        ill("scenes_extra", "forms_inlet", "top20", "입구부터 반듯하게", ["드롭다운 · 자동완성", "오탈자 원천 차단"]),
        light("등록 버튼에서 시트까지", save_flow(), "03"),

        divider("04", "Apps Script 웹앱 대시보드", ""),
        ill("scenes_ch4", "hang_window", "left40", "Apps Script로 시트와 연결", ["Code.gs: 시트 ↔ 화면", "Index.html: 화면 틀", "URL 하나로 공유"]),
        light("Code.gs의 세 함수", code("Code.gs", gas_code), "04"),
        light("만드는 순서", flow([("편집기 열기", "확장 프로그램 → Apps Script"), ("파일 2개", "Code.gs · Index.html"),
                                ("웹앱 배포", "배포 → 새 배포 → 웹 앱"), ("권한 승인", "처음 한 번")], hl=2), "04"),
        capture("① 편집기 열기", "04", [("gas-01-menu", "확장 프로그램 → Apps Script")], ["새 시트: 판매실적_마스터"]),
        capture("② 파일 두 개", "04", [("gas-02-files", "Code.gs · Index.html")], ["+ → HTML → 이름: Index (대소문자 그대로)"]),
        capture("③ 웹앱 배포", "04", [("gas-03-deploy", "새 배포 · 웹 앱 설정")], ["실행: 나", "액세스: 내 조직"]),
        capture("④ 권한 승인", "04", [("gas-04-auth", "확인하지 않은 앱 경고")], ["고급 → 이동", "허용 → 웹앱 URL"]),
        lab("2", "웹앱 대시보드", "04",
            "시트와 연결된 대시보드 주소 받기",
            ["판매실적_마스터에서 Apps Script 열기", "Code.gs · Index.html 붙여넣기", "웹앱 배포 → 권한 승인", "웹 화면에서 한 건 등록"],
            ["옆 사람이 URL로 접속", "등록한 한 건이 시트와 화면에 반영"],
            30, "판매실적_마스터 · 09(화면 틀)"),
        bridge("Skill은 정리, Apps Script는 연결", "", "전체", "원본 → Skill → 시트 마스터 → 웹앱"),
    ]


CSS = '''
  .websvg{width:100%; height:auto; max-height:430px;}
  .websvg.pipe2{max-height:470px;}
  .websvg .bt{font-family:var(--serif); font-size:20px; font-weight:800;}
  .websvg .bs{font-family:var(--serif); font-size:15px; fill:#44506A;}
  .websvg .bso{font-family:var(--serif); font-size:15px; fill:#F28C28; font-weight:700;}
  .websvg .bsw{font-family:var(--serif); font-size:15px; fill:#D9DDE3;}
'''
