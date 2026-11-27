# CORA: Clinical Competency Passport

**CORA** (Competency Optimization Readiness Agent) is a prototype that gives each clinician one living
view of their training evidence: seven skill areas, what is current, due soon, lapsed or missing, and the
experience behind it. An AI assistant answers questions about a passport, with citations. It never scores or ranks people.

Built for AIThon 2026 (track: Automate the everyday). Everything in the prototype is **synthetic data**.

## What is in this repository

```
.
├── app/prototype/        The passport app (single-page, no framework)
│   ├── src/              index.html, styles.css, app.js  (edit these)
│   ├── build.py          Inlines src/ into one hostable file
│   └── dist/             clinical-identity-passport.html (built, committed)
├── tests/                node:test + jsdom suite (access, AI chat, themes, docs pages)
├── tools/                Generators for the documents below
│   ├── poster/           Poster (SVG in HTML)
│   ├── architecture/     High-level and detailed design diagrams
│   ├── export/           PNG exports of the poster and diagrams
│   ├── deck/             PowerPoint deck (pptxgenjs) + theme step
│   └── jury-guide/       Jury Q&A preparation guide (PDF)
├── docs/                 Built documents and design notes
│   ├── poster/  architecture/  presentation/  jury-qa/
│   ├── decisions.md      Design decisions and why
│   └── architecture/data-model.md   Data model and mapping structures
├── assets/brand/         Laerdal logo (see "Brand" below)
├── Makefile  package.json  requirements.txt
```

## Quick start

### Run the app locally

The prototype is a static page and does not need Node.js, npm packages, API keys, or a backend.
With Python 3 installed, run:

```bash
make run
```

Then open <http://localhost:8000/clinical-identity-passport.html>. Stop the server with `Ctrl+C`.
The app uses synthetic data and mock sign-in; the password for every demo account is `passport-demo`.
Live AI is available only on a host that provides `window.claude.use("sample")`; otherwise the app
uses its built-in offline answers.

### Tests and document tooling

```bash
npm install                      # test and deck dependencies (requires Node.js 20+)
pip install -r requirements.txt  # document generators
npm test                         # builds the prototype, then runs 22 tests
```

To open the built page directly without a local server, use
`app/prototype/dist/clinical-identity-passport.html`.

**Demo sign-in.** Pick a demo account on the sign-in screen. The password for all of them is `passport-demo`.
Sign-in is a mock: nothing is authenticated.

| Role | Account | What it shows |
|---|---|---|
| Learner | `maya.okafor@northgate-health.example` | ED nurse, one skill due soon |
| Learner | `daniel.reyes@northgate-health.example` | NICU NP, lapsed CPR, one identity match waiting |
| Learner | `priya.nair@harborems.example` | Paramedic (PEPP, NEPP) |
| Administrator | `rhea.kapoor@northgate-health.example` | User list with search, filters and AI search |

## The AI assistant

Learners ask questions about one passport. Administrators ask about users in plain language, and the
assistant turns the question into a filter that the app applies. Each chat has demo question chips.
A toggle switches between two answer modes, and every answer is labelled with the mode that produced it:

* **Live AI** calls a model through the host page's `window.claude.use("sample")` capability.
  It exists only where the page is hosted with that capability (the Claude artifact host it was built on).
* **Offline rules** answer from the same records with plain code. Used automatically when no model is
  available or the model call fails.

Both modes pass the same checks: every sentence cites a record, no scoring language, no unknown record ids.
Names and emails are never sent to the model, and the administrator search sends only the question.
Statuses and dates are computed by code, never by the model. See `docs/decisions.md`.

## Themes

Laerdal style (default), Futuristic light and Futuristic dark. The theme button cycles through them.
The Laerdal palette is an approximation taken from the logo colours: replace the tokens at the end of
`app/prototype/src/styles.css` (and the matching block in `tools/poster/build.py`) with the official values.

## Building the documents

```bash
make poster architecture   # HTML pages in docs/
make images                # PNG exports (needs wkhtmltoimage on PATH)
make deck                  # docs/presentation/*.pptx
make guide                 # docs/jury-qa/*.pdf (best with the Inter font installed)
make all                   # prototype, documents, tests
```

The screenshots used in the deck (`tools/deck/img/`) were captured from the prototype with a headless
renderer. Re-take them if the interface changes; the capture script is not part of this repository.

## What is real and what is mocked

Real: the interface, status logic, the AI chat with guardrail checks, offline rules, identity-match logic with a pending queue.
Mocked or not built: source feeds (how sources deliver data is **not decided**: events, API pulls, PDFs or exports),
exposure logs, authentication, model-based matching and mapping, PDF conversion, consent and sources screens, the team view.
Consent and the team view are switched off in `app.js` (`FEATURES`) and can be turned back on.

## Brand

`assets/brand/` contains the Laerdal logo supplied for the prototype. It is a trademark: keep this repository
private or remove the logo and follow Laerdal brand rules before sharing it more widely.

## Status

Prototype. No security hardening, load testing, accuracy evaluation or privacy review has been done.
License: not chosen yet.
