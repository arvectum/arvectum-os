# P5.11 — Compatibility / ADR / Refactoring / Public-Boundary Hardening Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P5.11 — Compatibility / ADR / refactoring / public-boundary hardening review`
Phase: `Phase 5 — SDK, Contracts and Extension Experience`
Milestone target: `M5 — Repeatable product/extension integration`
Result: **`PASS — no implementation mechanism crosses an ADR or Stable/public compatibility threshold; no material runtime refactor is justified before P5.12. Preserve the current internal/provisional integration architecture. Hosted Reference Python CI #266 passes 704 tests with OK.`**

## 1. Purpose and decision level

P5.11 is the final Phase 5 architecture-governance/refactoring gate before the separate P5.12/M5 closure decision. It reviews accumulated implementation evidence for accidental architecture: mechanisms that may have become materially relied upon even though earlier work intentionally kept them internal/provisional.

This review does not create a public SDK, stabilize a Product Contract, promote a Platform Capability, claim operational readiness or decide M5. It creates an ADR/RFC/policy only if the implementation has actually crossed the applicable durability/public-compatibility threshold.

## 2. Canonical basis checked

P5.11 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC-0001 `1.0.0` — `Accepted`;
3. RFC-0003 `1.0.0` — `Accepted`;
4. RFC-0004 `1.0.0` — `Accepted`, Product Contract is the explicit versioned product/platform boundary and hidden coupling is prohibited;
5. `docs/rfc/README.md` — RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
6. `docs/adrs/README.md` — ADR format/boundary checked; no applicable Accepted ADR currently fixes Phase 5 integration mechanics;
7. P5.01 through P5.10 review evidence and R13/R14/R15/R16 engineering gates;
8. R16 `PASS after R16-F1 remediation` and hosted `Reference Python CI #262`, 695 tests, `OK`;
9. both executable Product Contracts remain `Provisional 0.1.0` reference evidence;
10. CAP-001 through CAP-004 remain `Incubating / Provisional` per current canonical Phase 5 state;
11. hosted `Reference Python CI #266` — `PASS`, 704 tests, `OK`, including all nine focused P5.11 hardening guards.

No conflict with Constitution `1.2.0` or the checked Accepted RFCs was identified.

## 3. Accidental architecture review

The accumulated implementation still has one intentional integration seam: Product Contract declaration/validation + exact governed dependency compatibility + composition + adapters. Reuse by two materially distinct consumers justifies retaining that seam as internal/provisional reference architecture; it does not by itself justify publication or stabilization.

The root `arvectum_os_ref` package does not export the Phase 5 integration facade/adapters/harness. Consumers use explicit submodule imports in the monorepo reference implementation. The package root explicitly states that the package is provisional and not a public platform contract.

Two internal compatibility conveniences remain visible inside the reference implementation:

- `IntegrationAdapters.workspace` lazily binds the optional workspace adapter;
- `LocalIntegrationHarnessResult.facade` exposes the underlying facade through the adapter-backed harness result.

Both were introduced/retained to keep existing internal reference callers readable during R15 refactoring. They are not root exports, not package/wire contracts and not used as authority sources. Removing them now would be cleanup without demonstrated organizational value, so P5.11 does **not** perform a speculative breaking refactor. They remain watch items for later removal if no real product integration relies on them.

## 4. Compatibility semantics review

P5.03 compatibility remains exact and governed:

- exact effective Product Contract Version continuity is required;
- exact declared dependency contract versions are matched only against explicit governed provider/version evidence;
- compatibility does not infer SemVer/package/module/dataclass/token compatibility;
- no fallback version is selected automatically;
- `VersionMismatch`, `Unsupported`, `Deprecated`, `Retired` and `Ambiguous` remain explicit fail-closed outcomes;
- changed reliance exposes migration obligations rather than silently selecting another version;
- R14 requires current governed provider/version evidence at dependency-backed reliance;
- R16 binds capability-adapter contract semantics to the exact declaration evidence already validated at facade composition.

