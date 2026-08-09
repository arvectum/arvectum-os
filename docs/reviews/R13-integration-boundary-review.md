# R13 — Integration Boundary Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform` integration-boundary review
Engineering gate: `R13 — Integration Boundary Review`
Phase: `Phase 5 — SDK, Contracts and Extension Experience`
Milestone target: `M5 — Repeatable product/extension integration`
Result: **`PASS — one material boundary-projection completeness defect was identified and remediated. The P5.02 tooling remains an internal/provisional derived validation view over the existing RFC-0004 Product Contract, not a second contract system, permission source, capability-lifecycle authority or Stable/public compatibility boundary. Phase 5 may proceed to P5.03 with R13-F1 retained as a fixed integration invariant.`**

## 1. Purpose

R13 is the mandatory engineering gate after P5.02 and before P5.03. It re-checks whether the new machine-checkable declaration-validation tooling still expresses the existing RFC-0004 Product Contract boundary or has begun to acquire independent semantic authority.

R13 specifically reviews whether P5.02 could become:

- a second Product Contract system or competing declaration source;
- a permission, Authorization or Organizational Authority source;
- a Platform Capability lifecycle authority;
- an accidental Stable/public schema, SDK/API, wire, package or registry compatibility boundary;
- a lossy projection that later Phase 5 tooling could incorrectly treat as the complete dependency contract.

R13 is an engineering boundary review. It does not stabilize the P4.08 Product Contract, promote a Platform Capability, approve production readiness, establish an SLA/support obligation or make a public compatibility commitment.

## 2. Canonical authority checked

R13 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — Product Contract dependency rules, product/platform separation, capability lifecycle, security/authority invariants, internal-interface containment, scoped conformance and commercial-commitment integrity;
4. RFC-0002 — stable Identity, immutable governed Version identity, exact-version reliance and the rule that references do not grant permission;
5. RFC-0003 — separation of Identity, Authentication, Authorization, Organizational Authority and Data Governance; deny-by-default Organization-scoped enforcement;
6. RFC-0004 — Product Contract as the explicit versioned boundary, required dependency/operation/security/data/compatibility/failure responsibilities, hidden-coupling prohibition, Product Contract lifecycle and capability-lifecycle separation;
7. RFC-0005 — exact effective Product Contract attribution and enforcement of applicable Product Contract operation, canonical-state, authority, security, data-handling, failure and compatibility declarations during Governed Execution;
8. `docs/adrs/README.md` — no applicable Accepted ADR currently constrains this bounded internal/provisional representation;
9. `Platform Capability Catalog 1.2.1` — CAP-001 through CAP-004 remain `Incubating / Provisional` and catalog/governance remains the capability-lifecycle authority;
10. `P5.01 — Integration Boundary Revalidation + Developer Journeys` — `PASS`;
11. `P5.02 — Product Contract Declaration Model + Machine-Checkable Validation Baseline` — `PASS`;
12. `P4.08 Bounded Product Entry Product Contract` — `Provisional 0.1.0`;
13. current `arvectum_os_ref.product_contract`, `arvectum_os_ref.product_contract_declaration`, P4.08 executable Product Contract fixture and P5.02 tests;
14. canonical Roadmap `2.29.0` and Phase 5 roadmap `1.2.0` at R13 start.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0005 is introduced by the R13 remediation.

## 3. Boundary model under review

The intended Phase 5 dependency direction remains:

```text
Product / Extension owned code
        |
        | exact governed Product Contract Subject/Version
        | dependencies / operations / canonical access
        | security / authority / data / compatibility / failure responsibilities
        v
RFC-0004 ProductContract semantic owner
        |
        +--> P5.02 declaration validation
        |        |
        |        `--> immutable derived inspection evidence
        |
        +--> runtime Product Contract admission / continuity
        |
        `--> future P5.03 dependency/version resolution

Capability lifecycle authority -----------------> capability catalog / RFC-0001 governance
Authorization / Organizational Authority -------> RFC-0003 / RFC-0005 semantic owners
Public/stable compatibility --------------------> separate evidence + ADR/governance gate when crossed
```

The P5.02 validation object is therefore a derived inspection result. It may make the Product Contract easier to inspect or validate, but it must not become an independently editable boundary source or a narrower substitute for the source Product Contract.

## 4. Material finding and remediation

### R13-F1 — Derived validation evidence omitted declared dependency and operation responsibilities

Severity: `Material — product-contract boundary / semantic completeness`
Disposition: `Remediated`

Before R13, `validate_product_contract_declaration()` correctly consumed the existing `ProductContract` object and preserved exact contract/product/dependency/operation/version identity, gates, canonical access, Organization scope, lifecycle and review/exit responsibilities.

However, its derived dependency evidence copied only:

- dependency Identity;
- dependency contract version;
- allowed operations;
- the existing `provisional` reliance qualifier.

It omitted three already-declared RFC-0004 boundary semantics from each `PlatformDependencyDeclaration`:

- provider responsibility;
- consumer responsibility;
- dependency failure behavior.

