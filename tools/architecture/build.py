import math,re
from PIL import ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf";FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def wid(t,size,bold):
    # text-fit checks use DejaVu Sans when it is installed; without it the checks are skipped
    try:return ImageFont.truetype(FB if bold else FR,int(round(size))).getlength(t)
    except OSError:return 0
BAD=[]
_logo=open(ROOT/'assets/brand/laerdal-logo.svg',encoding='utf8').read()
LOGO_INNER=re.sub(r'<title>.*?</title>','',re.search(r'<svg[^>]*>(.*)</svg>',_logo,re.S).group(1),flags=re.S)
def esc(s):return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
CLS={"h":True,"sh":True,"b":False,"bb":True}
def T(x,y,t,cls,size,anchor="start",maxw=None,style="fill:var(--ink)",extra=""):
    if maxw is not None and wid(t,size,CLS[cls])>maxw:BAD.append((t,round(wid(t,size,CLS[cls])),maxw))
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}" style="{style}" {extra}>{esc(t)}</text>'
def mark(kind,x,y,s,k):
    st=f"fill:var(--src-{k})"
    if kind=="circle":return f'<circle cx="{x}" cy="{y}" r="{s}" style="{st}"/>'
    if kind=="diamond":return f'<path d="M{x} {y-s-1}L{x+s+1} {y}L{x} {y+s+1}L{x-s-1} {y}Z" style="{st}"/>'
    if kind=="square":return f'<rect x="{x-s}" y="{y-s}" width="{2*s}" height="{2*s}" rx="2" style="{st}"/>'
    if kind=="triangle":return f'<path d="M{x} {y-s-1}L{x+s+1} {y+s}L{x-s-1} {y+s}Z" style="{st}"/>'
    if kind=="hex":
        p="L".join(f"{x+(s+1)*math.cos(math.pi/3*i+math.pi/6):.1f} {y+(s+1)*math.sin(math.pi/3*i+math.pi/6):.1f}" for i in range(6));return f'<path d="M{p}Z" style="{st}"/>'
    return f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" style="stroke:var(--src-{k});stroke-width:3;fill:none"/>'
def dot(kind,x,y,r=8):
    if kind=="full":return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--accent);stroke:var(--accent)" stroke-width="2"/>'
    if kind=="half":return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2"/><path d="M{x} {y-r}A{r} {r} 0 0 0 {x} {y+r}Z" style="fill:var(--accent)"/>'
    return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2"/>'
def pill(x,y,w=44):
    return f'<rect class="aip" x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="url(#ring)"/>'+T(x+w/2,y+17,"AI","h",14,"middle",None,"fill:#FFFFFF")
def aitag(x,y,w,status):
    px=x+w-64
    return dot(status,px-14,y,7)+pill(px,y-12,46)
def num(x,y,n):
    return f'<circle cx="{x+4}" cy="{y+4}" r="14" fill="url(#ring)" style="stroke:var(--panel-strong)" stroke-width="2.5"/>'+T(x+4,y+10,str(n),"h",15,"middle",None,"fill:#FFFFFF")
DEFS='''<defs>
<linearGradient id="band" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" style="stop-color:var(--band1)"/><stop offset="1" style="stop-color:var(--band2)"/></linearGradient>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--accent)"/><stop offset="1" style="stop-color:var(--accent2)"/></linearGradient>
<radialGradient id="gl1"><stop offset="0" style="stop-color:var(--glow1)"/><stop offset="1" style="stop-color:var(--glow1);stop-opacity:0"/></radialGradient>
<radialGradient id="gl2"><stop offset="0" style="stop-color:var(--glow2)"/><stop offset="1" style="stop-color:var(--glow2);stop-opacity:0"/></radialGradient>
<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" style="stroke:var(--grid)"/></pattern>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" style="fill:var(--accent)"/></marker>
<marker id="ahd" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" style="fill:var(--due)"/></marker>
</defs>'''
H=980
def bg(pref=""):
    return f'<rect width="1600" height="{H}" style="fill:var(--bg)"/><circle cx="120" cy="40" r="560" fill="url(#gl1)"/><circle cx="1560" cy="120" r="500" fill="url(#gl2)"/><rect width="1600" height="{H}" fill="url(#grid)"/>'
