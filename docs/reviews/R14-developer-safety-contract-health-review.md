# R14 — Developer Safety / Contract Health Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform` integration-boundary engineering review
Constitution: `1.2.0` — `Ratified`, frozen
Architecture basis: RFC-0001 `1.0.0`; RFC-0002 `1.0.0`; RFC-0003 `1.0.0`; RFC-0004 `1.0.0`; RFC-0005 `1.0.0`; RFC-0006 `1.0.0` — `Accepted`
Preceding baseline: P5.01/P5.02/R13/P5.03/P5.04/P5.05/P5.06 — `PASS`
ADR disposition: no Accepted ADR constrains this bounded internal/provisional remediation; no new ADR threshold crossed
Implementation PR: `#67`
Hosted validation: no GitHub Actions run/status was generated for the R14 PR head at review publication time; last confirmed hosted full-suite baseline remains P5.06 `Reference Python CI #223`, 634 tests, `OK`
Result: **`PASS — two material developer-safety/contract-health defects were identified and remediated. R14-F1 closes direct facade construction that could bypass the governed P5.02/P5.03 composition path. R14-F2 prevents composition-time dependency compatibility evidence from self-advancing as indefinitely current provider-support evidence. Dependency-backed J1/J2 actions now require explicit current governed dependency/version evidence and re-run the existing P5.03 resolver before reliance.`**

## 1. Purpose

R14 is the mandatory engineering gate after P5.06 and before P5.07. It reviews the accumulated P5.02-P5.06 integration surface for developer-safe defaults and Product Contract health rather than adding a new platform subsystem.

The gate specifically reviews:

- fail-closed developer behavior;
- separation of Authorization and Organizational Authority;
- continuity of purpose, rights and data-governance constraints;
- stale-evidence handling;
- error semantics;
- hidden-coupling pressure;
- accidental authority inflation;
- accidental Product Contract or public/stable compatibility inflation.

R14 is not a Product Contract stabilization decision, capability promotion, IAM design, provider-registry design, production-readiness decision or public SDK/API commitment.

## 2. Canonical authority checked

R14 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — explicit contracts, product/platform separation, fail-closed security/authority boundaries, internal-interface containment, scoped conformance and commercial-integrity constraints;
4. RFC-0002 — stable identity, immutable version identity, explicit effective-version resolution and the rule that possession/resolution does not grant permission or authority;
5. RFC-0003 — semantic separation of Identity, Authentication, Authorization, Organizational Authority and Data Governance; least privilege; purpose limitation; tenant isolation and fail-closed behavior;
6. RFC-0004 — Product Contract as the single explicit versioned product/platform boundary; semantic compatibility; provider/consumer/failure responsibilities; hidden-coupling prohibition; Product Contract lifecycle separation from Platform Capability lifecycle;
7. RFC-0005 — exact effective Product Contract attribution; independent execution gates; stale-gate re-evaluation; no Product Contract possession as authority;
8. RFC-0006 — provenance/evidence paths must not silently fail or acquire organizational authority; transport/observation/evidence does not itself establish permission or truth;
9. `docs/adrs/README.md` — no applicable Accepted ADR currently constrains the bounded internal/provisional integration facade or evidence snapshot mechanism;
10. P5.02, R13, P5.03, P5.04, P5.05 and P5.06 completion evidence;
11. P4.08 `Provisional 0.1.0` Product Contract;
12. current integration facade, scaffold, product journey and security/authority guard implementation/tests;
13. canonical Roadmap and Phase 5 workstream at R14 start.

No conflict with Constitution `1.2.0` or the checked Accepted RFCs is introduced by the R14 remediation.

## 3. Reviewed dependency direction

The intended developer path remains:

```text
Product / Extension owned code
        |
        | current explicit integration inputs
        v
IntegrationCompositionFacade
        |
        +--> P5.02 Product Contract declaration validation
        |
        +--> P5.03 exact dependency/version compatibility resolution
        |
        +--> capability admission -> current purpose/right/classification owner
        |
        +--> non-authoritative workspace presentation
        |
        `--> RFC-0005 Governed Execution -> independent governed gates

