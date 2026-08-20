# P8.06 — External product/extension onboarding + governed dependency resolution

Status: `Complete / PASS`  
Date: `2026-08-20`  
Task classification: `product_contract` with `platform` and `governance`  
Constitution: `1.2.0` (`Ratified`, frozen)  
Accepted architecture checked: RFC-0001, RFC-0003, RFC-0004; Phase 3 CAP-004 provisional contract; Platform Capability Candidate Catalog  
Accepted ADRs relevant to this boundary: none  
Owner: ООО «Арвектум»

## 1. Review outcome

P8.06 is `Complete / PASS` for one concrete, separately maintained external consumer: the `arvectum/creative-test-agent` repository.

The proof demonstrates that an optional Creative Test Agent audit/reconstruction extension can be onboarded only through an exact Provisional Product Contract and exact governed CAP-004 dependency/version/operation evidence, without private platform coupling or hidden shared mutable state.

No material objection remains after functional cross-review.

This review is functional evidence only. It is not formal approval of a Stable Product Contract, Platform Capability promotion, public API/SDK, operational-readiness expansion, conformance expansion or commercial support commitment.

## 2. Qualifying external consumer evidence

The consumer was not fabricated inside `arvectum/arvectum-os`.

Consumer repository:

- repository: `arvectum/creative-test-agent`;
- consumer kind: external extension;
- owner: ООО «Арвектум»;
- extension identity: `extension:creative-test-agent-audit-reconstruction@arvectum`;
- extension version: `0.1.0`;
- purpose: optional read-only governed audit/reconstruction support for Creative Test Agent operations.

Consumer-side evidence was merged independently before the Arvectum OS source pin was finalized:

- consumer PR: `arvectum/creative-test-agent#2`;
- merge commit: `8dd5aab83beb29be10629f06a2c4e3255e51f06c`;
- declaration path: `integrations/arvectum_os_p8_06_onboarding.json`;
- declaration blob SHA: `67d6e4cfe5f32577c82a3f35aff3c33fe2f71fd3`;
- declaration format owner: `arvectum/creative-test-agent`;
- declaration status: `product-local-provisional-p8.06-evidence`;
- consumer-side CI: `success`.

The product-owned declaration is intentionally not treated as a stable platform manifest schema.

## 3. Product Contract resolution

Canonical contract evidence:

- [`P8-06-CREATIVE-TEST-AGENT-PROVISIONAL-PRODUCT-CONTRACT.md`](../contracts/P8-06-CREATIVE-TEST-AGENT-PROVISIONAL-PRODUCT-CONTRACT.md);
- executable contract: `reference/python/external_creative_ref/contract.py`.

Contract state:

- Product Contract lifecycle: `Provisional`;
- Product Contract version: `0.1.0`;
- exact Product Contract Version Identity: `product-contract-version:creative-test-agent-audit-reconstruction-pc-v0.1.0@arvectum`;
- exact platform dependency: `platform-capability:CAP-004@platform`;
- exact dependency contract version: `1.0.0`;
- exact allowed operation: `p3.08.reconstruct-execution`;
- operation side effect: `ReadOnly`;
- direct canonical accesses declared by the extension operation: none;
- required gates: `Authorization`, `DataGovernance`.

The existing P5.03 resolver remains the semantic dependency-resolution mechanism. Compatibility is exact and static: nearby versions are not inferred compatible and no fallback version is automatically selected.

## 4. External source reconciliation

`reference/python/external_creative_ref/onboarding.py` pins the exact merged external source revision and declaration blob.

`reference/python/arvectum_os_ref/external_consumer_onboarding.py` then reconciles the consumer-owned source evidence with:

1. the exact Product Contract;
2. the exact consumer identity/version and Organization;
3. the exact CAP-004 dependency/version/operation;
4. the current least-privilege access context;
5. current governed provider/version evidence.

Successful resolution produces only a derived onboarding receipt. The receipt is not permission, authorization, Organizational Authority, approval, canonical truth or capability lifecycle state.

## 5. Least privilege and Organization boundary

The bounded proof requires exactly:

- Organization: `arvectum`;
- purpose: `creative-test-audit-reconstruction`;
- right: `read`;
- allowed classification: `internal`;
- required gates: `Authorization`, `DataGovernance`.

The implementation fails closed on:

- cross-Organization source/contract/request mismatch;
- excessive or changed rights/classification scope;
- undeclared dependency;
- undeclared operation;
- incompatible provider version;
- missing/ambiguous/unsupported/deprecated/retired governed provider evidence through the existing resolver;
- Product Contract Version continuity mismatch.

Onboarding does not grant authentication, authorization, Organizational Authority or approval.

## 6. Hidden-coupling rejection

The only admitted mechanism is `DeclaredPlatformContract`.

Fitness evidence rejects:

- internal platform table access;
- internal/private module reliance;
- undocumented endpoint reliance;
- private Event stream reliance;
- implicit shared state;
- any explicit hidden shared mutable state attestation.

