# P5.09 — Second Materially Distinct Integration Reuse Proof

Status: `Complete`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` (secondary evidence: `platform`)
Result: `PASS`

## 1. Purpose

P5.09 proves that the Phase 5 integration boundary is reusable by a second bounded integration that is materially different from the P4.08/P5.08 bounded product, rather than validating the abstraction only against the integration that motivated it.

The selected second integration is the P5.01 J3 candidate: a **read-only evidence/reconstruction extension**. It consumes CAP-004 Audit / Reconstruction Support through its own exact Provisional Product Contract and the same P5.08 `IntegrationAdapters` seam used by the first bounded product journey.

P5.09 does not create a public/stable SDK/API/package boundary, extension marketplace/runtime, registry, new Event store, canonical-state owner, permission source, Organizational Authority source, capability lifecycle transition, Product Contract stabilization, operational-readiness claim or production conformance claim.

## 2. Canonical basis checked

The implementation and review were checked against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
3. RFC-0001 — explicit product/platform contracts, validated reuse, capability lifecycle separation and no automatic promotion from successful reuse;
4. RFC-0003 — Organization sovereignty, deny-by-default access, purpose/right/data-governance continuity and separation of Authentication, Authorization and Organizational Authority;
5. RFC-0004 — explicit versioned Product Contract boundary, Provisional lifecycle, extension/product separation and prohibition of hidden coupling through internal tables/imports/endpoints/private streams/implicit shared state;
6. RFC-0006 — Event/provenance/reconstruction semantics, reconstruction as derived observational evidence rather than replay or authority;
7. P5.01 — J3 read-only evidence/reconstruction extension candidate retained specifically as a materially distinct future reuse candidate;
8. P5.02/P5.03/P5.04/R14 — declaration validation, exact dependency/version resolution, composition facade and current provider-evidence continuity;
9. P5.08 — internal/provisional workspace/capability adapter seam without product-side private coupling.

The ADR index contains no Accepted ADR selecting a conflicting Stable/public integration, package, transport, registry or extension-runtime boundary for this scope.

No conflict with Constitution or Accepted RFC/ADR was identified.

## 3. Why the second integration is materially distinct

The first P4.08/P5.08 bounded product and the P5.09 extension differ in the dimensions that matter to reuse evidence:

| Dimension | First bounded product | P5.09 second integration |
|---|---|---|
| Consumer identity | `product` | `extension` |
| Primary shape | product workflow/composition | read-only evidence inspection |
| Shared dependencies | CAP-001 + CAP-002 + governed runtime | CAP-004 only |
| Consequential mutation | present in declared product operation set | absent |
| Workspace composition | used | not used |
| Product task/disposition state | product-owned | absent |
| Reconstruction/evidence semantics | not the defining integration concern | defining concern |
| Direct canonical access declaration | present where product operations rely directly on canonical source state | absent because CAP-004 exposes a derived reconstruction view |

This is therefore not the same product with renamed identifiers, reordered calls or copied implementation logic.

## 4. Second Product Contract

`reference/python/evidence_extension_ref/contract.py` defines the bounded extension-owned Provisional Product Contract evidence.

The contract:

- uses a distinct Organization-scoped extension identity;
- remains `Provisional 0.1.0`;
- declares exactly one dependency: CAP-004 at the existing exact contract baseline;
- declares only `reconstruct-execution` as an allowed read-only operation;
- requires Authorization and Data Governance gates at the declared operation boundary;
- creates no canonical mutation declaration;
- creates no direct canonical-read declaration because the consumed CAP-004 result is a derived reconstruction view rather than a new direct canonical source-access surface;
- explicitly requires fail-closed behavior with no private Event/log/trace/database fallback, replay, hidden evidence disclosure or cross-Organization access;
- records bounded compatibility, portability, retention/deletion, review and exit responsibilities.

The contract itself grants no permission, approval, Organizational Authority or capability activation.

## 5. Same reusable integration boundary

`reference/python/evidence_extension_ref/reconstruction_journey.py` is the second integration's consumer-owned journey.

Its only Arvectum OS import is:

`arvectum_os_ref.integration_adapters`

The first P5.08 bounded product journey and this extension journey therefore consume the **same declared integration-facing adapter module**.

The extension does not import CAP-004 implementation modules, Event/provenance internals, cross-capability enforcement internals, canonical-state modules, governed-execution internals or workspace implementation modules. The reconstruction object remains platform-owned and is passed through the extension boundary opaquely rather than copied into a parallel extension data model.

## 6. Reuse path and semantic ownership

The second integration follows the same governed integration sequence:

`Product Contract → P5.02 declaration validation → P5.03 exact dependency/version resolution → P5.04 composition facade → P5.08 IntegrationAdapters → CAP-004 semantic owner`

Current governed provider/version evidence remains required at dependency-backed consumption time under the R14 rule. The extension cannot rely on stale composition-time compatibility evidence or smuggle an undeclared dependency through the adapter.

Capability-specific Organization/purpose/right/classification handling and reconstruction redaction remain owned by the existing CAP-004/P3.07 semantic owners. The adapter and extension do not recreate those rules.

## 7. Material reuse finding P5.09-F1 — P5.02 read-only overfit

The second consumer exposed one material abstraction defect in the P5.02 internal/provisional validator.

### Finding

The original P5.02 implementation required every `READ_ONLY` Product Contract operation to declare direct canonical `Read` access. That assumption fit the first J1/J2 product contract but overfit it: CAP-004 reconstruction is a **derived read-only governed view**, and consuming that view does not itself create a second direct canonical-state access surface for the extension.

Forcing a fake canonical-read declaration into the J3 contract would have made the declaration less truthful and would have confused derived reconstruction access with source canonical authority.

### Remediation

The internal P5.02 validator was narrowed to the actual semantic invariant:

- Authorization + Data Governance gates remain required for the bounded declared operations;
- when a read-only operation declares direct canonical accesses, at least one declared access must include `Read`;
- an operation that exposes only a derived governed view may declare no direct canonical access;
- canonical mutation still requires Organizational Authority and an explicit canonical `Write` declaration;
- declared canonical access still preserves authoritative source, authority scope and failure semantics;
- empty canonical-access declarations grant no source access and cannot bypass the capability's runtime access checks.

Regression coverage proves both the new derived-read case and the retained fail-closed direct-read/mutation cases.

This is an implementation-level correction to an internal/provisional validation assumption. It does not amend RFC-0004, create a new Product Contract semantic owner or weaken the canonical/security boundary.

## 8. Security, rights and provenance evidence

Focused P5.09 tests prove that:

1. the second contract is materially distinct from the first product contract;
2. both consumers use the same `IntegrationAdapters` module;
3. the extension consumer has no workspace/Event-store/capability-private import path;
4. the exact extension Product Contract Version remains present in the composed facade context;
5. reconstruction succeeds only through declared CAP-004 reliance with current provider/version evidence;
6. a right mismatch produces explicit redaction/incomplete reconstruction rather than private fallback;
7. cross-Organization reconstruction fails closed;
8. missing current provider/version evidence fails closed;
9. an undeclared dependency fails at the integration-composition continuity boundary;
10. reuse does not promote either Product Contract or capability lifecycle.

Hosted `Reference Python CI #242` passed the full **675-test** reference suite with `OK`, including all focused P5.08 and P5.09 cases and the accumulated architecture-fitness suite.

