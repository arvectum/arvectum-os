# P8.09 — External Operator / Developer Integration Runbook

Status: `Validated bounded reference experience`
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

It is a bounded reference procedure, not a universal extension specification. It proves only the exact Creative Test Agent case and the exact versions below. It does **not** define or promise:

- a public or stable SDK/API;
- a platform-owned manifest schema or package format;
- automatic semantic-version compatibility or version negotiation;
- a plugin registry or marketplace;
- general compatibility for arbitrary products or consumers;
- Production/customer readiness, SLA/support or certification;
- `Stable` Product Contract or `Active` Platform Capability status;
- multi-Organization isolation (P8.08 remains `NOT ACTIVATED / NOT PROVEN` for realistic two-Organization operation).

The Python types and helper functions referenced below are internal executable evidence in `reference/python/`. Their names and shapes are not external compatibility promises.

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
| Allowed operation | `p3.08.reconstruct-execution` |
| Operation side effect class | `ReadOnly` |
| Organization scope | `arvectum` |
| Purpose | `creative-test-audit-reconstruction` |
| Required right | `read` |
| Allowed classification | `internal` |
| Required gates | `Authorization`, `DataGovernance` |
| Boundary mechanism | declared Product Contract only |
| Shared mutable state | `false` |
| Enabled by declaration/install | `false` |

Canonical executable pins live in:

- `reference/python/external_creative_ref/onboarding.py`;
- `reference/python/external_creative_ref/contract.py`;
- `reference/python/arvectum_os_ref/external_consumer_onboarding.py`;
- `reference/python/arvectum_os_ref/product_contract_resolution.py`.

If this table disagrees with those reviewed executable artifacts, stop and resolve the drift before relying on the integration.

## 3. Responsibilities

### External product developer

The product side owns:

- its repository and immutable source revision;
- its product-local declaration and declaration format;
- product identity/version and product-owned business semantics;
- Creative Test Agent schemas, scoring, workflows, approvals, reports/UX and model/prompt choices;
- an explicit request for only the platform dependency/operation/scope it needs;
- a new immutable declaration and Product Contract version when the relied-upon boundary changes.

The product must not rely on internal platform tables, undocumented endpoints/imports, private event streams or implicit shared mutable state.

### Platform operator / maintainer

The platform side owns:

- validating the exact Provisional Product Contract boundary;
- resolving the exact dependency contract version against current governed provider evidence;
- enforcing current Organization/purpose/right/classification context and required security/data-governance gates;
- failing closed on missing, ambiguous, deprecated, retired or mismatched dependency evidence;
- preserving provenance, reconstruction limitations and non-authority semantics;
- disabling/removing reliance or requiring a fresh versioned upgrade when the boundary is no longer valid.

Neither side may treat successful onboarding as Authentication, Authorization, Organizational Authority, approval, capability activation or Product Contract stabilization.

## 4. Prerequisites

Before onboarding or revalidation:

1. Use the reviewed Arvectum OS revision containing the P8.06/P8.09 reference evidence and runbook.
2. Verify the external consumer repository is the exact repository above.
3. Verify the source commit and declaration blob SHA exactly; do not rely only on a branch name.
4. Confirm the effective Product Contract Version Identity is exactly the value above and remains `Provisional`.
5. Obtain current governed provider evidence for CAP-004 contract `1.0.0`; do not infer support from Python package/module versions.
6. Establish a current attributable actor and explicit Organization scope.
7. Establish current least-privilege access context: purpose `creative-test-audit-reconstruction`, right `read`, classification `internal`.
8. Confirm required Authorization and DataGovernance gates can be evaluated now.
9. Keep reusable credentials/secrets outside source declarations, Product Contracts, onboarding receipts, logs, prompts and portable evidence.
10. Treat the integration as disabled until exact validation succeeds and current reliance state is explicitly `Onboarded`.

## 5. Reproduce the validated reference path

From `reference/python/`, first run the focused P8.09 proof:

```bash
python -m unittest discover -s tests -p "test_p8_09_external_operator_developer_experience.py" -v
```

Then run the complete reference regression suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The full suite must finish with `OK`. Focused success alone is not closure evidence.

