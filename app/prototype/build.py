#!/usr/bin/env python3
"""Inline styles.css and app.js into index.html and write one self-contained file.

The single file is what gets hosted (and what the tests run against).
Usage: python3 app/prototype/build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE / "dist" / "clinical-identity-passport.html"

html = (SRC / "index.html").read_text(encoding="utf8")
css = (SRC / "styles.css").read_text(encoding="utf8")
js = (SRC / "app.js").read_text(encoding="utf8")

link = '<link rel="stylesheet" href="styles.css">'
script = '<script src="app.js"></script>'
assert html.count(link) == 1 and html.count(script) == 1, "index.html must contain one stylesheet link and one script tag"

html = html.replace(link, "<style>" + css + "</style>").replace(script, "<script>" + js + "</script>")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf8")
print(f"wrote {OUT.relative_to(HERE.parent.parent)} ({len(html)//1024} KB)")
