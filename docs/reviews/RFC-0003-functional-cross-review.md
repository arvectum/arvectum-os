# RFC-0003 Functional Role Cross-Review

Status: `Complete`
Reviewed proposal: `RFC-0003 v0.1.0`
Resulting proposal: `RFC-0003 v0.2.0`
Date: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Normative status: `Informative review evidence`

## 1. Purpose

This document records the functional role-based cross-review performed on the first complete working version of RFC-0003, `Identity, Security, Privacy, Tenant Sovereignty and Portability`.

The review is not an approval and does not give RFC-0003 normative force. Its purpose is to expose conflicts, missing operational constraints, hidden authority assumptions, implementation traps and commercial risks before owner decision.

The review baseline was:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0002 `1.0.0` — `Accepted`;
- Architecture Glossary `1.1.0` — informative;
- Canonical Roadmap `1.0.7` — planning source.

No Accepted ADR was found that narrows RFC-0003 scope.

## 2. Review Method

The working draft was reviewed from eight functional perspectives:

1. CEO / strategy and commercial integrity;
2. COO / operations and incident handling;
3. CTO / architecture and implementation independence;
4. CISO / security engineering;
5. Privacy / data governance and minimization;
6. Legal / rights and contractual boundaries;
7. Product / product-platform boundary;
8. Engineering / migration, enforceability and testability.

Each role assessed:

- constitutional and Accepted-RFC consistency;
- operational usefulness;
- hidden cross-cutting commitments;
- risk of overengineering;
- risk of authority ambiguity;
- testability;
- migration safety;
- commercial claim exposure.

## 3. CEO / Strategy Review

### Findings

The draft correctly treated security and portability as strategic trust foundations, but it risked allowing readers to interpret platform administration as a blanket customer-data access right. That would create commercial and governance risk.

The portability section also needed a sharper distinction between organizational continuity and a promise that every external credential or provider-bound key can be exported.

### Required changes

- explicitly separate infrastructure administration from entitlement to inspect organization content;
- state that portability preserves organizational meaning and replacement paths, not necessarily secret material;
- prevent the RFC from being presented as a compliance certification or universal enterprise IAM package.

### Resolution

Applied in RFC-0003 `0.2.0` Sections 13, 19, 20, 25 and 31.

## 4. COO / Operations Review

### Findings

The initial draft lacked enough treatment of support incidents, emergency access, asynchronous jobs and degraded identity/policy dependencies.

Operationally, these are common paths where architecture is bypassed accidentally.

### Required changes

- add governed break-glass semantics;
- preserve actual operator identity in support/impersonation flows;
- require explicit tenant and actor context for background jobs;
- define fail-closed behavior when tenant resolution or policy evaluation is unavailable;
- permit manual early-stage portability only when documented and tested.

### Resolution

Applied in Sections 8.4, 13, 14.4, 20.6 and 24.

## 5. CTO / Architecture Review

### Findings

The initial draft needed stronger semantic separation between identity, authentication, authorization, organizational authority and privacy/data-governance decisions.

Without this separation, an implementation could accidentally encode roles into identities or treat an authenticated session as organizational authority.

The tenant model also needed to avoid locking the architecture into one-tenant-per-organization or one-database-per-tenant assumptions.

### Required changes

- establish a five-layer security/authority model;
- define Organization as sovereignty boundary and Tenant as technical isolation context;
- allow multiple technical tenant partitions per Organization;
- reject mandatory per-tenant physical database topology;
- keep policy administration/decision/enforcement/information conceptually distinguishable without requiring separate services;
- preserve modular-monolith viability.

### Resolution

Applied in Sections 6, 7, 11.6, 26 and 34.

## 6. CISO / Security Engineering Review

### Findings

The first draft needed stronger failure-mode and lateral-leakage protection around caches, indexes, background workers, service accounts, AI context and shared credentials.

It also needed explicit handling of privileged access and secret material.

### Required changes

- deny by default and fail closed when scope is unresolved;
- require attributable machine identities for significant automated action;
- reject shared anonymous technical accounts where attribution would be lost;
- require bounded sessions/tokens and prohibit secret logging;
- state that relationship existence does not grant permission;
- add cross-tenant cache/index isolation tests;
- require break-glass attribution and expiry;
- require pre-retrieval authorization before model context assembly.

### Resolution

Applied in Sections 8.3, 10, 11, 13, 14, 23, 24 and fitness tests FT-04 through FT-07, FT-09, FT-14 and FT-15.

## 7. Privacy / Data Governance Review

### Findings

The draft handled source records well but under-specified derived data such as embeddings, indexes, summaries and model outputs. It also risked making auditability an excuse for copying sensitive content into logs.

Deletion semantics needed to distinguish immutable historical references from retained payload and to address downstream representations.

### Required changes

- propagate classification, purpose, retention and deletion constraints to derived data;
- prefer governed references over unnecessary duplication;
- minimize audit payload;
- permit lawful tombstone/lineage evidence after content deletion when allowed;
- require deletion workflows to account for replicas, caches, indexes, embeddings and derived artifacts;
- distinguish local replica deletion from external-authority deletion.

### Resolution

