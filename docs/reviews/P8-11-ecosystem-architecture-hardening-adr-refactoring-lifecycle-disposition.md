# P8.11 — Ecosystem Architecture Hardening + ADR / Refactoring / Lifecycle Disposition

Status: `Complete / PASS — bounded ecosystem architecture retained; no ADR, lifecycle promotion or shared-surface generalization justified`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract` implications
Constitution: `1.2.0` (`Ratified`, frozen)
Checked Accepted RFC: RFC-0001 through RFC-0008 (`1.0.0`)
Checked ADR: no Accepted ADR exists; `docs/adrs/` contains only the ADR process/index
Roadmap source: `docs/roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`
Predecessor: `P8.10 — Complete / PASS`

## 1. Decision

P8.11 completes the end-to-end Phase 8 architecture hardening review without inventing a new architecture layer merely because external integration evidence now exists.

The disposition is:

> **Retain the existing governed Product Contract / exact dependency / security / Governed Execution / Event-provenance architecture. Keep CAP-001 through CAP-004 `Incubating / Provisional`; retain CAP-004 with stronger external-reuse evidence but do not promote it to `Active`; contain the P8.06 external-consumer onboarding helper, P8.07 handover package and P8.09 runbook as bounded reference evidence; keep Creative Test Agent declaration semantics product-owned and EIS integration behavior Tender Operator-owned; defer any public SDK/API, generic manifest/registry, connector marketplace, universal handover format or multi-Organization protocol until materially stronger evidence and the applicable separate governed decision exist.**

No Constitution amendment, RFC amendment, ADR, Stable Product Contract transition, Platform Capability lifecycle transition, external Production approval, support/SLA commitment or new commercial promise is created by P8.11.

## 2. Authority and evidence reviewed

P8.11 rechecked the minimum-authority decision level against:

1. Constitution `1.2.0` — product/platform separation, security/privacy/isolation, organizational sovereignty, portability, AI authority limits, evidence over intuition and minimum sufficient governance level;
2. RFC-0001 — validated reuse, Capability lifecycle, Product/Platform boundary, operational-readiness requirements, technology independence, scoped conformance and commercial-commitment integrity;
3. RFC-0002 — stable Subject/Version identity, Canonical Record semantics, authority modes and non-authoritative projections;
4. RFC-0003 — deny-by-default authorization, Organization sovereignty, cross-Organization isolation, data governance and portability/handover;
5. RFC-0004 — Product Contract lifecycle, explicit dependencies, no hidden coupling and separate capability lifecycle;
6. RFC-0005 — Governed Execution for consequential canonical mutation and side-effect-safe execution/replay boundaries;
7. RFC-0006 — append-only Events, provenance, uncertainty/reconciliation and non-canonical telemetry;
8. RFC-0007 — Observation/Memory/Knowledge separation, governed promotion and cross-Organization learning restrictions;
9. RFC-0008 — Document/Artifact portability and generated/transient-output boundaries;
10. `docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`;
11. `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`;
12. P8.00-A6 ADR gate scan;
13. P8.01 through P8.10 plus R25, R26 and R27;
14. P8.06/P8.09 external-consumer reference implementation and executable evidence;
15. P8.07 portability/handover proof and P8.08 non-activation disposition;
16. current repository navigation state, including the root README;
17. Phase 3/M3 continuity regression evidence and the Phase 8 sequencing chain through R28 and P8.12.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was found.

The Decision Authority Policy remains `Proposed 0.2.1` and is not treated as approved delegation. Residual authority remains with the owner under the Accepted baseline.

## 3. Phase 8 architecture review

### 3.1 What Phase 8 actually validated

Phase 8 added evidence for three bounded categories without changing the fundamental architecture:

- **external authoritative source integration:** EIS read-only temporal revalidation preserves `External Reference` authority and immutable prior evidence;
- **separately maintained external product consumption:** Creative Test Agent consumes exact CAP-004 reconstruction semantics through an exact `Provisional 0.1.0` Product Contract and fail-closed dependency resolution;
- **semantic portability:** P8.07 demonstrates preservation of identity/version/relationship/provenance/handling/authority semantics across an isolated receiver boundary without exporting reusable secrets or replaying external effects.

P8.08 correctly records that realistic simultaneous two-Organization isolation remains `NOT ACTIVATED / NOT PROVEN` because no genuine second Organization is canonically in scope.

### 3.2 What Phase 8 did not validate

The evidence does not establish:

- arbitrary external integration compatibility;
- a generic platform-owned external-consumer manifest;
- plugin/extension registry or marketplace;
- public/stable SDK/API/wire/package protocol;
- universal export/import/customer-handover format;
- cross-Organization migration protocol;
- realistic two-Organization isolation;
- external/customer Production readiness;
- Stable Product Contracts;
- Active Platform Capabilities;
- customer support, SLA/SLO/RPO/RTO or certification commitments.

Those non-claims remain architectural inputs, not omissions to be filled speculatively.

## 4. ADR gate disposition

P8.11 re-opens the concrete ADR gate after the complete Phase 8 evidence set.

| Boundary | Current evidence | P8.11 disposition | Future ADR trigger |
|---|---|---|---|
| public/stable API, SDK, wire or serialization | exact internal/provisional Python/reference shapes only | `No ADR` | first durable supported cross-repository/public compatibility surface |
| external-consumer manifest / registry / package protocol | one product-owned declaration and one bounded onboarding helper | `No ADR` | platform-owned durable manifest/registry/protocol materially relied upon by multiple consumers |
| connector/plugin framework or marketplace | no admitted generic framework | `No ADR` | concrete shared runtime/discovery/install/compatibility mechanism becomes relied upon |
| customer export/import/handover format | P8.07 task-local proof schema only | `No ADR` | durable supported recipient-facing format/importer or migration topology |
| multi-Organization persistence/isolation topology | genuine second Organization absent; P8.08 not activated | `No ADR` | concrete shared datastore/cache/index/log/admin topology for multiple real Organizations |
| IAM / PDP / PEP / external trust protocol | semantic controls only; EIS credential/trust remains product-owned | `No ADR` | concrete shared IAM/policy/trust technology becomes materially relied upon |
| Event transport / broker / replay store | semantic Event/provenance model only | `No ADR` | durable shared broker/store/checkpoint topology becomes part of relied-upon behavior |
| external deployment/service topology | owner-operated internal contour only | `No ADR` | customer/public deployable service boundary or topology-specific failure contract |

**ADR decision: no new ADR is justified at P8.11.**

Creating ADR-0001 now would freeze an incidental implementation or an unproven generalization rather than a concrete architecture choice. The ADR gate remains armed for the explicit future triggers above.

## 5. Refactoring / hardening disposition

### 5.1 Shared runtime/code refactor

**No material runtime refactor is justified.**

The P8.06 onboarding helper already states and enforces that it is internal bounded reference evidence, not a public SDK/API, manifest, registry, authorization system, lifecycle transition or durable shared state. R27 found only one real external consumer and explicitly rejected shared-platform ownership admission for a generic onboarding abstraction.

P8.11 therefore rejects premature refactors that would:

- extract a generic `External Consumer Onboarding` Platform Capability;
- move Creative Test Agent declaration format into Arvectum OS;
- stabilize current Python dataclasses or operation tokens as public contracts;
- generalize the P8.07 proof package into a customer export standard;
- create connector/plugin registry, marketplace, package manager or automatic version negotiation;
- move EIS/procurement semantics into the platform;
- create multi-tenant infrastructure before a genuine second Organization and selected topology exist.

### 5.2 P8.11-F1 — root README planning drift

Severity: `Material navigation / contributor correctness`, lower-authority artifact.

Finding: the root `README.md` still described Phase 6 as Active and P6.03 as the current action after the canonical roadmap had advanced to P8.11.

Disposition: `Remediated in P8.11`.

The root README is refactored into a concise repository entry point that:

- identifies the canonical authority order;
- points to `docs/roadmap/ROADMAP.md` as the only source for current action and sequencing;
- summarizes Phase 8 without duplicating a mutable action pointer;
- preserves stable historical milestone continuity required by regression evidence;
- preserves current lifecycle/non-claim boundaries;
- links to the P8.11 disposition and relevant Phase 8 evidence.

This removes a recurring drift class rather than merely replacing one stale action label with another. The README remains subordinate and does not become a competing roadmap.

### 5.3 P8.11-F2 — hardening-test formatting brittleness

Severity: `Low / test-quality`, found by CI.

Finding: the first P8.11 guard compared a semantically continuous module-docstring phrase across a physical line break as a raw substring.

Disposition: `Remediated in P8.11`.

The guard now normalizes whitespace before asserting the bounded onboarding non-claims. This protects semantics rather than source formatting.

## 6. Lifecycle disposition

### 6.1 Platform Capabilities

| Subject | P8.11 disposition | Evidence / rationale | Missing before stronger transition |
|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | `Retain Incubating / Provisional` | Phase 8 portability/document semantics remain consistent; no new supported stable surface | stable supported contract, compatibility/migration, operational readiness/support and applicable external reliance evidence |
| `CAP-002 — Memory & Knowledge Governance` | `Retain Incubating / Provisional` | Phase 8 does not create new Knowledge promotion/reuse responsibility | stable supported contract and operational/external evidence appropriate to scope |
| `CAP-003 — Search / Index Projection` | `Retain Incubating / Provisional` | no Phase 8 evidence selects durable shared search/index topology or stable query interface | stable discovery contract, operational freshness/support model, topology decision if materially selected |
| `CAP-004 — Audit / Reconstruction Support` | `Retain Incubating / Provisional — stronger external reuse evidence` | Creative Test Agent is a real separately maintained external consumer of exact CAP-004 `1.0.0` reconstruction semantics | supported stable contract, compatibility/migration policy, accountable support, approved capability-level operational readiness and separate decision authority approval |

No capability is promoted to `Active`, deprecated, retired, returned to product scope or replaced.

### 6.2 Shared abstractions and bounded evidence

| Subject | Disposition |
|---|---|
| P8.06 `external_consumer_onboarding.py` | `Contain as internal bounded reference evidence`; not admitted as a Platform Capability |
| Creative Test Agent declaration format | `Remain product-owned / Provisional` |
| P8.09 integration runbook | `Contain as exact bounded external-consumer documentation` |
| P8.07 handover package/receipt schema | `Contain as task-local interoperability proof`; not a stable customer format |
| EIS SOAP/archive/revalidation behavior | `Remain Tender Operator product-owned` |
| generic external-consumer manifest/registry | `Defer / not admitted` |
| public SDK/API | `Defer / not admitted` |
| connector/plugin marketplace/framework | `Defer / not admitted` |
| universal customer handover/import format | `Defer` |
| cross-Organization migration/portability protocol | `Defer`; genuine multi-Organization scope absent |

### 6.3 Product Contracts

Relevant Phase 8 and inherited real-product Product Contracts remain `Provisional 0.1.0`. P8.11 creates no `Stable` transition because stable compatibility, migration/deprecation and support obligations have not been approved or evidenced for an externally supported boundary.

## 7. Security, authority, Event/provenance and portability invariants

P8.11 preserves the following closure invariants:

1. Organization scope remains explicit and deny-by-default; no cross-Organization right is inferred from identity, contract, source or receipt.
2. Authentication, Authorization, Organizational Authority and Data Governance remain distinct.
3. Consequential canonical mutation remains Governed Execution scope.
4. historical Event replay/reconstruction creates no new external effect without fresh authorization.
5. canonical Events remain append-only; telemetry remains non-canonical by default.
6. external authority remains external; no competing Arvectum OS source of truth is introduced.
7. generated/exported evidence grants no access, credentials or Organizational Authority.
8. non-exportable secrets remain omitted/reprovisioned rather than embedded in portability evidence.
9. Product Contract presence and onboarding receipts remain evidence, not permission or authority.
10. P8.08 realistic two-Organization isolation remains explicitly unproven until its re-entry trigger is satisfied.

## 8. Executable hardening guard

P8.11 adds:

- `reference/python/tests/test_p8_11_ecosystem_architecture_hardening.py`.

The guard fails if later unguided edits silently:

- promote CAP-001 through CAP-004 away from the current `Incubating / Provisional` baseline;
- make the bounded external onboarding helper look like a public platform contract/registry/lifecycle authority;
- turn the P8.07 task-local package into claimed customer-transfer activation;
- erase P8.08's `NOT ACTIVATED / NOT PROVEN` limitation;
- introduce an ADR file without updating the P8.11 governed disposition;
- reintroduce a root README current-action pointer that competes with the canonical roadmap;
- skip the mandatory R28 code-health gate in P8.11 sequencing.

The guard is not intended to prohibit future governed change. A later valid lifecycle/ADR/public-surface decision must update the canonical decision record and this guard together.

## 9. Functional cross-review

Functional cross-review completed in five iterations of the maximum seven.

### Iteration 1 — architecture / generalization

Result: `REVISE`.

Material objection: the generic-looking P8.06 onboarding helper could be mistaken for evidence that a shared external-integration capability should now be admitted.

Revision: applied R27's evidence threshold explicitly. One real external consumer validates reuse of existing Product Contract/dependency/CAP-004 semantics, but does not validate a new onboarding capability, manifest, registry or public SDK/API.

Disposition: `resolved`.

### Iteration 2 — lifecycle / authority

Result: `REVISE`.

Material objection: CAP-004 now has external reuse evidence, so an `Active` promotion might appear tempting.

Revision: separated stronger reuse evidence from RFC-0001 `Active` requirements. CAP-004 still lacks a supported stable contract, general compatibility/migration policy, accountable external support and approved capability-level operational readiness. No owner-approved lifecycle transition exists.

Disposition: `resolved`.

### Iteration 3 — ADR / refactoring proportionality

Result: `PASS`.

Checks:

- no concrete durable cross-cutting technology or stable public surface has become materially relied upon;
- current implementation remains replaceable and bounded;
- no runtime refactor is justified merely to make code look more generic;
- explicit future ADR triggers remain visible.

No material objection remains.

### Iteration 4 — repository navigation / closure integrity

Result: `REVISE`.

Material objection: root README planning content had drifted two phases behind canonical roadmap state and could misdirect contributors even though it had lower authority.

Revision: refactor README to a non-competing navigation/current-phase summary and keep exact action sequencing solely in the canonical roadmap.

Disposition: `provisionally resolved`, subject to full regression CI.

### Iteration 5 — CI regression continuity + sequencing

Result: `REVISE → PASS`.

CI run `Reference Python CI #204` exposed two regressions in the first P8.11 branch state:

1. README refactoring removed an exact Phase 3/M3 historical closure marker protected by the existing P3.12 regression suite;
2. the new onboarding guard compared raw docstring whitespace and failed on a physical line break.

Independent sequencing recheck also found that the first draft incorrectly named P8.12 as the immediate successor and skipped the canonical R28 gate.

Revisions:

- restored the stable Phase 3/M3 and Phase 4/Product Contract continuity markers in README without restoring a mutable current-action pointer;
- normalized docstring whitespace in the P8.11 semantic guard;
- corrected the next canonical action to R28 and retained P8.12 only after R28 passes;
- required final green CI after these corrections and roadmap synchronization before canonical P8.11 closure.

Disposition: `resolved subject to final green CI`.

Functional cross-review is not formal RFC/ADR acceptance, lifecycle promotion, operational-readiness approval, conformance certification or commercial authority.

## 10. Result and non-claims

`P8.11 = Complete / PASS` means, once final branch CI is green and the synchronized roadmap state is merged:

- complete Phase 8 architecture/evidence set was reviewed;
- minimum governance level was reassessed;
- no ADR threshold is currently crossed;
- no material runtime refactor/generalization is justified;
- repository navigation drift is hardened without creating a competing roadmap;
- historical milestone continuity remains regression-protected;
- every affected capability/shared abstraction has an explicit retain/contain/defer/product-owned disposition;
- security/privacy/isolation/authority/Event/provenance/Governed Execution/portability boundaries remain intact;
- executable guards protect the current bounded decision and sequencing.

It does **not** mean:

- any capability is `Active`;
- any Product Contract is `Stable`;
- a public SDK/API/manifest/registry/export format exists;
- realistic multi-Organization isolation is proven;
- customer handover or cross-Organization transfer is activated;
- external/customer Production is approved;
- SLA/support/certification/full-platform conformance is established;
- Phase 8/M8 is closed before R28 and P8.12 complete their own gates.

## 11. Next canonical action

After P8.11 branch CI succeeds, the change is merged and both canonical roadmaps are synchronized, proceed to:

> **`R28 — M8 Ecosystem Hardening + Milestone Code Health Gate`.**

R28 must run the full architecture/code-health regression and confirm that Phase 8 hardening did not create hidden lifecycle, product/platform, security, portability or compatibility drift.

**P8.12 remains after R28** and may start only if R28 passes. P8.12 then decides Phase 8 / M8 closure from accumulated evidence and explicit non-claims; it must not manufacture missing two-Organization, customer-handover, Stable/Active, Production, support or compatibility evidence.