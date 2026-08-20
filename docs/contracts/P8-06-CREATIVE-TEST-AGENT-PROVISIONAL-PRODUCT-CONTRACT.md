# P8.06 — Creative Test Agent external audit/reconstruction Product Contract

Version: `0.1.0`  
Status: `Provisional`  
Product Contract lifecycle: `Provisional`  
Consumer kind: external extension  
External product owner: ООО «Арвектум»  
Canonical boundary owner: Arvectum OS  
Decision authority: residual Arvectum OS owner under current Accepted governance  
Review point: `P8.06 / R26` or earlier on material boundary change

## 1. Purpose and scope

This Product Contract governs one optional, separately maintained external extension of `arvectum/creative-test-agent` that may request **read-only governed audit/reconstruction** through Arvectum OS CAP-004.

It proves the `P8.06` cross-repository onboarding boundary only. Creative Test Agent remains independently operable when the extension is absent, disabled or removed. The contract does not transfer Creative Test Agent business semantics into the platform and does not create a public SDK/API, registry, marketplace or support commitment.

## 2. Exact identities

- Organization: `organization:arvectum@platform`.
- Product/extension: `extension:creative-test-agent-audit-reconstruction@arvectum`.
- Product version: `0.1.0`.
- Product Contract subject: `product-contract-subject:creative-test-agent-audit-reconstruction@arvectum`.
- Product Contract version: `product-contract-version:creative-test-agent-audit-reconstruction-pc-v0.1.0@arvectum`.
- Product Contract executable schema marker: `p8.06-internal-1`.

The executable representation is `reference/python/external_creative_ref/contract.py`. It is internal reference evidence; its Python types and operation tokens are not a stable public compatibility promise.

## 3. External source evidence

The consumer-owned declaration is pinned to an immutable merged revision:

- repository: `arvectum/creative-test-agent`;
- merge commit: `8dd5aab83beb29be10629f06a2c4e3255e51f06c`;
- declaration path: `integrations/arvectum_os_p8_06_onboarding.json`;
- declaration blob SHA: `67d6e4cfe5f32577c82a3f35aff3c33fe2f71fd3`;
- declaration format owner: `arvectum/creative-test-agent`;
- declaration format status: `product-local-provisional-p8.06-evidence`.

The declaration format is product-owned. Arvectum OS consumes an exact evidence projection of it for this bounded proof; it does not standardize that JSON shape as a platform manifest.

## 4. Exact platform dependency

The Product Contract declares exactly one platform dependency:

- dependency: `platform-capability:CAP-004@platform` — Audit / Reconstruction Support;
- exact capability contract version: `1.0.0`;
- allowed operation: `p3.08.reconstruct-execution`;
- dependency lifecycle treatment: provisional;
- provider evidence reference: `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md:CAP-004:1.0.0`.

Compatibility is static and fail-closed. The current resolver must find explicit governed support evidence for that exact dependency identity and exact contract version. It must not infer compatibility from nearby semantic versions, Python/package versions, module shapes or operation-token similarity, and it must not auto-fallback.

### Provider responsibility

Resolve a read-only reconstruction only from governed evidence while preserving exact identity/version provenance, Organization scope, redaction, deletion/unavailability and incompleteness semantics.

### Consumer responsibility

Supply exact governed references plus current Organization/purpose/right/classification context. Treat reconstruction only as a derived evidence view. Do not infer approval, authorization, Organizational Authority or source truth from the derived view.

### Failure behavior

Fail closed if exact Product Contract continuity, dependency/version/operation compatibility, current governed provider evidence, Organization scope or required access context cannot be established. There is no fallback to internal tables, private modules, private Event streams, undocumented endpoints or implicit shared state.

## 5. Security, authority and least privilege

The bounded request is restricted to:

- Organization: `arvectum`;
- purpose: `creative-test-audit-reconstruction`;
- required right: exactly `read`;
- allowed classification: exactly `internal` for the P8.06 proof;
- required gates: `Authorization` and `DataGovernance`;
- operation side effect: `ReadOnly`;
- direct canonical access declared by the extension operation: none.

Onboarding, declaration possession, Product Contract validation and compatibility resolution grant **no** authentication, authorization, permission, Organizational Authority, approval or lifecycle promotion. Current access remains independently enforced by the owning security/data-governance controls.

Cross-Organization onboarding is rejected by default.

## 6. Product/platform boundary

Allowed boundary mechanism: `DeclaredPlatformContract` only.

Rejected reliance mechanisms:

- internal platform table/store/index access;
- platform-private module/import reliance;
- undocumented internal endpoint reliance;
- private Event stream reliance;
- implicit or hidden shared mutable state.

The extension performs no canonical mutation and creates no competing source of truth.

## 7. Product-owned semantics

The following remain owned by Creative Test Agent and are not promoted into Arvectum OS by this contract:

- creative input and asset schemas;
- audience simulation and scoring semantics;
- brand-safety and rubric configuration;
- creative-test workflows and approvals;
- reports, recommendations and product UX;
- model and prompt choices.

CAP-004 remains domain-neutral audit/reconstruction support. Product compliance interpretation, marketing recommendations and user-facing creative workflows remain outside the platform capability.

## 8. Onboard / disable / remove / upgrade

### Install / declare

The consumer may carry the product-owned declaration. Installation alone does not enable reliance.

### Onboard / enable

Before reliance, Arvectum OS must reconcile the exact external source evidence with this exact Provisional Product Contract, validate the declared capability request and resolve current governed provider/version evidence. Only a complete compatible result produces a derived `Onboarded` receipt.

### Disable

Disable the optional reliance explicitly. A disabled receipt cannot be used as enabled evidence. Disabling does not mutate Creative Test Agent product state or Arvectum OS canonical business state.

### Remove

Removal is permitted only from the explicitly disabled state. No hidden runtime state is required for removal. Applicable governance/audit evidence may remain subject to existing retention/deletion policy; the extension creates no independent retention authority.

### Upgrade

An upgrade requires:

1. the same external repository and consumer identity;
2. a new immutable consumer version;
3. a new immutable external source commit;
4. a new immutable Product Contract Version Identity;
5. a fresh exact governed dependency resolution.

No silent migration, semver inference or auto-fallback is permitted.

## 9. Non-claims

This Product Contract does **not**:

- make CAP-004 `Active` — CAP-004 retains its current governed lifecycle;
- make this Product Contract `Stable`;
- create a public/stable Arvectum OS SDK, API or manifest format;
- create a plugin marketplace, remote registry or package-resolution service;
- make Arvectum OS mandatory for Creative Test Agent core operation;
- grant any authorization, Organizational Authority or consequential approval;
- move Creative Test Agent business schemas/workflows into platform ownership.

## 10. Evidence

- Consumer-side declaration and tests: `arvectum/creative-test-agent` merge commit `8dd5aab83beb29be10629f06a2c4e3255e51f06c`.
- Platform executable contract: `reference/python/external_creative_ref/contract.py`.
- Exact source-evidence pin: `reference/python/external_creative_ref/onboarding.py`.
- Onboarding/resolution boundary: `reference/python/arvectum_os_ref/external_consumer_onboarding.py`.
- Fitness tests: `reference/python/tests/test_p8_06_external_product_extension_onboarding.py`.
- Functional review: `docs/reviews/P8-06-external-product-extension-onboarding-governed-dependency-resolution.md`.

Any later change to the external declaration version, Product Contract version, CAP-004 contract version, operation set, Organization/security scope or product/platform ownership boundary requires review and a new immutable contract/source version as applicable.