## 9. Reuse disposition — retain, refine, reject

P5.09 provides enough evidence to make a bounded reuse disposition before R15.

### Retain

- RFC-0004 Product Contract as the semantic boundary owner;
- P5.02 whole-contract validation, with P5.09-F1 refinement;
- P5.03 exact dependency/version resolution from explicit governed evidence;
- P5.04 composition facade and R14 current-provider-evidence rule;
- P5.08 `IntegrationAdapters` as the current internal/provisional integration-facing seam;
- capability-specific semantic ownership below adapters;
- explicit consumer-owned Product/Extension contracts and domain behavior.

### Refine / delete from the abstraction

- delete the universal implementation assumption that `READ_ONLY` always means direct canonical-read declaration;
- keep canonical-access validation conditional on actual direct canonical access instead of consumer shape;
- avoid workspace dependency for headless/read-only integrations that do not need workspace composition.

### Reject premature generalization

P5.09 does not justify:

- public or Stable SDK/package/API compatibility;
- generic extension/plugin loading framework;
- extension registry/discovery topology;
- duplicated CAP-004 reconstruction implementation;
- new Event store/log/trace authority source;
- generic consumer DTO schema copied from current Python objects;
- automatic capability promotion based on a second consumer;
- Stable Product Contract promotion.

These remain later evidence/governance questions.

## 10. Exit evidence

P5.09 roadmap exit criteria:

- both integrations use the same declared integration boundary/tooling — `PASS`;
- no copy/paste of implementation-private platform code is required — `PASS`;
- differences remain consumer-owned where appropriate — `PASS`;
- reuse evidence identifies abstractions worth retaining/deleting — `PASS`, including P5.09-F1 and the disposition above;
- Organization/rights/current-evidence negative paths remain fail-closed — `PASS`;
- no lifecycle/public-boundary overclaim is introduced — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #242`, 675 tests, `OK`).

## 11. ADR / RFC / lifecycle gate

No new RFC or ADR is required for P5.09 because the work remains inside Accepted Product Contract and capability semantics and does not select a new durable public/package/network/registry/runtime mechanism.

P5.09 does not change:

- Constitution `1.2.0`;
- any Accepted RFC status/content;
- CAP-001 through CAP-004 lifecycle (`Incubating / Provisional`);
- first bounded Product Contract lifecycle (`Provisional 0.1.0`);
- second extension Product Contract lifecycle (`Provisional 0.1.0`);
- operational readiness, production environment or conformance maturity.

A second consumer is **reuse evidence**, not an automatic lifecycle transition. Any later promotion must pass the applicable capability admission/readiness/governance criteria separately.

## 12. Result

**PASS.** A materially distinct read-only CAP-004 extension reuses the same Product Contract/composition/adapter boundary as the first bounded product without private coupling or copied platform internals. The second consumer also exposed and remediated one overfitted internal validator assumption, which is precisely the reuse-learning outcome P5.09 was intended to produce.

Next engineering gate:

> **R15 — Reuse / Developer Experience Refactoring Review.**

Next roadmap work item after the R15 gate:

> **P5.10 — Phase 5 conformance + architecture fitness matrix.**
