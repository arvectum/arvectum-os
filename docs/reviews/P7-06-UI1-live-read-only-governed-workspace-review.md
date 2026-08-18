# P7.06-UI1 Live Read-Only Governed Workspace — Repository Cross-Review

Status: `Complete / PASS for repository implementation; selected-Mac closure pending`
Date: `2026-08-18`
Task classification: `platform`
Review iterations: `2 / max 7`

## 1. Scope

This review covers the repository-side implementation of `P7.06-UI1 — Live read-only governed workspace` only.

It does not substitute for the required selected-Mac browser/live-runtime proof and therefore does not close UI1 itself.

## 2. Authority and boundary review

Checked against Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, the canonical roadmap, M4 workspace semantics, and the P7.03–P7.06 operational boundaries.

Result:

- no Constitution conflict found;
- no Accepted RFC conflict found;
- no Accepted ADR is required for the current private/reversible UI adapter;
- no Product Contract or capability lifecycle transition is introduced;
- the workspace remains a non-authoritative presentation adapter;
- authentication/authorization remains distinct from Organizational Authority and approval;
- presentation grouping does not redefine canonical semantic type or lifecycle;
- P7.03 recovery checkpoints remain explicitly non-authoritative;
- no public/stable API, browser matrix, frontend stack or support commitment is created.

## 3. Functional review iteration 1

Result: `REVISE`.

The first implementation correctly established the major boundaries:

- exact P7.04 human Organization/operation/resource/local authorization before protected reads;
- exact activated P7.06 release verification;
- P7.05 healthy runtime/release match;
- verified P7.03 item/checkpoint reads;
- exclusion of governed test fixtures;
- all M4 destinations;
- Subject versus Exact Version visibility;
- no governed payload rendering;
- loopback-only HTTP server;
- GET/HEAD-only surface and explicit mutation-method rejection;
- re-authorization on every request;
- generic protected blocked state.

Two material honesty/integrity objections remained:

1. if the governed item directory did not exist, UI1 returned an empty collection, which could misrepresent `unavailable` state as `zero records`;
2. checkpoint enumeration filtered to `*.json`, which could silently ignore an unexpected/staging entry instead of failing closed on store-integrity ambiguity.

Both findings were material because the UI1 exit criteria require honest unavailable/missing states and fail-closed protected reads.

## 4. Revision

The implementation was changed so that:

- missing governed-item or checkpoint roots are `unavailable` integrity failures rather than empty results;
- every checkpoint-store entry is inspected, and hidden, symlinked, non-file or non-JSON entries fail closed;
- regression tests explicitly cover both cases.

## 5. Functional review iteration 2

Result: `PASS — no material repository-side objections remain`.

The revised implementation preserves the intended read-only and authority boundaries and closes the two iteration-1 findings.

Executable evidence includes tests for:

- no runtime-root content change across an authorized live snapshot;
- real canonical governed metadata read with fixtures excluded;
- all M4 workspace destinations;
- Subject / Exact Version distinction;
- non-inference of missing source/lifecycle/validation metadata;
- wrong Organization failure before governed-state read;
- revoked/missing grant failure before governed-state read;
- service principal rejection for the current human-operator UI1 scope;
- runtime/current-release mismatch failure before governed-state disclosure;
- loopback HTTP GET behavior, security/no-cache headers and re-authorization after grant revocation;
- explicit rejection of mutation HTTP methods;
- non-loopback bind rejection;
- missing governed store and unexpected checkpoint-store entries failing closed;
- static absence of P7.03/P7.04/P7.05 mutation calls from the UI1 module.

GitHub `Reference Python CI` run `32132213609` on head `83fb21f19ae99552c8a1a665a94a32e9f008da4c` completed with conclusion `success`.

## 6. Remaining closure evidence

The following is deliberately **not** claimed by this review:

- UI1 browser visibility on the actual selected Mac;
- deployment of this implementation to the exact selected-Mac current release;
- inspection of an actual retained non-fixture governed item in that live browser session;
- selected-Mac before/after evidence proving zero canonical/external mutation from browsing.

Those items remain the current UI1 closure action and must be completed before `P7.06-UI1 = Complete / PASS` or before advancing canonical sequencing to UI2.

## 7. Final repository disposition

`Repository implementation = PASS`.

`P7.06-UI1 = Current / selected-Mac closure pending`.
