# RFC-0004 Functional Role Cross-Review

Status: `Complete`
Reviewed proposal sequence: `RFC-0004 v0.1.0 → v0.2.0 → v0.3.0`
Resulting proposal: `RFC-0004 v0.3.0`
Date: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Normative status: `Informative review evidence`
Review iterations used: `3 / 7 maximum`

## 1. Purpose

This document records the iterative functional role-based cross-review of RFC-0004, `Product Contract, Product Experiment and Extension Model`.

The review is not owner approval and does not give RFC-0004 normative force. Its purpose is to test the proposal against the Constitution, Accepted RFCs, product/platform responsibility, commercial integrity, security/privacy constraints, implementation practicality and migration safety before an owner decision.

The review baseline was:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0002 `1.0.0` — `Accepted`;
- RFC-0003 `0.2.0` — `Proposed`, considered only for forward compatibility and not as normative authority;
- Architecture Glossary `1.1.0` — informative;
- Canonical Roadmap `1.0.8` — planning source at review start.

No Accepted ADR was found that narrows RFC-0004 scope.

## 2. Review Method

The project rule requires iterative execution and functional cross-review until further changes are excessive for the current lifecycle stage, with a hard stop after seven review iterations.

The RFC was reviewed from eight functional perspectives:

1. CEO / strategy and commercial integrity;
2. COO / operations and supportability;
3. CTO / architecture and product-platform boundary;
4. CISO / security engineering;
5. Privacy / data governance;
6. Legal / rights and contractual boundaries;
7. Product / experimentation and delivery;
8. Engineering / migration, enforceability and testability.

Each iteration assessed:

- Constitution and Accepted-RFC consistency;
- whether RFC-0004 accidentally creates new Kernel semantics;
- whether Product Contracts remain minimal and proportional;
- whether product-domain logic stays product-owned;
- whether extension registration is confused with authorization;
- whether capability lifecycle is preserved independently;
- whether hidden coupling is testable;
- whether migration is reversible;
- whether commercial claims can outrun actual lifecycle state;
- whether the RFC prematurely defines RFC-0003/0005/0006/0007 scope.

## 3. Iteration 1 — Review of v0.1.0

### 3.1 CEO / Strategy

#### Findings

The first draft made the Product Contract sufficiently explicit but risked allowing a stable Product Contract to be read commercially as proof that every referenced capability was an `Active` supported platform capability.

A second strategic risk was automatic platformization: if a product declared or reused a mechanism, readers could infer that responsibility had moved to Arvectum OS.

#### Required changes

- separate Product Contract lifecycle from Platform Capability lifecycle;
- prohibit a Product Contract from upgrading a capability lifecycle state;
- make promotion to platform incubation a separate governed decision;
- preserve commercial-commitment integrity for provisional/incubating dependencies.

#### Resolution

Applied in RFC-0004 `0.2.0` Sections 6, 9, 10.2, 14 and 22.

### 3.2 COO / Operations

#### Findings

The first draft declared dependencies but did not consistently require failure behavior, support responsibility and termination/handover semantics.

That gap could create products that were contractually explicit at design time but operationally ambiguous during outage, migration or retirement.

#### Required changes

- require dependency failure/unavailability behavior where consequential;
- require support status for stable boundaries;
- add termination/handover responsibilities;
- preserve historical contract versions required to interpret past governed executions.

#### Resolution

Applied in Sections 10.2, 10.9, 21 and 26.

### 3.3 CTO / Architecture

#### Findings

The draft needed stronger protection against the Product Contract becoming a universal product manifest or plugin framework.

It also needed explicit treatment of direct database coupling/internal imports and circular architectural-responsibility dependencies.

#### Required changes

- state that the Product Contract describes only boundary-relevant semantics;
- reject direct database/internal endpoint/internal import coupling that bypasses contracts;
- reject circular product/platform responsibility;
- keep registry/runtime implementation technology-independent;
- preserve product ownership of domain types even when they cross the boundary.

#### Resolution

Applied in Sections 6.3, 10.3, 11, 17 and 25.

### 3.4 CISO / Security Engineering

#### Findings

Extension registration was too easy to confuse with permission to execute or access data.

The first draft also needed stronger failure behavior around extensions and explicit rejection of ambient trust created merely by possession of a Product Contract.

#### Required changes

- state that extension registration grants no access, authority or cross-organization visibility;
- state that a Product Contract is not a credential;
- require least privilege at the boundary;
- require extension failure not to broaden access, cross tenant boundaries or create unrecorded consequential mutation;
- ensure AI extensions gain no ambient organizational authority.

#### Resolution