The onboarding layer itself remains static/in-process reference evidence and imports no HTTP/network client, semantic-version negotiation package or remote registry client. It selects no marketplace, package manager, registry service, transport or deployment topology.

## 7. Install / onboard / disable / remove / upgrade

The external product declaration is disabled by default. Mere installation/declaration does not activate reliance.

The bounded operational reliance states are intentionally named `Onboarded`, `Disabled`, and `Removed` and are represented as **reliance state**, not as a third governed lifecycle model.

- `Onboarded`: exact source + Product Contract + dependency resolution passed.
- `Disabled`: reliance is explicitly stopped; the receipt cannot be used as enabled evidence.
- `Removed`: permitted only after `Disabled`; no hidden shared runtime state is required.
- `Upgrade`: requires the same repository/consumer identity, a new immutable consumer version, a new immutable source commit, a new Product Contract Version Identity, and a fresh exact governed dependency resolution.

No semantic-version inference, silent migration or automatic fallback is permitted.

## 8. Product-specific ownership

Creative Test Agent retains ownership of:

- creative input and asset schemas;
- audience simulation and scoring semantics;
- brand-safety and rubric configuration;
- creative-test workflows and approvals;
- reports, recommendations and product UX;
- model and prompt choices.

No product-specific schema or workflow was moved into CAP-004 or other Arvectum OS platform semantics.

CAP-004 remains domain-neutral audit/reconstruction support.

## 9. Functional cross-review iterations

### Iteration 1 — external declaration identity completeness

Material objection: the initial machine-checkable consumer declaration pinned CAP-004 namespace/id/version but left the dependency scope only in human-readable documentation.

Revision: added exact `dependency_scope = platform` and a consumer-side regression assertion.

Disposition: resolved.

### Iteration 2 — external boundary / ownership / unsupported claims

Reviewed the consumer PR after the scope fix for hidden platform imports, private coupling, exact dependency/version/operation, reversible removal/upgrade, product ownership and lifecycle/public-surface overclaim.

Disposition: no material objection. Consumer CI passed and `arvectum/creative-test-agent#2` was merged before the OS source pin was finalized.

### Iteration 3 — lifecycle terminology

Material objection: the first OS implementation called `Onboarded / Disabled / Removed` an `ExternalConsumerLifecycle`, which risked conflation with the governed Product Contract lifecycle and Platform Capability lifecycle.

Revision: renamed the concept to `ExternalConsumerRelianceState` and changed the receipt field to `state`; regression evidence explicitly forbids a `lifecycle` field on the receipt.

Disposition: resolved.

### Iteration 4 — security / authority / Organization scope

Reviewed least privilege, cross-Organization denial, access-context continuity and authority non-creation.

Disposition: no material objection. Authentication/authorization/Organizational Authority remain distinct, and onboarding does not grant any of them.

### Iteration 5 — compatibility / failure / upgrade semantics

Reviewed exact dependency version handling, unsupported nearby versions, hidden coupling, source pinning, disable/remove ordering and immutable upgrade requirements.

Disposition: no material objection. Resolution remains exact and fail-closed, with no semver inference or fallback.

### Iteration 6 — final code-health and governance consistency

Reviewed the post-revision implementation against Constitution/RFC/product-platform boundaries and the Phase 8 acceptance criteria. Full reference CI passed on the revised head.

Disposition: no material objection.

## 10. Executable evidence

Platform files:

- `reference/python/arvectum_os_ref/external_consumer_onboarding.py`;
- `reference/python/external_creative_ref/contract.py`;
- `reference/python/external_creative_ref/onboarding.py`;
- `reference/python/tests/test_p8_06_external_product_extension_onboarding.py`.

The P8.06 test file adds 13 focused fitness tests. The preceding P8.05 repository baseline was `1235 tests / OK`; no existing tests were removed, so the resulting reference suite is `1248 tests / OK` when the P8.06 head passes the full `python -m unittest discover -s tests -v` workflow.

CI evidence:

- `arvectum/creative-test-agent`: consumer-side PR head CI — `success`;
- `arvectum/arvectum-os`: `Reference Python CI` run `186` on post-review head `3de800eb90fb6db8f4eb5ce44ebc95d8e359820d` — `success`.

## 11. Explicit non-claims

P8.06 does not:

- promote CAP-004 from `Incubating / Provisional` to `Active`;
- promote the Product Contract from `Provisional` to `Stable`;
- create a public/stable Arvectum OS SDK, API or manifest format;
- create a plugin marketplace, remote registry or package-resolution service;
- make Arvectum OS mandatory for Creative Test Agent core operation;
- add a second Organization or prove multi-Organization production isolation;
- expand external/customer Production readiness, conformance, SLA/support or commercial guarantees.

## 12. Gate conclusion

`P8.06 = Complete / PASS`.

The acceptance criteria are met with a real separately maintained external consumer, exact Provisional Product Contract and dependency resolution, explicit least-privilege Organization-scoped access, fail-closed negative paths, no private coupling/shared state, reversible reliance handling and preserved product ownership.

The next canonical roadmap action is `R26 — Cross-Organization Security / Integration Health Review`.
