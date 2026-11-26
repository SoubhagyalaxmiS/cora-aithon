# -*- coding: utf-8 -*-
import sys,html,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import content as C
import weasyprint

def norm(t):
    for a,b in (("programmes","programs"),("programme","program"),("Programmes","Programs"),("Programme","Program"),("organisations","organizations"),("organisation","organization"),("Organisation","Organization"),("paediatric","pediatric"),("licence","license"),("centre","center")):
        t=t.replace(a,b)
    return t
def E(t):return html.escape(norm(t),quote=False)

pitch=("Clinicians’ training evidence sits in separate systems: RQI1Stop, AHA cards, PediaSkills for NRP and PEPP, SimCapture and local learning systems. "
 "Each shows one piece. CORA sits above them and builds one living clinical identity: seven skill areas, what is current, expiring or missing, and the experience behind it. "
 "No scores. AI does the work rules cannot: matching people, mapping activities to skills, explaining in plain language with citations, and answering educators’ questions. It never grades anyone.")
facts=[("12","synthetic clinicians"),("98","evidence records (95 counted, 3 awaiting an identity match)"),("6","sources: RQI1Stop, AHA cards, PediaSkills, SimCapture, local LMS, unit log"),("7","skill areas, 4 statuses, 45-day “due soon” window"),("3","live AI steps: cited summary, ask this passport, admin search"),("5","layers in the high-level design, 10 numbered steps in the detailed design")]
ext=["AHA 2025 guidelines: CPR skills can decline within about three months of training; monitoring exposure to resuscitation events is recommended; consistent mastery standards and teamwork measurement are open gaps.",
     "RQI Partners is the AHA and Laerdal venture formed in 2018. PEPP’s fifth edition launched on 15 September 2026 with AAP and RQI Partners.",
     "EU AI Act: AI that evaluates learning outcomes or employees can be high-risk. Obligations are currently postponed to December 2027 per legal summaries. Confirm with Laerdal legal before quoting."]
say=["evidence","describes what is on file","cited","synthetic data","a hypothesis we will test","not decided yet","we have not measured that yet","a person approves"]
avoid=["score","rank","competence rating","saves X percent","production-ready","validated","compliant","anonymous","replaces SimCapture or RQI"]
real=["Passport interface: constellation, timeline, evidence drawer, source records","Status logic (current, due soon, lapsed, no evidence), computed by code","Learner and administrator roles with demo sign-in","AI chat: cited summary, ask this passport, plain-English admin search (live model on the hosted link)","Guardrail checks on every answer, and refusals to rank","Offline rules mode with the same checks","Identity-match logic with a pending queue (rules)","Three visual themes"]
mock=["Source feeds and record shapes (assumptions). The intake route is not decided","Exposure logs (synthetic)","Authentication (demo accounts only)","Matching and mapping by a model (rules today) and their approval screens","PDF conversion with OCR or a model","Consent and sources screens, team view (marked later)","Security hardening, load tests, accuracy evaluation, bias and injection testing"]
recover=[("Permission prompt on the first AI question","Click Allow. It uses the viewer’s own account."),
 ("An answer takes long","The first call can take several seconds. If it drags, switch to Offline rules."),
 ("Model error or rate limit","The chat falls back to rules by itself and the label says so."),
 ("No connection","Use Offline rules and say plainly that it is rules."),
 ("Opened from a downloaded file","AI is unavailable by design there. Use the hosted link with the jury."),
 ("A question you have not rehearsed","Type it in Live AI mode. If it refuses, explain the guardrail.")]
demo=["Learner: open the constellation, click a record.","Ask: What should be refreshed next? Read the check chips.","Ask: Is this person the best in the unit? It refuses.","Switch to the administrator. Ask: NICU staff with CPR lapsed.","Ask: Rank the nurses. It refuses. Open Daniel Reyes’s passport."]
srcs=["AHA 2025 Guidelines for CPR and ECC, Part 12: Resuscitation Education Science (cpr.heart.org).","AHA and Laerdal alliance and RQI Partners announcements; RQI program and RQI Analytics pages.","AAP pages for PEPP, NRP, NEPP and PediaSkills.","EU AI Act high-risk categories and the Digital Omnibus postponement, from legal analyses. Not the regulation text itself.","Laerdal SimCapture and Samaritan AI pages; HealthStream and Relias vendor pages. These are vendor descriptions."]