Applied in Sections 15.3, 15.6 and 19.

### 3.5 Privacy / Data Governance

#### Findings

The draft covered source records but under-specified derived data created by product/platform interaction, such as embeddings, summaries, indexes and caches.

It also needed stronger portability language to avoid treating export as a right to disclose restricted or non-exportable material.

#### Required changes

- propagate organization scope, classification, retention and deletion constraints to derived data;
- prohibit Product Contract participation from creating cross-organization learning rights;
- make portability subject to legal/contractual/technical restrictions;
- preserve data minimization.

#### Resolution

Applied in Sections 10.8, 20 and 21.

### 3.6 Legal / Rights

#### Findings

The first draft needed a clearer distinction between architectural responsibility, technical integration and legal rights.

It also needed to prevent a stable contract from implying unrestricted portability, support or cross-organization reuse commitments.

#### Required changes

- ensure cross-organization reuse remains separately governed;
- ensure contract declaration does not create legal rights;
- constrain customer-facing claims to approved lifecycle/conformance/support scope;
- preserve restrictions during export and handover.

#### Resolution

Applied in Sections 20.4, 21 and 22.

### 3.7 Product

#### Findings

The first draft risked imposing too much ceremony on experiments and could have been interpreted as requiring a Product Contract for every product-local experiment.

It also needed explicit evidence-based review criteria for experiment continuation/promotion/retirement.

#### Required changes

- restate RFC-0001 conditions under which no Product Contract is required;
- require minimal proportional provisional contracts only at the platform boundary;
- add experiment outcome/review criteria;
- preserve product responsibility until promotion.

#### Resolution

Applied in Sections 7 and 13.

### 3.8 Engineering

#### Findings

The first draft lacked a practical staged migration path from legacy direct coupling.

A strict immediate prohibition without compatibility bridges could force disproportionate rewrites before the reference implementation exists.

#### Required changes

- add boundary inventory;
- permit bounded compatibility bridges with owner, review date and exit path;
- prioritize consequential/security-sensitive coupling before low-risk internal reads;
- keep physical contract representation open.

#### Resolution

Applied in Sections 11.2, 24, 25 and 28.

### Iteration 1 result

Material changes were required. RFC-0004 advanced from working `0.1.0` to `0.2.0`.

## 4. Iteration 2 — Review of v0.2.0

### 4.1 CEO / Commercial

No remaining lifecycle conflation was found. One refinement remained: semantic compatibility had to include changes in authority, side effects and approvals even if a wire format remained parse-compatible.

### 4.2 COO / Operations

Operational failure and handover were adequate. One refinement remained: retired contract versions must remain identifiable where required to interpret past executions.

### 4.3 CTO / Architecture

The boundary remained domain-neutral and did not redefine Kernel semantics. One refinement remained: cross-product interaction should explicitly allow records/events/contracts/shared capability while continuing to prohibit internal access.

### 4.4 CISO / Security

No material blocker remained. Registration, authorization and organizational authority were clearly separated.

### 4.5 Privacy

One refinement remained: derived data constraints should explicitly include generated artifacts in addition to indexes, embeddings, summaries and caches.

### 4.6 Legal

No material blocker remained. Portability and cross-organization reuse stayed subject to independent rights and governance.

### 4.7 Product

No material blocker remained. The proposal preserved the ability to run fully product-local experiments without a Product Contract.

### 4.8 Engineering

No material blocker remained. Static/versioned-file validation remained a valid early implementation; no dedicated registry service was forced.

### Iteration 2 required changes

The proposal was refined to:

1. define compatibility as semantic rather than merely syntactic;
2. preserve exact effective Product Contract versions in consequential evidence;
3. make historical retired contract versions resolvable where required;
4. add explicit cross-product interaction mechanisms;
5. extend derived-data constraints to generated artifacts.

These changes produced RFC-0004 `0.3.0`.

## 5. Iteration 3 — Review of v0.3.0

All eight functional perspectives re-reviewed the resulting proposal.

### CEO / Strategy

No further material change. Product Contract status cannot create capability status or unsupported commercial promises.

### COO / Operations

No further material change. Failure, support, migration, retirement and historical interpretability are sufficiently explicit for an architecture RFC.

### CTO / Architecture

No further material change. The RFC defines semantic boundaries without selecting protocol, storage, registry service or plugin runtime and does not redefine RFC-0002 Kernel semantics.

### CISO / Security

No further material change. Contract possession and extension registration create no ambient authorization or authority; least privilege and failure boundaries are preserved.

### Privacy / Data Governance

No further material change. Derived data, cross-organization reuse and portability remain constrained by organization scope, rights, classification, retention and deletion.

