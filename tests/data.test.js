"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { FILES, sleep, open } = require("./helpers");

test("synthetic data set has the expected shape", async () => {
  const env = open(FILES.prototype);
  await sleep(150);
  const ev = (code) => env.w.eval(code);
  assert.equal(ev("LEARNERS.length"), 12);
  assert.equal(ev("LEARNERS.reduce((a,l)=>a+l.events.length,0)"), 98);
  assert.equal(ev("LEARNERS.reduce((a,l)=>a+active(l).length,0)"), 95, "records counted");
  assert.equal(ev("LEARNERS.reduce((a,l)=>a+pending(l).length,0)"), 3, "records awaiting an identity match");
  assert.equal(ev("Object.keys(SRC).length"), 6);
  assert.equal(ev("DOMS.length"), 7);
  assert.equal(ev("new Set(LEARNERS.map(l=>l.unit)).size"), 9);
  assert.deepEqual(env.errors, []);
});

test("no learner data contains scores or rankings", async () => {
  const env = open(FILES.prototype);
  await sleep(150);
  const keys = env.w.eval("JSON.stringify(LEARNERS).toLowerCase()");
  assert.doesNotMatch(keys, /"score"|"rank"|"rating"/);
});