css='''
@page{size:A4;margin:18mm 16mm 20mm 16mm;
  @bottom-left{content:"CORA = Competency Optimization Readiness Agent - Your clinical competency passport";font:8pt Inter;color:#595959}
  @bottom-right{content:counter(page);font:8pt Inter;color:#595959}}
@page :first{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box}
html{font:10pt/1.5 Inter,"Liberation Sans",sans-serif;color:#1F1F1F}
body{margin:0}
h1,h2,h3{margin:0;font-weight:700;letter-spacing:-.01em}
.cover{page-break-after:always;height:297mm;background:#1F1F1F;color:#fff;padding:22mm 20mm;position:relative}
.cover .logo{background:#fff;border-radius:4mm;width:46mm;padding:3mm 4mm;display:block}
.cover .logo img{width:100%;display:block}
.cover h1{font-size:34pt;line-height:1.1;margin-top:62mm;max-width:150mm}
.cover .sub{font-size:16pt;margin-top:6mm;color:#D9D9D9;max-width:150mm}
.cover .meta{position:absolute;left:20mm;bottom:24mm;right:20mm;font-size:11pt;color:#D9D9D9;line-height:1.7}
.cover .meta b{color:#fff;font-size:15pt}
.cover .note{margin-top:4mm;font-size:9pt;color:#A0A0A0;max-width:150mm}
.red{color:#E42313}
.band{break-after:avoid;break-inside:avoid;display:flex;gap:5mm;align-items:center;background:#1F1F1F;color:#fff;border-radius:3mm;padding:5mm 6mm;margin:0 0 5mm}
.band .l{background:#E42313;color:#fff;font-weight:700;font-size:18pt;border-radius:2mm;width:12mm;height:12mm;text-align:center;line-height:12mm}
.band h2{font-size:15pt}
.band .w{margin-left:auto;font-size:15pt;font-weight:700;color:#fff}
.band .o{font-size:9pt;color:#D9D9D9;margin-top:1mm}
.sec{margin-top:4mm}
.qa{border:1px solid #DEDEDE;border-left:3px solid #E42313;border-radius:2mm;padding:4mm 5mm;margin:0 0 4mm;break-inside:avoid;background:#fff}
.qa .id{color:#E42313;font-weight:700;font-size:9pt}
.qa h3{font-size:11pt;margin:.5mm 0 2mm;line-height:1.35}
.qa p{margin:0 0 1.6mm}
.qa .say{font-size:10pt}
.qa .show,.qa .push{font-size:8.8pt;color:#404040}
.lab{font-weight:700;font-size:7.8pt;letter-spacing:.04em;text-transform:uppercase;margin-right:2mm}
.say .lab{color:#E42313}.show .lab{color:#595959}.push .lab{color:#A85A00}
.box{background:#F5F5F5;border-radius:3mm;padding:4mm 5mm;margin:0 0 4mm}
.box h3{font-size:11.5pt;margin-bottom:2mm}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:3mm 5mm}
.fact{display:flex;gap:3mm;align-items:baseline}
.fact b{font-size:15pt;color:#E42313;min-width:11mm}
.fact span{font-size:9pt;color:#404040}
ul{margin:0;padding-left:5mm}li{margin:0 0 1mm}
.tag{display:inline-block;background:#fff;border:1px solid #DEDEDE;border-radius:1.5mm;padding:.4mm 2mm;margin:0 1mm 1mm 0;font-size:8.8pt}
.tag.no{border-color:#E42313;color:#B3261E}
table{width:100%;border-collapse:collapse;font-size:9pt}
th{background:#1F1F1F;color:#fff;text-align:left;padding:2mm 3mm}
td{border-bottom:1px solid #DEDEDE;padding:2mm 3mm;vertical-align:top}
.cheat td:first-child{width:46mm;font-weight:700}
.cheat td:last-child{width:11mm;color:#E42313;font-weight:700}
.idx{columns:2;column-gap:8mm;font-size:8.6pt}
.idx div{break-inside:avoid;margin:0 0 .8mm}
.idx a{color:#1F1F1F;text-decoration:none;display:flex;gap:2mm;justify-content:space-between}.idx a span.p{color:#595959}
.idx a span.q{flex:1}
.idx h4{margin:3mm 0 1mm;font-size:9.5pt;color:#E42313;break-after:avoid}
.pg{page-break-before:always}
h1.pt{font-size:20pt;margin:0 0 4mm}
.sub2{color:#595959;margin:0 0 4mm}
'''
def card(q):
    i,qq,say_,show_,push_=q
    return (f'<section class="qa" id="{i}"><div class="id">{i}</div><h3>{E(qq)}</h3>'
            f'<p class="say"><span class="lab">Say</span>{E(say_)}</p>'
            f'<p class="show"><span class="lab">Show</span>{E(show_)}</p>'
            f'<p class="push"><span class="lab">If pushed</span>{E(push_)}</p></section>')
