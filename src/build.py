#!/usr/bin/env python3
"""이론 덱을 template.html 에 붙여 docs/grounding/index.html 을 만든다.

구성은 deck.py, 그림 부품은 art.py, 장면은 scenes_*.py.
사용: python3 src/build.py
"""
from pathlib import Path

import art
import deck
import explain
import intro

ROOT = Path(__file__).resolve().parent.parent


def build():
    parts = [art.DEFS] + deck.slides()
    tpl = (ROOT / "src" / "template.html").read_text()
    tpl = tpl.replace("</style>", intro.CSS + explain.CSS + deck.CSS + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", "AI로 일하는 방식을 바꾸는 이틀").replace("{{SLIDES}}", "\n\n".join(parts))
    out = ROOT / "docs" / "grounding" / "index.html"
    out.write_text(html)
    print(out, len(parts) - 1, "장")


if __name__ == "__main__":
    build()
