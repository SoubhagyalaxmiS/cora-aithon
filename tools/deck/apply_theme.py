#!/usr/bin/env python3
"""Write the Laerdal-style colour and font scheme (theme.json) into a .pptx file.

pptxgenjs builds the deck with scheme colours; this step gives those scheme slots
their real values. Usage: python3 apply_theme.py path/to/deck.pptx
"""
import json, re, shutil, sys, tempfile, zipfile
from pathlib import Path

theme = json.loads((Path(__file__).parent / "theme.json").read_text(encoding="utf8"))
slots = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"]
clr = "".join(f'<a:{k}><a:srgbClr val="{theme["colors"][k]}"/></a:{k}>' for k in slots)

def patch(xml: str) -> str:
    xml = re.sub(r'(<a:theme [^>]*?)name="[^"]*"', r'\1name="%s"' % theme["name"], xml, count=1)
    xml = re.sub(r"<a:clrScheme[^>]*>.*?</a:clrScheme>", '<a:clrScheme name="%s">%s</a:clrScheme>' % (theme["name"], clr), xml, flags=re.S)
    xml = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="%s"' % theme["name"], xml)
    xml = re.sub(r'(<a:majorFont><a:latin typeface=")[^"]*', r"\g<1>" + theme["headFontFace"], xml)
    xml = re.sub(r'(<a:minorFont><a:latin typeface=")[^"]*', r"\g<1>" + theme["bodyFontFace"], xml)
    return xml

src = Path(sys.argv[1])
tmp = Path(tempfile.mkdtemp()) / src.name
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if re.match(r"ppt/theme/theme\d+\.xml$", item.filename):
            data = patch(data.decode("utf8")).encode("utf8")
        zout.writestr(item, data)
shutil.move(str(tmp), src)
print(f"theme '{theme['name']}' applied to {src.name}")
