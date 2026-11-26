#!/usr/bin/env python3
"""Render PNG images of the poster and both architecture diagrams in the Laerdal theme.

Needs wkhtmltoimage on PATH and Pillow. The diagrams are plain SVG, so the colour
variables are resolved here before rendering (wkhtmltoimage predates CSS variables).
Usage: python3 tools/export/make_images.py
"""
import re, subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
TMP = Path(tempfile.mkdtemp())


def tokens(block):
    return dict(re.findall(r"--([a-z0-9-]+):([^;]+);", block))


def laerdal_tokens(css):
    base = tokens(css.split("@media (prefers-color-scheme: dark)")[0])
    lae = re.search(r':root\[data-theme="laerdal"\]\{(.*?)\}\n', css, re.S)
    base.update(tokens(lae.group(1)))
    return base


def load(path):
    s = path.read_text(encoding="utf8")
    css = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
    return s, laerdal_tokens(css)


def page(svg, t, w):
    t = dict(t)
    t["glow1"] = t["glow2"] = t["grid"] = "#F5F5F5"  # no background glows in static images
    svg = re.sub(r"var\(--([a-z0-9-]+)\)", lambda m: t.get(m.group(1), "#f0f").strip(), svg)
    svg = re.sub(
        r'<svg [^>]*?viewBox="0 0 (\d+) (\d+)"[^>]*>',
        lambda m: f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {m.group(1)} {m.group(2)}" width="{w}" height="{int(w * int(m.group(2)) / int(m.group(1)))}">',
        svg, count=1)
    css = ('body{margin:0;background:#F5F5F5}svg text{font-family:"DejaVu Sans",sans-serif}.h,.sh{font-weight:700}'
           '.b{font-weight:500}.bb{font-weight:700}.lgx{display:inline}.dec{display:none}rect.aip{fill:#E42313}')
    return f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{svg}</body></html>"


def render(name, svg, t, w, dest):
    html = TMP / f"{name}.html"
    html.write_text(page(svg, t, w), encoding="utf8")
    out = dest / f"{name}.png"
    subprocess.run(["wkhtmltoimage", "--quiet", "--width", str(w), "--disable-javascript", str(html), str(out)],
                   stderr=subprocess.DEVNULL, check=True)
    im = Image.open(out).convert("RGB")
    im.save(out, optimize=True)
    print(f"{out.relative_to(ROOT)}  {im.size[0]}x{im.size[1]}")


s, t = load(DOCS / "poster/clinical-competency-passport-poster.html")
svg = re.search(r'<svg id="poster".*?</svg>', s, re.S).group(0)
render("clinical-competency-passport-poster", svg, t, 1800, DOCS / "poster")

s, t = load(DOCS / "architecture/clinical-passport-architecture.html")
for idn, name in (("svg-hld", "architecture-high-level-design"), ("svg-detailed", "architecture-detailed-design")):
    svg = re.search(r'<svg class="d" id="' + idn + r'".*?</svg>', s, re.S).group(0)
    render(name, svg, t, 2400, DOCS / "architecture")
