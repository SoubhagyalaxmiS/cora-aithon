# Design decisions

Short records of the decisions that shape the product. Newest decisions go at the bottom.

## 1. Describe, never score
**Decision.** The passport shows evidence (current, due soon, lapsed, no evidence), recency and volume. It never scores, rates or ranks people, and the assistant refuses to.
**Why.** AI that evaluates staff or learning outcomes can be high-risk under the EU AI Act (obligations currently postponed to December 2027 per legal summaries; confirm with legal). The AHA 2025 guidelines also list consistent mastery standards and teamwork measurement as open gaps, so a score would be invented precision.
**Consequence.** Questions such as "Rank the nurses" return a refusal. Intended use must be documented and reviewed by legal before any pilot.

## 2. Code computes status; AI narrates and maps
**Decision.** Dates and statuses come from deterministic code. The model writes explanations, understands questions and (planned) maps activities and matches people.
**Why.** A model must not decide what is current or lapsed.

## 3. Every AI answer is cited and checked
**Decision.** The model gets only one person's structured records, must cite a record id after every claim, and the page checks the output: every sentence cited, ids exist, no scoring language. Failures are shown as warnings.
**Limit.** The checks prove a citation exists and is valid, not that the sentence is semantically right. Claim-level checks and an educator-built evaluation set are needed before a pilot.

## 4. No personal identifiers in prompts
**Decision.** Names, emails and employee ids are never sent to the model. The administrator search sends only the question and the allowed filter values, and the app runs the search.
**Note.** Role, unit and dates can still identify someone in a small team: treat this as pseudonymous, not anonymous.

## 5. Two answer modes
**Decision.** Live AI and Offline rules, switchable, every answer labelled. Offline rules also act as the fallback.
**Why.** The demo and the product must keep working when the model or network does not. Offline rules are a safety net, not the AI.

## 6. Identity by verified identifiers
**Decision.** A work email, or work plus personal, matches automatically. A personal email alone waits for a person, and the learner can prove ownership with a claim link. Ambiguous matches go to review and are never auto-merged. Stored emails are hashed. A stable source user id is planned.
**Weakness.** Email is a weak key (leavers, changed addresses). Needs a rule before a pilot.

## 7. Intake route is open
**Decision.** Sources may deliver events, API pulls, or PDFs and exports. All become one common evidence record through versioned adapters. Documents go through OCR or a model and a person reviews the extracted fields.
**Status.** Not decided and not built. The prototype uses synthetic records in the common format.

## 8. PostgreSQL with JSONB as the system of record
**Decision.** Relational tables for learners, identifiers, consent, taxonomy, mappings, role profiles, rules and audit; JSONB for variable payloads; raw input kept in object storage; personal data in a separate vault so erasure does not break history.
**Why.** Cross-user administrator queries, consent enforcement and versioned mappings favour a relational store. See `architecture/data-model.md`.
**Open.** Tenant model (one organization per deployment or many). `tenant_id` goes on every table from day one.

## 9. Prototype scope
**Decision.** Consent and sources screens and the team readiness view are deferred. They are switched off with `FEATURES` in `app/prototype/src/app.js`.