### Legal / Rights

No further material change. Architectural contracts do not create legal rights, unrestricted disclosure or unsupported commercial obligations.

### Product

No further material change. Fully product-local experiments remain lightweight, and platform-interacting experiments use minimal proportional provisional contracts.

### Engineering

No further material change. The model is testable through fitness tests and supports staged migration with bounded compatibility bridges.

### Iteration 3 result

No remaining material correction was identified for the current proposal lifecycle stage. Further polishing would be editorial or implementation-level and is therefore excessive before owner decision.

The iterative review cycle stopped after `3` of the maximum `7` review iterations.

## 6. Cross-role Conflicts and Resolutions

### 6.1 Strong contracts vs experiment speed

Architecture/Security favored explicit declarations; Product/Engineering rejected enterprise-level ceremony for early experiments.

Resolution: no Product Contract for fully product-local experiments; minimal `Provisional` Product Contract only when the platform boundary is crossed.

### 6.2 Stable integration vs capability maturity

Commercial/Operations wanted dependable product boundaries; Architecture required capability lifecycle integrity.

Resolution: Product Contract lifecycle and Platform Capability lifecycle are independent. A Stable Product Contract may only accurately expose a provisional/incubating dependency and cannot promote it.

### 6.3 Extension discoverability vs security

Product/Engineering wanted easy extension registration; CISO required deny-by-default access.

Resolution: registration provides identity/discoverability only. Authorization and organizational authority are evaluated separately.

### 6.4 Portability vs secret/legal restrictions

COO/Commercial required credible handover; CISO/Legal rejected unsafe or unauthorized export.

Resolution: portability preserves organizational meaning, governed references and migration paths, not unrestricted export of secrets or restricted material.

### 6.5 Contract completeness vs product autonomy

CTO wanted reconstructable dependencies; Product rejected duplication of internal product architecture.

Resolution: Product Contract declares only boundary-relevant semantics. Product internals and domain behavior remain product-owned.

### 6.6 Immediate purity vs legacy migration

Architecture preferred no hidden coupling; Engineering required a feasible transition path.

Resolution: hidden coupling is non-conforming as an end state, but bounded compatibility bridges are permitted with explicit ownership, review and exit path.

## 7. Material Changes Across the Review Loop

The resulting RFC-0004 `0.3.0` incorporates:

1. explicit independence of Product Contract and Platform Capability lifecycles;
2. explicit no-contract path for fully product-local experiments;
3. proportional minimal `Provisional` Product Contracts;
4. Product Contract stable Subject Identity and immutable Version Identity semantics;
5. consequential effective-contract version pinning;
6. boundary-only contract scope rather than universal product manifest;
7. prohibition of undocumented database/internal-import/private-interface coupling;
8. semantic compatibility rules including authority and side effects;
9. separate governed promotion from Product Experiment to platform incubation;
10. extension registration separated from authorization and organizational authority;
11. AI extension authority constraints;
12. derived-data scope/classification/retention/deletion propagation;
13. external-authority fidelity for adapters/connectors;
14. cross-product interaction through records/events/contracts/shared capabilities rather than internals;
15. staged migration and bounded compatibility bridges;
16. termination/handover and historical interpretability;
17. commercial-integrity constraints for provisional/incubating dependencies;
18. eighteen normative fitness tests.

## 8. Final Review Assessment

### Constitution alignment

No conflict found with Constitution `1.2.0`.

### Accepted RFC alignment

No conflict found with RFC-0001 `1.0.0` or RFC-0002 `1.0.0`.

RFC-0004 refines the Product Contract, Product Experiment and extension areas explicitly defined or reserved by RFC-0001 without changing the RFC-0002 Kernel metamodel.

### RFC-0003 dependency discipline

RFC-0003 `0.2.0` remains `Proposed` and was not treated as normative authority.

RFC-0004 is forward-compatible with its separation of identity, authorization, organizational authority, tenant scope and data governance, but acceptance of RFC-0004 must re-check RFC-0003 if RFC-0003 becomes Accepted first or changes materially.

### Scope discipline

The reviewed proposal avoids prematurely defining:

- a concrete Product Contract serialization/schema;
- IAM/authentication/authorization mechanisms;
- Governed Execution state machines;
- complete Event/provenance semantics;
- memory/knowledge lifecycle;
- plugin runtime or registry service;
- mandatory distributed architecture;
- product-specific business schemas.

### Review result

`RFC-0004 v0.3.0` is suitable to remain `Proposed` and be presented for owner decision after canonical index/roadmap synchronization.

This review is not owner approval and must not be cited as acceptance evidence.