The P8.09 test deliberately rebuilds the same explicit inputs a real integration review must reason about:

1. attributable actor + Organization scope;
2. exact Provisional Product Contract;
3. exact product-owned external source evidence;
4. exact capability-consumption request and least-privilege context;
5. exact governed provider-version evidence;
6. fail-closed onboarding;
7. explicit reliance-state handling.

This executable path is reference evidence only. External consumers must not import `arvectum_os_ref` private/reference modules as a supported public SDK contract.

## 6. Contract and dependency validation procedure

Before any reliance, validate all of the following as one boundary:

- source declaration Organization, product identity/version, dependency, operation, purpose, right and classification exactly match the Product Contract and request;
- the Product Contract is the exact effective immutable version expected by the integration;
- the dependency is declared exactly once;
- CAP-004 contract `1.0.0` has one unambiguous current governed support assertion;
- operation `p3.08.reconstruct-execution` is declared and remains read-only;
- Authorization and DataGovernance gates remain required;
- the declared boundary mechanism remains the Product Contract rather than a private/internal coupling path;
- no shared mutable platform/product state is introduced;
- the external declaration remains disabled by default.

Successful validation produces an `Onboarded` **reliance receipt** in the current reference harness. The receipt is derived point-in-time evidence. It is not a permission, current access grant, authority record, registry entry or lifecycle promotion. Persistent/future use must revalidate the current governed boundary when required by runtime/recovery policy.

## 7. Safe credential and configuration handling

The P8.06/P8.09 bounded CAP-004 case does not require an external system credential to prove onboarding. Do not invent one for the example.

If a future integration requires credentials:

- provision them through an approved secret-management/host configuration path separate from the product declaration and Product Contract;
- scope credentials to the minimum Organization/purpose/operation required;
- never commit reusable secrets, private keys or passwords to either repository;
- never copy secrets into onboarding receipts, compatibility evidence, logs, prompts, exported packages or reconstruction evidence;
- do not assume a recovered/exported integration is active: credentials must be separately reprovisioned and current authorization/data-governance must be re-evaluated;
- revoke credentials separately on termination where applicable.

Configuration is not authority. Possession of a token or endpoint does not establish Authorization or Organizational Authority.

## 8. Evidence and reconstruction inspection

For the validated CAP-004 case, inspect evidence in this order:

1. **Source pin** — repository, source commit, declaration path and blob SHA.
2. **Boundary pin** — product identity/version and Product Contract Version Identity.
3. **Dependency resolution** — exact CAP-004 identity, `1.0.0`, operation and governed provider reference.
4. **Security context** — Organization, purpose, right, classification and required gates.
5. **Reliance receipt** — state plus exact source/contract/provider pins returned by onboarding.
6. **CAP-004 reconstruction result** — a derived evidence view produced only through the declared read-only operation and current access checks.
7. **Provenance/incompleteness** — preserve exact identities/versions, disclosure/redaction constraints and explicit missing/incomplete evidence.

A reconstruction is not source authority, approval or permission and must not mutate canonical state or replay an external effect. Historical replay/reconstruction therefore remains inspection only unless a separate new Governed Execution authorizes a new consequential effect.

For regression evidence, the P8.06 and P8.09 tests cover exact onboarding/dependency behavior; CAP-004 behavior remains covered by the existing reference capability-consumption/reconstruction tests. Do not create a second reconstruction protocol merely for this runbook.

## 9. Predictable fail-closed outcomes

