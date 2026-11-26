"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { FILES, sleep, open } = require("./helpers");

test("architecture page switches between the high-level and detailed designs", async () => {
  const env = open(FILES.architecture);
  await sleep(150);
  const shown = () => ["#v-hld", "#v-detailed"].filter((s) => !env.d.querySelector(s).hidden);
  assert.deepEqual(shown(), ["#v-hld"]);
  env.click(".seg[data-v=detailed]");
  await sleep(30);
  assert.deepEqual(shown(), ["#v-detailed"]);
  assert.equal(env.w.location.hash, "#detailed");
  env.click(".seg[data-v=hld]");
  await sleep(30);
  assert.deepEqual(shown(), ["#v-hld"]);
  assert.equal(env.d.querySelectorAll("svg.d").length, 2);
});

test("architecture marks undecided intake and later features", async () => {
  const env = open(FILES.architecture);
  await sleep(150);
  const text = env.d.body.textContent;
  assert.match(text, /Not decided yet/);
  assert.match(text, /Consent: later/);
  assert.match(text, /Team view later/);
});
