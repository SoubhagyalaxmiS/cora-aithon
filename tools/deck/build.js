const pptxgen=require("pptxgenjs");
const path=require("path"),{spawnSync}=require("child_process");
const P=(p)=>path.join(__dirname,p);
const fs=require("fs"),React=require("react"),RDS=require("react-dom/server"),sharp=require("sharp");
const fa=require("react-icons/fa");

const THEME=require("./theme.json");
const HX=THEME.colors;
const pres=new pptxgen();
pres.layout="LAYOUT_WIDE";            // 13.33 x 7.5
pres.theme={headFontFace:"Calibri",bodyFontFace:"Calibri"};
pres.title="AI Clinical Competency Passport";
pres.subject="AIthon Round 1";
const C=pres.SchemeColor, S=pres.ShapeType;
const LOGO=P("../../assets/brand/laerdal-logo.png");

async function icon(name,color="#FFFFFF",size=256){
  const svg=RDS.renderToStaticMarkup(React.createElement(fa[name],{color,size:String(size)}));
  const buf=await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64,"+buf.toString("base64");
}
// ---------- layouts ----------
const SEC=["Idea","AI","Design","Delivery"];
const secStarts={};

function T(sl,text,o){return sl.addText(text,Object.assign({isTextBox:true,margin:0,fontFace:"Calibri",valign:"top"},o))}
function title(sl,t){sl.addText(t,{placeholder:"title"})}
function card(sl,x,y,w,h,o={}){
  sl.addShape(S.roundRect,Object.assign({x,y,w,h,rectRadius:0.1,fill:{color:o.fill||C.background2},line:{color:o.line||C.background2,width:o.lw||0.75},shadow:o.shadow?{type:"outer",color:"000000",blur:6,offset:2,angle:90,opacity:0.12}:undefined},o.extra||{}));
}
async function iconCircle(sl,x,y,d,name,fill){
  sl.addShape(S.ellipse,{x,y,w:d,h:d,fill:{color:fill||C.accent1},line:{color:fill||C.accent1,width:0.5}});
  sl.addImage({data:await icon(name),x:x+d*0.25,y:y+d*0.25,w:d*0.5,h:d*0.5});
}
function bullets(items,o={}){return items.map((t,i)=>({text:t,options:Object.assign({bullet:true,breakLine:i<items.length-1,paraSpaceAfter:o.gap===undefined?6:o.gap},o.opt||{})}))}

