"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { FILES, sleep, open } = require("./helpers");

for (const [name, file] of Object.entries(FILES)) {
  test(`${name}: theme button cycles Laerdal style, Futuristic light, Futuristic dark`, async () => {
    const env = open(file);
    await sleep(150);
    const seen = [env.d.documentElement.dataset.theme];
    for (let i = 0; i < 3; i++) {
      env.click("#themeBtn");
      seen.push(env.d.documentElement.dataset.theme);
    }
    assert.deepEqual(seen, ["laerdal", "light", "dark", "laerdal"]);
    assert.match(env.d.querySelector("#themeBtn").textContent, /Laerdal style/);
    assert.deepEqual(env.errors, []);
  });
}