Product Contract semantic owner ----------> RFC-0004 ProductContract
Authorization / rights -------------------> RFC-0003 + bounded access owners
Organizational Authority -----------------> RFC-0003 / RFC-0005 governed gate
Capability lifecycle ---------------------> RFC-0001 governance + capability catalog
Public/stable compatibility -------------> separate future evidence/governance/ADR gate
```

The facade may make the correct path easier, but it must not become an alternate semantic owner or permit stale derived evidence to become current authority by convenience.

## 4. Material finding R14-F1 — direct facade construction could bypass governed composition

Severity: `Material — developer safety / semantic-owner bypass`
Disposition: `Remediated`

### 4.1 Finding

P5.04 correctly provided `compose_integration_facade()` as the intended construction path. That factory invokes P5.02 declaration validation and P5.03 exact dependency/version resolution before creating the facade.

However, `IntegrationCompositionFacade.__init__()` remained directly callable. A developer could construct the class with caller-created `ProductContractDeclarationValidation` and `DependencyCompatibilityReport` objects that were structurally plausible without actually passing through the P5.02/P5.03 evaluation path.

The constructor performed continuity checks over the supplied derived evidence, but it could not prove that the evidence itself had been obtained from the semantic owners. Later facade operations relied on the stored compatibility report.

This was a material R14 defect because the convenient integration seam itself created a developer path around the very contract-health evaluation it was intended to compose.

### 4.2 Remediation

`reference/python/arvectum_os_ref/integration_composition.py` now:

- restricts facade construction to `compose_integration_facade()` through an internal construction token;
- raises typed `IntegrationCompositionConstructionError` when a caller directly invokes the constructor without the governed factory path;
- keeps the token implementation-private and explicitly non-public/non-stable;
- leaves P5.02/P5.03 as the existing validation and compatibility semantic owners;
- creates no new registry, admission authority or contract lineage.

The internal token is a developer-safety guard, not a security credential. Deliberately importing private module state to circumvent it would itself be hidden implementation coupling and is outside the supported integration path.

## 5. Material finding R14-F2 — composition-time support evidence could become stale

Severity: `Material — stale evidence / contract health`
Disposition: `Remediated`

### 5.1 Finding

P5.03 intentionally models `GovernedDependencyVersionEvidence` as an explicit provider/version support snapshot. P5.04 used such evidence during facade composition and retained the resulting immutable `DependencyCompatibilityReport`.

Before R14, later `admit_capability()` and `start_governed_execution()` operations checked only the stored `Compatible` evaluation. A long-lived facade could therefore continue dependency-backed reliance after the current provider/version evidence had become `Deprecated`, `Retired`, `Unsupported`, ambiguous or otherwise unavailable.

P5.06 proved stale RFC-0005 gate-decision rejection and stale Product Contract Version rejection, but it did not cover staleness of the dependency-support evidence that P5.03 uses to establish compatibility.

This was a direct R14 stale-evidence defect.

### 5.2 Remediation

Dependency-backed J1/J2 facade operations now require explicit current governed dependency/version evidence:

- `admit_capability(..., governed_versions=...)`;
- `start_governed_execution(..., governed_versions=...)`.

If current governed evidence is omitted, the facade raises typed `IntegrationCompositionEvidenceRequiredError` rather than silently reusing the composition-time compatibility report.

When evidence is supplied, the facade re-runs `resolve_product_contract_dependencies()` against:

- the exact source RFC-0004 Product Contract;
- the exact Product Contract Version already composed into the facade;
- the supplied current governed dependency/version evidence.

P5.03 typed errors remain visible without being translated into facade-owned compatibility decisions. A current `Deprecated`, `Retired`, `Unsupported`, `VersionMismatch` or `Ambiguous` result therefore fails through the existing P5.03 error semantics.

The composition-time `compatibility_evidence` property remains available for immutable inspection/history only and is explicitly documented as not being current provider-support authority.

## 6. Bounded freshness model — what R14 deliberately does not decide

R14 does not invent a provider registry, TTL, lease, polling protocol, clock-based freshness rule or externally supported compatibility service.

The current internal/provisional rule is smaller:

> Every dependency-backed J1/J2 reliance must explicitly present the governed provider/version evidence the caller intends to treat as current, and the existing P5.03 semantic owner must evaluate that evidence against the exact effective Product Contract before reliance.

This removes the unsafe implicit cache behavior without pretending that Arvectum OS already has a canonical provider-support registry or universal freshness protocol.

Residual boundary:

- caller-supplied evidence is still an explicit snapshot;
- the source and acquisition mechanism that establishes how a future operational system obtains the authoritative current snapshot remain outside this R14 implementation;
- if later work introduces a durable provider registry, TTL/freshness protocol, network resolver, public compatibility service or externally relied-upon negotiation mechanism, the ADR/governance gate must be re-opened before material reliance.

This residual is acceptable for the current `Provisional` internal reference stage because R14 removes silent self-advancement and makes the evidence dependency explicit.

## 7. Authorization, Organizational Authority and data-right continuity review

Result: `PASS`.

R14 confirms that the remediation does not merge or infer distinct governance decisions:

- Product Contract declaration/validation remains non-authoritative;
- provider/version compatibility remains compatibility evidence only;
- capability admission remains non-authoritative boundary evidence;
- actual capability access continues to enforce current Organization/purpose/right/classification constraints through the existing access semantic owner;
- consequential execution still begins with Authorization, Organizational Authority, Data Governance and applicable approval gates independently unresolved;
- a `Supported` dependency version does not satisfy Authorization or Organizational Authority;
- a Product Contract, facade, scaffold or local harness still grants no permission or approval.

No second IAM/PDP/PEP, role model, authority registry or policy evaluator was introduced.

## 8. Error-semantics review

Result: `PASS after remediation`.

The developer-facing failure model remains layered by semantic ownership:

- invalid direct facade construction -> `IntegrationCompositionConstructionError`;
- missing current dependency evidence -> `IntegrationCompositionEvidenceRequiredError`;
- Product Contract/Product/Organization/operation drift -> existing Product Contract or integration continuity errors;
- unsupported/deprecated/retired/version-mismatched/ambiguous provider evidence -> existing typed P5.03 dependency-resolution errors;
- current purpose/right/classification denial -> existing access-enforcement errors;
- unresolved/denied execution gates -> existing RFC-0005 governed-execution errors.

The facade does not catch and relabel P5.03 failures as generic success/failure booleans. This keeps error behavior attributable to the semantic owner and avoids turning developer convenience into a competing policy layer.

## 9. Hidden-coupling and developer-experience review

Result: `PASS after R14-F1/R14-F2 remediation`.

The bounded product journey still imports exactly one Arvectum OS integration-facing module: `arvectum_os_ref.integration_composition`.

Current governed provider/version evidence is passed opaquely through product-owned journey helpers. The product does not import the dependency resolver, Product Contract internals, canonical-state implementation, workspace internals or Governed Execution implementation directly.

The P5.05 template remains small, readable and replaceable. It opens only the non-authoritative workspace and therefore does not require provider-support evidence merely to render presentation state.

No new hidden table, internal store, private Event stream, undocumented endpoint or implicit shared-state dependency is created.

## 10. Authority/lifecycle/public-contract inflation review

Result: `PASS`.

R14 creates no field or state representing:

- Authentication success;
- Authorization allow;
- permission grant;
- Organizational Authority;
- consequential approval;
- capability lifecycle transition;
- capability activation;
- Product Contract stabilization;
- operational readiness;
- full-platform conformance.

P4.08 remains `Provisional 0.1.0`.

Platform Capability lifecycle remains owned by RFC-0001 governance and the canonical capability catalog. Provider/version support evidence used by P5.03 is still not Platform Capability lifecycle state.

No Stable/public Python SDK/package path, Product Contract serialization, REST/gRPC/wire API, registry topology, SemVer negotiation rule, automatic migration protocol or production support commitment is introduced.

## 11. Executable regression evidence

R14 adds:

- `reference/python/tests/test_r14_developer_safety_contract_health_review.py`.

The focused suite adds 10 cases covering:

1. direct facade construction fails closed through a typed construction error;
2. J1 dependency-backed reliance rejects omitted current dependency evidence;
3. J2 dependency-backed reliance rejects omitted current dependency evidence;
4. composition-time `Supported` evidence cannot hide current `Deprecated` evidence for J1;
5. composition-time `Supported` evidence cannot hide current `Unsupported` evidence for J2;
6. current `Supported` evidence permits J1 while admission remains non-authoritative;
7. current `Supported` evidence permits J2 while governed gates remain unresolved;
8. product-owned J1/J2 helpers pass current evidence without adding platform-private imports;
9. composition-time compatibility remains inspection evidence and cannot self-advance;
10. remediation remains internal/provisional and selects no public transport/serialization/registry/SemVer stack.

Existing P5.04 and P5.06 regression tests were updated only to provide explicit current governed dependency evidence at their dependency-backed J1/J2 calls. Their existing authority, Organization, rights, gate and integration-boundary assertions remain intact.

### Hosted validation status

PR `#67` was opened for the R14 branch.

