import math,re,json
from PIL import ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf";FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def wid(t,size,bold):
    # text-fit checks use DejaVu Sans when it is installed; without it the checks are skipped
    try:return ImageFont.truetype(FB if bold else FR,int(round(size))).getlength(t)
    except OSError:return 0
BAD=[]
def esc(s):return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
CLS={"h":True,"sh":True,"b":False,"bb":False}
def T(x,y,t,cls,size,anchor="start",maxw=None,extra=""):
    if maxw is not None:
        ww=wid(t,size,CLS[cls])
        if ww>maxw:BAD.append((t,round(ww),maxw))
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}" {extra}>{esc(t)}</text>'
def mark(kind,x,y,s,style):
    if kind=="circle":return f'<circle cx="{x}" cy="{y}" r="{s}" style="{style}"/>'
    if kind=="diamond":return f'<path d="M{x} {y-s-1}L{x+s+1} {y}L{x} {y+s+1}L{x-s-1} {y}Z" style="{style}"/>'
    if kind=="square":return f'<rect x="{x-s}" y="{y-s}" width="{2*s}" height="{2*s}" rx="2" style="{style}"/>'
    if kind=="triangle":return f'<path d="M{x} {y-s-1}L{x+s+1} {y+s}L{x-s-1} {y+s}Z" style="{style}"/>'
    if kind=="hex":
        p="L".join(f"{x+(s+1)*math.cos(math.pi/3*i+math.pi/6):.1f} {y+(s+1)*math.sin(math.pi/3*i+math.pi/6):.1f}" for i in range(6))
        return f'<path d="M{p}Z" style="{style}"/>'
    return f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" style="{style};stroke-width:3;fill:none"/>'
SRC=[("rqi","RQI1Stop","circle"),("hc","AHA cards","diamond"),("pedia","PediaSkills","square"),("sim","SimCapture","triangle"),("lms","Local LMS","hex"),("log","Unit log","cross")]
def sm(k,x,y,s):
    kind=[z[2] for z in SRC if z[0]==k][0]
    st=f"fill:var(--src-{k});stroke:var(--src-{k})" if kind=="cross" else f"fill:var(--src-{k})"
    if kind=="cross":st=f"stroke:var(--src-{k})"
    return mark(kind,x,y,s,st)

o=[]
# ---------- defs and background ----------
o.append('''<defs>
<linearGradient id="band" x1="0" y1="0" x2="1" y2="0.4"><stop offset="0" style="stop-color:var(--band1)"/><stop offset="1" style="stop-color:var(--band2)"/></linearGradient>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--accent)"/><stop offset="1" style="stop-color:var(--accent2)"/></linearGradient>
<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" style="stop-color:var(--tg2)"/></linearGradient>
<radialGradient id="cg"><stop offset="0" style="stop-color:var(--panel-strong)"/><stop offset="1" style="stop-color:var(--accent-soft)"/></radialGradient>
<radialGradient id="gl1"><stop offset="0" style="stop-color:var(--glow1)"/><stop offset="1" style="stop-color:var(--glow1);stop-opacity:0"/></radialGradient>
<radialGradient id="gl2"><stop offset="0" style="stop-color:var(--glow2)"/><stop offset="1" style="stop-color:var(--glow2);stop-opacity:0"/></radialGradient>
<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" style="stroke:var(--grid)"/></pattern>
<filter id="bl" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<rect width="1200" height="1697" style="fill:var(--bg)"/>
<circle cx="140" cy="60" r="520" fill="url(#gl1)"/><circle cx="1180" cy="120" r="460" fill="url(#gl2)"/><circle cx="600" cy="1560" r="520" fill="url(#gl1)" opacity=".6"/>
<rect width="1200" height="1697" fill="url(#grid)"/>''')

