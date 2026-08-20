# P8.00-A7 — Activation Evidence and Success / Failure Envelope

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Roadmap work item: `P8.00-A7 — Activation evidence and success/failure envelope`
Selected outcome: [`P8.00-A3`](P8-00-A3-bounded-external-outcome-selection.md)
Boundary map: [`P8.00-A4`](P8-00-A4-organization-authority-data-rights-map.md)
Platform necessity: [`P8.00-A5`](P8-00-A5-platform-responsibility-necessity-test.md)
Gate scan: [`P8.00-A6`](P8-00-A6-stable-readiness-adr-gate-scan.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — the selected EIS revalidation outcome has an explicit activation envelope and is ready for a fresh owner A8 decision.**

## 2. Selected outcome and accountable owner

Selected outcome:

> Re-observe the same real EIS notice `0344100006426000005` at a later time, compare the fresh exact source/document snapshot with the immutable P6 baseline, and prove governed external-authority/freshness/version-drift semantics without rewriting prior history.

Accountable owner: `ООО «Арвектум»`.

Operational execution remains owner-operated inside the existing M7 internal contour.

## 3. Exact external boundary

External system: ЕИС / `zakupki.gov.ru`.

External authority:

- EIS remains authoritative for registry/document source facts within the retrieved scope;
- Arvectum OS governs only its own observation/reference/provenance/execution history;
- Tender Operator owns the EIS retrieval adapter and procurement-specific behavior.

Authority mode: `External Reference`.

No `Governed Replica` or `Native` substitution is authorized.

## 4. Initial contract need

Before live Phase 8 external reliance:

- P8.01 must define the exact execution/evidence baseline;
- P8.02 must refine identity/trust/rights/data-governance controls for the active phase;
- P8.03 must create the minimum explicit `Provisional` integration contract for the EIS revalidation boundary;
- R25 must pass before P8.04 real live connector validation.

No Stable Product Contract/public surface is required or authorized by A7.

## 5. Permitted data and effects

Permitted:

- one bounded read-only EIS retrieval for the selected notice during the P8.04 validation attempt;
- local owner-controlled storage of source archive/documents needed for exact verification;
- minimized source identifiers, names where appropriate, sizes, hashes, timestamps and comparison metadata;
- governed Arvectum OS records/events/references required to attribute external authority, freshness, exact version and reconstruction evidence;
- deterministic local comparison to the immutable P6 baseline;
- read-only reconstruction/inspection.

Permitted result classes:

- `NO_CHANGE`;
- `CHANGE_DETECTED`;
- `FAIL_CLOSED`;
- `INCOMPLETE`;
- `UNCERTAIN_RECONCILIATION_REQUIRED` where an external outcome cannot be established safely.

## 6. Prohibited data and effects

Prohibited:

- EIS/ETP mutation;
- procurement application submission;
- EDS/digital signature;
- supplier/customer messaging;
- public redistribution of source documents through this validation;
- cross-Organization data movement;
- customer-facing Production use;
- storing reusable credentials/private keys in canonical history or ordinary committed logs;
- weakening TLS/certificate verification;
- silently using stale P6 evidence as if it were a fresh EIS observation;
- mutation of historical P6 evidence;
- promotion of product-local EIS parsing/retrieval logic into shared platform behavior without a later governed decision.

## 7. Required provenance and reconstruction evidence

A successful P8.04 evidence package must make it possible to reconstruct, directly or by governed reference:

1. governing Organization;
2. initiating/acting Actor or service identity;
3. exact P8.03 integration-contract version;
4. exact external system and notice identity;
5. external authority mode/source;
6. observation time and retrieval outcome;
7. TLS/trust posture facts needed to show verification was not weakened, without secret/certificate dumping;
8. exact new source/document snapshot integrity evidence;
9. immutable P6 baseline reference and baseline manifest hash;
10. deterministic comparison result and per-material-item disposition;
11. required platform Canonical Record/Event/Execution Context references;
12. terminal success/failure/incomplete/uncertain state;
13. known omissions, deleted data or unavailable evidence.

Historical replay or reconstruction must never trigger a new EIS retrieval or another external effect automatically.

## 8. Failure-closed behavior

Stop the live attempt and preserve explicit failure/incomplete evidence if any material condition is not satisfied, including:

- unresolved Organization/Actor context;
- failed TLS trust or hostname verification;
- failed/ambiguous authentication;
- wrong notice identity;
- source retrieval unavailable or unverifiable;
- unsafe archive extraction;
- missing/duplicate/ambiguous exact source set;
- manifest/hash verification mismatch;
- comparison cannot determine current state;
- contract/dependency/version preflight fails;
- required platform evidence path fails;
- requested action exceeds read-only scope;
- rights/purpose would need to be widened to proceed.

Do not downgrade required controls merely to produce a PASS.

## 9. Rollout / rollback / containment

Rollout is deliberately one bounded validation path:

1. complete P8.01–P8.03 and R25 in repository governance;
2. run one owner-operated local P8.04 live validation against the selected EIS notice;
3. preserve minimized evidence and compare against the P6 baseline;
4. review result before advancing to P8.05.

Rollback/containment:

- no EIS state needs rollback because the operation is read-only;
- local transient/raw files may be quarantined or deleted under existing retention controls if the run fails;
- platform records already admitted remain immutable and may be followed by correction/invalidation evidence rather than mutation;
- if shared platform semantics prove unnecessary or require EIS-specific leakage, return the adapter/logic to product-local containment and record the limitation;
- if a stable/public/Production/second-Organization threshold appears, stop before material reliance and open the required governance gate.

## 10. Review triggers

Immediate review is required when:

- EIS endpoint/authentication/trust behavior materially changes;
- the product needs a different retrieval protocol with new stable dependency pressure;
- the first live run reveals uncertain source state or incomplete evidence;
- a second product needs the same external-authority/freshness semantics;
- a second Organization/customer enters scope;
- redistribution, customer delivery, mutation or signature is proposed;
- a public/stable interface or compatibility promise becomes necessary;
- an Incubating capability lifecycle transition is proposed.

## 11. Activation success criteria

P8.00 may activate Phase 8 only if A8 records fresh owner approval after confirming:

- A1–A7 are `Complete / PASS`;
- selected outcome remains bounded and materially new;
- one Organization only is explicit;
- unresolved rights remain deny-by-default;
- platform responsibility is narrow and justified;
- A6 remains `NO-GATE` for the bounded scope;
- P8.01–P8.03 + R25 remain mandatory before live P8.04 execution;
- no lifecycle, Production, SLA or public-interface claim is implied.

## 12. Conditions for defer / product-local return

Return to `DEFER` or product-local containment if:

- A8 owner approval is not granted;
- no fresh EIS observation can be performed within the declared rights/security boundary;
- P8.01 cannot define verifiable technical success evidence;
- P8.02 identifies an unresolved rights/authority condition that blocks the declared purpose;
- P8.03 would require premature Stable/public commitment;
- R25 finds material product/platform leakage or security ambiguity that cannot be bounded;
- P8.04 shows that platform semantics add no governed value beyond product-local state;
- implementation requires a higher gate that is not approved.

## 13. Cross-review

### Iteration 1 — operations

Ensured the live validation is one bounded read-only path with explicit failure states and no hidden retry into external mutation.

### Iteration 2 — security/data governance

Separated minimized canonical evidence from raw owner-local source data and secrets; unresolved rights fail closed.

### Iteration 3 — lifecycle/governance

Made P8.01–P8.03 and R25 mandatory before P8.04 and preserved all non-claims.

**Result:** `PASS`; no material objection remains.

## 14. Handoff

A7 exit criteria are satisfied.

Next canonical action:

> **P8.00-A8 — Fresh owner activation decision.**