This is compatibility **semantics**, not a public version-negotiation protocol. No durable freshness service, package resolver, migration daemon or external compatibility API has been selected.

## 5. Public-boundary / ADR gate matrix

| Gate | Current evidence | P5.11 disposition | Threshold that would require a governed decision |
|---|---|---|---|
| Language-specific SDK/package boundary | Python modules are monorepo reference code; Phase 5 integration surfaces are not root-exported and no package/distribution metadata is selected for them. | **No ADR / no public boundary.** | Supported installable SDK/package with compatibility/versioning/support obligations. |
| Stable/public API or wire/serialization contract | No HTTP/gRPC/GraphQL route, OpenAPI/schema, broker protocol or serialization format is selected by integration tooling. | **No ADR / no public boundary.** | Externally relied-upon stable API/wire/schema contract. |
| Package registry/distribution topology | No registry, publishing pipeline, repository topology or package support policy is selected. | **No ADR.** | Material reliance on a specific distribution/publishing mechanism. |
| Plugin loading/sandboxing/isolation mechanism | No dynamic plugin loader, entry-point mechanism, sandbox or extension process model exists. | **No ADR.** | Dynamic third-party extension execution/loading/isolation becomes supported behavior. |
| Extension registry/discovery topology | P5.09 extension is explicit product-owned code; no registry/discovery service exists and registration grants no authority. | **No ADR.** | Durable extension registry/discovery identity and lifecycle mechanism. |
| Version negotiation/migration/freshness protocol | Exact governed evidence and explicit migration obligations exist, but no negotiation/fallback/freshness service or wire protocol is selected. | **No ADR.** | Automated negotiation/fallback, durable freshness protocol/service or externally relied-upon migration mechanism. |
| Generated-code compatibility boundary | P5.05 renders readable/replaceable provisional starter source; generated output is not authoritative or supported as a compatibility surface. | **No ADR / no public boundary.** | Generated clients/stubs/config become relied-upon supported artifacts. |
| Separately deployable integration service | Composition, adapters, evidence and harness are in-process reference modules with no independent lifecycle/scaling/failure topology. | **No ADR.** | Separate service/process/worker with independent operational contract. |
| Stable design-system/component integration contract | Phase 5 integration has no design-system/component-library dependency or stable UI component contract. | **No ADR / no public boundary.** | Cross-product stable component/design-system compatibility obligation. |

**ADR decision:** no new ADR is justified by the current Phase 5 implementation. Creating one now would prematurely standardize mechanisms that Accepted architecture intentionally leaves replaceable.

## 6. Refactoring disposition

No material runtime refactor is justified before P5.12:

- R15 already reduced shared adapter state to `facade + capabilities` and made workspace optional;
- R16 already repaired same-version Product Contract semantic drift at the adapter seam;
- declaration, compatibility, capability, workspace, security, Governed Execution and Event semantics still have clear existing owners;
- the remaining compatibility accessors are bounded internal conveniences, not public contract commitments;
- extracting a generic SDK/package, plugin system, registry, protocol DTO layer or service boundary would be speculative generalization.

The P5.11 refactoring decision is therefore **preserve the current bounded implementation and guard its provisional status**.

## 7. Security / authority / lifecycle preservation

P5.11 changes none of the following:

- Product Contract declaration or lifecycle;
- Platform Capability lifecycle;
- Authentication, Authorization or Organizational Authority semantics;
- Data Governance, purpose, right, classification, minimization, retention or deletion controls;
- Governed Execution gates or canonical mutation rules;
- Event/provenance semantic ownership;
- external-system authority modes;
- operational readiness or conformance maturity.

No compatibility helper, adapter, scaffold, extension identity or import path grants permission, approval, authority or lifecycle promotion.

## 8. Executable hardening evidence