# ---------- header ----------
o.append('<rect x="30" y="30" width="1140" height="250" rx="36" fill="url(#band)"/>')
for r in (52,92,132):o.append(f'<circle class="dec" cx="1020" cy="155" r="{r}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-dasharray="3 8"/>')
for i in range(7):
    a=math.radians(-90+i*360/7);o.append(f'<circle class="dec" cx="{1020+92*math.cos(a):.1f}" cy="{155+92*math.sin(a):.1f}" r="7" fill="#fff" fill-opacity=".92"/>')
o.append('<circle class="dec" cx="1020" cy="155" r="26" fill="none" stroke="#fff" stroke-width="3"/>')
_logo=open(ROOT/"assets/brand/laerdal-logo.svg",encoding="utf8").read()
LOGO_INNER=re.sub(r"<title>.*?</title>","",re.search(r"<svg[^>]*>(.*)</svg>",_logo,re.S).group(1),flags=re.S)
o.append('<g class="lgx"><rect x="968" y="84" width="176" height="96" rx="18" fill="#FFFFFF"/><g transform="translate(985 93) scale(1.6)">'+LOGO_INNER+'</g></g>')
o.append(T(76,122,"AI Clinical Competency","h",54,"start",840,'fill="#FFFFFF"'))
o.append(T(76,214,"Passport","h",104,"start",600,'fill="url(#tg)"'))
o.append(T(76,260,"From training completion to a living clinical identity.","sh",25,"start",900,'fill="#FFFFFF"'))
o.append(T(700,166,"CORA","sh",28,"start",420,'fill="#FFFFFF"'))
o.append(T(700,194,"Automate the everyday","b",18,"start",420,'fill="#FFFFFF" fill-opacity=".92"'))
o.append(T(700,220,"27 Nov 2026, 10:15  |  6th floor, Positron/Electron","b",16,"start",450,'fill="#FFFFFF" fill-opacity=".92"'))

