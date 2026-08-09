# P5.03 — Governed Dependency/Version Resolution + Compatibility Semantics Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform` integration-boundary implementation
Constitution: `1.2.0` — `Ratified`
Architecture basis: RFC-0001 `1.0.0`; RFC-0002 `1.0.0`; RFC-0003 `1.0.0`; RFC-0004 `1.0.0`; RFC-0005 `1.0.0` — `Accepted`
Product Contract under resolution: P4.08 `Provisional 0.1.0`
Preceding engineering gate: R13 — `PASS`
ADR disposition: no threshold crossed by the bounded internal/static resolver
Result: `PASS`

## 1. Purpose

P5.03 makes relied-upon Product Contract dependency versions and compatibility outcomes explicit for the current bounded Phase 5 integration baseline.

The implementation preserves RFC-0004 `ProductContract` as the single executable semantic owner. It adds an internal/provisional static resolver that evaluates the exact dependency declarations from the effective Product Contract against explicit governed provider/version support evidence.

P5.03 deliberately does **not** create:

- a second Product Contract or independently editable dependency manifest;
- semantic-version range inference or automatic nearest-version selection;
- a public/stable version-negotiation or migration protocol;
- a package, module, dataclass or operation-token compatibility contract;
- a runtime registry service;
- an Authorization, Organizational Authority, permission or approval mechanism;
- a Platform Capability lifecycle authority.

## 2. Canonical constraints revalidated

The work was checked against Constitution `1.2.0`, the RFC Index, Accepted RFC-0001 through RFC-0005 where directly relevant, the ADR index, P5.01, P5.02, R13, the P4.08 Provisional Product Contract and the current Phase 5 roadmap.

The implementation preserves these binding semantics:

- Product Contract remains the explicit versioned product/platform boundary;
- exact effective Product Contract Version is preserved before dependency resolution;
- exact dependency identity and declared dependency contract version remain inspectable;
- compatibility is semantic and governed rather than inferred from implementation syntax;
- consequential reliance does not silently advance from one Product Contract or dependency version to another;
- dependency provider responsibility, consumer responsibility and dependency failure behavior remain boundary semantics;
- operation failure behavior remains available from the exact effective Product Contract;
- unsupported, deprecated, retired and ambiguous reliance fails closed deterministically;
- a changed relied-upon dependency boundary creates an explicit migration obligation rather than silent fallback;
- resolution is not Authentication, Authorization, Organizational Authority, Data Governance approval, permission or capability activation;
- Product Contract lifecycle and Platform Capability lifecycle remain independent;
- current Python types remain internal/provisional implementation evidence.

## 3. Implemented baseline

`reference/python/arvectum_os_ref/product_contract_resolution.py` adds the bounded P5.03 resolver.

### 3.1 Governed provider/version evidence

`GovernedDependencyVersionEvidence` represents one explicit support assertion for an exact dependency Identity and contract version together with:

- `Supported`, `Deprecated`, `Retired` or `Unsupported` provider/version disposition;
- a non-empty governance reference identifying the canonical catalog/decision/provider evidence from which the observation was obtained;
- an explicit migration obligation for `Deprecated` and `Retired` versions.

This object is an input snapshot for deterministic resolution. It is **not** a Product Contract source and is **not** Platform Capability lifecycle state. Capability lifecycle remains governed by RFC-0001 and the canonical capability catalog/decisions.

### 3.2 Explicit compatibility decisions

The resolver produces one immutable `DependencyCompatibilityEvaluation` per Product Contract dependency using these explicit outcomes:

- `Compatible`;
- `VersionMismatch`;
- `Unsupported`;
- `Deprecated`;
- `Retired`;
- `Ambiguous`.

Each evaluation preserves from the exact Product Contract:

- exact Product Contract Version pin;
- dependency Identity;
- declared dependency contract version;
- allowed operations;
- provider responsibility;
- consumer responsibility;
- dependency failure behavior;
- operation failure behavior for operations owned by that dependency.

It also records observed governed dependency versions, governance references, reason and any migration obligation.

### 3.3 Exact-only Provisional compatibility rule