At review publication time GitHub returned:

- PR mergeability: `true`;
- no workflow run associated with the R14 head;
- no combined commit status entries for the R14 head.

R14 therefore does **not** claim a hosted CI success that did not occur.

The last confirmed hosted full reference-suite evidence remains:

- P5.06 `Reference Python CI #223`;
- 634 tests;
- result `OK`.

The new R14 tests are committed deterministic regression evidence and must be exercised by the next available full reference-suite run before a later gate claims hosted validation over the R14 changes.

## 12. Functional cross-review iterations

### Iteration 1 — developer-safe construction path

Finding: R14-F1. Direct `IntegrationCompositionFacade` construction could accept caller-created derived evidence and bypass the intended P5.02/P5.03 factory path.

Disposition: restrict construction to the governed composition factory and add typed fail-closed direct-construction behavior.

### Iteration 2 — stale contract-health evidence

Finding: R14-F2. Composition-time compatibility could be reused after provider/version support changed.

Disposition: require explicit current governed provider/version evidence for every dependency-backed J1/J2 reliance and re-run P5.03 resolution.

### Iteration 3 — authority separation

Finding: making current provider evidence mandatory must not turn support evidence into Authorization or Organizational Authority.

Disposition: compatibility remains compatibility only; access and execution gates remain independent existing semantic owners.

