"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { FILES, sleep, open } = require("./helpers");

test("poster carries the team, track, slot and booth", async () => {
  const env = open(FILES.poster);
  await sleep(150);
  const text = env.d.querySelector("#poster").textContent;
  for (const s of ["CORA", "Automate the everyday", "27 Nov 2026", "10:15", "Positron/Electron"]) {
    assert.ok(text.includes(s), s);
  }
  assert.ok(!text.includes("PR vanguards"));
});
