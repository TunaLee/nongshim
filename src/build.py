#!/usr/bin/env python3
"""덱을 template.html 에 붙여 docs/<덱>/index.html 을 만든다.

사용: python3 src/build.py         → docs/grounding (본 강의)
      python3 src/build.py gas     → docs/gas-dashboard (Skill + Apps Script 짧은 강의)
"""
import sys
from pathlib import Path

import art
import deck
import explain
import intro

ROOT = Path(__file__).resolve().parent.parent
DECKS = {
    "grounding": ("course", "grounding", "AI로 일하는 방식 바꾸기"),
    "gas": ("deck_gas", "gas-dashboard", "Skill과 Apps Script 실적 대시보드"),
}


def build(name="grounding"):
    mod_name, out_dir, title = DECKS[name]
    mod = __import__(mod_name)
    parts = [art.DEFS] + mod.slides()
    extra = getattr(mod, "CSS", "") if mod is not deck else ""
    tpl = (ROOT / "src" / "template.html").read_text()
    tpl = tpl.replace("</style>", intro.CSS + explain.CSS + deck.CSS + extra + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", title).replace("{{SLIDES}}", "\n\n".join(parts))
    out = ROOT / "docs" / out_dir / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(out, len(parts) - 1, "장")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "grounding")
