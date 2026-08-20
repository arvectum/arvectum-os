# P8.00-A3 — Bounded External Outcome Selection

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Roadmap work item: `P8.00-A3 — Select one bounded external outcome`
Parent: [`P8.00 — Phase 8 Activation / External-Ecosystem Boundary Revalidation`](../roadmap/P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md)
Predecessor: [`P8.00-A2 — Candidate Triage and Value Test`](P8-00-A2-candidate-triage-and-value-test.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — one bounded external outcome is selected from the A2 shortlist.**

Selected outcome:

> **EIS authoritative-source revalidation across time:** for the already evidenced real 44-ФЗ notice `0344100006426000005`, perform a new independent read-only retrieval from ЕИС / `zakupki.gov.ru` after the P6 observation, produce a second exact source snapshot, compare it with the preserved P6 exact-attachment baseline, and prove that Arvectum OS can represent external freshness/version drift without rewriting prior history or converting ЕИС data into `Native` authority.

This is a validation outcome, not a technology goal and not a decision to move the EIS connector into Arvectum OS.

## 2. Why this is materially new

P6.05-L7 proved one point-in-time exact retrieval:

- notice `0344100006426000005`;
- read-only `getDocsIP` / `getDocsByReestrNumber` path;
- exact `7/7` document set;
- baseline manifest SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- external authority preserved;
- no EIS mutation, submission, email or digital signature.

A3 does not repeat that proof. The selected Phase 8 outcome adds a second temporal observation and tests a different external-ecosystem property:

1. the external authoritative system may remain unchanged or may change outside Arvectum OS control;
2. a later governed execution must know which external observation/version/freshness it relied upon;
3. changed, added, removed or byte-different source documents must create new governed observations/references rather than mutate the P6 history;
4. an unchanged result must also be evidenced as a fresh observation rather than inferred from the old snapshot;
5. failure to establish current authoritative evidence must fail closed instead of silently reusing stale source state.

The outcome therefore validates authority preservation, temporal freshness, exact-version reliance and external drift handling rather than another one-off download.

## 3. External boundary

- External authoritative system: ЕИС / `zakupki.gov.ru`.
- External object: procurement notice `0344100006426000005` and its current source-listed documentation package.
- Product: Tender Operator.
- Governing Organization for this validation: `ООО «Арвектум»` only.
- Authority mode: `External Reference` for EIS registry/document facts and source content.
- Connector ownership: Tender Operator / product-owned.
- Platform responsibility under evaluation: governed external-authority observation, exact-version/freshness attribution, provenance and reconstruction around the product-owned connector.

No second Organization, external customer, portability recipient or new external product consumer is introduced by assumption.

## 4. Exact organizational result to validate

After the new live retrieval, the system must be able to answer, from retained governed evidence and without trusting only transient stdout:

1. which EIS notice was queried;
2. when the new external observation was made;
3. whether the current source-listed document set is unchanged or differs from the P6 baseline;
4. for every material document, whether it is `UNCHANGED`, `ADDED`, `REMOVED` or `CHANGED` based on exact source identity and byte-integrity evidence available to the bounded run;
5. which exact external observation/version a later governed execution is allowed to rely on;
6. whether required evidence is complete, unavailable, ambiguous or stale;
7. that the P6 observation remains immutable historical evidence regardless of the later EIS state.

A valid outcome may be either `NO_CHANGE` or `CHANGE_DETECTED`. The experiment is not conditioned on EIS actually changing the documents.

## 5. Success criteria

A3 defines success for the later live validation as all of the following:

- exactly one new top-level read-only EIS retrieval for the selected notice;
- TLS certificate and hostname verification are not weakened;
- a fresh source observation timestamp and exact second snapshot are produced;
- the second snapshot is independently verifiable from owner-only runtime state;
- comparison to the P6 baseline is deterministic and complete for the declared material set;
- every comparison result is explicit rather than inferred;
- old P6 evidence remains unchanged;
- external authority remains ЕИС;
- no secret/token/raw credential enters canonical repository history or ordinary committed evidence;
- no EIS/ETP mutation, bid submission, signature, supplier/customer communication or other external organizational commitment occurs;
- required platform evidence can reconstruct the external-authority/freshness decision or state exactly why reconstruction is incomplete.

## 6. Failure-closed behavior

The validation must not claim a current authoritative snapshot when any material prerequisite is unresolved.

Examples requiring `FAIL-CLOSED`, `INCOMPLETE` or explicit `UNCERTAIN/RECONCILIATION_REQUIRED` as applicable:

- TLS/trust verification failure;
- credential/authentication failure;
- external request failure or timeout with no reliable current-state evidence;
- ambiguous notice identity;
- unsafe archive or path handling;
- missing/duplicate source-listed documents where the comparison contract requires uniqueness;
- inability to recompute/verify required hashes or manifest integrity;
- inability to determine whether a material source item changed;
- local comparison logic failure;
- attempted fallback to the old P6 snapshot while representing it as fresh EIS state.

No failure mode authorizes weakening certificate verification, broadening credentials, retrying consequential external mutations, or treating cached product state as EIS authority.

## 7. Explicit non-goals

A3 does not select or authorize:

- a generic EIS connector Platform Capability;
- a public/stable government-system API or wire format;
- `Governed Replica` synchronization;
- EIS/ETP mutation, application submission or digital-signature actions;
- automated customer-facing service;
- cross-Organization access or sharing;
- redistribution of source documents;
- SLA/SLO/RPO/RTO/support commitments;
- Product Contract `Stable` transition;
- Platform Capability `Active` transition;
- customer/external `Production` claim;
- a claim that technical EIS access establishes legal or contractual rights.

## 8. Cross-review

### Iteration 1 — architecture / product boundary

**Finding:** a temporal EIS validation could be misread as platform ownership of the EIS adapter.

**Revision:** the selected object is the domain-neutral governed external-authority/freshness envelope; the connector and procurement semantics remain product-owned.

### Iteration 2 — evidence novelty

**Finding:** simply downloading the same notice again would duplicate P6.

**Revision:** success now requires a second time-indexed external snapshot, deterministic comparison against the immutable P6 baseline, and explicit current-version/freshness reliance semantics.

### Iteration 3 — authority / rights

**Finding:** read-only technical access must not be described as broader permission.

**Revision:** rights remain bounded and unresolved cases move to A4 under deny-by-default; A3 adds no redistribution, mutation or customer-facing permission claim.

**Result:** `PASS`; no material objection remains.

## 9. Handoff

A3 exit criteria are satisfied. The selected outcome is concrete, bounded, externally meaningful, materially distinct from the prior P6 proof and reversible.

Next canonical action:

> **P8.00-A4 — Organization / identity / authority / data-rights map.**