def ar(d,dashed=False,op=.75,w=2.2):
    col="var(--due)" if dashed else "var(--accent)"
    return f'<path d="{d}" fill="none" style="stroke:{col}" stroke-opacity="{op}" stroke-width="{w}"{" stroke-dasharray=\"6 5\"" if dashed else ""} marker-end="url(#{"ahd" if dashed else "ah"})"/>'
def header(title,sub):
    return '<rect x="30" y="24" width="1540" height="90" rx="30" fill="url(#band)"/>'+T(62,76,title,"h",34,"start",1250,"fill:#FFFFFF")+T(62,102,sub,"b",18,"start",1300,"fill:#FFFFFF;fill-opacity:.92")+'<g class="lgx"><rect x="1398" y="36" width="156" height="66" rx="14" fill="#FFFFFF"/><g transform="translate(1421 40) scale(1.25)">'+LOGO_INNER+'</g></g>'
def legend(y,detail):
    s=f'<rect x="30" y="{y}" width="1540" height="58" rx="24" style="fill:var(--panel);stroke:var(--line)" stroke-width="1.5"/>'
    cy=y+29
    if detail:
        s+=ar(f"M50 {cy}H104",w=2.4)+T(116,cy+6,"Data flow","bb",15,"start",90)
        s+=ar(f"M226 {cy}H280",dashed=True,w=2.4)+T(292,cy+6,"Held, failed or fallback","bb",15,"start",200)
        x0=520
    else:x0=50
    s+=dot("full",x0,cy)+T(x0+18,cy+6,"Live model in the prototype" if not detail else "Live model today","bb",15,"start",300 if not detail else 170)
    x1=x0+(300 if not detail else 190)
    s+=dot("half",x1,cy)+T(x1+18,cy+6,"Rules stand in","bb",15,"start",140)
    x2=x1+(190 if not detail else 168)
    s+=dot("hollow",x2,cy)+T(x2+18,cy+6,"Planned or optional","bb",15,"start",180)
    x3=x2+(230 if not detail else 212)
    s+=pill(x3,cy-12,44)+T(x3+56,cy+6,"AI-assisted step","bb",15,"start",150)
    if detail:
        x4=x3+230
        s+=f'<circle cx="{x4}" cy="{cy}" r="13" fill="url(#ring)"/>'+T(x4,cy+6,"1","h",14,"middle",None,"fill:#FFFFFF")+T(x4+22,cy+6,"Follow 1 to 10, end to end","bb",15,"start",240)
    return s