# ---------- problem / solution ----------
def card(x,y,w,h,fill="panel",rx=30):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="fill:var(--{fill});stroke:var(--line)" stroke-width="1.5"/>'
o.append(card(30,296,540,240)); o.append(card(630,296,540,240,"panel-strong"))
o.append(T(54,344,"Today","sh",30,"start",300,'style="fill:var(--ink)"'))
o.append(T(54,374,"Six systems, six partial views","bb",20,"start",480,'style="fill:var(--muted)"'))
xs=[54,222,390]
for i,(k,name,kind) in enumerate(SRC):
    x=xs[i%3];y=396+(i//3)*66
    o.append(f'<rect x="{x}" y="{y}" width="156" height="52" rx="16" style="fill:var(--panel-strong);stroke:var(--line-strong)" stroke-dasharray="5 5" stroke-width="1.5"/>')
    o.append(sm(k,x+24,y+26,7))
    o.append(T(x+42,y+32,name,"bb",16,"start",106,'style="fill:var(--ink)"'))
o.append(T(654,344,"With the Passport","sh",30,"start",440,'style="fill:var(--ink)"'))
o.append(T(654,374,"One living clinical identity","bb",20,"start",480,'style="fill:var(--muted)"'))
cx,cy,rx,ry=900,462,175,56
pts=[]
for i,(k,name,kind) in enumerate(SRC):
    a=math.radians(-90+i*60+30)
    pts.append((cx+rx*math.cos(a),cy+ry*math.sin(a),k))
for x,y,k in pts:o.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" style="stroke:var(--src-{k})" stroke-opacity=".55" stroke-width="2"/>')
for x,y,k in pts:
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="20" style="fill:var(--src-{k})" opacity=".22" filter="url(#bl)"/>')
    o.append(sm(k,round(x,1),round(y,1),9))
o.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="url(#cg)" stroke="url(#ring)" stroke-width="4"/>')
o.append(T(cx,cy+9,"ID","h",26,"middle",None,'style="fill:var(--ink)"'))
o.append('<path d="M584 416H610M598 402L612 416L598 430" fill="none" style="stroke:var(--accent)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')

# ---------- hero ----------
o.append(card(30,552,1140,640,"panel-strong",36))
o.append(T(60,626,"Seven skills. One identity.","sh",32,"start",600,'style="fill:var(--ink)"'))
o.append('<g></g>')
DOMS=[("CPR &","resuscitation","current",5,"Current"),("Airway","management","current",3,"Current"),("Patient","assessment","current",4,"Current"),("Emergency","response","due",2,"Due soon"),("Medication","administration","lapsed",1,"Lapsed"),("Communication","& teamwork","current",3,"Current"),("Maternal & neonatal","emergencies","none",0,"No evidence")]
CX,CY,R=600,895,162
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" style="stroke:var(--line-strong)" stroke-dasharray="2 7"/><circle cx="{CX}" cy="{CY}" r="{R-80}" fill="none" style="stroke:var(--line-strong)" stroke-dasharray="2 7"/>')
nodes=[];spokes=[]
for i,(l1,l2,st,c,stl) in enumerate(DOMS):
    a=math.radians(-90+i*360/7);x=CX+R*math.cos(a);y=CY+R*math.sin(a)
    r=16+min(c,6)*2.4 if c else 15
    col=f"var(--{st})"
    spokes.append(f'<line x1="{CX+74*math.cos(a):.1f}" y1="{CY+74*math.sin(a):.1f}" x2="{x-(r+6)*math.cos(a):.1f}" y2="{y-(r+6)*math.sin(a):.1f}" style="stroke:{col}" stroke-opacity=".5" stroke-width="2"{" stroke-dasharray=\"3 6\"" if st=="none" else ""}/>')
    g=[]
    if c:g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+16:.1f}" style="fill:{col}" opacity=".28" filter="url(#bl)"/>')
    g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" style="fill:var(--panel-strong);stroke:{col}" stroke-width="3"{" stroke-dasharray=\"4 4\"" if st=="none" else ""}/>')
    g.append(T(f"{x:.1f}",f"{y+6:.1f}",str(c) if c else "–","h",16,"middle",None,'style="fill:var(--ink)"'))
    cosv=math.cos(a)
    if i==0:
        tx=x;an="middle";ys=(y-r-16,y-r-16-24,None)
        g.append(T(f"{tx:.1f}",f"{y-r-16-26:.1f}",f"{l1} {l2}","sh",21,"middle",300,'style="fill:var(--ink)"'))
        g.append(T(f"{tx:.1f}",f"{y-r-16:.1f}",stl,"sh",19,"middle",None,f'style="fill:{col}"'))
    else:
        if cosv>0:tx=x+r+18;an="start"
        else:tx=x-r-18;an="end"
        w1=max(wid(l1,21,True),wid(l2,21,True))
        avail=(1170-30-tx) if an=="start" else (tx-60)
        if w1>avail:BAD.append((l1+l2,round(w1),round(avail)))
        g.append(T(f"{tx:.1f}",f"{y-14:.1f}",l1,"sh",21,an,None,'style="fill:var(--ink)"'))
        g.append(T(f"{tx:.1f}",f"{y+11:.1f}",l2,"sh",21,an,None,'style="fill:var(--ink)"'))
        g.append(T(f"{tx:.1f}",f"{y+37:.1f}",stl,"sh",19,an,None,f'style="fill:{col}"'))
    nodes.append("".join(g))
