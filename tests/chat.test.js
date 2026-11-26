"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { FILES, sleep, open, login, ACCOUNTS } = require("./helpers");

const LEARNER_QUESTIONS = [
  "Summarize this passport", "What expires first?", "What should be refreshed next?", "Which skills are current?",
  "What evidence is there for CPR?", "How many events are logged?", "Is anything waiting for identity confirmation?",
  "Is this person the best in the unit?",
];
const warnings = (msg) => msg.querySelectorAll(".chk.warn").length;
const text = (msg) => msg.textContent.replace(/\s+/g, " ");

test("learner: every demo question is answered offline with all guardrail checks green", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.maya);
  const chips = [...env.d.querySelectorAll(".ai-box .qchip")].map((c) => c.textContent);
  assert.deepEqual(chips, LEARNER_QUESTIONS);
  for (const q of LEARNER_QUESTIONS) {
    const msg = await env.chip(q);
    assert.match(msg.querySelector("small").textContent, /Rules \(offline\)/, q);
    assert.equal(warnings(msg), 0, `guardrail warning on: ${q}`);
  }
  assert.deepEqual(env.errors, []);
});

test("learner: answers contain the right facts", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.maya);
  let t = text(await env.chip("What expires first?"));
  assert.match(t, /Medication administration/);
  assert.match(t, /3 Dec 2026/);
  t = text(await env.chip("What should be refreshed next?"));
  assert.match(t, /Worth refreshing/);
  assert.match(t, /option:/);
  t = text(await env.chip("How many events are logged?"));
  assert.match(t, /17 resuscitation events/);
  t = text(await env.chip("Is this person the best in the unit?"));
  assert.match(t, /only describe what is on file/);
  t = text(await env.chip("Is anything waiting for identity confirmation?"));
  assert.match(t, /Nothing is on file waiting/);
});

test("learner: typed questions work, and unknown ones get guidance", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.maya);
  env.type("#aiQ", "what evidence do i have for airway");
  env.click("[data-act=ai-send]");
  await sleep(60);
  assert.match(text([...env.d.querySelectorAll(".ai-box .msg.a")].pop()), /Airway management:/);
  env.type("#aiQ", "what is the weather");
  env.click("[data-act=ai-send]");
  await sleep(60);
  assert.match(text([...env.d.querySelectorAll(".ai-box .msg.a")].pop()), /I can answer questions/);
});

test("learner with a pending match: the pending record is listed and cited", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.daniel);
  let msg = await env.chip("Is anything waiting for identity confirmation?");
  assert.match(text(msg), /PALS Provider eCard/);
  assert.equal(warnings(msg), 0);
  msg = await env.chip("What should be refreshed next?");
  assert.match(text(msg), /CPR & resuscitation lapsed/);
});

test("administrator: demo questions return exactly the expected people", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.admin, { admin: true });
  const expected = {
    "Who has something expiring in 30 days?": ["Amara Mensah", "Marcus Lee", "Maya Okafor", "Priya Nair"],
    "NICU staff with CPR lapsed": ["Daniel Reyes"],
    "Who has lapsed skills?": ["Daniel Reyes", "Elena Marchetti", "Priya Nair", "Tomás Silva"],
    "Who has no evidence in teamwork?": ["Amara Mensah", "Chloe Dubois", "Tomás Silva"],
    "Who has an identity match pending?": ["Chloe Dubois", "Daniel Reyes"],
  };
  for (const [q, names] of Object.entries(expected)) {
    await env.chip(q);
    assert.deepEqual(env.names(), names, q);
  }
  const msg = await env.chip("Rank the nurses");
  assert.match(text(msg), /Not supported/);
  assert.equal(env.d.querySelectorAll("#view-users .ur").length, 12, "a refused question shows everyone");
});

test("live mode: guardrail checks catch invented ids, uncited sentences and scoring language", async () => {
  const prompts = [];
  const model = async (prompt) => {
    prompts.push(prompt);
    return { text: "Maya has current CPR evidence from quarterly RQI sessions [MO-04]. Her airway evidence runs to 2027 [MO-05, MO-06]. She is the best performer in her unit [MO-99]. She has logged 17 resuscitation events [UNIT-LOG]. This sentence has no citation." };
  };
  const env = open(FILES.prototype, { claude: { use: async (n) => (n === "sample" ? model : null) } });
  await login(env, ACCOUNTS.maya);
  const msg = await env.chip("What expires first?");
  assert.match(msg.querySelector("small").textContent, /AI \(live model\)/);
  const checks = [...msg.querySelectorAll(".chk")].map((c) => c.textContent.trim());
  assert.ok(checks.some((c) => /1 unknown id removed/.test(c)), "MO-99 is removed and flagged");
  assert.ok(checks.some((c) => /Scoring language found/.test(c)));
  assert.ok(checks.some((c) => /sentence.*without a citation/.test(c)));
  assert.ok(!msg.textContent.includes("MO-99"));
  // privacy: nothing identifying leaves the page
  assert.doesNotMatch(prompts[0], /Okafor|northgate-health\.example|Maya/);
  assert.match(prompts[0], /<data>/);
});

test("live mode: admin search keeps only valid filter values and sends no user data", async () => {
  const prompts = [];
  const model = async () => ({ text: "" });
  model.json = async (prompt) => {
    prompts.push(prompt);
    return { units: ["NICU", "Not a real unit"], areas: ["CPR & resuscitation", "Made up area"], status: "lapsed", identity_pending: false, expiring_within_days: null, unsupported: null };
  };
  const env = open(FILES.prototype, { claude: { use: async (n) => (n === "sample" ? model : null) } });
  await login(env, ACCOUNTS.admin, { admin: true });
  await env.chip("NICU staff with CPR lapsed");
  assert.deepEqual(env.names(), ["Daniel Reyes"]);
  assert.doesNotMatch(prompts[0], /Okafor|Reyes|Nair|northgate-health\.example/);
});

test("mode toggle bypasses the model, and a failing model falls back to rules with a note", async () => {
  let calls = 0;
  const model = async () => { calls++; return { text: "Medication safety expires on 3 Dec 2026 [MO-09]." }; };
  const env = open(FILES.prototype, { claude: { use: async (n) => (n === "sample" ? model : null) } });
  await login(env, ACCOUNTS.maya);
  await env.chip("What expires first?");
  assert.equal(calls, 1);
  env.click("[data-act=ai-mode][data-m=rules]");
  await sleep(30);
  const msg = await env.chip("What expires first?");
  assert.equal(calls, 1, "offline mode must not call the model");
  assert.match(msg.querySelector("small").textContent, /Rules \(offline\)/);

  const failing = async () => { const e = new Error("x"); e.code = "rate_limited"; throw e; };
  failing.json = failing;
  const env2 = open(FILES.prototype, { claude: { use: async (n) => (n === "sample" ? failing : null) } });
  await login(env2, ACCOUNTS.maya);
  const msg2 = await env2.chip("What expires first?");
  assert.match(msg2.textContent, /Rules \(offline\)/);
  assert.match(msg2.textContent, /Too many AI requests/);
});