Likewise, derived operation evidence preserved side-effect and required-gate semantics but omitted the operation's declared failure behavior.

P5.02 itself did not yet become a second Product Contract system because the source `ProductContract` remained the only accepted input and the validator created no independently editable manifest. The defect was nevertheless material at R13 because P5.03 is specifically about dependency/version and compatibility semantics. A downstream resolver built only against the narrower validation projection could have started treating that projection as a self-contained dependency contract and silently dropped responsibilities already owned by RFC-0004 Product Contract state.

R13 remediates the defect in `reference/python/arvectum_os_ref/product_contract_declaration.py`:

- `DeclaredDependencyEvidence` now preserves `provider_responsibility`, `consumer_responsibility` and dependency `failure_behavior` exactly from the source Product Contract;
- `DeclaredOperationEvidence` now preserves operation `failure_behavior` exactly from the source Product Contract;
- all newly preserved responsibility/failure fields fail closed when empty;
- the derived evidence remains immutable and contains no independent lifecycle, permission, authority or activation state;
- the source `ProductContract` remains the only executable declaration model accepted by the validator.

Implementation commit: `96ac766bce72ca2584478273aecc474518a4d052`.

The remediation is internal, additive and reversible. It changes no Accepted RFC, Product Contract lifecycle, capability lifecycle or public compatibility surface.

## 5. Second-contract-system review

Result: `PASS after R13-F1 remediation`.

R13 confirms:

- `validate_product_contract_declaration()` accepts an explicit `ProductContract`, not an independent manifest shape;
- Product Contract Subject/Version and Product identity/version remain preserved in the derived result;
- dependencies, operations, canonical access and boundary responsibilities are copied from the source declaration rather than independently authored in P5.02;
- the validation evidence is immutable inspection evidence and has no admission registry, mutation API or independently effective version lineage;
- no YAML, JSON, protobuf, OpenAPI or other serialization format is selected;
- no package registry, extension registry, public SDK/API or wire contract is selected;
- current Python dataclass/module shape remains internal/provisional reference evidence.

P5.03 and later Phase 5 tooling MUST continue to treat the RFC-0004 Product Contract as the governed semantic owner. A derived validation result may be cached, displayed or passed internally only as evidence tied to the exact Product Contract Version; it must not become an independently evolving contract source.

## 6. Security, permission and authority review

Result: `PASS`.

The validation result and its dependency/operation evidence contain no fields that represent:

- Authentication;
- Authorization decisions;
- permission grants;
- Organizational Authority decisions;
- consequential approvals;
- capability activation.

Required gate kinds remain declarations about what the governed operation requires. Their presence in a Product Contract or validation result does not satisfy those gates.

Consequential canonical mutation continues to require the existing RFC-0005 Governed Execution path and independently evaluated RFC-0003/RFC-0005 security, authority, data-governance and approval evidence.

No P5.02 or R13 object becomes an IAM/PDP/PEP, policy engine, approval authority or organizational decision authority.

## 7. Product Contract lifecycle and capability lifecycle review

Result: `PASS`.

The current P5.02 validator remains intentionally bounded to `Provisional` Product Contracts. This is a validation-scope restriction, not a lifecycle decision mechanism.

The dependency `provisional` field remains only the existing Product Contract reliance/support qualifier. It does not copy, infer or replace Platform Capability lifecycle state.

CAP-001 through CAP-004 remain `Incubating / Provisional` according to the canonical Platform Capability Catalog. No R13 change creates `Active`, operational-readiness or support status.

The P4.08 Product Contract remains `Provisional 0.1.0`. R13 does not create evidence for `Stable`, `Deprecated` or `Retired` validation semantics.

## 8. Stable/public compatibility and ADR review

Result: `PASS — no ADR threshold crossed`.

R13 found no material reliance on a stable/public:

- language-specific SDK/package boundary;
- Product Contract serialization format;
- API or wire protocol;
- package or extension registry;
- plugin loading/sandboxing model;
- generated-code boundary;
- version-negotiation protocol;
- separately deployable integration service.

The current internal Python classes remain implementation evidence only. Preserving more RFC-0004 semantics in an internal derived dataclass does not itself stabilize that dataclass.

The ADR/public-boundary gate remains armed for later Phase 5 work. If P5.03 introduces durable version negotiation, externally relied-upon compatibility machinery or another constraining integration mechanism, the ADR/governance gate must be re-opened before material reliance.

## 9. P5.03 handoff invariants

P5.03 may now begin, subject to the following fixed R13 invariants:

1. the RFC-0004 Product Contract remains the semantic owner of product/platform dependency declarations;
2. any dependency resolver must preserve exact Product Contract Version identity and exact dependency contract-version identity;
3. provider responsibility, consumer responsibility, dependency failure behavior and operation failure behavior must remain available from the exact effective Product Contract boundary;
4. derived P5.02 validation evidence is inspection/validation evidence, not an independent contract authority;
5. compatibility must be explicit and must not be inferred from Python package versions, module paths, dataclass shape or operation-token spelling;
6. unsupported, incompatible, deprecated or retired reliance must have deterministic fail-closed behavior appropriate to the actual governed lifecycle evidence available;
7. Product Contract declaration/admission/resolution grants no Authorization or Organizational Authority;
8. capability lifecycle remains owned by RFC-0001 governance and the canonical capability catalog;
9. no Stable/public compatibility promise is created merely by implementing version resolution;
10. durable version-negotiation/migration protocols or public compatibility mechanisms re-open the ADR/governance gate.

These constraints are boundary conditions for P5.03, not a predefinition of its implementation mechanism.

## 10. Executable regression evidence

R13 adds:

- `reference/python/tests/test_r13_integration_boundary_review.py`.

The regression evidence checks that:

1. derived dependency evidence preserves exact dependency version/operation plus provider, consumer and failure responsibilities;
2. derived operation evidence preserves exact dependency/side-effect/gate/failure semantics;
3. erased derived responsibility/failure semantics fail closed;
4. derived validation evidence remains free of permission, Organizational Authority and capability-lifecycle state;
5. the validator remains an internal/provisional derived view over the existing `ProductContract` and does not select a manifest/serialization/registry boundary.

Test commit: `914cd3fcf1cc6f5fa0ecbcef59cee61d82f4e1c9`.

At R13 review time no new combined commit status was returned for the direct-push R13 head. R13 therefore does not claim a new hosted CI run. The last observed hosted full-suite evidence remains the P5.02 baseline `Reference Python CI #205`; R13's new regression test file is committed as executable evidence and must be included in the next normal full reference-suite execution.

Absence of a newly observed hosted run is not treated as an architectural exception or a production-readiness claim. R13's scope is the integration-boundary gate; later engineering evidence must continue to include the committed R13 regression invariant.

## 11. Functional cross-review iterations

### Iteration 1 — semantic owner / duplicate-contract review

Finding: the validator still accepts only the existing `ProductContract` and creates no independently editable manifest, registry or contract lineage.

Disposition: retain the current semantic-owner direction; inspect whether the derived view is semantically complete enough not to become a narrower substitute during P5.03.

### Iteration 2 — dependency / compatibility completeness review

Finding: R13-F1. Derived dependency evidence omitted provider responsibility, consumer responsibility and dependency failure behavior; derived operation evidence omitted operation failure behavior.

Disposition: preserve those fields exactly from the source Product Contract and fail closed if the derived evidence cannot carry them.

### Iteration 3 — security / authority review

Finding: adding responsibility/failure semantics must not turn validation evidence into a security or authority decision.

Disposition: no Authentication, Authorization, permission, Organizational Authority, approval or activation fields added. Required gates remain declarations only; Governed Execution keeps decision/enforcement ownership.

### Iteration 4 — lifecycle / commercial-integrity review

Finding: dependency `provisional` could be misread as capability lifecycle if P5.03 uses it without the canonical catalog context.

Disposition: retain the existing field only as RFC-0004 Product Contract reliance/support qualification, keep capability lifecycle absent from validation evidence, and record the catalog as the lifecycle authority.

### Iteration 5 — compatibility / ADR / public-boundary review

Finding: R13 remediation requires no serialization, version-negotiation protocol, package boundary or public SDK/API commitment.

Disposition: no ADR required. Keep all current representation internal/provisional and explicitly re-open the ADR/governance gate if P5.03 crosses a durable version-negotiation or public-compatibility threshold.

No remaining material objection exists after iteration 5.

## 12. Exit criteria

- [x] Product Contract remains the single governed product/platform boundary source;
- [x] derived declaration validation remains tied to an exact Product Contract Version;
- [x] dependency/operation/version semantics remain exact and inspectable;
- [x] R13-F1 semantic-completeness defect is remediated;
- [x] dependency provider/consumer/failure responsibilities are preserved in derived evidence;
- [x] operation failure semantics are preserved in derived evidence;
- [x] validation/admission evidence grants no Authorization or Organizational Authority;
- [x] Product Contract lifecycle remains separate from Platform Capability lifecycle;
- [x] no capability is promoted or activated;
- [x] no Stable/public serialization, SDK/API, wire, package or registry boundary is created;
- [x] no ADR threshold is crossed by the remediation;
- [x] deterministic R13 regression evidence is committed;
- [x] P5.03 handoff invariants are explicit;
- [x] canonical roadmap, Phase 5 roadmap and README are to be synchronized as part of R13 closure.

## 13. Handoff

R13 closes with `PASS` after remediation of R13-F1.

The next canonical roadmap work item is:

> **`P5.03 — Governed dependency/version resolution + compatibility semantics`.**

P5.03 must consume the exact RFC-0004 Product Contract boundary and the fixed R13 invariants above. It must make dependency/version compatibility decisions explicit rather than guessing them from implementation/package structure, preserve deterministic failure behavior and avoid creating a Stable/public compatibility mechanism without the applicable evidence and governance.
