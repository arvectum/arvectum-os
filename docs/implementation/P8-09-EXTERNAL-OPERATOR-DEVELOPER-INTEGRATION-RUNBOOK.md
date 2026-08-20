# P8.09 — External Operator / Developer Integration Runbook

Status: `Validated bounded reference experience`
Version: `1.0.0`
Date: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` boundary implications
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Validated consumer: `arvectum/creative-test-agent`
Validated integration: optional read-only Creative Test Agent audit reconstruction through CAP-004
Product Contract lifecycle: `Provisional 0.1.0`
Public/stable surface: `NONE`

## 1. Purpose and claim boundary

This runbook makes the **already validated P8.06 external-consumer integration** repeatable for an operator or developer without exposing or promoting private Arvectum OS internals.

It is a bounded reference procedure, not a universal extension specification. It proves only the exact Creative Test Agent case and exact pins below. It does **not** define or promise a public/stable SDK/API, platform manifest/package format, version negotiation, plugin registry/marketplace, arbitrary-product compatibility, Production/customer readiness, SLA/support/certification, `Stable` Product Contract, `Active` Platform Capability or realistic multi-Organization isolation. P8.08 remains `NOT ACTIVATED / NOT PROVEN` for the latter.

The Python types/helpers referenced in `reference/python/` are internal executable evidence. Their names and shapes are not external compatibility promises.

## 2. Exact validated pins

Do not substitute nearby versions or infer compatibility.

| Item | Exact validated value |
|---|---|
| Consumer repository | `arvectum/creative-test-agent` |
| Consumer source commit | `8dd5aab83beb29be10629f06a2c4e3255e51f06c` |
| Product-owned declaration path | `integrations/arvectum_os_p8_06_onboarding.json` |
| Declaration blob SHA | `67d6e4cfe5f32577c82a3f35aff3c33fe2f71fd3` |
| Declaration owner/status | `arvectum/creative-test-agent` / `product-local-provisional-p8.06-evidence` |
| Consumer identity | `extension:creative-test-agent-audit-reconstruction@arvectum` |
| Consumer version | `0.1.0` |
| Product Contract Version Identity | `product-contract-version:creative-test-agent-audit-reconstruction-pc-v0.1.0@arvectum` |
| Product Contract lifecycle | `Provisional` |
| Platform dependency | `platform-capability:CAP-004@platform` |
| Dependency contract version | `1.0.0` |
| Provider governance reference | `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md:CAP-004:1.0.0` |
| Allowed operation | `p3.08.reconstruct-execution` |
| Side effect class | `ReadOnly` |
| Organization | `arvectum` |
| Purpose / right / classification | `creative-test-audit-reconstruction` / `read` / `internal` |
| Required gates | `Authorization`, `DataGovernance` |
| Boundary mechanism | declared Product Contract only |
| Shared mutable state / enabled by declaration | `false` / `false` |

Executable pins live in `reference/python/external_creative_ref/onboarding.py`, `external_creative_ref/contract.py`, `arvectum_os_ref/external_consumer_onboarding.py` and `arvectum_os_ref/product_contract_resolution.py`. If this table disagrees with reviewed executable evidence, stop and resolve the drift before reliance.

## 3. Responsibilities

### External product developer

The product side owns its repository/source revision, product-local declaration and format, product identity/version and product semantics. Creative Test Agent keeps ownership of creative schemas, scoring/rubrics, workflows/approvals, reports/recommendations/UX and model/prompt choices. It requests only the declared dependency/operation/scope and must publish a new immutable declaration/Product Contract version when that boundary changes.

The product must not rely on platform internal tables, undocumented endpoints/imports, private streams or implicit shared mutable state.

### Platform operator / maintainer

The platform side validates the exact Provisional Product Contract, resolves the exact dependency contract version against current governed provider evidence, enforces current Organization/purpose/right/classification plus security/data-governance gates, preserves provenance/reconstruction limitations and fails closed when current evidence is absent, ambiguous, deprecated, retired or mismatched.

Successful onboarding is not Authentication, Authorization, Organizational Authority, approval, capability activation or Product Contract stabilization.

## 4. Prerequisites

Before onboarding or revalidation:

1. Checkout a reviewed **exact Arvectum OS commit**, not a drifting branch reference; the selected commit must contain this runbook and its P8.06/P8.09 evidence.
2. Verify the external consumer repository, source commit, declaration path and declaration blob SHA exactly.
3. Confirm the exact Product Contract Version Identity remains `Provisional`.
4. Obtain current governed provider evidence for CAP-004 `1.0.0` from the exact governance reference above; do not infer support from package/module/semver proximity.
5. Establish an attributable actor and explicit Organization scope.
6. Establish least privilege: purpose `creative-test-audit-reconstruction`, right `read`, classification `internal`.
7. Confirm Authorization and DataGovernance can be evaluated now.
8. Keep reusable credentials/secrets outside declarations, Product Contracts, receipts, logs, prompts and portable evidence.
9. Treat the integration as disabled until exact validation succeeds and reliance state is explicitly `Onboarded`.

## 5. Reproduce the validated reference path

From `reference/python/`:

```bash
python -m unittest discover -s tests -p "test_p8_09_external_operator_developer_experience.py" -v
python -m unittest discover -s tests -p "test_*.py"
```

The full suite must finish with `OK`; focused success alone is not closure evidence.

The P8.09 proof rebuilds the same explicit boundary inputs: attributable actor/Organization, exact Provisional Product Contract, exact consumer-owned source evidence, exact capability request/least-privilege context, exact governed provider evidence, fail-closed onboarding and explicit reliance states.

This is a reference proof only. External consumers must not import `arvectum_os_ref` private/reference modules as a supported public SDK contract.

## 6. Contract and dependency validation

Before reliance, validate all together:

- source, Product Contract and request match exactly on Organization, product identity/version, dependency/version, operation, purpose, right and classification;
- the Product Contract is the intended exact immutable effective version;
- CAP-004 `1.0.0` has one unambiguous current governed support assertion at the pinned governance reference;
- `p3.08.reconstruct-execution` remains declared and read-only;
- Authorization and DataGovernance remain required;
- only the declared Product Contract boundary is used;
- no hidden shared mutable state exists;
- the product declaration remains disabled by default.

Success produces an `Onboarded` **reliance receipt** in the current reference harness. It is derived point-in-time evidence, not permission, current access, authority, registry state or lifecycle promotion. Persistent/future use must revalidate current governed conditions when required by runtime/recovery policy.

## 7. Safe credential/configuration handling

The bounded CAP-004 case needs no external-system credential to prove onboarding; do not invent one for the example.

If a future integration requires credentials, provision them through an approved secret-management/host configuration path separate from declaration/Product Contract; scope them minimally; never commit or copy reusable secrets/private keys/passwords into repositories, receipts, compatibility evidence, logs, prompts, exports or reconstruction evidence. Recovery/export does not reactivate credentials: credentials must be separately reprovisioned and current authorization/data governance re-evaluated. Revoke separately provisioned credentials/access on termination where applicable.

Configuration is not authority. Token/endpoint possession does not establish Authorization or Organizational Authority.

## 8. Evidence and reconstruction inspection

Inspect in this order:

1. source repository/commit/declaration path/blob SHA;
2. consumer identity/version and Product Contract Version Identity;
3. exact CAP-004 identity/version/operation/provider-governance reference;
4. Organization/purpose/right/classification and required gates;
5. reliance receipt with exact source/contract/provider pins;
6. CAP-004 reconstruction as a derived read-only evidence view under current access checks;
7. provenance, exact identities/versions, disclosure/redaction constraints and explicit incompleteness.

Reconstruction is not source authority, approval or permission. It must not mutate canonical state or replay an external effect. Historical replay/reconstruction remains inspection unless a separate new Governed Execution authorizes a new consequential effect.

P8.06/P8.09 tests cover onboarding/dependency behavior; existing CAP-004 tests cover reconstruction semantics. Do not create a second reconstruction protocol for documentation convenience.

## 9. Predictable fail-closed outcomes

| Condition | Expected result | Action |
|---|---|---|
| Nearby provider version but no exact `1.0.0` support | version mismatch | new reviewed immutable Product Contract if migration is intended; never auto-fallback |
| Exact provider evidence absent | unsupported | restore governed evidence or stop reliance |
| Exact provider deprecated/retired | fail closed + migration obligation | stop/new governed boundary; never auto-select another version |
| Conflicting exact provider assertions | ambiguous | repair governance evidence before reliance |
| Organization differs across source/contract/request | fail closed | correct scoped boundary; never widen access |
| Dependency/operation undeclared | fail closed | new reviewed Product Contract version if legitimate |
| Purpose/right/classification exceeds declaration | fail closed | reduce scope or review a new boundary |
| Internal table/import/endpoint/private stream/implicit state requested | fail closed | remove hidden coupling |
| Declaration enables reliance by default | fail closed | keep declaration passive |
| Reliance state is `Disabled`/`Removed` | use denied | explicit fresh review/onboarding, never silent enable |
| Removal while `Onboarded` | fail closed | disable first, then remove |
| Upgrade reuses consumer/source/Product Contract version | fail closed | new consumer version + source commit + Product Contract version + fresh resolution |
| Current authorization/data governance unavailable | fail closed | previous receipt/credential cannot substitute |

Errors are expected safety behavior; do not catch/downgrade them into implicit compatibility.

## 10. Upgrade, deprecation and termination

### Upgrade

Require a new consumer version, new immutable source commit, new declaration blob when declaration changes, new immutable Product Contract Version Identity, fresh exact provider resolution, fresh access/security evaluation and regression/evidence review. No semver range, nearest-version fallback or branch drift is accepted by the validated path.

### Deprecation / retirement

Provider support disposition is exact dependency-version evidence, not Platform Capability lifecycle authority. Deprecated/retired exact dependencies fail closed with a migration obligation. Migration requires a freshly reviewed immutable boundary.

### Disable / remove

Operational reliance is explicit:

`Onboarded → Disabled → Removed`

`Disabled` blocks use while preserving bounded historical evidence; `Removed` requires prior disable. These are reliance states, not a new Platform Capability or Product Contract lifecycle.

### Termination

Disable, then remove where appropriate; separately revoke credentials/access; apply governing retention/deletion/classification/purpose rules; do not rewrite canonical historical Events; do not treat restoration as authorization to resume reliance or replay effects.

## 11. Platform/product boundary

**Platform-owned/reusable:** exact Product Contract validation; exact governed dependency/version resolution; Organization/access-gate preservation; hidden-coupling rejection; provenance/reconstruction semantics; explicit reliance-state safety.

**Creative Test Agent-owned:** product declaration format; creative schemas; scoring/rubrics; workflows/approvals; reports/recommendations/UX; model/prompt choices; product value decision.

This single case does not justify moving Creative Test Agent business logic into Arvectum OS or inferring a broader stable/shared abstraction. R27 must decide what, if anything, is genuinely reusable; a second consumer is relevant evidence before generalization.

## 12. Repeat-review checklist

- [ ] exact external repository/source/declaration pins verified;
- [ ] exact Provisional Product Contract version verified;
- [ ] exact dependency/version/operation/provider governance evidence current and unambiguous;
- [ ] Organization/purpose/right/classification explicit and least-privilege;
- [ ] Authorization/DataGovernance independently enforceable;
- [ ] no private coupling/shared mutable state;
- [ ] no secret embedded in declaration/contract/evidence/logging;
- [ ] installation/declaration alone does not enable reliance;
- [ ] reconstruction remains derived/attributable/non-authoritative;
- [ ] fail-closed cases behave as documented;
- [ ] disable/remove/upgrade path remains explicit;
- [ ] full reference regression suite green;
- [ ] non-claims preserved.

A checked list records only this bounded reviewed integration. It creates no public compatibility or support promise.