o+=spokes
o.append(f'<circle cx="{CX}" cy="{CY}" r="86" fill="none" stroke="url(#ring)" stroke-width="1.5" stroke-dasharray="3 5"/><circle cx="{CX}" cy="{CY}" r="78" fill="url(#cg)" stroke="url(#ring)" stroke-width="4"/>')
o.append(T(CX,CY+8,"ID","h",34,"middle",None,'style="fill:var(--ink)"'))
o.append(T(CX,CY+34,"Clinical identity","b",15,"middle",150,'style="fill:var(--muted)"'))
o+=nodes
# legend chips
lx=60
for st,lab,w in (("current","Current",118),("due","Due soon",134),("lapsed","Lapsed",112),("none","No evidence",162)):
    o.append(f'<rect x="{lx}" y="1098" width="{w}" height="34" rx="17" style="fill:var(--{st}-soft)"/><circle cx="{lx+18}" cy="1115" r="6" style="fill:var(--{st})"/>')
    o.append(T(lx+32,1121,lab,"sh",17,"start",w-40,f'style="fill:var(--{st})"'))
    lx+=w+14
o.append(T(1140,1121,"Status shows when evidence expires, not performance.","b",17,"end",560,'style="fill:var(--muted)"'))
# principle pills
px=60
for lab,w in (("No scores or ranks",262),("Every claim cites its source",346),("Learner controls sharing",320)):
    o.append(f'<rect x="{px}" y="1146" width="{w}" height="0" rx="0" fill="none"/>')
    px+=0
