# P5.08 — Workspace / Capability Integration Adapters Without Private Coupling

Status: `Complete`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Result: `PASS`

## 1. Scope

P5.08 adds the smallest bounded integration-facing adapter seam for workspace navigation and CAP-001 through CAP-004 read-oriented capability consumption above the R14-hardened Phase 5 composition boundary.

The goal is to let product/extension code rely on one explicit integration-facing adapter module instead of importing workspace, capability, canonical-state, search, knowledge or audit implementation modules directly.

P5.08 does **not** create a new semantic owner, Stable/public SDK/API, package contract, route schema, wire/serialization contract, registry, network protocol, deployment topology, IAM/policy engine, capability lifecycle transition or production support commitment.

## 2. Canonical basis checked

The implementation was checked against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC-0001 through RFC-0008 — `Accepted 1.0.0` per the canonical RFC Index;
3. RFC-0003 — Organization sovereignty, deny-by-default boundaries and separation of identity/access/authority concerns;
4. RFC-0004 — Product Contract as the explicit product/platform reliance boundary and prohibition of hidden coupling through private tables/imports/endpoints/streams/shared state;
5. P3.08 — existing bounded Product Contract capability-consumption semantic owner;
6. P4 workspace shell — non-authoritative workspace presentation and explicit Organization/Actor scope;
7. P5.04/P5.05/P5.06/R14 — governed integration composition, local harness, security continuity and current dependency/version evidence requirements;
8. P5.07 — exact integration attribution/provenance/portability support without creating a competing integration authority source.

No conflict with the checked higher-priority canonical sources was identified in the implemented seam.

The ADR index contains no accepted ADR that establishes a conflicting stable integration/package/transport boundary for this scope.

## 3. Implementation disposition

`reference/python/arvectum_os_ref/integration_adapters.py` is added as an **internal / provisional integration-facing adapter seam**.

`compose_integration_adapters()` always constructs the underlying `IntegrationCompositionFacade` through the existing R14-hardened `compose_integration_facade()` factory. P5.08 therefore cannot create a supported construction path that bypasses P5.02 declaration validation or P5.03 dependency/version compatibility resolution.

The composed result contains:

- `IntegrationWorkspaceAdapter`;
- `IntegrationCapabilityAdapter`;
- the exact underlying `IntegrationCompositionFacade` used by both adapters.

All three preserve one exact Organization, Actor, Product Identity/Product Version and Product Contract Version context.

## 4. Workspace adapter

`IntegrationWorkspaceAdapter` delegates opening and navigation to the existing workspace semantic owner.

It preserves:

- non-authoritative workspace presentation;
- exact Organization and Actor continuity;
- exact Product Identity and Product Contract Version entry context;
- explicit Subject versus exact Version navigation semantics.

P5.08 adds one adapter-level fail-closed guard that the supplied Subject and Version `Identity.scope` must match the composed Organization. This prevents a client from embedding a foreign-Organization identity inside an otherwise Organization-A navigation reference.

The adapter does not resolve a Subject to a current Version, grant access, approve actions or mutate canonical state.

## 5. Capability adapter

`IntegrationCapabilityAdapter` delegates capability behavior to the existing P3.08 capability-consumption and cross-capability semantic owners.

It supports the existing bounded read-oriented operations for:

- CAP-001 Document & Artifact Governance;
- CAP-002 Memory & Knowledge Governance;
- CAP-003 Search / Index Projection;
- CAP-004 Audit / Reconstruction Support.

Every dependency-backed capability reliance first calls `IntegrationCompositionFacade.admit_capability()` with explicit current governed provider/version evidence. The R14 current-evidence requirement therefore remains in force and composition-time compatibility cannot silently self-advance.

The adapter then delegates the actual capability operation to the existing `consume_*` semantic owner. It does not duplicate access, canonical-read, search-source, reconstruction or Product Contract validation rules.

## 6. Product-side private-coupling proof

`reference/python/bounded_product_ref/integration_adapter_journey.py` is added as bounded product-owned evidence.

The product-side helper imports exactly one Arvectum OS module:

`arvectum_os_ref.integration_adapters`

It does not import private workspace/capability implementation modules such as:

- `workspace_shell`;
- `product_capability_consumption`;
- `cross_capability_enforcement`;
- `document_artifact_governance`;
- `memory_knowledge_governance`;
- `search_index_projection`;
- `audit_reconstruction_support`.

Private implementation dependencies remain behind the platform-owned adapter seam and are not promoted into a product compatibility contract.

## 7. Security / authority continuity

P5.08 grants or infers none of the following:

- Authentication;
- Authorization;
- Organizational Authority;
- permission;
- approval;
- capability lifecycle state;
- canonical mutation authority;
- cross-Organization access;
- Product Contract `Stable` lifecycle.

Wrong-Organization workspace identity scope fails closed at the adapter boundary. Capability reliance still requires the existing current access context and current governed provider/version evidence.

## 8. Executable evidence

Focused regression/fitness evidence is committed in:

`reference/python/tests/test_p5_08_workspace_capability_integration_adapters.py`

The test module defines coverage for:

1. exact facade/Product Contract continuity across adapters;
2. non-authoritative workspace entry with exact Product Contract Version;
3. Subject navigation through the adapter;
4. exact Version navigation through the adapter;
5. fail-closed cross-Organization Subject/Version identity scope;
6. capability admission through the existing current compatibility gate;
7. failure when current governed dependency/version evidence is omitted;
8. one integration-facing platform import in product-owned P5.08 code;
9. product journey entry without private workspace/capability imports;
10. absence of authority/lifecycle fields in adapter evidence;
11. internal/provisional and stack-neutral adapter implementation constraints.

Hosted `Reference Python CI #242` executed the full reference suite on the P5.09 PR merge candidate and passed **675 tests** with `OK`. The run includes all focused P5.08 regression cases, so the previously pending hosted-verification condition is now satisfied by observable accumulated evidence.

## 9. ADR / RFC / lifecycle gate

No new RFC or ADR is required by the implemented P5.08 seam because it does not select a new fundamental semantic owner, stable/public compatibility boundary, durable package/runtime model, transport protocol, network/service boundary or infrastructure technology.

P5.08 does not change:

- Constitution `1.2.0`;
- Accepted RFC content/status;
- P4.08 Product Contract lifecycle (`Provisional 0.1.0`);
- CAP-001 through CAP-004 lifecycle (`Incubating / Provisional`);
- operational-readiness or production-conformance claims.

If this adapter seam later becomes a durable externally relied-upon SDK/package/API boundary, the Phase 5 ADR/public-boundary gate must be re-evaluated before stabilization.

## 10. Result

**PASS.** P5.08 is complete for its bounded internal/provisional scope. Hosted full-suite evidence is observable in `Reference Python CI #242` with 675 tests passing.

The next canonical work item is:

> **P5.09 — Second materially distinct integration reuse proof.**