Applied in Sections 16, 17 and 18 and fitness tests FT-10 and FT-11.

## 8. Legal / Rights Review

### Findings

The initial draft needed a stronger statement that technical access, authentication or tenancy does not create legal or contractual rights. Cross-organization sharing also needed an explicit governed basis.

Portability needed to preserve restrictions rather than imply unrestricted transfer.

### Required changes

- make export an authorized disclosure subject to rights, classification and contractual limits;
- require explicit cross-organization purpose, rights basis, retention and accountable authority;
- ensure shared-platform learning does not arise automatically from customer operations;
- distinguish legal/contractual deletion obligations from technical local deletion;
- prevent non-exportable secrets from becoming a false portability failure or unsafe export promise.

### Resolution

Applied in Sections 15, 17.4, 19.4 and 20.4-20.5.

## 9. Product Review

### Findings

The first draft risked allowing common authorization vocabulary to expand into a universal platform role catalog. That would violate the product/platform boundary and create speculative generality.

The Product Contract model also must remain RFC-0004 scope.

### Required changes

- keep product-specific roles, entitlements and business approval rules product-owned by default;
- define only the shared authorization architecture here;
- prohibit direct platform-state bypass while deferring exact Product Contract declarations to RFC-0004;
- preserve the rule that a product relationship or role is not automatically a platform permission.

### Resolution

Applied in Sections 11.4, 22 and 33.

## 10. Engineering Review

### Findings

The initial draft was architecturally sound but needed a clearer migration path from existing product-local users, roles, service credentials and tenant assumptions.

A big-bang IAM migration would be disproportionate and could slow product delivery.

### Required changes

- inventory legacy identities, aliases, implicit permissions, services, secrets and cross-organization flows;
- support staged migration;
- preserve legacy identifiers as external aliases where useful;
- require explicit resolution of ambiguous identity merges;
- permit compatibility layers when they preserve security and migration safety;
- add objective conformance tests rather than relying on prose.

### Resolution

Applied in Sections 27-29.

## 11. Cross-Role Conflicts and Resolution

### 11.1 Strong isolation vs operational support

CISO/Privacy favored strict default isolation; COO required practical emergency support.

Resolution: ordinary administrative capability does not grant content access; support access uses explicit governed support/impersonation flows or time-bounded break-glass with attribution and review.

### 11.2 Portability vs secret security

CEO/Legal required credible portability; CISO rejected unsafe export of private keys and provider-bound credentials.

Resolution: portability preserves organizational semantics, dependency manifests and replacement/re-binding paths; it does not require export of prohibited secret material.

### 11.3 Auditability vs minimization

CISO/COO required reconstructability; Privacy required reduced sensitive duplication.

Resolution: preserve identities, references, policy/version context, operation and outcome by default; retain full payload only where necessary and permitted.

### 11.4 Shared authorization vs product autonomy

CTO sought coherent shared enforcement; Product rejected a universal role model.

Resolution: shared platform architecture defines decision/enforcement semantics and invariants; product-specific entitlements remain product-owned until justified for promotion.

### 11.5 Strong governance vs delivery speed

Security roles favored explicit controls; Engineering rejected mandatory enterprise infrastructure before first implementation.

Resolution: semantic invariants are mandatory; physical mechanisms remain proportionate and technology-independent, and a modular monolith/manual early-stage process may conform within a declared scope.

## 12. Material Changes from 0.1.0 to 0.2.0

The resulting proposal incorporates the following material changes:

1. explicit five-layer separation of identity, authentication, authorization, organizational authority and data governance;
2. Organization/tenant mapping semantics without a one-database-per-tenant requirement;
3. actual-actor preservation for impersonation/support operations;
4. privileged administration separated from unrestricted content access;
5. governed break-glass model;
6. explicit asynchronous/background tenant scoping;
7. derived-data classification and deletion propagation;
8. AI pre-retrieval authorization requirement;
9. non-exportable secret/key portability boundary and dependency manifest;
10. staged migration from legacy/product-local IAM;
11. explicit fail-closed behavior for unresolved scope and unavailable security decisions;
12. version-aware evidence limited to consequential authorization contexts;
13. product-specific entitlements kept outside shared platform semantics by default;
14. fifteen normative fitness tests covering identity, authority, isolation, deletion, portability and AI retrieval.

## 13. Final Review Assessment

### Constitution alignment

No conflict found with Constitution `1.2.0`.

### Accepted RFC alignment

No conflict found with RFC-0001 `1.0.0` or RFC-0002 `1.0.0`.

The proposal refines explicitly deferred identity administration, authentication, authorization, isolation, sovereignty and portability architecture without redefining the RFC-0002 Kernel metamodel.

### Scope discipline

The reviewed proposal avoids prematurely defining:

- Product Contract details;
- Governed Execution state machines;
- complete event/provenance architecture;
- memory/knowledge lifecycle;
- specific IAM/crypto/storage technologies;
- jurisdiction-specific compliance mappings.

### Review result

`RFC-0003 v0.2.0` is suitable to remain `Proposed` and be presented for owner decision.

This review is not owner approval and must not be cited as acceptance evidence.