px=60
for lab,w in (("No scores or ranks",258),("Every claim cites its source",344),("Learner controls sharing",318)):
    o.append(f'<rect x="{px}" y="1146" width="{w}" height="34" rx="17" style="fill:var(--accent-soft)"/><path d="M{px+14} {1163}L{px+20} {1169}L{px+30} {1157}" fill="none" style="stroke:var(--accent)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(T(px+42,1169,lab,"sh",17,"start",w-52,'style="fill:var(--accent)"'))
    px+=w+16

# ---------- why it matters ----------
cells=[("One view","AHA, AAP and Laerdal together"),("Early warning","Fading skills spotted early"),("Skills evidenced","Beyond courses completed")]
for i,(t,c) in enumerate(cells):
    x=30+i*385
    o.append(card(x,1208,370,90,"panel",26))
    o.append(f'<rect x="{x+22}" y="1232" width="6" height="42" rx="3" fill="url(#ring)"/>')
    o.append(T(x+44,1250,t,"sh",24,"start",300,'style="fill:var(--ink)"'))
    o.append(T(x+44,1278,c,"b",18,"start",300,'style="fill:var(--muted)"'))

# ---------- flow ----------
flow=[("Sources",["Systems, PDFs, files.","Not decided yet."]),("Match and map",["Any format to one","record, by email"]),("Common record",["Every record in","one common format"]),("Two views",["Learner passport,","educator view"])]
for i,(t,ls) in enumerate(flow):
    x=30+i*295
    stroke="var(--accent)" if i==1 else "var(--line)"
    o.append(f'<rect x="{x}" y="1316" width="255" height="104" rx="26" style="fill:var(--panel-strong);stroke:{stroke}" stroke-width="{3 if i==1 else 1.5}"/>')
    o.append(T(x+22,1352,t,"sh",21,"start",211,'style="fill:var(--ink)"'))
    for j,l in enumerate(ls):o.append(T(x+22,1382+j*24,l,"b",17,"start",211,'style="fill:var(--muted)"'))
    if i<3:o.append(f'<path d="M{x+266} 1368H{x+282}M{x+274} 1358L{x+284} 1368L{x+274} 1378" fill="none" style="stroke:var(--accent)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
def dot(kind,x,y,r=7):
    if kind=="full":return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--accent);stroke:var(--accent)" stroke-width="2"/>'
    if kind=="half":return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2"/><path d="M{x} {y-r}A{r} {r} 0 0 0 {x} {y+r}Z" style="fill:var(--accent)"/>'
    return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2"/>'
o.append('<rect x="30" y="1430" width="1140" height="46" rx="23" style="fill:var(--accent-soft)"/>')
o.append('<rect class="aip" x="44" y="1441" width="48" height="24" rx="12" fill="url(#ring)"/>'+T(68,1458,"AI","h",14,"middle",None,"fill:#FFFFFF"))
ax=112
for st,lab in (("full","Cited summary"),("full","Ask the passport"),("full","Admin search"),("half","Match by email"),("half","Map to skills")):
    o.append(dot(st,ax+7,1453)+T(ax+22,1459,lab,"sh",16,"start",None,'style="fill:var(--ink)"'))
    ax+=22+int(wid(lab,16,True))+30
if ax>1170:BAD.append(("AI strip",ax,1170))

# ---------- status ----------
cols=[("Working now","current",["Passport and timeline","Cited AI summary and Q&A","Plain-English admin search","Email identity matching"]),("Mocked","due",["All source feeds","Exposure logs","Sign-in: no real login"]),("Next","accent",["Confirm real data access","Validate with educators","Privacy and governance","Pilot at one centre"])]
for i,(t,st,items) in enumerate(cols):
    x=30+i*385
    o.append(card(x,1490,370,172,"panel",28))
    o.append(f'<circle cx="{x+30}" cy="1526" r="9" style="fill:var(--{st})"/>')
    o.append(T(x+50,1534,t,"sh",24,"start",290,'style="fill:var(--ink)"'))
    for j,it in enumerate(items):
        yy=1566+j*27
        o.append(f'<circle cx="{x+30}" cy="{yy-6}" r="3.5" fill="url(#ring)"/>')
        o.append(T(x+46,yy,it,"b",19,"start",300,'style="fill:var(--ink)"'))
o.append(T(600,1676,"Prototype with synthetic data. Source names are real systems; record shapes are assumptions. Not a credential.","b",14,"middle",1100,'style="fill:var(--muted)"'))
o.append(dot("full",330,1690,5)+T(342,1694,"live model in the hosted prototype","b",13.5,"start",260,'style="fill:var(--muted)"')+dot("half",640,1690,5)+T(652,1694,"rules stand in today","b",13.5,"start",200,'style="fill:var(--muted)"'))

svg='<svg id="poster" viewBox="0 0 1200 1697" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Poster: AI Clinical Competency Passport. Six training systems, each with a partial view, become one living clinical identity across seven skill areas, shown as current, due soon, lapsed or no evidence. No scores, every claim cites a source, the learner controls sharing. Prototype with synthetic data.">'+"\n".join(o)+'</svg>'

css='''
:root{
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
  color-scheme:light;
  --bg:#EDF2FF;--glow1:rgba(70,110,255,.22);--glow2:rgba(0,200,225,.20);--grid:rgba(40,70,160,.07);
  --panel:#F7F9FF;--panel-strong:#FFFFFF;--line:rgba(40,70,160,.20);--line-strong:rgba(40,70,160,.36);
  --ink:#0B1230;--muted:#4A5480;--accent:#3752EE;--accent2:#00A8C8;--accent-soft:rgba(55,82,238,.12);
  --current:#0A8F76;--current-soft:rgba(10,156,129,.14);--due:#A86400;--due-soft:rgba(178,106,0,.15);
  --lapsed:#CC2A45;--lapsed-soft:rgba(204,42,69,.13);--none:#5F6A8E;--none-soft:rgba(107,117,151,.16);
  --band1:#1F2FA8;--band2:#0A7FA8;--tg2:#A5F4FF;
  --src-rqi:#2F6FEA;--src-hc:#7B4FE0;--src-pedia:#C43BC9;--src-sim:#0E9FBB;--src-lms:#5B6688;--src-log:#7A84A6;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#070C26;--glow1:rgba(90,110,255,.30);--glow2:rgba(0,220,240,.16);--grid:rgba(140,170,255,.07);
    --panel:#0E1540;--panel-strong:#131B52;--line:rgba(150,175,255,.20);--line-strong:rgba(150,175,255,.38);
    --ink:#EAEFFF;--muted:#A3AEDA;--accent:#8196FF;--accent2:#3FE3F2;--accent-soft:rgba(129,150,255,.18);
    --current:#35E2C0;--current-soft:rgba(53,226,192,.16);--due:#FFB454;--due-soft:rgba(255,180,84,.17);
    --lapsed:#FF6C84;--lapsed-soft:rgba(255,108,132,.17);--none:#9AA6D2;--none-soft:rgba(141,153,198,.18);
    --band1:#2A3BD0;--band2:#0B8CB8;
    --src-rqi:#5E9BFF;--src-hc:#A184FF;--src-pedia:#E877EE;--src-sim:#3FD3EC;--src-lms:#93A0CC;--src-log:#8792BA;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#070C26;--glow1:rgba(90,110,255,.30);--glow2:rgba(0,220,240,.16);--grid:rgba(140,170,255,.07);
  --panel:#0E1540;--panel-strong:#131B52;--line:rgba(150,175,255,.20);--line-strong:rgba(150,175,255,.38);
  --ink:#EAEFFF;--muted:#A3AEDA;--accent:#8196FF;--accent2:#3FE3F2;--accent-soft:rgba(129,150,255,.18);
  --current:#35E2C0;--current-soft:rgba(53,226,192,.16);--due:#FFB454;--due-soft:rgba(255,180,84,.17);
  --lapsed:#FF6C84;--lapsed-soft:rgba(255,108,132,.17);--none:#9AA6D2;--none-soft:rgba(141,153,198,.18);
  --band1:#2A3BD0;--band2:#0B8CB8;
  --src-rqi:#5E9BFF;--src-hc:#A184FF;--src-pedia:#E877EE;--src-sim:#3FD3EC;--src-lms:#93A0CC;--src-log:#8792BA;
}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*,*::before,*::after{box-sizing:inherit}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Figtree,"DejaVu Sans",system-ui,sans-serif}
body::before{content:"";position:fixed;left:0;right:0;top:0;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.tools{position:fixed;top:calc(12px + env(safe-area-inset-top,0px));right:14px;z-index:30;display:flex;gap:8px}
.tool{border:1px solid var(--line-strong);background:var(--panel-strong);color:var(--ink);border-radius:12px;padding:7px 13px;font:600 13px Figtree,sans-serif;cursor:pointer}
.tool:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1200px;margin:0 auto}
#poster{display:block;width:100%;height:auto}
#poster text{font-family:Figtree,"DejaVu Sans",sans-serif}
#poster .h,#poster .sh{font-family:Sora,"DejaVu Sans",sans-serif;font-weight:700;letter-spacing:-.01em}
#poster .sh{font-weight:600}
#poster .b{font-weight:500}#poster .bb{font-weight:600}
@media print{
  :root,:root[data-theme],:root:not([data-theme="light"]){
    color-scheme:light;
    --bg:#FFFFFF;--panel:#F7F9FF;--panel-strong:#FFFFFF;--line:rgba(40,70,160,.28);--line-strong:rgba(40,70,160,.45);
    --ink:#0B1230;--muted:#3D466C;--accent:#3752EE;--accent2:#00A8C8;--accent-soft:rgba(55,82,238,.12);
    --current:#0A8570;--current-soft:rgba(10,156,129,.14);--due:#A05E00;--due-soft:rgba(178,106,0,.15);
    --lapsed:#CC2A45;--lapsed-soft:rgba(204,42,69,.13);--none:#56608A;--none-soft:rgba(107,117,151,.16);
    --glow1:rgba(70,110,255,.10);--glow2:rgba(0,200,225,.10);--grid:rgba(40,70,160,.05);
    --band1:#1F2FA8;--band2:#0A7FA8;
    --src-rqi:#2F6FEA;--src-hc:#7B4FE0;--src-pedia:#C43BC9;--src-sim:#0E9FBB;--src-lms:#5B6688;--src-log:#7A84A6;
  }
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  body{background:#fff}.tools,body::before{display:none}
  .wrap{max-width:none}
  #poster{width:297mm;height:420mm}
  @page{size:A3 portrait;margin:0}
}

/* ===== Laerdal style (approximation from the brand logo colours; swap in official values) ===== */
.lgx{display:none}
:root[data-theme="laerdal"] .lgx{display:inline}
:root[data-theme="laerdal"] .dec{display:none}
:root[data-theme="laerdal"]{
  color-scheme:light;
  --bg:#F5F5F5;--glow1:transparent;--glow2:transparent;--grid:transparent;
  --panel:#FFFFFF;--panel-strong:#FFFFFF;--line:#DEDEDE;--line-strong:#BBBBBB;
  --ink:#1F1F1F;--muted:#595959;--accent:#1F1F1F;--accent2:#4A4A4A;--accent-soft:rgba(31,31,31,.07);
  --brand:#E42313;--tg2:#FFFFFF;
  --current:#1B7F4B;--current-soft:rgba(27,127,75,.12);
  --due:#A85A00;--due-soft:rgba(168,90,0,.13);
  --lapsed:#B3261E;--lapsed-soft:rgba(179,38,30,.10);
  --none:#616161;--none-soft:rgba(97,97,97,.12);
  --outside:#8C8C8C;--outside-soft:rgba(140,140,140,.10);
  --band1:#1F1F1F;--band2:#2A2A2A;--shadow:none;--header-bg:#FFFFFF;
  --src-rqi:#2F6FEA;--src-hc:#7B4FE0;--src-pedia:#C43BC9;--src-sim:#0E9FBB;--src-lms:#5B6688;--src-log:#8C8C8C;
}
:root[data-theme="laerdal"] rect.aip{fill:var(--brand)}
:root[data-theme="laerdal"] body{font-family:Inter,"DejaVu Sans",sans-serif}
:root[data-theme="laerdal"] #poster text,:root[data-theme="laerdal"] svg.d text{font-family:Inter,"DejaVu Sans",sans-serif}
:root[data-theme="laerdal"] #poster .h,:root[data-theme="laerdal"] #poster .sh,:root[data-theme="laerdal"] svg.d .h,:root[data-theme="laerdal"] svg.d .sh{font-family:Inter,"DejaVu Sans",sans-serif;letter-spacing:-.015em}
'''
js='''
const $=s=>document.querySelector(s);
const THEMES=["laerdal","light","dark"],NAMES={laerdal:"Laerdal style",light:"Futuristic light",dark:"Futuristic dark"};
function cur(){return document.documentElement.dataset.theme||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")}
function label(){$("#themeBtn").textContent="Theme: "+NAMES[cur()]}
function setTheme(){const nx=THEMES[(THEMES.indexOf(cur())+1)%3];document.documentElement.dataset.theme=nx;try{localStorage.setItem("cccp-poster-theme",nx)}catch(e){}label()}
try{const s=localStorage.getItem("cccp-poster-theme");if(s)document.documentElement.dataset.theme=s}catch(e){}
label();$("#themeBtn").addEventListener("click",setTheme);$("#printBtn").addEventListener("click",()=>{try{window.print()}catch(e){}});
'''
html=f'''<!DOCTYPE html>
<html lang="en" data-theme="laerdal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>AI Clinical Competency Passport (poster)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=Sora:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="tools"><button class="tool" id="themeBtn" aria-label="Switch colour theme">Theme</button><button class="tool" id="printBtn">Print or save as PDF</button></div>
<main class="wrap">{svg}</main>
<script>{js}</script>
</body>
</html>'''
OUT=ROOT/"docs/poster/clinical-competency-passport-poster.html";OUT.parent.mkdir(parents=True,exist_ok=True)
open(OUT,"w",encoding="utf8").write(html)
print("written",len(html))
print("TEXT FIT ISSUES (DejaVu worst case):",BAD if BAD else "none")
