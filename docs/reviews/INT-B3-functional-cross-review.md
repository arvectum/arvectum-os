# INT-B3 — Functional Cross-Review

Status: `Complete`
Reviewed artifact: [`INT-B3 — 1С First-Candidate Design`](../architecture/INT-B3-1c-erp-first-candidate-design.md) `1.0.0`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Iterations: `3 of maximum 7`
Result: `PASS after bounded reconciliation`

## 1. Review scope

The review tested INT-B3 against Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, INT-B1, INT-B2 and the canonical roadmap.

Review focus:

- whether one sufficiently concrete 1С target was selected without pretending a live customer deployment exists;
- external authority preservation;
- identity and metadata mapping;
- read/write/effect boundary;
- credential and least-privilege design;
- freshness, pagination, incomplete snapshot and reconciliation semantics;
- Product Contract boundary;
- product-owned procurement semantics;
- Event/provenance boundaries;
- failure/termination/portability;
- ADR triggers and avoidance of premature platformization.

Functional review is not RFC/ADR acceptance, Product Contract stabilization, capability promotion, security certification or operational-readiness approval.

## 2. Iteration 1 — target concreteness and authority review

### Findings

1. Selecting only “1С” would be too broad and would violate the roadmap requirement for a concrete first candidate.
2. Selecting `1С:ERP 2` without a bounded deployment/interface profile would still leave transport and compatibility assumptions ambiguous.
3. A local normalized representation could accidentally be described as authoritative rather than derived from 1С.
4. A reference design could be mistaken for proof of a discovered/live customer installation.

### Reconciliation

The artifact now fixes:

- one configuration family: `1С:ERP Управление предприятием 2`, standard `2.5` family;
- one reference deployment profile: self-hosted/client-server with published standard OData;
- one bounded outcome: read-only procurement attention projection;
- 1С as the external authoritative source;
- `External Reference` as the first Arvectum OS authority mode;
- explicit language that no actual customer deployment has yet been discovered/tested/certified and that exact platform/configuration/authentication/metadata must be pinned before reliance.

Result: material objections closed.

## 3. Iteration 2 — integration semantics and security review

### Findings

1. OData technically supports writes, so an implementation might accidentally expose mutation merely because the transport allows it.
2. External 1С object identifiers could be reused incorrectly as Arvectum identities.
3. A dedicated integration account might still be overprivileged or its secret copied into canonical state/configuration history.
4. Assuming a universal `modified_at` field/change feed would overfit unknown 1С metadata and create unsafe incremental-sync semantics.
5. A partial/paginated retrieval could be mistaken for a complete authoritative population.

### Reconciliation

The artifact now:

- enumerates only `metadata.discover`, `procurement_orders.list`, `procurement_orders.get` and `counterparties.get` as first operations;
- explicitly prohibits create/update/post/cancel/receipt/payment and arbitrary generic execution operations;
- treats external IDs as governed aliases/references rather than Arvectum Subject Identities;
- requires a dedicated least-privilege read-only 1С principal with indirect secret reference;
- avoids assuming universal CDC/change-marker support and requires discovery-backed incremental, bounded polling or bounded full reconciliation;
- requires explicit incomplete/pagination/freshness state and forbids presenting partial retrieval as complete current source state.

Result: material objections closed.

## 4. Iteration 3 — product/platform, proportionality and lifecycle review

### Findings

1. Procurement concepts could leak into the domain-neutral INT-B2 connector envelope.
2. Workspace “needs attention” semantics could accidentally be attributed to 1С rather than to Arvectum/product logic.
3. The design could prematurely force OData as the universal Arvectum connector protocol.
4. Requiring a Product Contract at design-document creation time would over-govern an architecture artifact that has no runtime reliance yet.
5. Terminating the connector could be confused with deleting external 1С state or historical evidence.

### Reconciliation

The artifact explicitly:

- keeps procurement interpretation, supplier risk, approval thresholds and attention criteria product-owned;
- separates authoritative 1С state from Arvectum-native attention/workflow state and AI/product interpretation;
- makes OData a concrete adapter decision only, not a universal connector protocol;
- requires the Product Contract before governed product/shared-platform reliance, not merely for existence of the design baseline;
- defines connector termination as stopping retrieval/revoking credentials/removing local caches while preserving lawful historical attribution and leaving authoritative 1С state untouched.

Result: no remaining material objection.

## 5. External feasibility evidence review

Official 1С sources were checked for the specific feasibility assumptions used by INT-B3:

- `1С:ERP Управление предприятием` has a procurement-management domain with supplier orders and execution control;
- the 1С platform can publish the standard OData REST interface and expose metadata/application objects;
- custom HTTP services remain an available future system-specific option.

The review does not elevate vendor documentation into Arvectum OS normative authority. It is external implementation evidence only.

## 6. Higher-authority compatibility

- **Constitution 1.2.0:** compatible; external authority, domain boundaries, security and proportionality preserved.
- **RFC-0001:** compatible; no competing source of truth and no speculative platform capability admitted.
- **RFC-0002:** compatible; external identifiers remain aliases/references and physical schema is not prescribed.
- **RFC-0003:** compatible; dedicated principal, least privilege, secret minimization, Organization scope and separation of authentication/authorization/Organizational Authority/Data Governance preserved.
- **RFC-0004:** compatible; Product Contract required before governed product/platform reliance and no hidden coupling allowed.
- **RFC-0005:** compatible; no consequential external effect is admitted; future writes would require Governed Execution and explicit operation semantics.
- **RFC-0006:** compatible; OData responses/polling receipts are not automatically canonical Events and telemetry remains non-canonical by default.
- **RFC-0007 / RFC-0008:** no automatic promotion to Knowledge/Memory or document-authority semantics introduced.

No Accepted ADR conflict was found. No new ADR is required for the design baseline because no cross-product runtime/topology is selected.

## 7. Final result

**PASS after bounded reconciliation — 3 of maximum 7 iterations.**

INT-B3 is fit to close as `Complete / concrete integration design baseline`.

Closure does not prove a live/customer 1С deployment, create a real connector implementation, authorize any 1С write/effect, stabilize a Product Contract, activate a Platform Capability or establish public compatibility/support commitments.

Next integration-lane action: `INT-B4 — CRM designs`, with Битрикс24 and amoCRM remaining separate concrete designs until reuse evidence exists.