The current P4.08 boundary is Provisional and has no approved Stable compatibility policy. Therefore P5.03 uses the smallest safe compatibility rule justified by existing evidence:

> the exact dependency contract version declared by the exact effective Product Contract must have one unambiguous governed `Supported` assertion.

P5.03 does not infer compatibility from SemVer syntax or adjacency. For example, governed evidence for `1.0.1` does not satisfy a Product Contract that declares `1.0.0` unless a new governed Product Contract version or later approved compatibility policy explicitly establishes that reliance.

No automatic fallback version is selected.

## 4. Deterministic failure and migration semantics

The resolver separates inspection from admission:

- `evaluate_product_contract_dependencies()` returns explicit immutable compatibility evidence;
- `resolve_product_contract_dependencies()` admits only `Compatible` evaluations and raises typed fail-closed errors for every other outcome.

Behavior is deterministic:

1. multiple exact support assertions for the same dependency/version → `Ambiguous` → reject;
2. provider evidence exists only for another version → `VersionMismatch` → reject and require a new/reviewed immutable Product Contract version before reliance;
3. no governed evidence for the declared dependency/version → `Unsupported` → reject;
4. exact version explicitly `Unsupported` → reject;
5. exact version `Deprecated` → reject new reliance and surface its migration obligation;
6. exact version `Retired` → reject reliance and surface its migration obligation;
7. exact version `Supported` → `Compatible` only when exact Product Contract continuity also holds.

A migration obligation is evidence about what must be reviewed or changed. P5.03 does not itself mutate Product Contract state, change provider lifecycle or execute migration.

## 5. Exact Product Contract continuity

Every evaluation requires both:

- the source `ProductContract` object; and
- an explicit `effective_product_contract` `GovernedVersionPin`.

The resolver first runs the existing P5.02 declaration validation and then requires the effective pin to equal the source Product Contract's exact immutable version pin.

A stale, newer or different Product Contract Version cannot self-advance through dependency resolution.

The P5.02 validation result remains derived inspection evidence; P5.03 iterates the source RFC-0004 `ProductContract.dependencies` and `ProductContract.operations` rather than treating the validation projection as an independently evolving contract authority.

## 6. R13 invariant preservation

R13-F1 established that downstream tooling must not lose already-declared boundary responsibilities.

P5.03 preserves this invariant directly in every compatibility evaluation:

- dependency provider responsibility;
- dependency consumer responsibility;
- dependency failure behavior;
- operation failure behavior.

This prevents a compatibility report from becoming a narrower competing dependency contract.

## 7. Security, authority and lifecycle separation

Resolution/evaluation objects intentionally contain no fields for:

- Authentication;
- Authorization decision;
- permission grant;
- Organizational Authority decision;
- consequential approval;
- capability lifecycle;
- capability activation.

A `Compatible` result means only that the exact Product Contract dependency/version reliance is compatible with the supplied governed support evidence under the bounded P5.03 rule. Runtime security, authority, data-governance and approval gates remain owned by RFC-0003/RFC-0005 mechanisms.

The provider/version `disposition` in P5.03 is not a Platform Capability lifecycle transition. It cannot promote `Candidate`, `Incubating`, `Active`, `Deprecated` or `Retired` capability lifecycle state and cannot override the canonical capability catalog.

## 8. Stable/public compatibility and ADR review

Result: `PASS — no ADR threshold crossed`.

P5.03 does not select or stabilize:

- a language-specific public SDK/package contract;
- a Product Contract serialization format;
- a public API or wire protocol;
- SemVer/range negotiation as a platform contract;
- a package/extension registry topology;
- a generated-code compatibility boundary;
- a separately deployed resolver or integration service;
- an automatic migration protocol.

The implementation is a static internal Python reference mechanism. If later work relies materially on durable version negotiation, public compatibility ranges, registry behavior or automated migration, the ADR/governance gate must be re-opened before that reliance becomes architectural or externally supported.

## 9. Executable evidence

P5.03 adds:

- `reference/python/tests/test_p5_03_product_contract_dependency_resolution.py`.

The focused suite contains 12 regression/fitness cases covering:

1. exact declared versions resolve only with explicit `Compatible` decisions;
2. R13 provider/consumer/dependency/operation failure semantics are preserved;
3. stale/different effective Product Contract Version fails closed;
4. a nearby `1.0.1` version is not inferred compatible with declared `1.0.0`;
5. missing governed dependency evidence is `Unsupported`;
6. explicitly unsupported exact versions fail closed;
7. deprecated exact versions require migration evidence and fail closed;
8. retired exact versions require migration evidence and fail closed;
9. deprecated/retired support evidence cannot be created without a migration obligation;
10. duplicate exact support assertions are `Ambiguous`;
11. compatibility evidence is not a permission/authority/capability-lifecycle source;
12. the resolver remains static/internal/provisional and does not select SemVer/package/serialization negotiation machinery.

The authored resolver and focused test source passed local Python syntax compilation before repository publication. GitHub read-after-write verification confirmed the committed source/test contents on the P5.03 branch.

PR `#63` was opened for the P5.03 branch. Hosted `Reference Python CI` run **#215** completed successfully for P5.03 head `d36050ae0c9afcae3c950391718eeaaab1834b86`, covering the normal full reference suite including the committed P5.03 and R13 regression evidence.

## 10. Functional cross-review iterations

### Iteration 1 — semantic owner / second-contract-system review

Finding: a standalone dependency manifest, registry-owned dependency state or resolver-owned version lineage would duplicate RFC-0004 Product Contract semantics.

Disposition: rejected. P5.03 consumes the exact `ProductContract` and its immutable version pin; provider/version evidence is an explicit governed observation input only.

### Iteration 2 — compatibility inference review

Finding: using package SemVer, module version, dataclass structure or token spelling as compatibility would convert implementation details into an accidental public/stable contract.

Disposition: use exact declared dependency version plus explicit governed support evidence only. No implicit version range or automatic fallback is implemented.

### Iteration 3 — lifecycle / failure / migration review

Finding: unsupported, deprecated and retired reliance must be distinguishable and deterministic, and a changed relied-upon boundary must not lose migration responsibility.

Disposition: explicit decision enum, typed fail-closed errors and mandatory migration obligations for deprecated/retired evidence; version mismatch records a Product Contract revision obligation.

### Iteration 4 — security / authority / capability lifecycle review

Finding: a successful compatibility decision could be mistaken for runtime admission, permission or provider activation.

Disposition: compatibility evidence contains no Authorization, Organizational Authority, approval or capability-lifecycle fields. Runtime enforcement remains separate; provider lifecycle remains canonical elsewhere.

### Iteration 5 — ADR / public-boundary review

Finding: a static exact-version resolver is reversible and does not require a durable public version-negotiation protocol.

Disposition: no ADR required now. Keep the implementation internal/provisional and re-open the gate if later evidence justifies ranges, registries, automatic negotiation/migration or a public compatibility contract.

No remaining material objection was identified after iteration 5.

## 11. Exit evidence

- exact Product Contract and dependency/version pins are inspectable — `PASS`;
- compatibility decisions are explicit and do not depend on package/module/dataclass versions — `PASS`;
- ambiguous, unsupported, deprecated and retired reliance has deterministic fail-closed behavior — `PASS`;
- migration obligations are explicit when the relied-upon dependency boundary changes or is deprecated/retired — `PASS`;
- R13 provider/consumer/failure semantics remain preserved — `PASS`;
- Product Contract remains the single governed dependency semantic owner — `PASS`;
- dependency resolution grants no Authorization or Organizational Authority — `PASS`;
- capability lifecycle remains external to resolver state — `PASS`;
- no Stable/public negotiation/registry/package/API/wire boundary is created — `PASS`;
- no new RFC or ADR threshold is crossed — `PASS`;
- focused executable regression evidence is committed — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #215`).

## 12. Final disposition

**PASS — P5.03 is complete for the declared internal/provisional governed dependency/version resolution and compatibility-semantics baseline.**

The implementation satisfies the current Phase 5 exit evidence without stabilizing the P4.08 Product Contract, promoting a Platform Capability, establishing production readiness, expanding conformance, or creating public/SLA/support/commercial compatibility commitments.

Next canonical work item after roadmap synchronization:

> **P5.04 — Integration composition API/facade boundary.**
