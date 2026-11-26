"use strict";
const { JSDOM } = require("jsdom");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const FILES = {
  prototype: path.join(ROOT, "app/prototype/dist/clinical-identity-passport.html"),
  poster: path.join(ROOT, "docs/poster/clinical-competency-passport-poster.html"),
  architecture: path.join(ROOT, "docs/architecture/clinical-passport-architecture.html"),
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Open one of the built pages in a headless DOM. Pass `claude` to stand in for the hosted model. */
function open(file, { claude } = {}) {
  const errors = [];
  const dom = new JSDOM(fs.readFileSync(file, "utf8"), {
    runScripts: "dangerously",
    pretendToBeVisual: true,
    url: "https://example.test/",
    beforeParse(w) {
      w.matchMedia = () => ({ matches: false });
      w.scrollTo = () => {};
      if (claude) w.claude = claude;
      w.addEventListener("error", (e) => errors.push(e.message));
    },
  });
  const w = dom.window;
  const d = w.document;
  const env = {
    w, d, errors,
    clickEl: (el) => el.dispatchEvent(new w.MouseEvent("click", { bubbles: true })),
    click(sel) {
      const el = typeof sel === "string" ? d.querySelector(sel) : sel;
      if (!el) throw new Error("missing element: " + sel);
      env.clickEl(el);
    },
    type(sel, value) {
      const el = d.querySelector(sel);
      if (!el) throw new Error("missing input: " + sel);
      el.value = value;
      el.dispatchEvent(new w.Event("input", { bubbles: true }));
    },
    visible: () => [...d.querySelectorAll("main section")].filter((s) => !s.hidden).map((s) => s.id).join(),
    tabs: () => (d.querySelector("#tabs").hidden ? "(hidden)" : [...d.querySelectorAll("#tabs .tab")].map((t) => t.textContent).join(" | ")),
    async chip(question) {
      const scope = d.querySelector("main section:not([hidden])");
      const el = [...scope.querySelectorAll(".qchip")].find((c) => c.textContent === question);
      if (!el) throw new Error("no chip: " + question);
      env.clickEl(el);
      await sleep(80);
      return [...d.querySelector("main section:not([hidden])").querySelectorAll(".msg.a")].pop();
    },
    names: () => [...d.querySelectorAll("#view-users .ur .nm b")].map((b) => b.textContent).sort(),
  };
  return env;
}

/** Sign in with a demo account. `email` is the work email shown on the sign-in screen. */
async function login(env, email, { admin = false } = {}) {
  await sleep(150);
  if (admin) env.click("[data-act=lrole][data-r=admin]");
  env.click(`[data-act=fill][data-e='${email}']`);
  await sleep(10);
  env.click("[data-act=signin]");
  await sleep(100);
}

const ACCOUNTS = {
  maya: "maya.okafor@northgate-health.example",
  daniel: "daniel.reyes@northgate-health.example",
  admin: "rhea.kapoor@northgate-health.example",
};

module.exports = { FILES, ROOT, sleep, open, login, ACCOUNTS };