| Condition | Expected result | Operator/developer action |
|---|---|---|
| Nearby provider version exists but exact `1.0.0` support does not | fail closed: version mismatch | publish/review a new immutable Product Contract version if migration is intended; never auto-fallback |
| Exact provider evidence absent | fail closed: unsupported | restore current governed evidence or stop reliance |
| Exact provider version is deprecated | fail closed with migration obligation | follow governed migration obligation; review a new contract/version before reliance |
| Exact provider version is retired | fail closed with migration obligation | stop reliance; migrate only through a new governed boundary |
| Multiple conflicting exact provider assertions | fail closed: ambiguous | repair governance evidence before reliance |
| Product Contract/source/request Organization differs | fail closed | correct the scoped boundary; do not widen Organization access |
| Dependency or operation is undeclared | fail closed | change the Product Contract through a new reviewed version if the need is legitimate |
| Purpose/right/classification exceeds declaration | fail closed | reduce to the declared least-privilege context or review a new boundary |
| Internal table/import/undocumented endpoint/private stream/implicit shared state is requested | fail closed | remove hidden coupling and use an explicit governed boundary |
| Declaration tries to enable reliance by default | fail closed | keep declaration passive; onboarding and current controls decide reliance |
| Integration is `Disabled` or `Removed` | fail closed on use | explicitly re-onboard/review rather than silently re-enable |
| Removal requested while still `Onboarded` | fail closed | disable first, then remove |
| Upgrade reuses old product/source/Product Contract version | fail closed | provide a new consumer version, new immutable source/declaration evidence and new Product Contract version, then re-resolve |
| Current authorization/data-governance cannot be established | fail closed | do not rely on previous receipt or credential possession |

Errors are expected safety behavior. Do not catch and downgrade them into implicit compatibility.

## 10. Upgrade, deprecation and termination

### Upgrade

An upgrade is not an in-place reinterpretation of old evidence. It requires:

1. a new consumer version;
2. a new immutable consumer source commit;
3. a new declaration blob when the declaration changes;
4. a new immutable Product Contract Version Identity;
5. fresh exact dependency resolution against current governed provider evidence;
6. fresh current access/security evaluation;
7. new regression/evidence review appropriate to the changed boundary.

No semver range, nearest-version fallback or source-branch drift is accepted by the validated path.

### Provider deprecation or retirement

Provider support disposition is evidence about an exact dependency version, not Platform Capability lifecycle authority. A deprecated or retired exact dependency fails closed and carries an explicit migration obligation. The consumer may migrate only through a freshly reviewed immutable boundary; deprecation is not permission to select another version automatically.

### Disable and remove

The operational reliance path is intentionally explicit:

`Onboarded → Disabled → Removed`

- `Disabled` blocks use but preserves bounded historical evidence.
- `Removed` requires prior disable.
- these are reliance states only; they are not a new platform or Product Contract lifecycle.

### Termination

On termination:

- disable reliance first;
- remove the optional integration when appropriate;
- revoke separately provisioned credentials/access where applicable;
- preserve or delete evidence according to the governing retention/deletion/classification/purpose rules;
- do not delete or rewrite canonical historical Events merely because the integration ended;
- do not treat later restoration as authorization to resume reliance or replay effects.

## 11. Platform/product responsibility boundary

**Platform-owned/reusable:** exact Product Contract validation, exact governed dependency/version resolution, Organization/access gate preservation, fail-closed hidden-coupling rejection, provenance/reconstruction semantics and explicit reliance-state safety.

**Creative Test Agent-owned:** product declaration format, creative schemas, scoring/rubrics, workflows/approvals, reports/recommendations/UX, model/prompt choices and whether the optional feature is useful to the product.

This example does not justify moving Creative Test Agent business logic into Arvectum OS. A second consumer and separate governed evidence are required before any broader stable/shared abstraction should be inferred.

## 12. Completion checklist for a repeated review

A repeated operator/developer integration review is acceptable only when all are true:

- [ ] external repository and immutable source/declaration pins are verified;
- [ ] exact Product Contract Version Identity and `Provisional` lifecycle are verified;
- [ ] exact dependency identity/version/operation is current and unambiguous;
- [ ] Organization/purpose/right/classification are explicit and least-privilege;
- [ ] Authorization and DataGovernance remain independently enforceable;
- [ ] no private/internal coupling or shared mutable state exists;
- [ ] no secret is embedded in declaration/contract/evidence/logging;
- [ ] onboarding/reliance is not enabled by installation or declaration alone;
- [ ] evidence/reconstruction remains derived, attributable and non-authoritative;
- [ ] documented fail-closed cases behave as expected;
- [ ] disable/remove/upgrade path remains explicit;
- [ ] full repository reference regression suite is green;
- [ ] scope/non-claims are preserved in the review evidence.

A checked list records only the bounded reviewed integration. It does not create a public compatibility or support promise.