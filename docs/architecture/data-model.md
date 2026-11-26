# Data model and mapping structures

Proposal. Everything below is data, not code, so sources, skills, fields and rules can be added without a deployment.
How sources deliver data (events, API pulls, PDFs or exports) is **not decided**: each route ends as the same canonical evidence record.

## Intake

```
source data → raw input store (immutable) → source adapter (versioned) → canonical evidence record → projections
```

* **Idempotent writes:** deduplicate on `(source_id, source_record_id)`.
* **Corrections:** model `issued`, `completed`, `revoked` and `corrected` as record types, not edits.
* **Replay:** keep raw input so results can be re-run after a mapping or rule change.
* **Order independent:** compute status from record time, not arrival order.
* **Bad input:** unknown schema versions and unparseable documents go to a review queue, not into the passport.
* **Delivery by queue:** at-least-once, so expect duplicates, late and out-of-order records. Save the raw message before acknowledging.

## Structures

**Skill taxonomy** (the seven areas are rows, not constants)
```json
{ "skill_id": "airway.supraglottic", "parent_id": "airway", "label": "Supraglottic airway",
  "scope": "global | tenant:<id>", "status": "active", "version": 3 }
```

**Source registry and adapter config**
```json
{ "source_id": "rqi1stop", "intake": "event | api | file", "adapter_version": "2.1",
  "field_map": { "learner_ref": "$.user.id", "email": "$.user.email",
                 "occurred_at": "$.session.completed_at", "expires_at": "$.credential.expires" },
  "identity_keys": ["work_email", "personal_email"] }
```

**Activity-to-skill mapping** (AI proposes, a person approves)
```json
{ "mapping_id": "m-1042", "source_id": "pediaskills", "match": { "program_code": "PEPP-ALS" },
  "skills": [ { "skill_id": "assessment", "coverage": "primary" },
              { "skill_id": "airway", "coverage": "partial" } ],
  "status": "approved", "proposed_by": "ai", "approved_by": "usr-77", "valid_from": "2026-09-15", "version": 1 }
```
`coverage` is `primary` or `partial`, never a number, so it cannot turn into a hidden score.

**Validity rule**
```json
{ "rule_id": "v-rqi-quarterly", "match": { "source_id": "rqi1stop" }, "basis": "provider_stated | fixed_window", "window_days": 90 }
```

**Role profile** (which skills a role is expected to show)
```json
{ "role_profile_id": "rn-ed", "label": "RN, Emergency", "tenant": "northgate",
  "expected_skills": ["cpr", "airway", "assessment", "emergency", "medication", "comm"],
  "unit_overrides": { "NICU": { "add": ["matneo"] } } }
```

**Canonical evidence record**
```json
{ "evidence_id": "ev-2041", "learner_id": "lrn-5", "source_id": "rqi1stop", "source_record_id": "...",
  "type": "session.completed", "skills": ["cpr"], "occurred_at": "2026-11-04", "valid_until": "2027-02-02",
  "modality": "manikin", "assessed_by": "automated", "verification": "verified | self_reported | pending",
  "metrics": { "depth_in_range_pct": 94 }, "extra": {}, "mapping_version": "m-1042@1", "raw_ref": "..." }
```

**Attribute definition** (lets administrators add user fields later)
```json
{ "attr_id": "license_no", "applies_to": "learner", "type": "string", "pii": true,
  "visible_to": ["learner", "admin"], "tenant": "northgate" }
```

## Identity resolution

Identifiers a learner owns:
```json
{ "identifier_id": "id-91", "learner_id": "lrn-5", "kind": "email", "value_hash": "hmac(normalised address)",
  "email_class": "work | personal | unknown", "status": "verified | unverified | retired",
  "verified_via": "claim_link | sso | admin" }
```
An administrator-editable domain registry classifies addresses as work, personal or unknown.

| Incoming email | Result |
|---|---|
| Matches a verified identifier | Attach automatically |
| Matches an unverified identifier | Attach as tentative, held out of the passport |
| No match, known work domain | Unclaimed record; suggest candidates by name similarity (a weak hint) |
| No match, personal or unknown domain | Quarantine; the learner proves ownership with a claim link |
| Matches two learners | Administrator review; never auto-merge |

After the first confirmed match, bind `(source_id, source_user_id)` to the learner so later records do not depend on email.
Store only an HMAC of the address in records and logs; keep the plain text in a separate encrypted vault so erasure does not break history.

## Database choice

PostgreSQL as system of record, with JSONB for the variable parts. Relational tables for learners, identifiers, consent, taxonomy, mappings, role profiles, rules and audit.
JSONB columns for metrics, extras and custom attributes. Raw input in object storage or an append-only log. A materialised passport view per learner, rebuilt when mappings change.
Put `tenant_id` on every table from day one and enforce it with row-level security.