h=[]
h.append(f'<div class="cover"><span class="logo"><img src="file://{ROOT}/assets/brand/laerdal-logo.png" alt="Laerdal"></span><h1>Jury Q&amp;A preparation guide</h1><div class="sub">CORA: AI Clinical Competency Passport<br>Likely questions, convincing answers, and the honest limits behind them</div><div class="meta"><b>CORA</b><br>Automate the everyday<br>AIThon 2026, 27 Nov 2026, 10:15<br>6th floor, Positron/Electron<div class="note">Internal preparation material, not for the jury. The answers are written to be truthful: where something is not built or not decided, the guide says so.</div></div></div>')
# page 2
h.append(f'<h1 class="pt">Start here</h1><p class="sub2">How to use this guide: every question has a short spoken answer (Say), what to open on screen (Show), and the honest limit if the jury pushes (If pushed). Questions follow the six scoring criteria.</p>')
h.append(f'<div class="box"><h3>The 30-second pitch</h3><p style="margin:0">{E(pitch)}</p></div>')
h.append('<div class="box"><h3>Numbers you can quote (from the prototype)</h3><div class="facts">'+"".join(f'<div class="fact"><b>{n}</b><span>{E(t)}</span></div>' for n,t in facts)+'</div></div>')
h.append('<div class="box"><h3>Outside facts you can rely on</h3><ul>'+"".join(f'<li>{E(t)}</li>' for t in ext)+'</ul></div>')
h.append('<div class="box" ><h3>Three-minute demo path</h3><ol style="margin:0;padding-left:5mm">'+"".join(f'<li>{E(t)}</li>' for t in demo)+'</ol></div>')
# cheat sheet
h.append('<div class="pg"></div><h1 class="pt">Ten questions to be ready for</h1><p class="sub2">One-line answers. The last column is the question number for the full answer.</p><table class="cheat"><tr><th>If asked</th><th>Answer in one breath</th><th>Q</th></tr>'+"".join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{c}</td></tr>' for a,b,c in C.CHEAT)+'</table>')
h.append('<div class="grid2" style="margin-top:6mm"><div class="box"><h3>Words to use</h3>'+"".join(f'<span class="tag">{E(t)}</span>' for t in say)+'</div><div class="box"><h3>Words to avoid</h3>'+"".join(f'<span class="tag no">{E(t)}</span>' for t in avoid)+'</div></div>')
# real vs mocked
h.append('<div class="pg"></div><h1 class="pt">What is real, and what is not</h1><p class="sub2">Say this before they ask. It builds trust and protects the claims you do make.</p><div class="grid2"><div class="box"><h3>Real today</h3><ul>'+"".join(f'<li>{E(t)}</li>' for t in real)+'</ul></div><div class="box"><h3>Mocked or not built</h3><ul>'+"".join(f'<li>{E(t)}</li>' for t in mock)+'</ul></div></div>')
h.append('<h3 style="margin:2mm 0 3mm">If something goes wrong in the demo</h3><table><tr><th style="width:62mm">Situation</th><th>What to do</th></tr>'+"".join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a,b in recover)+'</table>')
h.append('<div class="box" style="margin-top:5mm;border-left:3px solid #A85A00"><h3>Before the session</h3><p style="margin:0">The live AI has been tested with a stand-in model and the offline rules have been tested in full, but the live call has not yet been run against a real model. Open the hosted prototype once, ask the three demo questions in Live AI mode and click Allow when asked.</p></div>')
# sections
for L,name,w,obj,qs in C.SECTIONS:
    wt=f'<div class="w">{w}</div>' if w else ""
    h.append(f'<div class="sec"></div><div class="band"><div class="l">{L}</div><div><h2>{E(name)}</h2><div class="o">{E(obj)}</div></div>{wt}</div>')
    for q in qs:h.append(card(q))
# sources + index
h.append('<h1 class="pt" style="margin-top:8mm">Where the outside facts come from</h1><p class="sub2">Confirm each before quoting it outside this room.</p><ul>'+"".join(f'<li>{E(t)}</li>' for t in srcs)+'</ul>')
h.append('<h1 class="pt" style="margin-top:8mm">Question index</h1><div class="idx">')
for L,name,w,obj,qs in C.SECTIONS:
    h.append(f'<h4>{L}. {E(name)}</h4>')
    for q in qs:
        h.append(f'<div><a href="#{q[0]}"><span class="q">{q[0]}  {E(q[1])}</span><span class="p">@@{q[0]}@@</span></a></div>')
h.append('</div>')
doc='<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>CORA: Jury Q&amp;A preparation guide</title><style>'+css+'</style></head><body>'+"".join(h)+'</body></html>'
# make the page-number span use the parent's href
doc=doc.replace('<span class="p"></span></a>','<span class="p"></span></a>')


import re as _re
first=weasyprint.HTML(string=_re.sub(r"@@[A-Z0-9]+@@","00",doc)).render()
pages={}
for n,pg in enumerate(first.pages,1):
    for name in pg.anchors:
        pages.setdefault(name,n)
doc2=_re.sub(r"@@([A-Z0-9]+)@@",lambda m:str(pages.get(m.group(1),"")),doc)

OUT=ROOT/"docs/jury-qa/CORA-Jury-QA-Preparation-Guide.pdf";OUT.parent.mkdir(parents=True,exist_ok=True)
weasyprint.HTML(string=doc2).write_pdf(str(OUT))
print("pdf written; anchors found:",len(pages))
