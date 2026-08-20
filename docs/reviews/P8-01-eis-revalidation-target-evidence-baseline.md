# P8.01 — EIS Revalidation Target Execution Baseline + Evidence Package

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`, `product_specific` and `governance`
Phase: `Phase 8 — Active`
Activation decision: [`DECISION-2026-08-20-PHASE-8-ACTIVATION`](../governance/decisions/DECISION-2026-08-20-PHASE-8-ACTIVATION.md)
Selected outcome: [`P8.00-A3`](P8-00-A3-bounded-external-outcome-selection.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — one exact external validation case is defined and is ready for P8.02/P8.03 boundary design.**

No live EIS request is performed by P8.01.

## 2. Exact validation target

- Governing Organization: `ООО «Арвектум»`.
- Product: Tender Operator.
- External authoritative system: ЕИС / `zakupki.gov.ru`.
- Notice: `0344100006426000005`.
- Law/subsystem baseline from P6: `44-ФЗ`, `PRIZ`.
- Product retrieval path baseline: read-only EIS `getDocsIP` / `getDocsByReestrNumber`, archive download enabled, analysis disabled for the evidence capture.
- Authority mode: `External Reference`.
- Operational environment: existing M7 `Persistent Internal / owner-operated` contour.

## 3. Immutable predecessor evidence

P6.05-L7 attempt #2 is the historical baseline and must not be modified.

Canonical facts:

- attempt date: `2026-08-15`;
- exact source set: `7/7` required documents;
- baseline manifest SHA-256: `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- P6 evidence status: `PASS_EXACT_ATTACHMENT_EVIDENCE`;
- TLS certificate verification and hostname verification were preserved;
- external actions were false;
- no platform submission, email or digital signature occurred;
- raw owner-only runtime artifacts were not committed.

The P8 run compares to this evidence; it does not reconstruct the P6 source files by mutating or regenerating historical evidence.

## 4. Current integration path and observed limitation

Current path:

1. Tender Operator performs EIS-specific discovery/retrieval locally.
2. It can download and safely extract the EIS document archive.
3. It can produce exact attachment evidence and a deterministic manifest.
4. Arvectum OS can govern exact external document references/provenance and reconstruct platform-backed execution evidence within the existing Product Contract contour.

Observed limitation relevant to Phase 8:

> P6 proves one exact point-in-time source observation but does not yet prove how a later governed execution distinguishes a fresh EIS observation from historical/cached state, or how external source change/no-change is represented without mutating prior history.

P8.01 validates that missing temporal external-authority boundary.

## 5. Exact data / effect boundary

External effect class: `ReadOnly` external retrieval only.

Data in scope:

- selected EIS notice reference;
- current source-listed document set for that notice;
- exact downloaded bytes needed for local verification;
- observation/retrieval time;
- source names/identifiers where necessary;
- sizes and cryptographic hashes;
- deterministic comparison to the P6 baseline;
- governed references/provenance/Execution Context/Event evidence needed for reconstruction.

Data/effects out of scope:

- EIS/ETP writes;
- application submission/signature;
- supplier/customer communication;
- customer data or a second Organization;
- source redistribution;
- product analysis/recommendation execution during the capture unless separately needed and authorized;
- public/stable integration exposure.

## 6. External dependency and freshness assumptions

- EIS is external and may be unavailable, changed, rate-limited or differently configured without Arvectum OS control.
- A previous successful snapshot is not evidence of current freshness.
- A new observation time is required for the P8.04 result.
- `NO_CHANGE` requires a successful new source retrieval and deterministic comparison; it cannot be inferred from old state.
- `CHANGE_DETECTED` requires explicit per-item evidence sufficient to show added/removed/changed material source state.
- If current authoritative state cannot be established, the result is not success and the old snapshot must not be presented as fresh.

No SLA or external availability guarantee is assumed.

## 7. Measurable technical success criteria

A live P8.04 attempt passes only if all required checks below pass:

1. one top-level bounded execution is attributable to the explicit Organization/Actor;
2. exact selected notice identity is preserved;
3. verified TLS remains enabled and no certificate/hostname verification is weakened;
4. current EIS source retrieval completes or fails explicitly;
5. a new exact observation manifest/equivalent is produced with observation time and integrity evidence;
6. the new snapshot is independently verified from owner-only runtime state;
7. comparison to the immutable P6 baseline is deterministic;
8. material items are classified as `UNCHANGED`, `ADDED`, `REMOVED` or `CHANGED` as applicable;
9. overall result is exactly one of `NO_CHANGE`, `CHANGE_DETECTED`, or an explicit non-success state;
10. historical P6 evidence remains unchanged;
11. external authority remains ЕИС;
12. required platform evidence identifies exact contract/workflow/input/external-observation references;
13. no secret/raw credential is committed or written into canonical evidence;
14. no prohibited external effect occurs;
15. reconstruction/inspection can explain which external observation the execution relied on and whether evidence is complete.

No invented business-value percentage, SLA, reliability target or customer commitment is required for PASS.

## 8. Failure-closed criteria

The live run must terminate or remain explicitly incomplete if:

- Organization/Actor cannot be resolved;
- contract/dependency preflight fails;
- TLS trust fails;
- authentication fails;
- request/response identity is ambiguous;
- archive/path safety fails;
- exact source evidence is incomplete or internally inconsistent;
- hash/manifest verification fails;
- comparison cannot determine the declared material state;
- required platform evidence cannot be admitted/preserved;
- proceeding would require rights expansion or a prohibited effect.

A cached P6 snapshot is never an allowed substitute for a failed current retrieval.

## 9. Evidence retention and minimization

Canonical/repository evidence should retain only what is necessary to reconstruct the validation, such as:

- immutable references;
- notice/source identity;
- observation times;
- counts;
- sizes/hashes;
- comparison dispositions;
- non-secret trust posture;
- relevant exact contract/workflow/version references;
- result/failure state.

Keep owner-only/raw runtime data outside Git history:

- token/credentials;
- archive and raw document bytes unless a safely redacted fixture is separately justified;
- raw SOAP/XML when not required;
- absolute local paths;
- private keys/certificates;
- unnecessary opaque runtime IDs.

## 10. Non-goals

P8.01 does not create a generic EIS connector, public API, Stable contract, Active capability, second Organization, customer Production environment, SLA/support commitment or redistribution right.

## 11. Cross-review

### Iteration 1 — evidence

Made the temporal novelty measurable: a fresh source observation and deterministic comparison are mandatory even for `NO_CHANGE`.

### Iteration 2 — security

Preserved the P6 TLS/secret boundary and prohibited stale fallback masquerading as freshness.

### Iteration 3 — architecture/product

Kept EIS retrieval implementation and procurement semantics product-owned while defining only platform-governed reliance evidence.

**Result:** `PASS`; no material objection remains.

## 12. Handoff

P8.01 exit criteria are satisfied.

Next canonical action:

> **P8.02 — Cross-Organization identity, trust, rights + data-governance boundary.**
