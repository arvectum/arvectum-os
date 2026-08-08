# P4.08 Bounded Product Entry Product Contract

Status: `Provisional`
Version: `0.1.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Roadmap work item: `P4.08 — Cross-capability task/context composition + bounded product entry point`
Authority: RFC-0004 `1.0.0` — `Accepted`

## 1. Purpose

This Product Contract defines the first bounded Product Contract-backed product entry into the shared Phase 4 Arvectum OS workspace.

The bounded reference product exists only to prove that product-owned task semantics can compose shared platform operator surfaces without private platform coupling and without moving product workflow/business meaning into the platform.

This contract is `Provisional`. It is not a Stable Product Contract, public API/SDK, production support commitment, capability activation decision, SLA or commercial promise.

## 2. Product and contract identity

Executable reference identity is Organization-scoped and created by `reference/python/bounded_product_ref/contract.py`:

- Product: `product/bounded-review-product@<organization>`;
- Product version: `0.1.0`;
- Product Contract subject: `product-contract-subject/p4-08-bounded-review-product@<organization>`;
- Product Contract version: `product-contract-version/p4-08-bounded-review-product-v0.1.0@<organization>`;
- Product Contract lifecycle: `Provisional`;
- Product-owned task type: `product.bounded-review-task`;
- product task authority scope: `product.bounded-review-task/state`.

The concrete Organization value is supplied by the attributable current Actor context. No ambient/default Organization is permitted.

## 3. Declared dependencies and operations

| Dependency | Status / contract | Operation token | Boundary effect |
| --- | --- | --- | --- |
| `CAP-001 — Document & Artifact Governance` | `Incubating`, Provisional `1.0.0` | `p3.08.resolve-document` | bounded governed Document/Artifact context/read |
| `CAP-002 — Memory & Knowledge Governance` | `Incubating`, Provisional `1.0.0` | `p3.08.retrieve-knowledge` | bounded governed Knowledge context/retrieval |
| Governed Runtime reference contract | bounded internal P2 contract | `p4.08.record-task-decision` | product-owned task-state canonical mutation through Governed Execution |

The operation tokens are internal executable evidence only. They are not stable protocol methods, route names, SDK symbols or compatibility commitments.

P4.08 intentionally composes only the minimum two shared capability surfaces needed for the proof. CAP-003 and CAP-004 remain available through their existing contracts but are not pulled into this product entry without demonstrated need.

## 4. Canonical access declarations

The executable contract declares only the following bounded canonical access:

- `platform.document` / `platform.document/state` — `Read`;
- `platform.knowledge` / `platform.knowledge/state` — `Read`;
- `product.bounded-review-task` / `product.bounded-review-task/state` — `Read` + `Write` for the product-owned task state only.

No contract declaration grants access by itself. Actual current Organization/Actor authorization, purpose, rights, classification, data-governance and applicable authority/approval gates remain independently enforced.

The shared workspace remains presentation state. It does not become a canonical owner of product task state or platform governed sources.

## 5. Product-owned semantics

The product owns:

- product task identity and title;
- task-specific composition intent;
- product disposition values such as `Needs review`, `Ready to proceed` and `Declined`;
- product decision notes;
- any later product-specific workflow/business rules.

These semantics live under `reference/python/bounded_product_ref/`, outside `arvectum_os_ref`.

The shared platform owns only the existing domain-neutral semantics for Organization/Actor workspace scope, Product Contract validation, CAP-001/CAP-002 behavior, canonical/version/provenance semantics, Governed Execution and R10 operator safety.

The platform package MUST NOT import the bounded product package. Product success MUST NOT promote these task/disposition semantics into a Platform Capability or shared platform contract.

## 6. Workspace entry and context composition

A product task may enter the shared workspace only after:

1. Actor and Product Contract share the explicit Organization scope;
2. Product identity/version exactly match the Product Contract;
3. the exact Product Contract lifecycle is `Provisional`;
4. at least two distinct shared capability dependencies and operations are declared and validated;
5. each capability request carries the current Actor/Organization `AccessRequest` context.

Successful Product Contract validation then opens `WorkspaceProductContext` with the exact Product Contract Version Identity.

That context grants no authorization, Organizational Authority, approval or source visibility. P4.06/P4.07 independently enforce their current source/access/handling rules before protected content is presented or relied upon.

## 7. Exact version, authority and provenance

The composition MUST preserve the distinctions already owned by the shared surfaces:

- logical Subject versus exact immutable Version;
- canonical versus working/transient/derived state;
- authority mode and authority scope;
- source/provenance attribution;
- Knowledge freshness and exact-version reliance requirements;
- Document Version and Artifact identity where exact reliance occurs.

The exact Product Contract Version Identity is carried in the shared product-entry context and returned to product-owned decision context.

A product decision based on the composed view is transient product-owned state by default. It does not become canonical, approved or authoritative merely because it was produced from governed context.

## 8. Security, authority and handling

Read-side capability operations preserve separate `Authorization` and `DataGovernance` boundaries.

The product task-state mutation operation requires, independently:

- `Authorization`;
- `OrganizationalAuthority`;
- `DataGovernance`;
- `ConsequentialApproval`.

Product Contract possession or successful entry satisfies none of those gates.

Current source authorization and purpose/right/classification handling remain owned by the existing source/capability boundaries. Cross-Organization access is denied by default. Protected counts, previews or hidden source metadata must not be reconstructed product-side when a shared surface omits them.

No IAM/PDP/PEP provider, policy language or entitlement store is selected by this contract.

## 9. Consequential operator action boundary

A consequential product operator action MUST NOT call the lower-level P4.05 action adapter directly.

The product boundary composes action preparation and execution only through R10 `operator_safety.py`:

- action preparation pins the exact source-authorization decision used by the inspected view;
- preparation fails if that decision is no longer the unique current allow decision;
- execution rechecks the same condition immediately before delegation to the existing P4.05/runtime path;
- replacement, revocation, absence or ambiguity requires re-inspection;
- the R10 guard grants no permission or Organizational Authority and creates no second canonical-mutation path.

The governed product interaction separately pins this exact Product Contract version through the existing RFC-0005 Product Contract runtime boundary.

## 10. Hidden coupling prohibition

The bounded product MUST NOT depend on:

- platform internal tables or direct storage access;
- undocumented internal imports as product/platform contracts;
- private Event streams;
- private search/vector indexes;
- hidden prompts or model context;
- implicit shared state;
- direct calls to lower-level consequential mutation helpers that bypass R10;
- incidental frontend routes or component internals.

The Python reference imports are executable proof inside one repository, not a Stable/public SDK boundary. Phase 5 remains responsible for repeatable extension/integration experience.

## 11. Failure behavior

The product boundary fails closed on:

- absent/non-`Provisional` Product Contract;
- product identity/version mismatch;
- Organization or Actor drift;
- undeclared or incompatible capability dependency/version/operation;
- fewer than two distinct shared capabilities at product entry;
- current source authorization failure or ambiguity at the underlying workspace surface;
- handling/purpose/right/classification failure;
- stale/replaced/revoked/missing/ambiguous source access before consequential operator action;
- unresolved or denied Governed Execution gates;
- undeclared product task-state canonical access.

Failure MUST NOT fall back to a private platform path.

## 12. Portability, retention and minimization

The product preserves governed identities and exact references needed for its declared task context but SHOULD avoid copying protected governed payload when source references or minimized presentation are sufficient.

Source retention/deletion/classification constraints remain applicable. Product context does not create a new retention right.

No database, object store, search technology, frontend framework, BFF/API topology, serialization format, broker, workflow engine, IAM provider or separately deployable service boundary is selected.

## 13. Review and exit path

Review condition: `R11 — Composition / Usability Refactoring Review` or earlier on material Product Contract, capability, security, authority or composition change.

Exit paths:

- issue a new immutable `Provisional` Product Contract version;
- contain or retire the bounded reference product;
- stabilize only through a separate RFC-0004 lifecycle decision with required compatibility, migration, support and conformance evidence.

This contract does not promote CAP-001 or CAP-002. Both remain `Incubating / Provisional`.

## 14. ADR gate assessment

No ADR threshold is crossed by this bounded contract because it selects no durable or externally constraining frontend/API/service/storage/IAM/search/runtime technology.

Material reliance on such a choice reopens the ADR gate before the dependency is normalized.