P5.11 adds `reference/python/tests/test_p5_11_compatibility_adr_public_boundary_hardening_review.py`.

The guard verifies:

1. integration facade/adapters/harness remain internal submodules rather than package-root exports;
2. no Python package/distribution boundary is selected for the reference integration surface;
3. no public API/wire/serialization framework is selected by Phase 5 integration modules;
4. no plugin loader or extension registry runtime is selected;
5. compatibility remains exact governed evidence with no automatic fallback/version-range resolver dependency;
6. scaffolding remains readable/replaceable rather than a generated-code compatibility contract;
7. integration remains in-process rather than a separately deployable service topology;
8. both executable Product Contracts remain Provisional and not Stable;
9. no stable design-system/component integration contract is introduced.

Hosted `Reference Python CI #266` ran `python -m unittest discover -s tests -v` under Python 3.12 and completed **704 tests with `OK`**. All nine P5.11 guards passed together with the accumulated reference suite.

These guards protect the current reviewed disposition. A future legitimate ADR/public-boundary decision must update the guard and canonical governance together rather than bypassing it.

## 9. Functional cross-review iterations

### Iteration 1 — compatibility and package boundary

Finding: repeated reuse exists at the Product Contract/composition/adapter semantic seam, but no evidence shows reliance on an installable Python package, root-exported SDK surface, SemVer range contract or distribution registry.

Disposition: retain the semantic seam; reject package/SDK stabilization and automatic version negotiation.

### Iteration 2 — plugin/registry/service and generated-code boundary

Finding: the second integration is explicit code using the same adapter seam, not dynamically loaded plugin infrastructure. P5.05 starter output is readable/replaceable and the harness is in-process.

Disposition: no plugin/extension registry, sandbox, generated-client compatibility contract or deployable integration service; no ADR.

### Iteration 3 — refactoring and accidental compatibility

Finding: `IntegrationAdapters.workspace` and `LocalIntegrationHarnessResult.facade` are explicitly internal compatibility conveniences. They are not root exports or authority sources, and no evidence shows that removing them now reduces meaningful risk.

Disposition: keep them bounded for current internal callers, record them as watch items and do not create a speculative breaking cleanup before P5.12.

### Iteration 4 — public boundary / governance closure readiness

Finding: none of the nine explicit P5.11 gates is crossed. Product Contracts remain Provisional, capabilities remain Incubating/Provisional, and the current integration modules explicitly disclaim Stable/public SDK/API/package/wire/registry/service commitments.

Disposition: explicit **no-ADR / no-public-boundary**. Hosted full-suite validation is green. P5.12 remains the separate M5 closure decision.

No material objection remains after iteration 4.

## 10. Exit assessment

P5.11 exit conditions are satisfied:

- [x] language-specific SDK/package gate reviewed;
- [x] stable/public API/wire/serialization gate reviewed;
- [x] package registry/distribution gate reviewed;
- [x] plugin loading/sandboxing/isolation gate reviewed;
- [x] extension registry/discovery gate reviewed;
- [x] version negotiation/migration/freshness gate reviewed;
- [x] generated-code compatibility gate reviewed;
- [x] separately deployable integration-service gate reviewed;
- [x] stable design-system/component gate reviewed;
- [x] refactoring threshold reviewed against demonstrated reuse;
- [x] explicit no-ADR/no-public-boundary disposition recorded;
- [x] executable regression guards added;
- [x] full current Reference Python CI green on the P5.11 head (`#266`, 704 tests, `OK`);
- [x] P5.11 completion is ready for canonical roadmap synchronization to P5.12.

## 11. Handoff

P5.11 closes with:

> **`PASS — no material runtime refactor, ADR or Stable/public compatibility boundary is required before P5.12; preserve the current internal/provisional Phase 5 integration architecture.`**

Proceed only to:

> **`P5.12 — Phase 5 / M5 closure review`.**