(async()=>{
 // ---- title placeholders must be declared on layouts: do it with a second pass using master options ----
 // pptxgenjs: placeholders are defined in defineSlideMaster objects; redefine with placeholders
 const pres2=pres; // alias
 pres2.defineSlideMaster({title:"T_TITLE",background:{color:HX.dk1},objects:[
   {rect:{x:0.7,y:0.6,w:2.0,h:1.1,fill:{color:HX.lt1},rectRadius:0.12}},
   {image:{x:0.85,y:0.75,w:1.7,h:0.93,path:LOGO}},
   {placeholder:{options:{name:"title",type:"title",x:0.7,y:2.3,w:7.4,h:2.0,fontSize:50,bold:true,color:HX.lt1,fontFace:"Calibri",valign:"bottom",align:"left",margin:0},text:""}},
   {placeholder:{options:{name:"body",type:"body",x:0.7,y:4.5,w:7.2,h:1.0,fontSize:24,color:"D9D9D9",fontFace:"Calibri",valign:"top",align:"left",margin:0},text:""}}
 ]});
 pres2.defineSlideMaster({title:"T_CONTENT",background:{color:HX.lt1},objects:[
   {image:{x:11.8,y:0.42,w:1.0,h:0.55,path:LOGO}},
   {text:{text:"CORA  =  Competency Optimization Readiness Agent - Your clinical competency passport",options:{x:0.6,y:7.02,w:10.5,h:0.3,fontSize:10,color:HX.dk2,fontFace:"Calibri",margin:0}}},
   {placeholder:{options:{name:"title",type:"title",x:0.6,y:0.3,w:10.9,h:0.95,fontSize:36,bold:true,color:HX.dk1,fontFace:"Calibri",valign:"middle",align:"left",margin:0},text:""}}
  ],slideNumber:{x:12.2,y:7.02,w:0.6,h:0.3,fontSize:10,color:HX.dk2,fontFace:"Calibri",align:"right"}});
 pres2.defineSlideMaster({title:"T_CLOSE",background:{color:HX.dk1},objects:[
   {rect:{x:0.7,y:0.6,w:2.0,h:1.1,fill:{color:HX.lt1},rectRadius:0.12}},
   {image:{x:0.85,y:0.75,w:1.7,h:0.93,path:LOGO}},
   {placeholder:{options:{name:"title",type:"title",x:0.7,y:2.4,w:9.5,h:2.2,fontSize:44,bold:true,color:HX.lt1,fontFace:"Calibri",valign:"bottom",align:"left",margin:0},text:""}},
   {placeholder:{options:{name:"body",type:"body",x:0.7,y:4.8,w:9.0,h:0.9,fontSize:22,color:"D9D9D9",fontFace:"Calibri",valign:"top",align:"left",margin:0},text:""}}
 ]});
 function add(sec,master,notes){
   if(!secStarts[sec]){pres.addSection({title:sec});secStarts[sec]=1}
   const sl=pres.addSlide({masterName:master,sectionTitle:sec});if(notes)sl.addNotes(notes);return sl;
 }
 const GREENB="35C98A",AMBERB="FFB454",REDB="FF6B5E",GRAYB="A0A0A0";

 // ================= 1 TITLE =================
 {
  const sl=add("Idea","T_TITLE","Welcome. This is the AI Clinical Competency Passport: a living clinical identity built from the training systems clinicians already use. In the next few minutes we cover the problem, how AI is central and kept within limits, a working prototype, the architecture, and what comes next.");
  sl.addText("AI Clinical Competency Passport",{placeholder:"title"});
  sl.addText("From training completion to a living clinical identity",{placeholder:"body"});
  T(sl,[{text:"CORA",options:{bold:true,color:"FFFFFF",fontSize:20,breakLine:true}},{text:"Automate the everyday  |  AIThon 2026, 27 Nov, 10:15  |  6th floor, Positron/Electron",options:{fontSize:14,color:"BFBFBF",breakLine:true}},{text:"Prototype with synthetic data",options:{fontSize:12,color:"9A9A9A"}}],{x:0.7,y:5.7,w:8.8,h:1.2});
  // constellation motif
  const cx=10.4,cy=3.85,R=2.0;
  sl.addShape(S.ellipse,{x:cx-R,y:cy-R,w:2*R,h:2*R,fill:{type:"none"},line:{color:"595959",width:1,dashType:"sysDot"}});
  sl.addShape(S.ellipse,{x:cx-R*0.55,y:cy-R*0.55,w:R*1.1,h:R*1.1,fill:{type:"none"},line:{color:"4A4A4A",width:0.75,dashType:"sysDot"}});
  const cols=[GREENB,GREENB,GREENB,AMBERB,REDB,GREENB,GRAYB];
  for(let i=0;i<7;i++){const a=(-90+i*360/7)*Math.PI/180,x=cx+R*Math.cos(a),y=cy+R*Math.sin(a);
    sl.addShape(S.line,{x:Math.min(cx,x),y:Math.min(cy,y),w:Math.abs(x-cx),h:Math.abs(y-cy),line:{color:"595959",width:1},flipH:x<cx,flipV:y<cy});
    sl.addShape(S.ellipse,{x:x-0.2,y:y-0.2,w:0.4,h:0.4,fill:{color:"1F1F1F"},line:{color:cols[i],width:2.25,dashType:i===6?"dash":"solid"}});}
  sl.addShape(S.ellipse,{x:cx-0.62,y:cy-0.62,w:1.24,h:1.24,fill:{color:"2B2B2B"},line:{color:"FFFFFF",width:2.5}});
  T(sl,"ID",{x:cx-0.62,y:cy-0.62,w:1.24,h:1.24,fontSize:30,bold:true,color:"FFFFFF",align:"center",valign:"middle"});
 }

 // ================= 2 CRITERIA =================
 {
  const sl=add("Idea","T_CONTENT","Before the detail, here is how this deck maps to the six judging criteria. AI usage carries the most weight at thirty percent, so slides six to nine show where AI sits, what is live in the prototype, and the guardrails around it. The other criteria each have a slide you can jump to.");
  title(sl,"How this deck covers the judging criteria");
  sl.addChart(pres.charts.BAR,[{name:"Weight",labels:["AI usage","User value and impact","Domain relevance","Feasibility and reuse","Working prototype","Poster and deck"],values:[30,20,20,10,10,10]}],
   {x:0.5,y:1.45,w:4.7,h:5.2,barDir:"bar",chartColors:[HX.accent1],showValue:true,dataLabelFormatCode:'0"%"',dataLabelColor:HX.dk1,dataLabelFontSize:14,dataLabelFontFace:"+mn-lt",dataLabelPosition:"outEnd",
    catAxisOrientation:"maxMin",catAxisLabelColor:HX.dk1,catAxisLabelFontSize:14,catAxisLabelFontFace:"+mn-lt",valAxisHidden:true,valAxisMaxVal:36,valGridLine:{style:"none"},catGridLine:{style:"none"},showLegend:false,barGapWidthPct:45,
    showTitle:true,title:"Weight in the round score",titleFontSize:14,titleColor:HX.dk2,titleFontFace:"+mn-lt"});
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:HX.dk1},fontSize:14,fontFace:"Calibri",valign:"middle"}});
  const cell=(t,b)=>({text:t,options:{fontSize:14,fontFace:"Calibri",color:HX.dk1,bold:!!b,valign:"middle"}});
  const rows=[[hdr("Criterion"),hdr("What you will see"),hdr("Slides")],
   [cell("AI usage",1),cell("Live model plus offline rules, demo chat questions, guardrail checks, AI at every layer"),cell("6, 7, 8, 9",1)],
   [cell("User value and business impact",1),cell("Four audiences and the measures we will use in a pilot"),cell("14",1)],
   [cell("Domain and product relevance",1),cell("Built on AHA and AAP programs and Laerdal systems"),cell("15",1)],
   [cell("Feasibility and reuse",1),cell("Flexible intake (events, API, PDFs) and extension by data, not code"),cell("11, 12, 13",1)],
   [cell("Working prototype",1),cell("Sign-in, passport, chat, admin list, 12 synthetic clinicians"),cell("10",1)],
   [cell("Poster and presentation",1),cell("Problem, value, output and AI usage, in this deck and on the poster"),cell("3, 4, 5",1)]];
  sl.addTable(rows,{x:5.5,y:1.5,w:7.25,colW:[2.35,3.9,1.0],rowH:[0.45,0.8,0.8,0.8,0.8,0.8,0.8],border:{type:"solid",pt:0.75,color:"D9D9D9"},fill:{color:HX.lt1},margin:[0.04,0.1,0.04,0.1]});
 }

 // ================= 3 PROBLEM =================
 {
  const sl=add("Idea","T_CONTENT","The problem is not a lack of data. Records sit in six systems: quarterly skills sessions, provider cards, simulation checklists, local courses and unit logs. Each shows one piece. Skills also fade, and the AHA 2025 guidelines note decline within months. And experience with real events is rarely visible next to training.");
  title(sl,"Skills are recorded everywhere and seen nowhere");
  const facts=[["FaThLarge","Six systems, six partial views","A card here, a quarterly session there, an observer checklist elsewhere. No single place shows one clinician across programs."],
   ["FaHourglassHalf","Skills fade","CPR skills can decline within three months of training, according to the AHA 2025 guidelines."],
   ["FaEyeSlash","Experience stays invisible","Guidelines recommend tracking exposure to real events. In the evidence reviewed, recent exposure, not years on the job, tracked with outcomes (observational, mostly EMS)."]];
  for(let i=0;i<3;i++){const y=1.5+i*1.7;await iconCircle(sl,0.6,y,0.75,facts[i][0]);
   T(sl,facts[i][1],{x:1.6,y,w:5.4,h:0.4,fontSize:20,bold:true,color:C.text1});
   T(sl,facts[i][2],{x:1.6,y:y+0.42,w:5.4,h:1.15,fontSize:14,color:C.text2});}
  T(sl,"Source: AHA 2025 Guidelines for CPR and ECC, Part 12, Resuscitation Education Science",{x:0.6,y:6.55,w:7,h:0.3,fontSize:10,color:C.text2});
  const srcs=[["RQI1Stop",HX.accent5,S.ellipse],["AHA eCards",HX.accent6,S.diamond],["PediaSkills","C43BC9",S.rect],["SimCapture","0E9FBB",S.triangle],["Hospital LMS",HX.dk2,S.hexagon],["Unit log","8C8C8C",S.plus]];
  T(sl,"Today",{x:7.7,y:1.5,w:5,h:0.4,fontSize:20,bold:true,color:C.text1});
  for(let i=0;i<6;i++){const x=7.7+(i%2)*2.6,y=2.1+Math.floor(i/2)*1.05;
   sl.addShape(S.roundRect,{x,y,w:2.45,h:0.85,rectRadius:0.1,fill:{color:C.background1},line:{color:"BBBBBB",width:1.25,dashType:"dash"}});
   sl.addShape(srcs[i][2],{x:x+0.2,y:y+0.28,w:0.28,h:0.28,fill:{color:srcs[i][1]},line:{color:srcs[i][1],width:0.5}});
   T(sl,srcs[i][0],{x:x+0.62,y:y+0.2,w:1.75,h:0.45,fontSize:15,bold:true,color:C.text1,valign:"middle"});}
  card(sl,7.7,5.35,5.05,1.0,{fill:C.background2});
  T(sl,"No single place shows one clinician across programs, or where skills are slipping.",{x:7.95,y:5.5,w:4.6,h:0.75,fontSize:15,bold:true,color:C.text1,valign:"middle"});
 }

 // ================= 4 SOLUTION =================
 {
  const sl=add("Idea","T_CONTENT","Our answer is a layer above the systems that already exist. Sources stay as they are. We take in their data, whether events, files or PDFs, convert it, match each record to a person using work or personal email, map the activity to seven skill areas, and show what is current, expiring or missing, with no scores. AI then explains it in plain language, with every sentence cited.");
  title(sl,"One clinical identity above existing systems");
  const steps=[["1","Take in","Systems, PDFs or exports stay as they are. Adapters convert them to one record."],["2","Match people","By work or personal email. Weak matches wait for a person."],["3","Map to skills","Each activity is linked to the seven skill areas."],["4","Show evidence","What is current, expiring or missing, plus experience. No scores."],["5","Explain with AI","Cited summaries and plain-English questions."]];
  for(let i=0;i<5;i++){const x=0.6+i*2.45;const ai=i===4;
   card(sl,x,1.55,2.3,3.1,{fill:ai?C.accent1:C.background2});
   sl.addShape(S.ellipse,{x:x+0.2,y:1.75,w:0.6,h:0.6,fill:{color:ai?C.background1:C.text1},line:{color:ai?C.background1:C.text1,width:0.5}});
   T(sl,steps[i][0],{x:x+0.2,y:1.75,w:0.6,h:0.6,fontSize:20,bold:true,color:ai?C.accent1:C.background1,align:"center",valign:"middle"});
   T(sl,steps[i][1],{x:x+0.2,y:2.5,w:1.95,h:0.45,fontSize:19,bold:true,color:ai?C.background1:C.text1});
   T(sl,steps[i][2],{x:x+0.2,y:3.0,w:1.95,h:1.5,fontSize:14,color:ai?C.background1:C.text2});}
  const outs=[["FaUserMd","Learner passport","Evidence, recency and a cited summary, for each clinician."],["FaChalkboardTeacher","Educator and admin view","Who has something expiring, lapsed or missing, found by asking in plain English."]];
  for(let i=0;i<2;i++){const x=0.6+i*6.2;card(sl,x,5.0,5.9,1.55,{fill:C.background1,line:"D9D9D9"});await iconCircle(sl,x+0.25,5.4,0.75,outs[i][0],HX.dk1);
   T(sl,outs[i][1],{x:x+1.25,y:5.2,w:4.4,h:0.4,fontSize:18,bold:true,color:C.text1});
   T(sl,outs[i][2],{x:x+1.25,y:5.65,w:4.4,h:0.8,fontSize:14,color:C.text2});}
 }

 // ================= 5 WHAT IT SHOWS =================
 {
  const sl=add("Idea","T_CONTENT","This is the main view. Seven skill areas around one identity. Each circle counts evidence records. Status shows when evidence expires, not how well someone performed. That is a deliberate choice: we describe what is on file and never score or rank people.");
  title(sl,"Seven skills around one identity");
  sl.addImage({path:P("img/constellation.png"),x:0.6,y:1.45,w:6.15,h:5.11,sizing:{type:"contain",w:6.15,h:5.11}});
  T(sl,"Seven skill areas",{x:7.2,y:1.5,w:5.5,h:0.4,fontSize:20,bold:true,color:C.text1});
  const areas=["CPR and resuscitation","Airway management","Patient assessment","Emergency response","Medication administration","Communication and teamwork"];
  for(let i=0;i<6;i++){const x=7.2+(i%2)*2.78,y=2.0+Math.floor(i/2)*0.5;
   sl.addShape(S.roundRect,{x,y,w:2.7,h:0.42,rectRadius:0.1,fill:{color:C.background2},line:{color:C.background2,width:0.5}});
   T(sl,areas[i],{x:x+0.12,y,w:2.5,h:0.42,fontSize:12,color:C.text1,valign:"middle"});}
  sl.addShape(S.roundRect,{x:7.2,y:3.5,w:5.48,h:0.42,rectRadius:0.1,fill:{color:C.background2},line:{color:C.background2,width:0.5}});
  T(sl,"Maternal and neonatal emergencies",{x:7.32,y:3.5,w:5.2,h:0.42,fontSize:12,color:C.text1,valign:"middle"});
  T(sl,"Four statuses",{x:7.2,y:4.15,w:5.5,h:0.4,fontSize:20,bold:true,color:C.text1});
  const st=[[C.accent3,"Current","valid evidence runs more than 45 days ahead"],[C.accent4,"Due soon","expires within 45 days"],[C.accent1,"Lapsed","the latest record has expired"],[C.text2,"No evidence","nothing on file for a skill the role expects"]];
  for(let i=0;i<4;i++){const y=4.65+i*0.4;sl.addShape(S.ellipse,{x:7.22,y:y+0.07,w:0.2,h:0.2,fill:{color:st[i][0]},line:{color:st[i][0],width:0.5}});
   T(sl,[{text:st[i][1]+": ",options:{bold:true,color:C.text1}},{text:st[i][2],options:{color:C.text2}}],{x:7.6,y,w:5.1,h:0.35,fontSize:14,valign:"middle"});}
  T(sl,"Not a score. Status shows when evidence expires, not how well someone performed.",{x:7.2,y:6.35,w:5.5,h:0.5,fontSize:13,italic:true,color:C.text2});
 }

 // ================= 6 AI CENTRAL =================
 {
  const sl=add("AI","T_CONTENT","AI is central because the hard part of this product is not storing records, it is understanding them: who a record belongs to, which skill it evidences, and how to explain it. The experience layer is live with a real model today. Matching and mapping use rules in the prototype and are the next steps to move to a model, always with a person approving. The rest is planned. Everywhere, a person decides.");
  title(sl,"AI is central, and kept within limits");
  const hdr=(t)=>({text:t,options:{bold:true,color:"FFFFFF",fill:{color:HX.dk1},fontSize:14,fontFace:"Calibri",valign:"middle"}});
  const c=(t,o)=>({text:t,options:Object.assign({fontSize:14,fontFace:"Calibri",color:HX.dk1,valign:"middle"},o||{})});
  const live=c("Live model",{bold:true,color:HX.accent3}),rules=c("Rules today",{bold:true,color:HX.accent4}),plan=c("Planned",{bold:true,color:HX.dk2});
  const rows=[[hdr("Layer"),hdr("AI step"),hdr("Today"),hdr("A person decides")],
   [c("Sources",{bold:true}),c("Convert PDFs and exports to the common record, transcribe debriefs"),plan,c("Reviews extracted fields")],
   [c("Intake",{bold:true}),c("Spot odd records, route unknown formats to review"),plan,c("Reviews flagged records")],
   [c("Process",{bold:true}),c("Match the person by email and name, map each activity to skills"),rules,c("Approves weak matches and mappings")],
   [c("Data",{bold:true}),c("Retrieval index, redact personal data before any model call"),plan,c("Redaction runs automatically")],
   [c("Experience",{bold:true}),c("Cited summary, ask the passport, plain-English admin search"),live,c("Nothing is scored or ranked")]];
  sl.addTable(rows,{x:0.6,y:1.45,w:12.1,colW:[1.6,5.6,1.6,3.3],rowH:[0.45,0.8,0.7,0.8,0.7,0.8],border:{type:"solid",pt:0.75,color:"D9D9D9"},fill:{color:HX.lt1},margin:[0.04,0.12,0.04,0.12]});
  T(sl,"Live model: runs in the hosted prototype.   Rules today: a rule-based stand-in, model comes next.   Planned: in the design, not built.",{x:0.6,y:6.2,w:12.1,h:0.5,fontSize:13,color:C.text2});
 }

 // ================= 7 AI LIVE =================
 {
  const sl=add("AI","T_CONTENT","Here is the AI assistant in the prototype. On the left, a learner asks questions about one passport. Each answer comes only from that person's records, cites them, and is checked by the page: every sentence cited, no scoring language, no unknown record ids, and no names or emails sent. On the right, an administrator asks about users in plain language. The assistant turns the question into a filter, the app does the search, and the model never sees user data. The toggle switches between a live model and offline rules, so the demo works even without a connection.");
  title(sl,"AI assistant in the working prototype");
  T(sl,"Learner: ask this passport",{x:0.6,y:1.3,w:3.8,h:0.3,fontSize:13,bold:true,color:C.text2});
  sl.addImage({path:P("img/learner_ai.png"),x:0.6,y:1.65,w:3.7,h:4.92,sizing:{type:"contain",w:3.7,h:4.92}});
  T(sl,"Administrator: ask about your users",{x:4.65,y:1.3,w:6,h:0.3,fontSize:13,bold:true,color:C.text2});
  sl.addImage({path:P("img/admin_ai2.png"),x:4.65,y:1.65,w:8.05,h:5.45*0.9,sizing:{type:"contain",w:8.05,h:4.9}});
  T(sl,"Live AI calls a model. Offline rules answer from the same records. Both pass the same citation checks.",{x:4.65,y:6.55,w:8.05,h:0.4,fontSize:13,italic:true,color:C.text2});
 }

 // ================= 8 DEMO QUESTIONS =================
 {
  const sl=add("AI","T_CONTENT","Use these questions in the demo. As a learner, start with what should be refreshed next, then ask for a summary, and finish with the best-in-unit question to show that it refuses to rank. As an administrator, try expiring in thirty days, then NICU staff with CPR lapsed, and finish with rank the nurses to show the refusal. The toggle at the top of the chat switches between Live AI and Offline rules, so if the connection fails at the booth, the same questions still work.");
  title(sl,"Questions to try in the demo");
  card(sl,0.6,1.45,6.0,4.55,{fill:C.background2});
  T(sl,"As a learner: ask this passport",{x:0.85,y:1.62,w:5.5,h:0.4,fontSize:18,bold:true,color:C.text1});
  const lq=["Summarize this passport","What expires first?","What should be refreshed next?","Which skills are current?","What evidence is there for CPR?","How many events are logged?","Is anything waiting for identity confirmation?","Is this person the best in the unit?"];
  T(sl,lq.map((q,i)=>({text:q,options:{bullet:true,breakLine:i<lq.length-1,paraSpaceAfter:9,italic:i===7,color:i===7?HX.accent1:HX.dk1}})),{x:0.85,y:2.15,w:5.5,h:3.7,fontSize:17});
  card(sl,6.8,1.45,5.9,4.55,{fill:C.background2});
  T(sl,"As an administrator: ask about your users",{x:7.05,y:1.62,w:5.4,h:0.4,fontSize:18,bold:true,color:C.text1});
  const aq=[["Who has something expiring in 30 days?","4 people"],["NICU staff with CPR lapsed","1 person"],["Who has lapsed skills?","4 people"],["Who has no evidence in teamwork?","3 people"],["Who has an identity match pending?","2 people"],["Rank the nurses","refused"]];
  T(sl,aq.map((q,i)=>({text:q[0],options:{bullet:true,breakLine:false,color:i===5?HX.accent1:HX.dk1,italic:i===5}})).reduce((acc,r,i)=>{acc.push(r);acc.push({text:"   "+aq[i][1],options:{color:HX.dk2,fontSize:14,breakLine:i<aq.length-1,paraSpaceAfter:14}});return acc},[]),{x:7.05,y:2.15,w:5.4,h:3.7,fontSize:17});
  sl.addShape(S.roundRect,{x:0.6,y:6.15,w:12.1,h:0.72,rectRadius:0.1,fill:{color:C.accent2},line:{color:C.accent2,width:0.5}});
  T(sl,"Live AI calls a model. Offline rules answer from the same records, so the demo still works without a connection. Both pass the same checks.",{x:0.85,y:6.15,w:11.6,h:0.72,fontSize:14,color:C.background1,valign:"middle"});
 }

 // ================= 8 GUARDRAILS =================
 {
  const sl=add("AI","T_CONTENT","These guardrails are what keep AI within limits. It describes and never scores. Every claim is cited and checked. A person approves weak matches and mappings. Personal data stays out of prompts. Text inside records is treated as data, not instructions. And we know that rating staff could be high-risk under the EU AI Act, with obligations currently postponed to December 2027, so legal review comes before any scoring.");
  title(sl,"Guardrails keep AI within limits");
  const g=[["FaBan","Describes, never scores","No scores, ranks or fitness judgements. A wording check flags scoring language."],["FaQuoteRight","Every claim is cited","Each sentence links to a source record. Unknown ids are removed and flagged."],["FaUserCheck","A person decides","People approve weak matches and mappings. AI proposes, it does not commit."],["FaUserShield","Personal data stays out","Names and emails are never sent to the model. Admin search sends only the question."],["FaExclamationTriangle","Record text is untrusted","Text inside records is treated as data, never as instructions."],["FaBalanceScale","Built for regulation","Rating staff could be high-risk under the EU AI Act (postponed to Dec 2027). Legal review before any scoring."]];
  for(let i=0;i<6;i++){const x=0.6+(i%3)*4.1,y=1.5+Math.floor(i/3)*2.5;
   card(sl,x,y,3.9,2.3,{fill:C.background2});await iconCircle(sl,x+0.25,y+0.25,0.7,g[i][0],i===5?HX.dk1:HX.accent1);
   T(sl,g[i][1],{x:x+1.1,y:y+0.3,w:2.6,h:0.65,fontSize:18,bold:true,color:C.text1,valign:"middle"});
   T(sl,g[i][2],{x:x+0.25,y:y+1.1,w:3.45,h:1.1,fontSize:14,color:C.text2});}
  T(sl,"These checks run on every AI answer in the prototype.",{x:0.6,y:6.55,w:9,h:0.3,fontSize:13,italic:true,color:C.text2});
 }

 // ================= 9 PROTOTYPE =================
 {
  const sl=add("Design","T_CONTENT","This is the working prototype, built with synthetic data. There are two roles: learners see their own passport, administrators see everyone. A good three-minute demo path is on the right: open the constellation, open a record, ask what should be refreshed next and read the checks, switch to the administrator, ask in plain English for NICU staff with CPR lapsed, and open a passport.");
  title(sl,"A working prototype, with sample data");
  sl.addImage({path:P("img/learner_top.png"),x:0.6,y:1.4,w:7.0,h:4.4,sizing:{type:"contain",w:7.0,h:4.4}});
  T(sl,"Working today",{x:8.0,y:1.45,w:4.7,h:0.4,fontSize:20,bold:true,color:C.text1});
  T(sl,bullets(["Sign-in for learners and administrators","Passport: constellation, timeline, source records","Ask-this-passport chat with demo questions","Live AI or offline rules, with guardrail checks","Users overview, filters and AI search","Three themes: Laerdal, Futuristic light and dark","12 synthetic clinicians, 98 records, 6 sources"],{gap:5}),{x:8.0,y:1.95,w:4.7,h:3.85,fontSize:14,color:C.text1});
  T(sl,"Demo path, three minutes",{x:0.6,y:5.95,w:6,h:0.35,fontSize:16,bold:true,color:C.text1});
  const demo=["Open the constellation and a record","Ask: What should be refreshed next?","Switch to the administrator","Ask: NICU staff with CPR lapsed","Open a passport from the list"];
  for(let i=0;i<5;i++){const x=0.6+i*2.45;
   sl.addShape(S.ellipse,{x,y:6.38,w:0.4,h:0.4,fill:{color:i===3?C.accent1:C.text1},line:{color:i===3?C.accent1:C.text1,width:0.5}});
   T(sl,String(i+1),{x,y:6.38,w:0.4,h:0.4,fontSize:14,bold:true,color:C.background1,align:"center",valign:"middle"});
   T(sl,demo[i],{x:x+0.5,y:6.3,w:1.85,h:0.6,fontSize:12,color:C.text1,valign:"middle"});}
 }

 // ================= 10 HLD =================
 {
  const sl=add("Design","T_CONTENT","This is the high-level design, five layers from sources to experience. Under each layer is an AI band showing what AI does there and its status: filled is a live model in the prototype, half is rules standing in today, hollow is planned. Every layer ends with the human check.");
  title(sl,"High-level design");
  sl.addImage({path:P("../../docs/architecture/architecture-high-level-design.png"),x:0.5,y:1.3,w:9.4,h:5.76,sizing:{type:"contain",w:9.4,h:5.76}});
  T(sl,"How to read it",{x:10.2,y:1.45,w:2.6,h:0.4,fontSize:18,bold:true,color:C.text1});
  T(sl,bullets(["Data flows left to right","An AI band sits under every layer","Filled: live model. Half: rules today. Hollow: planned","Each layer ends with a human check"],{gap:8}),{x:10.2,y:1.95,w:2.6,h:4.5,fontSize:14,color:C.text2});
 }

 // ================= 11 DETAILED =================
 {
  const sl=add("Design","T_CONTENT","This is the detailed design. Follow the numbers one to ten: source data arrives as events, API pulls or file uploads and goes through a queue, the consumer saves the raw input, identity resolution matches the person, the adapter maps it to one record, skills are mapped, validity rules are applied, and the result lands in PostgreSQL. Passport views are rebuilt and served behind one API to the learner passport, admin console and AI services. Consent screens and the team view are marked later.");
  title(sl,"Detailed design: follow numbers 1 to 10");
  sl.addImage({path:P("../../docs/architecture/architecture-detailed-design.png"),x:0.5,y:1.3,w:9.4,h:5.76,sizing:{type:"contain",w:9.4,h:5.76}});
  T(sl,"What to notice",{x:10.2,y:1.45,w:2.6,h:0.4,fontSize:18,bold:true,color:C.text1});
  T(sl,bullets(["Intake is open: events, API pulls or files","Raw input is kept, so results can be replayed","Identity by verified email, claim link for unknown","Consent and team view are marked Later"],{gap:8}),{x:10.2,y:1.95,w:2.6,h:4.5,fontSize:14,color:C.text2});
 }

 // ================= 12 FEASIBILITY =================
 {
  const sl=add("Design","T_CONTENT","Feasibility and reuse. Every source is translated into one canonical evidence record, shown on the left. New sources, skills, fields and roles are added as data, not code, so the same layer can serve AHA and AAP programs and Laerdal systems. Events are idempotent and replayable, and the store is PostgreSQL with JSONB for the variable parts.");
  title(sl,"Feasible to build, easy to extend");
  sl.addShape(S.roundRect,{x:0.6,y:1.5,w:5.7,h:5.0,rectRadius:0.1,fill:{color:HX.dk1},line:{color:HX.dk1,width:0.5}});
  T(sl,"One common record",{x:0.9,y:1.7,w:5.1,h:0.35,fontSize:14,bold:true,color:"FFFFFF"});
  const code=['{ "evidence_id": "ev-2041",','  "learner_id": "lrn-5",','  "source_id": "rqi1stop",','  "type": "session.completed",','  "skills": ["cpr"],','  "occurred_at": "2026-11-04",','  "valid_until": "2027-02-02",','  "modality": "manikin",','  "verification": "verified",','  "metrics": { "depth_in_range_pct": 94 },','  "mapping_version": "m-1042@1" }'];
  T(sl,code.map((t,i)=>({text:t,options:{breakLine:i<code.length-1}})),{x:0.9,y:2.15,w:5.2,h:4.2,fontSize:12,fontFace:"Courier New",color:"E6E6E6",valign:"top"});
  T(sl,"Extend by data, not code",{x:6.8,y:1.5,w:5.9,h:0.4,fontSize:20,bold:true,color:C.text1});
  const ext=[["FaPlug","New source","A registry row, an adapter or file template, and a validity rule"],["FaSitemap","New skill","A taxonomy row and its mappings"],["FaIdCard","New user field","An attribute definition"],["FaUsersCog","New role or unit rule","A role profile"]];
  for(let i=0;i<4;i++){const y=2.05+i*0.85;await iconCircle(sl,6.8,y,0.6,ext[i][0],HX.accent1);
   T(sl,ext[i][1],{x:7.6,y,w:5.1,h:0.32,fontSize:16,bold:true,color:C.text1});T(sl,ext[i][2],{x:7.6,y:y+0.32,w:5.1,h:0.35,fontSize:14,color:C.text2});}
  card(sl,6.8,5.55,5.9,0.95,{fill:C.background2});
  T(sl,"Reuse: one layer for AHA and AAP programs and Laerdal systems. Any intake route, idempotent, replayable. PostgreSQL with JSONB.",{x:7.0,y:5.65,w:5.5,h:0.75,fontSize:14,color:C.text1,valign:"middle"});
 }

 // ================= 13 VALUE =================
 {
  const sl=add("Delivery","T_CONTENT","User value and business impact. Learners see what is current or expiring. Educators and administrators find lapsing skills early and ask questions in plain English instead of compiling spreadsheets. Institutions get one view of readiness evidence. For Laerdal it shifts the conversation from courses delivered to skills evidenced. The measures on the right are what we would test in a pilot. They are hypotheses, not results.");
  title(sl,"Value for learners, educators and Laerdal");
  const a=[["FaUserMd","Learners","See what is current, expiring or missing, and what they have shown."],["FaChalkboardTeacher","Educators and admins","Spot lapsing skills early and ask in plain English instead of compiling lists."],["FaHospital","Institutions","One view of readiness evidence across programs and systems."],["FaChartLine","Laerdal","From courses delivered to skills evidenced, across AHA and AAP programs."]];
  for(let i=0;i<4;i++){const x=0.6+(i%2)*3.65,y=1.5+Math.floor(i/2)*2.55;
   card(sl,x,y,3.5,2.35,{fill:C.background2});await iconCircle(sl,x+0.25,y+0.25,0.65,a[i][0],i===3?HX.accent1:HX.dk1);
   T(sl,a[i][1],{x:x+1.1,y:y+0.3,w:2.3,h:0.55,fontSize:18,bold:true,color:C.text1,valign:"middle"});
   T(sl,a[i][2],{x:x+0.25,y:y+1.05,w:3.05,h:1.2,fontSize:16,color:C.text2});}
  card(sl,8.2,1.5,4.5,4.9,{fill:C.background1,line:"D9D9D9",lw:1});
  T(sl,"What we will measure in a pilot",{x:8.45,y:1.7,w:4.0,h:0.7,fontSize:18,bold:true,color:C.text1});
  T(sl,bullets(["Time to prepare a readiness view","Days between a record expiring and someone noticing","Share of expiring credentials renewed on time","Educator and learner satisfaction"],{gap:10}),{x:8.45,y:2.5,w:4.0,h:3.0,fontSize:16,color:C.text1});
  T(sl,"Hypotheses to test. No results yet.",{x:8.45,y:5.7,w:4.0,h:0.4,fontSize:13,italic:true,color:C.text2});
 }

 // ================= 14 DOMAIN =================
 {
  const sl=add("Delivery","T_CONTENT","Domain and product relevance. This sits directly on the AHA and AAP programs and the Laerdal systems that deliver them: RQI1Stop and RQI Partners programs, SimCapture, and PediaSkills for NRP and PEPP. The AHA 2025 guidelines give the evidence base: skills fade within months, exposure to real events matters, and measuring teamwork is still an open research gap, which is why we show evidence rather than ratings. It complements existing tools rather than replacing them.");
  title(sl,"Built on the programs and systems we know");
  const cols=[["FaHeartbeat","Programs",["AHA: RQI quarterly skills, provider cards, HeartCode","AAP: NRP, PEPP 5th edition (Sept 2026), NEPP","On RQI1Stop and PediaSkills"]],["FaCogs","Laerdal systems",["RQI Partners programs (AHA and Laerdal, since 2018)","SimCapture: simulation and observer checklists","Simulators and manikin feedback data"]],["FaBook","Evidence base",["AHA 2025 guidelines: skills fade within months","Track exposure to real events","Teamwork measurement is an open gap, so we show evidence, not ratings"]]];
  for(let i=0;i<3;i++){const x=0.6+i*4.1;card(sl,x,1.5,3.9,3.8,{fill:C.background2});await iconCircle(sl,x+0.25,1.7,0.65,cols[i][0],i===1?HX.accent1:HX.dk1);
   T(sl,cols[i][1],{x:x+1.1,y:1.75,w:2.6,h:0.55,fontSize:20,bold:true,color:C.text1,valign:"middle"});
   T(sl,bullets(cols[i][2],{gap:10}),{x:x+0.25,y:2.6,w:3.45,h:2.6,fontSize:15,color:C.text1});}
  card(sl,0.6,5.55,12.1,1.1,{fill:C.accent2});
  T(sl,[{text:"Complements, not replaces.  ",options:{bold:true,color:"FFFFFF"}},{text:"RQI Analytics, SimCapture dashboards and LMS competency suites each show their own piece. The Passport adds one identity across programs and objective, simulator-derived evidence.",options:{color:"E6E6E6"}}],{x:0.9,y:5.65,w:11.5,h:0.9,fontSize:15,valign:"middle"});
 }

 // ================= 15 STATUS & ROADMAP =================
 {
  const sl=add("Delivery","T_CONTENT","Where we are and what comes next. Now: the prototype with three live AI steps. Next: real data access, validating the skill mapping with educators, model-assisted matching and mapping with approval, and the privacy and consent design. Then a pilot at one training centre. Later, after the MVP: the sources and consent screens, the team readiness view, mapping admin and single sign-on. Still mocked today: source feeds, exposure logs, sign-in, and rule-based matching and mapping.");
  title(sl,"Status and roadmap");
  const ph=[["Now","Built",HX.dk1,["Sign-in, passport, constellation, timeline","AI chat: live model or offline rules, with checks","Users overview and AI search","12 synthetic clinicians, 98 records"]],["Next","MVP work",HX.accent1,["Decide how each source delivers data: events, API, PDF or export","Validate skill mapping with educators","Model-assisted matching and mapping, with approval","Privacy, consent and governance design"]],["Pilot","One training centre",HX.dk2,["Measure time to readiness view","Measure detection of lapsing skills","Collect educator and learner feedback"]],["Later","After the MVP","8C8C8C",["Sources and consent screens","Team readiness view","Mapping admin","Single sign-on"]]];
  for(let i=0;i<4;i++){const x=0.6+i*3.05;
   sl.addShape(S.chevron,{x,y:1.45,w:3.05,h:0.8,fill:{color:ph[i][2]},line:{color:ph[i][2],width:0.5}});
   T(sl,[{text:ph[i][0],options:{bold:true,fontSize:18}},{text:"  "+ph[i][1],options:{fontSize:13}}],{x:x+0.45,y:1.45,w:2.3,h:0.8,color:"FFFFFF",valign:"middle"});
   T(sl,bullets(ph[i][3],{gap:8}),{x:x+0.1,y:2.5,w:2.8,h:3.4,fontSize:15,color:C.text1});}
  card(sl,0.6,5.95,12.1,0.8,{fill:C.background2});
  T(sl,[{text:"Still mocked today:  ",options:{bold:true,color:C.text1}},{text:"all source feeds, exposure logs, sign-in, and the rule-based matching and mapping.",options:{color:C.text2}}],{x:0.85,y:6.0,w:11.6,h:0.7,fontSize:14,valign:"middle"});
 }

 // ================= 16 RISKS & ASKS =================
 {
  const sl=add("Delivery","T_CONTENT","Finally, what we need and what we watch. We need answers from the source owners on how each source delivers data, a stable user id, an organization id, retention, and the tenant model. And we manage five risks: EU AI Act exposure by never scoring, personal email sensitivity through hashing, claim links and consent, varied PDFs and exports through conversion plus human review, model errors through citations, checks and approval, and overlap with existing Laerdal tools by positioning as the cross-program layer.");
  title(sl,"What we need, and what we manage");
  card(sl,0.6,1.5,5.9,5.0,{fill:C.background2});
  T(sl,"What we need from source owners",{x:0.85,y:1.7,w:5.4,h:0.4,fontSize:18,bold:true,color:C.text1});
  T(sl,bullets(["How will each source deliver data: events, API, PDF or export?","Does each record carry a stable user id, not only an email?","Does it carry an organization id?","Can we backfill history, and how far back?","Tenant model: one organization per deployment, or many?"],{gap:9}),{x:0.85,y:2.25,w:5.4,h:4.1,fontSize:16,color:C.text1});
  card(sl,6.8,1.5,5.9,5.0,{fill:C.background1,line:"D9D9D9",lw:1});
  T(sl,"Risks and how we handle them",{x:7.05,y:1.7,w:5.4,h:0.4,fontSize:18,bold:true,color:C.text1});
  const rk=[["Scoring staff may be high-risk under the EU AI Act","We describe, never score. Legal review first."],["Personal email is sensitive and a weak key","Hashed in stored records, claim link, explicit consent."],["PDFs and exports vary in layout","Convert with OCR or a model, then a person reviews."],["Model errors","Cited, checked, and approved by a person."],["Overlap with existing Laerdal tools","The cross-program layer. Align with those teams."]];
  for(let i=0;i<5;i++){const y=2.2+i*0.88;T(sl,rk[i][0],{x:7.05,y,w:5.4,h:0.4,fontSize:15,bold:true,color:C.text1});T(sl,rk[i][1],{x:7.05,y:y+0.42,w:5.4,h:0.45,fontSize:15,color:C.text2});}
 }

 // ================= 17 CLOSE =================
 {
  const sl=add("Delivery","T_CLOSE","Thank you. In short: one living clinical identity across the systems clinicians already use, with AI that describes, cites and never scores. We are happy to show the prototype, the poster and the architecture, and to take questions.");
  sl.addText("From training completion to a living clinical identity",{placeholder:"title"});
  sl.addText("Questions, and a live demo of the prototype",{placeholder:"body"});
  T(sl,"CORA  |  AIThon 2026  |  6th floor, Positron/Electron",{x:0.7,y:6.3,w:9,h:0.4,fontSize:14,color:"BFBFBF"});
  const cx=11.0,cy=4.0,R=1.7;
  sl.addShape(S.ellipse,{x:cx-R,y:cy-R,w:2*R,h:2*R,fill:{type:"none"},line:{color:"595959",width:1,dashType:"sysDot"}});
  const cols=[GREENB,GREENB,GREENB,AMBERB,REDB,GREENB,GRAYB];
  for(let i=0;i<7;i++){const a=(-90+i*360/7)*Math.PI/180,x=cx+R*Math.cos(a),y=cy+R*Math.sin(a);
   sl.addShape(S.ellipse,{x:x-0.17,y:y-0.17,w:0.34,h:0.34,fill:{color:"1F1F1F"},line:{color:cols[i],width:2,dashType:i===6?"dash":"solid"}});}
  sl.addShape(S.ellipse,{x:cx-0.5,y:cy-0.5,w:1.0,h:1.0,fill:{color:"2B2B2B"},line:{color:"FFFFFF",width:2.25}});
  T(sl,"ID",{x:cx-0.5,y:cy-0.5,w:1.0,h:1.0,fontSize:24,bold:true,color:"FFFFFF",align:"center",valign:"middle"});
 }

 const OUT=P("../../docs/presentation/AI-Clinical-Competency-Passport.pptx");
 require("fs").mkdirSync(path.dirname(OUT),{recursive:true});
 await pres.writeFile({fileName:OUT});
 const r=spawnSync("python3",[P("apply_theme.py"),OUT],{stdio:"inherit"});
 if(r.status!==0)throw new Error("apply_theme.py failed");
 console.log("deck written");
})().catch(e=>{console.error("BUILD ERROR",e);process.exit(1)});