# =============================== HIGH-LEVEL DESIGN ===============================
def hld():
    o=[DEFS,bg()]
    o.append(header("High-level design: where AI helps at each layer","Data flows left to right. AI assists at every layer. People approve and decide."))
    LX=[30+i*312 for i in range(5)];LW=280
    layers=[("Sources",["Systems, PDFs, exports","Format not decided yet","e.g. RQI1Stop, SimCapture"],"e.g. a CPR session ends"),
            ("Intake",["Events, API or file upload","Raw input saved first","Failures go to review"],"e.g. input saved, queued"),
            ("Process",["Identity resolution","Skill mapping","Validity rules"],"e.g. email matched to CPR"),
            ("Data",["PostgreSQL with JSONB","Raw store and PII vault","Passport views"],"e.g. record stored"),
            ("Experience",["Learner passport","Admin console","One API, role-based access"],"e.g. passport updates")]
    LY=134;LH=186
    for i,(t,ls,ex) in enumerate(layers):
        x=LX[i]
        o.append(f'<rect x="{x}" y="{LY}" width="{LW}" height="{LH}" rx="26" style="fill:var(--panel-strong);stroke:var(--line-strong)" stroke-width="1.8"/>')
        o.append(f'<circle cx="{x+36}" cy="{LY+38}" r="18" fill="url(#ring)"/>'+T(x+36,LY+45,str(i+1),"h",19,"middle",None,"fill:#FFFFFF"))
        o.append(T(x+64,LY+46,t,"sh",21,"start",LW-80 if i else 110))
        for j,l in enumerate(ls):o.append(T(x+26,LY+86+j*24,l,"b",16,"start",LW-44,"fill:var(--muted)"))
        o.append(f'<line x1="{x+22}" y1="{LY+146}" x2="{x+LW-22}" y2="{LY+146}" style="stroke:var(--line-strong)" stroke-dasharray="3 5"/>')
        o.append(T(x+26,LY+169,ex,"bb",14.5,"start",LW-44,"fill:var(--accent)"))
        if i<4:o.append(f'<path d="M{x+LW+3} {LY+LH//2}H{x+312-5}" fill="none" style="stroke:var(--accent)" stroke-width="3.2" marker-end="url(#ah)"/>')
    for j,(k,kind) in enumerate([("rqi","circle"),("hc","diamond"),("pedia","square"),("sim","triangle"),("lms","hex"),("log","cross")]):
        o.append(mark(kind,LX[0]+LW-104+j*18,LY+36,5,k))
    AY=372;AH=336
    for i in range(5):
        cx=LX[i]+LW/2
        o.append(f'<path d="M{cx} {LY+LH}V{AY}" fill="none" style="stroke:var(--accent)" stroke-width="2.4" stroke-dasharray="6 5" stroke-opacity=".8"/>')
        o.append(pill(cx-22,LY+LH+14))
    cards=[
     [("hollow","Convert documents",["Extract fields from PDFs","or exports, then review"]),("hollow","Transcribe debriefs",["Speech to text for","simulation recordings"])],
     [("hollow","Spot odd events",["Flag schema changes,","bad dates, duplicates"]),("hollow","Route unknowns",["Unknown formats go to","a person for review"])],
     [("half","Match the person",["Fuzzy email and name","match, with a reason"]),("half","Map to skills",["AI proposes, a person","approves the mapping"])],
     [("hollow","Retrieval index",["Search consented records","for cited answers"]),("hollow","Redact personal data",["Strip identifiers before","any model call"])],
     [("full","Cited summary",["Plain language. Every","sentence links a record"]),("full","Ask the passport",["Answers only from cited","records, never guesses"]),("full","Admin questions",["A plain question becomes","a filter on users"])]]
    notes=[("A person reviews","extracted fields."),("A person reviews","flagged events."),("A person approves","weak matches."),("Redaction runs","before any model."),("Nothing is scored","or ranked.")]
    for i,rows in enumerate(cards):
        x=LX[i]
        o.append(f'<rect x="{x}" y="{AY}" width="{LW}" height="{AH}" rx="26" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2.4" stroke-dasharray="8 6"/>')
        o.append(T(x+22,AY+36,"AI in this layer","sh",17,"start",200,"fill:var(--accent)"))
        for j,(st,title,ds) in enumerate(rows):
            ry=AY+58+j*72
            o.append(dot(st,x+30,ry+8)+T(x+50,ry+14,title,"sh",16,"start",LW-66))
            for k,d in enumerate(ds):o.append(T(x+50,ry+35+k*18,d,"b",14.5,"start",LW-66,"fill:var(--muted)"))
        o.append(f'<line x1="{x+20}" y1="{AY+AH-58}" x2="{x+LW-20}" y2="{AY+AH-58}" style="stroke:var(--line-strong)" stroke-width="1.5"/>')
        o.append(f'<circle cx="{x+30}" cy="{AY+AH-30}" r="10" style="fill:var(--current-soft)"/><path d="M{x+25} {AY+AH-30}L{x+29} {AY+AH-26}L{x+36} {AY+AH-35}" fill="none" style="stroke:var(--current)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(T(x+50,AY+AH-34,notes[i][0],"bb",14,"start",LW-62)+T(x+50,AY+AH-15,notes[i][1],"bb",14,"start",LW-62))
    o.append(T(30,748,"Guardrails on every AI step","sh",23,"start",600,"fill:var(--accent)"))
    g=[("Describes, never","scores or ranks"),("Every output cites","a source record"),("A person approves","weak matches"),("Only consented data","reaches a model"),("Record text is","untrusted input")]
    for i,(a,b) in enumerate(g):
        x=30+i*312
        o.append(f'<rect x="{x}" y="764" width="{LW}" height="78" rx="22" style="fill:var(--accent-soft)"/><circle cx="{x+30}" cy="803" r="13" fill="url(#ring)"/><path d="M{x+23} 803L{x+28} 808L{x+37} 796" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(T(x+56,797,a,"sh",16,"start",LW-70)+T(x+56,819,b,"sh",16,"start",LW-70))
    o.append(legend(862,False))
    o.append(T(1570,952,"High-level design. How sources deliver data is not decided. AI steps beyond the prototype are proposals. Consent screens and the team view come after the MVP.","b",15,"end",1400,"fill:var(--muted)"))
    lab="High-level design in five layers: sources, event ingestion, process, data and experience, each with an example event and an AI band showing what AI does and its status. Guardrails: AI describes and never scores, cites a source record, a person approves weak matches and mappings, only consented data reaches a model, and record text is untrusted input."
    return f'<svg id="svg-hld" viewBox="0 0 1600 {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{lab}">'+"\n".join(o)+'</svg>'

# =============================== DETAILED DESIGN ===============================
def box(x,y,w,h,title,lines,dashed=False,accent=False,tsize=19,lsize=15,n=None,ai=None):
    stroke="var(--accent)" if accent else "var(--line-strong)"
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" style="fill:var(--panel-strong);stroke:{stroke}" stroke-width="{2.4 if accent else 1.5}"{" stroke-dasharray=\"7 6\"" if dashed else ""}/>'
    s+=T(x+20,y+30,title,"sh",tsize,"start",w-40)
    for i,l in enumerate(lines):s+=T(x+20,y+54+i*20,l,"b",lsize,"start",w-40,"fill:var(--muted)")
    if n:s+=num(x-4,y-4,n)
    if ai:s+=aitag(x,y,w,ai)
    return s
def detailed():
    o=[DEFS,bg()]
    o.append(header("Detailed design: from source data to a cited passport","Follow the numbers 1 to 10. AI steps carry an AI tag and a status marker."))
    cols=[(30,240,"1  Sources"),(294,240,"2  Intake"),(558,330,"3  Process"),(912,330,"4  Store"),(1266,304,"5  Serve")]
    for x,w,t in cols:
        o.append(f'<rect x="{x}" y="132" width="{w}" height="652" rx="26" style="fill:var(--panel);stroke:var(--line)" stroke-width="1.5"/>')
        o.append(T(x+20,164,t,"sh",19,"start",w-30,"fill:var(--accent)"))
    SRC=[("rqi","RQI1Stop","Quarterly skills","circle"),("hc","AHA eCards","Provider cards","diamond"),("pedia","PediaSkills","NRP, PEPP, NEPP","square"),("sim","SimCapture","Simulation sessions","triangle"),("lms","Hospital LMS","LMS completions","hex"),("log","Unit log","Attested events","cross")]
    SY=[]
    for i,(k,nme,sub,kind) in enumerate(SRC):
        y=184+i*68;SY.append(y)
        o.append(f'<rect x="46" y="{y}" width="208" height="58" rx="16" style="fill:var(--panel-strong);stroke:var(--line-strong)" stroke-width="1.5"/>'+mark(kind,70,y+29,8,k)+T(90,y+25,nme,"bb",16,"start",156)+T(90,y+44,sub,"b",13,"start",156,"fill:var(--muted)"))
    o.append('<rect x="46" y="612" width="208" height="112" rx="16" fill="none" style="stroke:var(--due)" stroke-width="1.8" stroke-dasharray="7 6"/>')
    o.append(T(62,642,"Files and PDFs","bb",16,"start",176,"fill:var(--due)"))
    for i,l in enumerate(["PDF or file exports are","converted by OCR or a","model, then reviewed."]):o.append(T(62,666+i*19,l,"b",14,"start",180,"fill:var(--muted)"))
    o.append(aitag(46,612,208,"hollow"))
    # B
    o.append(box(304,206,226,84,"Source intake",["Events, API or files.","Route not decided."],tsize=17,n=1))
    o.append(box(304,346,226,112,"Downstream queue",["At-least-once delivery.","Duplicates, late and","out-of-order events"],tsize=17,n=2))
    o.append(box(304,530,226,112,"Dead-letter queue",["Unparseable events or","unknown schema, then","retry and review."],dashed=True,tsize=17))
    for y in SY:o.append(ar(f"M254 {y+29}C282 {y+29} 284 248 302 248",op=.45,w=1.8))
    o.append(ar("M417 290V344"));o.append(ar("M417 458V528",dashed=True));o.append(T(431,498,"failures","b",14,"start",90,"fill:var(--due)"))
    o.append('<rect x="304" y="662" width="226" height="86" rx="18" fill="none" style="stroke:var(--due)" stroke-width="1.8" stroke-dasharray="7 6"/>')
    o.append(T(322,692,"Not decided yet","bb",16,"start",190,"fill:var(--due)"))
    for i,l in enumerate(["How each source delivers","data is still open."]):o.append(T(322,716+i*19,l,"b",14,"start",190,"fill:var(--muted)"))
    # C
    cb=[("Consumer",["Save the raw event,","then acknowledge."],78,False,3,"hollow"),
        ("Identity resolution",["Match a verified email or source ID.","Unknown email: send a claim link."],80,False,4,"half"),
        ("Held events",["Wait for the claim, then re-run."],62,True,None,None),
        ("Source adapter",["Versioned field map to one","canonical evidence event."],78,False,5,None),
        ("Skill mapping",["Activity to skills. AI proposes,","a person approves."],80,False,6,"half"),
        ("Validity rules",["Provider-stated or fixed window."],62,False,7,None)]
    y=186;CY=[]
    for t,ls,h,d,n,ai in cb:
        CY.append((y,h))
        o.append(box(574,y,298,h,t,ls,dashed=d,accent=(t=="Skill mapping"),lsize=14.5 if t=="Identity resolution" else 15,n=n,ai=ai))
        y+=h+14
    for i in range(5):
        y1=CY[i][0]+CY[i][1];y2=CY[i+1][0]
        o.append(ar(f"M723 {y1+1}V{y2-1}",dashed=(i==1),w=2))
    o.append(ar(f"M530 402C552 402 548 {CY[0][0]+39} 572 {CY[0][0]+39}"))
    o.append('<rect x="574" y="706" width="298" height="52" rx="14" style="fill:var(--accent-soft)"/>')
    o.append(T(590,727,"Idempotent: duplicates are ignored.","b",14,"start",270)+T(590,747,"Status uses event time, not arrival.","b",14,"start",270))
    # D
    o.append(box(928,186,298,78,"Raw event store",["Immutable. Replayable after","any mapping change."]))
    ry=278;rh=212
    o.append(f'<rect x="928" y="{ry}" width="298" height="{rh}" rx="18" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2.4"/>')
    o.append(T(946,ry+30,"PostgreSQL","sh",19,"start",200)+T(1208,ry+30,"System of record","b",14,"end",120,"fill:var(--muted)")+num(924,ry-4,8))
    for i,t in enumerate(["Learners","Consent","Identifiers","Taxonomy","Mappings","Role profiles","Evidence","Audit log"]):
        px=946+(i%2)*138;py=ry+46+(i//2)*36
        if t=="Consent":
            o.append(f'<rect x="{px}" y="{py}" width="126" height="28" rx="14" fill="none" style="stroke:var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/>'+T(px+63,py+19,"Consent: later","bb",13,"middle",118,"fill:var(--muted)"))
        else:
            o.append(f'<rect x="{px}" y="{py}" width="126" height="28" rx="14" style="fill:var(--accent-soft)"/>'+T(px+63,py+19,t,"bb",14,"middle",112,"fill:var(--accent)"))
    o.append(T(946,ry+rh-12,"JSONB for metrics and custom fields","b",14,"start",270,"fill:var(--muted)"))
    o.append(box(928,504,298,64,"Passport views",["Rebuilt when mappings change."],n=9))
    o.append(box(928,582,298,84,"PII vault",["Emails encrypted. Redacted","before any model call."]))
    o.append(box(928,680,298,82,"Retrieval index",["Search over consented","records for cited answers"],dashed=True,ai="hollow"))
    o.append(ar("M1077 490V502",w=2));o.append(ar("M872 224H926"))
    o.append(ar(f"M872 {CY[5][0]+31}C900 {CY[5][0]+31} 900 400 926 400"))
    # E
    o.append('<rect x="1282" y="186" width="44" height="576" rx="20" style="fill:var(--accent-soft);stroke:var(--accent)" stroke-width="2"/>')
    o.append(num(1278,182,10))
    o.append(T(1304,478,"API and access control","sh",18,"middle",None,"fill:var(--accent)",'transform="rotate(-90 1304 478)"'))
    o.append(T(1318,478,"tenant · role · consent (later)","b",14,"middle",None,"fill:var(--muted)",'transform="rotate(-90 1318 478)"'))
    o.append(box(1342,186,214,82,"Learner passport",["Evidence, recency,","cited summary"],tsize=17))
    o.append(box(1342,282,214,82,"Admin console",["Users and passports.","Team view later."],tsize=17,lsize=14.5))
    ay=384;ah=232
    o.append(f'<rect x="1342" y="{ay}" width="214" height="{ah}" rx="18" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2.4" stroke-dasharray="7 6"/>')
    o.append(T(1362,ay+30,"AI services","sh",19,"start",130)+aitag(1342,ay,214,"full"))
    for i,(st,l) in enumerate([("full","Cited summary"),("full","Ask the passport"),("full","Admin questions"),("half","Refresher ideas")]):
        o.append(dot(st,1370,ay+58+i*28)+T(1388,ay+64+i*28,l,"b",15,"start",150))
    for i,l in enumerate(["Consented, cited records","only. Never scores","or ranks."]):o.append(T(1362,ay+178+i*18,l,"b",13.5,"start",180,"fill:var(--muted)"))
    o.append('<rect x="1342" y="628" width="214" height="134" rx="18" style="fill:var(--accent-soft)"/>')
    o.append(T(1362,658,"Extensible by data","sh",16,"start",176,"fill:var(--accent)"))
    for i,l in enumerate(["New sources, skills","and fields are added","as data, not code."]):o.append(T(1362,684+i*21,l,"b",14.5,"start",176))
    o.append(ar("M1226 400C1250 400 1250 400 1280 400"));o.append(ar("M1226 536C1250 536 1250 536 1280 536"));o.append(ar("M1226 721C1250 721 1250 721 1280 721",dashed=True))
    for yy in (227,323,496):o.append(ar(f"M1326 {yy}H1340",w=2))
    # governance + legend
    o.append('<rect x="30" y="804" width="1540" height="84" rx="26" style="fill:var(--panel-strong);stroke:var(--accent)" stroke-width="2"/>')
    o.append(T(60,840,"Across every layer","sh",20,"start",300,"fill:var(--accent)"))
    o.append(T(60,870,"tenant_id on every table, with row-level security  ·  consent on every read and AI query (screens later)  ·  audit trail  ·  no scoring or ranking","b",17,"start",1470))
    o.append(legend(900,True))
    o.append(T(1570,976,"Prototype design. How sources deliver data (events, API or files) is not decided. “Later” marks pieces planned after the MVP.","b",15,"end",1400,"fill:var(--muted)"))
    lab="Detailed design in five columns. Source data arrives as events, API pulls or file uploads (1) and downstream queue (2) with a dead-letter queue. A consumer (3) saves raw events, identity resolution (4), source adapter (5), skill mapping (6) and validity rules (7) build canonical evidence in PostgreSQL (8), with a raw event store, passport views (9), a PII vault and a retrieval index. An API with access control (10) serves the learner passport, admin console and AI services. Tenant isolation, consent, audit and no scoring apply across every layer."
    return f'<svg id="svg-detailed" viewBox="0 0 1600 {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{lab}">'+"\n".join(o)+'</svg>'

css=open(ROOT/"tools/poster/build.py",encoding="utf8").read().split("css='''")[1].split("'''")[0]
css=css.replace("#poster","svg.d").replace("@page{size:A3 portrait;margin:0}","@page{size:A3 landscape;margin:0}").replace("svg.d{width:297mm;height:420mm}","svg.d{width:420mm;height:257mm}")
css=css.replace(".tools{position:fixed;top:calc(12px + env(safe-area-inset-top,0px));right:14px;z-index:30;display:flex;gap:8px}",
 ".bar{max-width:1600px;margin:0 auto;padding:14px 18px 6px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}.bar .sp{flex:1}.seg{border:1px solid var(--line-strong);background:var(--panel-strong);color:var(--ink);border-radius:12px;padding:8px 16px;font:600 14px Figtree,sans-serif;cursor:pointer}.seg[aria-pressed=\"true\"]{background:var(--accent);border-color:var(--accent);color:#fff}[hidden]{display:none!important}")
css=css.replace(".tools,body::before{display:none}",".bar,body::before{display:none}").replace(".wrap{max-width:1200px;margin:0 auto}",".wrap{max-width:1600px;margin:0 auto;padding:0 12px 16px}")
js='''
const $=s=>document.querySelector(s);
const THEMES=["laerdal","light","dark"],NAMES={laerdal:"Laerdal style",light:"Futuristic light",dark:"Futuristic dark"};
function cur(){return document.documentElement.dataset.theme||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")}
function label(){$("#themeBtn").textContent="Theme: "+NAMES[cur()]}
function setTheme(){const nx=THEMES[(THEMES.indexOf(cur())+1)%3];document.documentElement.dataset.theme=nx;try{localStorage.setItem("cip-arch-theme",nx)}catch(e){}label()}
function route(){const v=location.hash.slice(1)==="detailed"?"detailed":"hld";$("#v-hld").hidden=v!=="hld";$("#v-detailed").hidden=v!=="detailed";document.querySelectorAll(".seg").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.v===v)))}
try{const s=localStorage.getItem("cip-arch-theme");if(s)document.documentElement.dataset.theme=s}catch(e){}
label();route();
document.querySelectorAll(".seg").forEach(b=>b.addEventListener("click",()=>{location.hash=b.dataset.v;route()}));
window.addEventListener("hashchange",route);
$("#themeBtn").addEventListener("click",setTheme);$("#printBtn").addEventListener("click",()=>{try{window.print()}catch(e){}});
document.addEventListener("keydown",e=>{if(e.key==="ArrowRight"){location.hash="detailed";route()}if(e.key==="ArrowLeft"){location.hash="hld";route()}});
'''
H1=hld().replace('<svg id="svg-hld"','<svg class="d" id="svg-hld"');D1=detailed().replace('<svg id="svg-detailed"','<svg class="d" id="svg-detailed"')
html=f'''<!DOCTYPE html>
<html lang="en" data-theme="laerdal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Clinical Identity Passport: architecture</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=Sora:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}
svg.d{{display:block;width:100%;height:auto}}
svg.d text{{font-family:Figtree,"DejaVu Sans",sans-serif}}
svg.d .h,svg.d .sh{{font-family:Sora,"DejaVu Sans",sans-serif;font-weight:700;letter-spacing:-.01em}}
svg.d .sh{{font-weight:600}}svg.d .b{{font-weight:500}}svg.d .bb{{font-weight:600}}
</style>
</head>
<body>
<div class="bar"><button class="seg" data-v="hld" aria-pressed="true">High-level design</button><button class="seg" data-v="detailed" aria-pressed="false">Detailed design</button><span class="sp"></span><button class="tool" id="themeBtn" aria-label="Switch colour theme">Theme</button><button class="tool" id="printBtn">Print or save as PDF</button></div>
<main class="wrap"><section id="v-hld">{H1}</section><section id="v-detailed" hidden>{D1}</section></main>
<script>{js}</script>
</body>
</html>'''
OUT=ROOT/"docs/architecture/clinical-passport-architecture.html";OUT.parent.mkdir(parents=True,exist_ok=True)
open(OUT,"w",encoding="utf8").write(html)
print("written",len(html));print("FIT ISSUES:",BAD if BAD else "none")
