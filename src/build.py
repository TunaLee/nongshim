#!/usr/bin/env python3
"""그림 슬라이드 8장을 template.html 에 붙여 docs/grounding/index.html 을 만든다.

그림은 전부 인라인 SVG. 색은 남색·밝은 회색·주황 세 가지와 흰색만 쓴다.
사용: python3 src/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N, G, O, W = "#1F3A5F", "#D9DDE3", "#F28C28", "#FFFFFF"

# ── 공통 인물 ─────────────────────────────────────────────
# 로봇: 원점 = 발 가운데. 어깨 (±44,-86). 입·팔은 장면마다 따로 그린다.
ROBOT = f'''<g id="robot">
  <line x1="0" y1="-190" x2="0" y2="-206" stroke="{N}" stroke-width="4"/>
  <circle cx="0" cy="-210" r="7" fill="{N}"/>
  <rect x="-12" y="-108" width="24" height="14" fill="{N}"/>
  <rect x="-30" y="-34" width="20" height="34" rx="6" fill="{N}"/>
  <rect x="10" y="-34" width="20" height="34" rx="6" fill="{N}"/>
  <rect x="-44" y="-98" width="88" height="70" rx="20" fill="{G}" stroke="{N}" stroke-width="4"/>
  <circle cx="0" cy="-64" r="9" fill="{W}" stroke="{N}" stroke-width="3"/>
  <rect x="-54" y="-190" width="108" height="86" rx="43" fill="{G}" stroke="{N}" stroke-width="4"/>
  <rect x="-38" y="-172" width="76" height="50" rx="22" fill="{W}" stroke="{N}" stroke-width="3"/>
  <circle cx="-15" cy="-152" r="7.5" fill="{O}"/>
  <circle cx="15" cy="-152" r="7.5" fill="{O}"/>
</g>'''

# 회사원 상반신: 원점 = 허리. 어깨 (±54,-140). 머리 중심 (0,-210).
PERSON = f'''<g id="person">
  <circle cx="-38" cy="-206" r="8" fill="{W}" stroke="{N}" stroke-width="3"/>
  <circle cx="38" cy="-206" r="8" fill="{W}" stroke="{N}" stroke-width="3"/>
  <rect x="-11" y="-178" width="22" height="24" fill="{W}" stroke="{N}" stroke-width="3"/>
  <path d="M-58 0 L-62 -118 Q-60 -150 -28 -158 L28 -158 Q60 -150 62 -118 L58 0 Z" fill="{N}"/>
  <path d="M-20 -158 L0 -116 L20 -158 Z" fill="{W}"/>
  <path d="M-5 -152 L5 -152 L8 -112 L0 -102 L-8 -112 Z" fill="{G}"/>
  <path d="M-20 -158 L-6 -96 M20 -158 L6 -96" stroke="{G}" stroke-width="2" fill="none"/>
  <circle cx="0" cy="-210" r="38" fill="{W}" stroke="{N}" stroke-width="4"/>
  <path d="M-41 -206 Q-46 -256 0 -256 Q44 -256 41 -208 Q30 -234 -2 -234 Q-28 -232 -41 -206 Z" fill="{N}"/>
  <circle cx="-13" cy="-204" r="3.8" fill="{N}"/>
  <circle cx="13" cy="-204" r="3.8" fill="{N}"/>
  <path d="M-10 -188 Q0 -180 10 -188" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>
</g>
<g id="legs">
  <rect x="-50" y="-4" width="44" height="146" rx="8" fill="{G}" stroke="{N}" stroke-width="3"/>
  <rect x="6" y="-4" width="44" height="146" rx="8" fill="{G}" stroke="{N}" stroke-width="3"/>
  <ellipse cx="-30" cy="148" rx="28" ry="10" fill="{N}"/>
  <ellipse cx="30" cy="148" rx="28" ry="10" fill="{N}"/>
</g>'''

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
{ROBOT}
{PERSON}
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
</defs></svg>'''


def robot(x, y, s, extra="", mouth="smile"):
    """extra = 로봇 좌표계에서 그릴 팔·소품. 몸 위에 그려진다."""
    m = {
        "smile": f'<path d="M-9 -138 Q0 -131 9 -138" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "grin": f'<path d="M-14 -140 Q0 -124 14 -140" stroke="{N}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "wavy": f'<path d="M-12 -134 Q-6 -140 0 -134 Q6 -128 12 -134" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "flat": f'<path d="M-9 -135 L9 -135" stroke="{N}" stroke-width="3" stroke-linecap="round"/>',
    }[mouth]
    return f'<g transform="translate({x},{y}) scale({s})"><use href="#robot"/>{m}{extra}</g>'


def rarm(x1, y1, x2, y2, cx=None, cy=None, hand=True):
    """로봇 팔. 손은 회색 원."""
    d = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}" if cx is not None else f"M{x1} {y1} L{x2} {y2}"
    h = f'<circle cx="{x2}" cy="{y2}" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>' if hand else ""
    return f'<path d="{d}" stroke="{N}" stroke-width="9" fill="none" stroke-linecap="round"/>{h}'


def person(x, y, s, extra_back="", extra_front="", legs=False):
    lg = '<use href="#legs"/>' if legs else ""
    return (f'<g transform="translate({x},{y}) scale({s})">{lg}{extra_back}'
            f'<use href="#person"/>{extra_front}</g>')


def parm(x1, y1, x2, y2, cx=None, cy=None, hand=True):
    """회사원 팔. 남색 소매 + 흰 손."""
    d = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}" if cx is not None else f"M{x1} {y1} L{x2} {y2}"
    h = f'<circle cx="{x2}" cy="{y2}" r="12" fill="{W}" stroke="{N}" stroke-width="3"/>' if hand else ""
    return f'<path d="{d}" stroke="{N}" stroke-width="22" fill="none" stroke-linecap="round"/>{h}'


def lines(x1, x2, ys, color=G, w=6):
    return "".join(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>' for y in ys)


def floor(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="14" fill="{G}"/>'


# ── ① 돋보기 ───────────────────────────────────────────
def s1():
    lens = (900, 410)
    return f'''
{floor(870, 648, 390)}
<rect x="650" y="300" width="140" height="210" rx="22" fill="{G}" stroke="{N}" stroke-width="4"/>
{person(720, 505, .9,
        extra_back=parm(-54, -140, -122, -14, -96, -70),
        extra_front=parm(54, -140, 142, -66, 104, -128))}
<path d="M765 268 L777 256 M776 284 L791 280 M752 258 L756 242" stroke="{N}" stroke-width="4" stroke-linecap="round"/>
<rect x="530" y="505" width="470" height="16" rx="6" fill="{N}"/>
<rect x="555" y="521" width="14" height="124" fill="{N}"/>
<rect x="962" y="521" width="14" height="124" fill="{N}"/>
<rect x="556" y="408" width="108" height="88" rx="6" fill="{W}" stroke="{N}" stroke-width="5"/>
{lines(572, 646, [428, 444])}{lines(572, 620, [460])}
<rect x="571" y="470" width="78" height="16" rx="3" fill="none" stroke="{N}" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M545 505 L676 505 L668 496 L553 496 Z" fill="{N}"/>
<circle cx="610" cy="492" r="11" fill="{W}" stroke="{N}" stroke-width="3"/>
{robot(1075, 640, 1.25, rarm(-44, -86, -88, -168, -80, -110, hand=False) + rarm(44, -86, 70, -36, hand=True))}
<g transform="rotate(-5 915 420)">
  <rect x="865" y="355" width="100" height="130" rx="5" fill="{W}" stroke="{N}" stroke-width="4"/>
  {lines(880, 950, [376, 394, 430, 448, 466])}
</g>
<circle cx="965" cy="430" r="11" fill="{G}" stroke="{N}" stroke-width="3"/>
<clipPath id="lens1"><circle cx="{lens[0]}" cy="{lens[1]}" r="34"/></clipPath>
<g clip-path="url(#lens1)">
  <rect x="860" y="370" width="80" height="80" fill="{W}"/>
  {lines(866, 934, [388, 432], G, 9)}
  <line x1="872" y1="410" x2="928" y2="410" stroke="{O}" stroke-width="13" stroke-linecap="round"/>
</g>
<circle cx="{lens[0]}" cy="{lens[1]}" r="34" fill="none" stroke="{N}" stroke-width="7"/>
<path d="M880 392 A24 24 0 0 1 896 384" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round"/>
<line x1="876" y1="433" x2="848" y2="452" stroke="{N}" stroke-width="10" stroke-linecap="round"/>
<circle cx="848" cy="447" r="12" fill="{W}" stroke="{N}" stroke-width="3"/>
'''


# ── ② 퍼즐 ────────────────────────────────────────────
def s2():
    x0, y0, c = 310, 225, 104
    hole = (4, 1)
    out = [f'<rect x="290" y="205" width="560" height="450" rx="16" fill="{W}" stroke="{N}" stroke-width="6"/>']
    for r in range(4):
        for k in range(5):
            x, y = x0 + k * c, y0 + r * c
            if (k, r) == hole:
                out.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{W}" stroke="{N}" stroke-width="3" stroke-dasharray="8 6"/>')
            else:
                out.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{G}" stroke="{N}" stroke-width="3"/>')
    # 이음새의 둥근 돌기. 빈칸 오른쪽 돌기 하나는 빈칸 안으로 들어가 모양을 보여 준다
    for r in range(4):
        for k in range(4):
            X, Y = x0 + (k + 1) * c, y0 + r * c + c // 2
            sweep = 1 if (k + r) % 2 == 0 else 0
            if (k + 1, r) == hole:
                sweep = 1
            elif (k, r) == hole:
                continue
            out.append(f'<path d="M{X} {Y-13} A13 13 0 0 {sweep} {X} {Y+13} Z" fill="{G}" stroke="{N}" stroke-width="3"/>')
    for r in range(3):
        for k in range(5):
            if hole in ((k, r), (k, r + 1)):
                continue
            X, Y = x0 + k * c + c // 2, y0 + (r + 1) * c
            sweep = 1 if (k + r) % 2 else 0
            out.append(f'<path d="M{X-13} {Y} A13 13 0 0 {sweep} {X+13} {Y} Z" fill="{G}" stroke="{N}" stroke-width="3"/>')
    piece = (f'<g transform="translate(768,366) rotate(9)">'
             f'<path d="M-52 -52 L-14 -52 L0 -74 L14 -52 L52 -52 L52 52 L-52 52 L-52 14 L-36 0 L-52 -14 Z" '
             f'fill="{O}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/></g>'
             f'<path d="M700 306 L688 296 M712 300 L708 284 M836 430 L850 440" stroke="{N}" stroke-width="4" stroke-linecap="round"/>')
    bot = robot(1010, 660, 1.7, rarm(-44, -86, -108, -168, -90, -112) + rarm(44, -86, 72, -40), mouth="grin")
    return floor(700, 662, 470) + "".join(out) + piece + bot


# ── ③ 생각 구름 ─────────────────────────────────────────
def s3():
    circles = [(540, 280, 70), (612, 222, 80), (700, 228, 74), (762, 286, 62), (650, 312, 74), (558, 324, 50), (734, 328, 52)]
    cloud = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{N}" stroke="{N}" stroke-width="10"/>' for x, y, r in circles)
    cloud += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{W}"/>' for x, y, r in circles)
    # 서가: 세 칸에 책을 꽂는다
    shelf = [f'<rect x="548" y="196" width="188" height="156" rx="6" fill="{G}" stroke="{N}" stroke-width="4"/>']
    widths = [14, 18, 12, 16, 14, 20, 12, 16, 14]
    heights = [38, 32, 40, 30, 36, 34, 40, 28, 36]
    for row, base in enumerate([246, 298, 350]):
        x = 558 + row * 3
        i = row
        while x < 712:
            w, h = widths[i % 9], heights[(i * 2) % 9]
            fill = N if i % 3 else W
            shelf.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{N}" stroke-width="2.5"/>')
            x += w + 3
            i += 1
        shelf.append(f'<rect x="548" y="{base}" width="188" height="6" fill="{N}"/>')
    bubbles = f'<circle cx="618" cy="392" r="10" fill="{W}" stroke="{N}" stroke-width="4"/><circle cx="596" cy="414" r="6" fill="{W}" stroke="{N}" stroke-width="3"/>'
    cal = f'''
<ellipse cx="262" cy="520" rx="70" ry="8" fill="{G}"/>
<path d="M205 452 L320 452 L304 402 L222 402 Z" fill="{N}"/>
<rect x="196" y="328" width="132" height="122" rx="8" fill="{O}" stroke="{N}" stroke-width="4"/>
{"".join(f'<rect x="{212+i*27}" y="{356+j*26}" width="18" height="16" rx="2" fill="{W}"/>' for i in range(4) for j in range(3))}
<path d="M206 334 Q236 266 320 282 Q298 310 300 340 Z" fill="{W}" stroke="{O}" stroke-width="4" stroke-linejoin="round"/>
{"".join(f'<rect x="{x}" y="318" width="6" height="22" rx="3" fill="{N}"/>' for x in (222, 252, 282, 310))}
<path d="M340 286 Q352 300 346 318 M356 278 Q372 298 364 324" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round"/>
<rect x="188" y="450" width="148" height="12" rx="6" fill="{N}"/>'''
    cab = f'''
<ellipse cx="1025" cy="520" rx="80" ry="8" fill="{G}"/>
<rect x="955" y="288" width="140" height="204" rx="10" fill="{O}" stroke="{N}" stroke-width="5"/>
{"".join(f'<rect x="969" y="{302+i*62}" width="112" height="52" rx="6" fill="{O}" stroke="{N}" stroke-width="3"/><rect x="1009" y="{318+i*62}" width="32" height="8" rx="4" fill="{N}"/>' for i in range(3))}
<rect x="1021" y="296" width="8" height="190" fill="{N}"/>
<path d="M1013 376 V362 A12 12 0 0 1 1037 362 V376" stroke="{N}" stroke-width="6" fill="none"/>
<rect x="1004" y="374" width="42" height="36" rx="7" fill="{N}"/>
<circle cx="1025" cy="388" r="5" fill="{W}"/><rect x="1023" y="390" width="4" height="10" fill="{W}"/>'''
    bot = robot(640, 665, 1.25,
                rarm(-44, -86, -100, -150, -80, -96) + rarm(44, -86, 100, -150, 80, -96), mouth="flat")
    return floor(640, 668, 160) + cloud + "".join(shelf) + bubbles + cal + cab + bot


# ── ④ 두 방향 ──────────────────────────────────────────
def webdoc(x, y, w, h, rot):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{W}" stroke="{N}" stroke-width="3.5"/>'
            f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="14" rx="4" fill="{G}"/>'
            + "".join(f'<circle cx="{x+12+i*10}" cy="{y+9}" r="3" fill="{N}"/>' for i in range(3))
            + lines(x + 14, x + w - 14, [y + 34, y + 50, y + 66][: max(1, (h - 30) // 18)])
            + "</g>")


def s4():
    left = f'''
{floor(320, 655, 270)}
<path d="M98 452 A72 72 0 0 0 214 566" stroke="{N}" stroke-width="5" fill="none"/>
<circle cx="160" cy="500" r="62" fill="{G}" stroke="{N}" stroke-width="4"/>
<ellipse cx="160" cy="500" rx="26" ry="62" fill="none" stroke="{N}" stroke-width="3"/>
<ellipse cx="160" cy="500" rx="62" ry="20" fill="none" stroke="{N}" stroke-width="3"/>
<line x1="98" y1="500" x2="222" y2="500" stroke="{N}" stroke-width="3"/>
<line x1="160" y1="566" x2="160" y2="602" stroke="{N}" stroke-width="6"/>
<ellipse cx="160" cy="606" rx="42" ry="8" fill="{N}"/>
{webdoc(96, 236, 140, 100, -8)}{webdoc(292, 205, 132, 96, 5)}{webdoc(470, 300, 122, 92, -4)}
<path d="M246 470 L270 470 M240 492 L262 492" stroke="{G}" stroke-width="5" stroke-linecap="round"/>
{robot(330, 650, 1.15, rarm(44, -86, 117, -222, 100, -120) + rarm(-44, -86, -78, -78))}
<rect x="210" y="562" width="30" height="40" fill="{W}" stroke="{N}" stroke-width="2.5" transform="rotate(-10 225 582)"/>
<rect x="240" y="558" width="30" height="40" fill="{W}" stroke="{N}" stroke-width="2.5" transform="rotate(9 255 578)"/>
<path d="M205 584 Q240 540 276 584" stroke="{N}" stroke-width="4" fill="none"/>
<path d="M194 584 L286 584 L274 640 L206 640 Z" fill="{G}" stroke="{N}" stroke-width="4"/>
{"".join(f'<line x1="{x}" y1="588" x2="{x-2}" y2="636" stroke="{N}" stroke-width="2"/>' for x in (218, 240, 262))}
<line x1="200" y1="612" x2="280" y2="612" stroke="{N}" stroke-width="2"/>
<circle cx="240" cy="560" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>
<line x1="465" y1="395" x2="484" y2="376" stroke="{N}" stroke-width="9" stroke-linecap="round"/>
<circle cx="503" cy="356" r="28" fill="{W}" fill-opacity=".55" stroke="{N}" stroke-width="6"/>
<circle cx="465" cy="395" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>'''
    blur = f'''<g filter="url(#soft)" opacity=".45">
  <rect x="690" y="612" width="74" height="16" rx="3" fill="{N}"/><rect x="696" y="596" width="64" height="16" rx="3" fill="{G}" stroke="{N}" stroke-width="2"/><rect x="688" y="628" width="78" height="16" rx="3" fill="{G}" stroke="{N}" stroke-width="2"/>
  {webdoc(690, 260, 110, 80, -6)}{webdoc(1020, 220, 116, 84, 7)}
  <rect x="1150" y="300" width="100" height="120" rx="4" fill="{G}" stroke="{N}" stroke-width="3"/>
  {"".join(f'<rect x="{1158+i*16}" y="318" width="12" height="38" fill="{N}"/>' for i in range(5))}
  {"".join(f'<rect x="{1158+i*16}" y="368" width="12" height="40" fill="{W}" stroke="{N}" stroke-width="2"/>' for i in range(5))}
  <rect x="700" y="420" width="60" height="78" rx="3" fill="{W}" stroke="{N}" stroke-width="3" transform="rotate(-12 730 459)"/>
</g>'''
    right = f'''
{floor(960, 665, 290)}
{blur}
{robot(960, 640, 1.2, rarm(-44, -86, -70, -100, hand=False) + rarm(44, -86, 70, -100, hand=False))}
<rect x="780" y="556" width="360" height="16" rx="6" fill="{N}"/>
<rect x="796" y="572" width="328" height="62" fill="{G}" stroke="{N}" stroke-width="3"/><rect x="800" y="572" width="14" height="94" fill="{N}"/><rect x="1106" y="572" width="14" height="94" fill="{N}"/>
<path d="M960 558 L870 548 L874 468 L960 478 L1046 468 L1050 548 Z" fill="{O}" stroke="{N}" stroke-width="3"/>
<path d="M960 548 L880 540 L884 478 L960 486 Z" fill="{W}" stroke="{N}" stroke-width="3"/>
<path d="M960 548 L1040 540 L1036 478 L960 486 Z" fill="{W}" stroke="{N}" stroke-width="3"/>
{"".join(f'<line x1="{896}" y1="{y}" x2="{948}" y2="{y+4}" stroke="{G}" stroke-width="5" stroke-linecap="round"/><line x1="{972}" y1="{y+4}" x2="{1024}" y2="{y}" stroke="{G}" stroke-width="5" stroke-linecap="round"/>' for y in (496, 512, 528))}
{"".join(f'<circle cx="960" cy="{y}" r="4" fill="{N}"/>' for y in (496, 514, 532))}
<circle cx="876" cy="520" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>
<circle cx="1044" cy="520" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>
{person(1205, 665-152*.68, .68, extra_back=parm(54, -140, 70, -40), extra_front=parm(-54, -140, -126, -100, -96, -150), legs=True)}'''
    return left + f'<line x1="640" y1="170" x2="640" y2="690" stroke="{G}" stroke-width="3"/>' + right


# ── ⑤ 계획서 ──────────────────────────────────────────
def s5():
    rows = [368, 400, 432, 464]
    items = "".join(f'<rect x="880" y="{y-9}" width="18" height="18" rx="3" fill="none" stroke="{N}" stroke-width="3"/>' + lines(912, 1006, [y], G, 8) for y in rows)
    return f'''
{floor(930, 662, 330)}
{person(790, 662-152*.85, .85, extra_back=parm(-54, -140, -70, -30, -74, -90), extra_front=parm(54, -140, 112, 2, 128, -90), legs=True)}
{robot(1125, 662, 1.3, rarm(-44, -86, -67, -178, -70, -120, hand=False) + rarm(44, -86, 75, -30))}
<g transform="rotate(10 1230 612)"><rect x="1205" y="595" width="52" height="36" rx="4" fill="{W}" stroke="{N}" stroke-width="3"/>{lines(1214, 1248, [607, 619], G, 4)}</g>
<circle cx="1222" cy="623" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>
<rect x="852" y="318" width="186" height="236" rx="12" fill="{N}"/>
<rect x="866" y="338" width="158" height="204" rx="4" fill="{W}"/>
<rect x="915" y="306" width="60" height="24" rx="6" fill="{G}" stroke="{N}" stroke-width="3"/>
{items}
<line x1="900" y1="432" x2="1016" y2="432" stroke="{O}" stroke-width="5" stroke-linecap="round"/>
<rect x="880" y="487" width="18" height="18" rx="3" fill="none" stroke="{O}" stroke-width="3" stroke-dasharray="4 3"/>
<line x1="912" y1="496" x2="948" y2="496" stroke="{O}" stroke-width="7" stroke-linecap="round"/>
<circle cx="1038" cy="431" r="10" fill="{G}" stroke="{N}" stroke-width="3"/>
<g transform="translate(954,499) rotate(150)">
  <path d="M0 0 L16 -7 L16 7 Z" fill="{N}"/>
  <rect x="16" y="-7" width="62" height="14" fill="{O}" stroke="{N}" stroke-width="2"/>
  <rect x="78" y="-7" width="12" height="14" fill="{G}" stroke="{N}" stroke-width="2"/>
</g>
<circle cx="885" cy="534" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>'''


# ── ⑥ 시험장 ──────────────────────────────────────────
def desk(dx):
    return (f'<path d="M{140+dx} 515 L{515+dx} 515 L{535+dx} 545 L{120+dx} 545 Z" fill="{G}" stroke="{N}" stroke-width="3"/>'
            f'<rect x="{120+dx}" y="545" width="415" height="14" fill="{N}"/>'
            f'<rect x="{140+dx}" y="559" width="12" height="110" fill="{N}"/><rect x="{503+dx}" y="559" width="12" height="110" fill="{N}"/>')


def sheet(x):
    return (f'<path d="M{x} 520 L{x+95} 520 L{x+103} 540 L{x-5} 540 Z" fill="{W}" stroke="{N}" stroke-width="2"/>'
            f'<line x1="{x+8}" y1="527" x2="{x+86}" y2="527" stroke="{G}" stroke-width="3"/><line x1="{x+6}" y1="533" x2="{x+70}" y2="533" stroke="{G}" stroke-width="3"/>')


def s6():
    left = f'''
<rect x="30" y="170" width="595" height="520" rx="24" fill="{G}" fill-opacity=".55"/>
{person(330, 520, .85, extra_front=parm(-54, -140, -32, -246, -100, -214) + parm(54, -140, 98, -14, 104, -80))}
{desk(0)}{sheet(375)}
<line x1="413" y1="508" x2="430" y2="530" stroke="{N}" stroke-width="5" stroke-linecap="round"/>
<circle cx="413" cy="508" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>
<text x="392" y="300" font-family="Pretendard, sans-serif" font-size="72" font-weight="800" fill="{N}">?</text>
<text x="446" y="252" font-family="Pretendard, sans-serif" font-size="44" font-weight="800" fill="{N}" fill-opacity=".55">?</text>'''
    tabs = "".join(f'<rect x="{x}" y="505" width="11" height="14" rx="2" fill="{O}" stroke="{N}" stroke-width="1.5"/>' for x in (800, 822, 884, 904, 926))
    right = f'''
<rect x="655" y="170" width="595" height="520" rx="24" fill="{W}" stroke="{G}" stroke-width="3"/>
{person(955, 520, .85, extra_front=parm(-54, -140, -129, -4, -110, -90) + parm(54, -140, 100, -4, 104, -80))}
{desk(625)}
{tabs}
<path d="M772 543 L860 539 L948 543 L944 520 L860 516 L782 520 Z" fill="{N}"/>
<path d="M860 516 L782 520 L776 540 L860 537 Z" fill="{W}" stroke="{N}" stroke-width="2.5"/>
<path d="M860 516 L938 520 L944 540 L860 537 Z" fill="{W}" stroke="{N}" stroke-width="2.5"/>
<line x1="792" y1="527" x2="850" y2="525" stroke="{G}" stroke-width="3"/><line x1="870" y1="525" x2="928" y2="527" stroke="{G}" stroke-width="3"/>
{sheet(1000)}
<circle cx="845" cy="517" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>
<line x1="1040" y1="510" x2="1054" y2="532" stroke="{N}" stroke-width="5" stroke-linecap="round"/>
<circle cx="1040" cy="517" r="10" fill="{W}" stroke="{N}" stroke-width="3"/>'''
    return left + right


# ── ⑦ 세 가지 답 ───────────────────────────────────────
def s7():
    cx = [227, 640, 1053]
    s = 1.45
    out = [f'<line x1="433" y1="190" x2="433" y2="670" stroke="{G}" stroke-width="3"/>',
           f'<line x1="847" y1="190" x2="847" y2="670" stroke="{G}" stroke-width="3"/>']
    out += [floor(x, 642, 130) for x in cx]
    # 1. 빈손으로 어깨를 으쓱
    x = cx[0]
    eyes = f'<circle cx="-11" cy="-154" r="3" fill="{N}"/><circle cx="19" cy="-154" r="3" fill="{N}"/>'
    out.append(robot(x, 640, s, eyes + rarm(-44, -86, -96, -138, -84, -96) + rarm(44, -86, 96, -138, 84, -96), mouth="wavy"))
    out.append(f'<text x="{x+74}" y="356" font-family="Pretendard, sans-serif" font-size="52" font-weight="800" fill="{N}">?</text>')
    # 2. 문서의 한 곳을 짚는다
    x = cx[1]
    out.append(robot(x, 640, s, rarm(44, -86, 44, -76, hand=False), mouth="grin"))
    out.append(f'''<rect x="{x+62}" y="416" width="94" height="120" rx="5" fill="{W}" stroke="{O}" stroke-width="5"/>
<rect x="{x+64}" y="418" width="90" height="12" fill="{O}"/>
{lines(x+76, x+142, [448, 462, 490, 504, 518])}
<line x1="{x+76}" y1="476" x2="{x+142}" y2="476" stroke="{O}" stroke-width="7" stroke-linecap="round"/>
<path d="M{x+128} 412 L{x+142} 412 L{x+142} 448 L{x+135} 440 L{x+128} 448 Z" fill="{O}" stroke="{N}" stroke-width="2"/>
<circle cx="{x+66}" cy="528" r="13" fill="{G}" stroke="{N}" stroke-width="3"/>''')
    out.append(f'<g transform="translate({x},640) scale({s})">{rarm(-44, -86, 59, -114, 0, -70, hand=False)}</g>')
    out.append(f'<line x1="{x+86}" y1="475" x2="{x+104}" y2="476" stroke="{N}" stroke-width="7" stroke-linecap="round"/><circle cx="{x+86}" cy="475" r="12" fill="{G}" stroke="{N}" stroke-width="3"/>')
    # 3. 빈 폴더를 열어 보이며 고개를 젓는다
    x = cx[2]
    out.append(robot(x, 640, s, rarm(-44, -86, -62, -70, hand=False) + rarm(44, -86, 62, -70, hand=False), mouth="flat"))
    out.append(f'''<path d="M{x-92} 500 L{x} 512 L{x} 594 L{x-92} 582 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M{x-92} 500 L{x-92} 490 L{x-56} 490 L{x-50} 504" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M{x} 512 L{x+92} 500 L{x+92} 582 L{x} 594 Z" fill="{G}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>
<path d="M{x-80} 512 L{x-6} 522 L{x-6} 582 L{x-80} 572 Z M{x+6} 522 L{x+80} 512 L{x+80} 572 L{x+6} 582 Z" fill="{W}"/>
<circle cx="{x-92}" cy="540" r="13" fill="{G}" stroke="{N}" stroke-width="3"/><circle cx="{x+92}" cy="540" r="13" fill="{G}" stroke="{N}" stroke-width="3"/>
<path d="M{x-96} 400 Q{x-108} 428 {x-96} 456 M{x-114} 408 Q{x-124} 428 {x-114} 448" stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M{x+96} 400 Q{x+108} 428 {x+96} 456 M{x+114} 408 Q{x+124} 428 {x+114} 448" stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round"/>''')
    return "".join(out)


# ── ⑧ 기초 ────────────────────────────────────────────
def s8():
    offs = [-6, 0, 5, -3, 4, -5, 2, -2]
    stack = []
    for i, o in enumerate(offs):
        y = 525 + i * 19.5
        stack.append(f'<rect x="{824+o}" y="{y}" width="232" height="17" rx="3" fill="{W}" stroke="{N}" stroke-width="2.5"/>')
        stack.append(f'<line x1="{840+o}" y1="{y+8.5}" x2="{900+o}" y2="{y+8.5}" stroke="{G}" stroke-width="3"/>')
    for i, side in ((1, "L"), (2, "R"), (4, "L"), (5, "R"), (6, "L"), (3, "R")):
        y = 529 + i * 19.5
        x = 812 + offs[i] if side == "L" else 1054 + offs[i]
        stack.append(f'<rect x="{x}" y="{y}" width="16" height="10" rx="2" fill="{O}" stroke="{N}" stroke-width="1.5"/>')
    win = "".join(f'<rect x="{862+i*46}" y="{176+j*44}" width="26" height="26" rx="3" fill="{G}"/>' for i in range(4) for j in range(7))
    lean = (f'<g transform="rotate(7 1130 520)"><rect x="1130" y="332" width="80" height="188" rx="3" fill="{G}" stroke="{N}" stroke-width="4"/>'
            + "".join(f'<rect x="{1144+i*30}" y="{350+j*38}" width="20" height="22" rx="2" fill="{W}" stroke="{N}" stroke-width="2"/>' for i in range(2) for j in range(4))
            + "</g>")
    return f'''
<rect x="540" y="520" width="720" height="175" fill="{G}" fill-opacity=".55"/>
{"".join(stack)}
<line x1="540" y1="520" x2="1260" y2="520" stroke="{N}" stroke-width="4"/>
<rect x="830" y="140" width="220" height="14" rx="3" fill="{N}"/>
<rect x="840" y="152" width="200" height="370" fill="{N}"/>
{win}
<rect x="920" y="476" width="40" height="46" rx="3" fill="{G}"/>
{lean}
<path d="M1146 524 L1156 544 L1148 560 L1160 582" stroke="{N}" stroke-width="3" fill="none" stroke-linecap="round"/>
{person(735, 520-152*.68, .68, extra_back=parm(-54, -140, -70, -30), extra_front=parm(54, -140, 100, 4, 104, -80), legs=True)}
<line x1="803" y1="420" x2="818" y2="436" stroke="{N}" stroke-width="6" stroke-linecap="round"/>
<circle cx="803" cy="420" r="9" fill="{W}" stroke="{N}" stroke-width="3"/>
{robot(625, 520, 1.0, rarm(44, -86, 92, -40, 80, -80) + rarm(-44, -86, -66, -40))}
<line x1="717" y1="480" x2="734" y2="492" stroke="{N}" stroke-width="7" stroke-linecap="round"/>'''


# ── 슬라이드 ─────────────────────────────────────────
SLIDES = [
    ("left", "AI 답, 그대로 써도 될까요?", "AI가 건넨 문장은 출처를 확인하기 전까지 초안이다.", s1),
    ("top25", "AI는 모를 때도 문장을 완성한다", "언어 모델은 아는 내용과 모르는 내용을 같은 말투로 쓴다.", s2),
    ("top", "AI가 모르는 두 가지: 최신 정보, 우리 회사", "학습이 끝난 뒤의 일과 사내 문서는 모델의 기억에 없다.", s3),
    ("top", "근거를 찾아오게 하거나, 근거 안에 가두거나", "Deep Research는 웹에서 근거를 모으고, NotebookLM은 올린 자료만 본다.", s4),
    ("left", "Deep Research는 계획부터 세운다", "검색 계획을 실행 전에 고치면 엉뚱한 보고서를 다시 받을 일이 준다.", s5),
    ("top", "노트북은 오픈북 시험이다", "NotebookLM은 올린 자료 안에서만 답하고, 답마다 출처를 단다.", s6),
    ("top", "같은 질문, 세 가지 답", "근거가 없을 때 없다고 말하는 답도 쓸 수 있는 답이다.", s7),
    ("left", "AI 답의 품질은 근거의 품질이다", "확인된 문서를 먼저 쌓아야 그 위의 답이 버틴다.", s8),
]

CSS = '''
  /* ── 그림 슬라이드: 남색·회색·주황 3색 ── */
  .slide.ill{padding:0; background:#fff; border:none;}
  .slide.ill svg.scene{position:absolute; inset:0; width:1280px; height:720px;}
  .ill .cap{position:absolute; z-index:2; color:#1F3A5F;}
  .ill .cap.left{left:72px; top:0; bottom:0; width:420px; display:flex; flex-direction:column; justify-content:center;}
  .ill .cap.top, .ill .cap.top25{left:72px; right:72px; top:40px;}
  .ill .cap h2{font-size:46px; line-height:1.2; letter-spacing:-.03em; font-weight:800; margin:0; word-break:keep-all;}
  .ill .cap.top h2, .ill .cap.top25 h2{font-size:38px;}
  .ill .cap .bar{width:56px; height:5px; border-radius:3px; background:#F28C28; margin:22px 0 18px;}
  .ill .cap p{font-size:18px; line-height:1.6; margin:0; color:#1F3A5F; opacity:.78; word-break:keep-all;}
  .ill .cap.top .bar, .ill .cap.top25 .bar{display:none;}
  .ill .cap.top p, .ill .cap.top25 p{margin-top:10px;}
  .ill .coord{z-index:3;}
'''


def build():
    parts = [DEFS]
    for i, (pos, title, line, fn) in enumerate(SLIDES):
        active = " active" if i == 0 else ""
        parts.append(f'''<section class="slide ill{active}" data-title="{title}">
  <svg class="scene" viewBox="0 0 1280 720" aria-hidden="true">{fn()}</svg>
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="cap {pos}"><h2>{title}</h2><div class="bar"></div><p>{line}</p></div>
</section>''')
    tpl = (ROOT / "src" / "template.html").read_text()
    tpl = tpl.replace("</style>", CSS + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", "AI 답과 근거").replace("{{SLIDES}}", "\n\n".join(parts))
    out = ROOT / "docs" / "grounding" / "index.html"
    out.write_text(html)
    print(out)


if __name__ == "__main__":
    build()