### Iteration 4 — rights/purpose/data-governance continuity

Finding: re-resolution before facade admission must not move current purpose/right/classification evaluation into the Product Contract layer.

Disposition: facade checks contract health only, then existing capability access paths continue to enforce current rights/purpose/classification; Governed Execution retains independent Data Governance gates.

### Iteration 5 — error semantics and hidden coupling

Finding: convenience code could hide semantic-owner failures behind generic facade errors or force product code to import resolver internals.

Disposition: P5.03 typed failures propagate; product helpers receive provider evidence opaquely and still import only the facade module.

### Iteration 6 — lifecycle/public-boundary/ADR review

Finding: defining a canonical registry, TTL/freshness protocol or public compatibility service at R14 would exceed current evidence and create a durable boundary decision.

Disposition: do not select one. Keep the explicit-snapshot model internal/provisional and re-open ADR/governance if later work establishes a durable provider-currentness mechanism.

No remaining material objection was identified after iteration 6 for the declared internal/provisional scope.

## 13. Exit criteria

- [x] developer-safe construction path fails closed and cannot normally bypass P5.02/P5.03;
- [x] dependency-backed J1/J2 reliance cannot silently reuse composition-time provider compatibility;
- [x] current governed provider/version evidence is explicit at each dependency-backed reliance;
- [x] current provider support is re-evaluated by the existing P5.03 semantic owner;
- [x] P5.03 typed compatibility failures remain visible;
- [x] Product Contract remains the single product/platform dependency semantic owner;
- [x] Authorization remains separate from Organizational Authority;
- [x] purpose/right/classification and Data Governance remain with their existing semantic owners;
- [x] wrong/stale Product Contract and stale gate evidence remain fail closed through prior guards;
- [x] product-owned journey retains one Arvectum OS integration-facing import boundary;
- [x] no capability lifecycle or Product Contract lifecycle transition is created;
- [x] no Stable/public registry, SDK/API, wire, serialization or SemVer compatibility mechanism is selected;
- [x] no new RFC or ADR threshold is crossed;
- [x] focused R14 regression evidence is committed;
- [x] hosted R14 CI is explicitly unclaimed because GitHub generated no run/status;
- [x] bounded residual freshness-source question is explicit rather than silently solved by a cache.

## 14. Final disposition

**PASS — R14 is complete after remediation of R14-F1 and R14-F2 for the current internal/provisional Phase 5 integration surface.**

The safe developer path now preserves both exact Product Contract continuity and explicit current dependency-support evidence without converting contract health into permission, Organizational Authority, capability lifecycle or public compatibility state.

No Constitution amendment, Accepted RFC change, new RFC, ADR, Product Contract stabilization, capability promotion, production-readiness claim, conformance expansion, SLA/support promise or commercial commitment is created by R14.

Next canonical work item after roadmap synchronization:

> **P5.07 — Event/provenance/portability integration support.**
