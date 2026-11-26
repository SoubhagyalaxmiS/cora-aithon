"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { FILES, sleep, open, login, ACCOUNTS } = require("./helpers");

test("sign-in screen is shown first and rejects bad credentials", async () => {
  const env = open(FILES.prototype);
  await sleep(200);
  assert.equal(env.visible(), "view-login");
  assert.equal(env.d.querySelector("#tabs").hidden, true);
  env.type("#loginEmail", ACCOUNTS.maya);
  env.type("#loginPass", "wrong");
  env.click("[data-act=signin]");
  await sleep(20);
  assert.match(env.d.querySelector("#view-login").textContent, /doesn’t match/);
  // a learner account cannot use the administrator option
  env.click("[data-act=lrole][data-r=admin]");
  env.type("#loginEmail", ACCOUNTS.maya);
  env.type("#loginPass", "passport-demo");
  env.click("[data-act=signin]");
  await sleep(20);
  assert.match(env.d.querySelector("#view-login").textContent, /administrator access/);
  assert.equal(env.visible(), "view-login");
});

test("learner sees only their own passport and is redirected from admin pages", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.maya);
  assert.equal(env.visible(), "view-passport");
  assert.equal(env.tabs(), "(hidden)", "a single page needs no tab bar");
  assert.match(env.d.querySelector("#who").textContent, /Maya Okafor/);
  for (const hash of ["users", "team", "sources"]) {
    env.w.location.hash = hash;
    await sleep(60);
    assert.equal(env.visible(), "view-passport", "#" + hash);
  }
  assert.equal(env.d.querySelector(".adminbar"), null);
});

test("pending identity match is shown without a review button", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.daniel);
  const notice = env.d.querySelector(".notice");
  assert.ok(notice, "Daniel has a record waiting for identity confirmation");
  assert.equal(notice.querySelector("button"), null);
});

test("administrator sees Users and Passport only", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.admin, { admin: true });
  assert.equal(env.visible(), "view-users");
  assert.equal(env.tabs(), "Users | Passport");
  for (const hash of ["team", "sources"]) {
    env.w.location.hash = hash;
    await sleep(60);
    assert.equal(env.visible(), "view-users", "#" + hash);
  }
  assert.equal(env.d.querySelectorAll("#view-users .ur").length, 12);
  const header = [...env.d.querySelectorAll("#view-users .uh span")].map((x) => x.textContent);
  assert.deepEqual(header, ["User", "Role and unit", "Account", "Records", "Needs attention", "Next expiry"]);
  env.click("[data-act=open][data-l=CD]");
  await sleep(80);
  assert.equal(env.visible(), "view-passport");
  assert.ok(env.d.querySelector(".adminbar"));
});

test("signed-out users cannot open the passport", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.maya);
  env.click("[data-act=signout]");
  await sleep(60);
  env.w.location.hash = "passport";
  await sleep(60);
  assert.equal(env.visible(), "view-login");
});

test("removed features do not leak into the visible text", async () => {
  const env = open(FILES.prototype);
  await login(env, ACCOUNTS.admin, { admin: true });
  for (const view of ["users", "passport"]) {
    env.w.location.hash = view;
    await sleep(50);
    const text = [...env.d.querySelectorAll("main section")].filter((s) => !s.hidden).map((s) => s.textContent).join(" ").toLowerCase();
    for (const word of ["consent", "sources and", "chosen to share", "team readiness", "sources shared"]) {
      assert.ok(!text.includes(word), `${view} mentions "${word}"`);
    }
  }
});
