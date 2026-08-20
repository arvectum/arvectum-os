# P8.02 — Identity, Trust, Rights and Data-Governance Boundary

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Phase: `Phase 8 — Active`
Predecessor: [`P8.01`](P8-01-eis-revalidation-target-evidence-baseline.md)
Activation decision: [`DECISION-2026-08-20-PHASE-8-ACTIVATION`](../governance/decisions/DECISION-2026-08-20-PHASE-8-ACTIVATION.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — the active EIS validation has a deny-by-default identity/trust/rights/data-governance boundary suitable for P8.03 contract publication.**

The roadmap label is cross-Organization because Phase 8 must make that boundary explicit. This specific activated case includes **one Organization only** and does not claim cross-Organization validation.

## 2. Governing Organization and tenant scope

Governing Organization: `ООО «Арвектум»`.

Technical isolation:

- use the existing M7 owner-operated Organization/tenant context;
- the local runtime must resolve the Organization unambiguously before governed reliance;
- opaque local Organization/Principal identifiers remain runtime configuration/evidence and are not turned into public contracts;
- no second Organization may be introduced by reusing the same email, token, product account or external identifier.

Cross-Organization default: `DENY`.

## 3. Identity model

| Referent | Identity treatment |
|---|---|
| `ООО «Арвектум»` | governing Organization |
| owner/operator | Arvectum human Principal/Actor within the explicit Organization context |
| local Tender Operator service/process | attributable service/workload Principal where applicable |
| ЕИС / `zakupki.gov.ru` | external system identity/reference |
| notice `0344100006426000005` | external EIS namespace identifier / alias, not automatic Arvectum Subject Identity |
| EIS credential/token identity | authentication reference only; not authorization or authority |
| P6 observation | immutable historical governed reference/evidence |
| P8 fresh observation | separate later governed reference/evidence |

Identity resolution never grants permission or Organizational Authority by itself.

## 4. Authentication and trust

### EIS server trust

Required:

- verified TLS;
- hostname verification enabled;
- certificate verification enabled;
- no fallback to insecure TLS or disabled verification;
- any system-truststore remediation must preserve verification and remain owner-operated.

### EIS caller authentication

Where the product path requires the existing individual-person token or equivalent credential:

- the credential remains in the approved local secret mechanism;
- raw secret/token values must not be admitted to canonical records, Git, ordinary logs, prompts or evidence bundles;
- only minimized non-secret evidence of the authentication context may be retained when needed for reconstruction;
- the token's existence or success does not establish authorization, Organizational Authority or legal rights beyond the bounded operation.

### Platform authentication

The local Arvectum Actor/service must use the already approved M7 least-privilege identity/access path for the owner-operated contour. P8.02 selects no new IAM provider or protocol.

## 5. Authorization

Allowed operation set:

1. resolve/read the exact Phase 8 Provisional integration contract and required platform dependency versions;
2. perform the declared product-owned read-only EIS retrieval for one selected notice during the bounded P8.04 attempt;
3. compute local exact integrity/comparison evidence;
4. admit/preserve only the governed records/events/references explicitly required by the contract;
5. reconstruct/read the completed or failed execution evidence.

Denied operation set:

- EIS/ETP mutation;
- bid/application submission;
- signing;
- unrelated broad credential use;
- supplier/customer communication;
- cross-Organization read/write;
- public redistribution;
- bypass of contract/version or evidence preflight;
- runtime access to product/platform internals not declared by contract.

Authorization is deny-by-default and limited to the explicit resource/operation/Organization scope.

## 6. Organizational Authority

- Owner authority is required for the Phase 8 activation and any material widening of this scope.
- The approved A8 decision authorizes the bounded Phase 8 program, not arbitrary EIS operations.
- P8.04 local execution may be initiated by the attributable owner/operator within the approved envelope.
- No service, Product Contract, token, AI component or connector receives Organizational Authority merely through technical capability.
- Any proposed mutation, signature, customer commitment, second Organization or accepted rights exception must escalate to a new owner/governance decision before execution.

The `Proposed 0.2.1` Decision Authority Policy remains informative only; residual authority remains with owner.

## 7. Data Governance

### Purpose

Only: external-authority freshness/version-drift validation for the selected EIS notice.

### Collection/minimization

Collect only what is required for exact comparison and governed reconstruction:

- external source/notice identifiers;
- observation time;
- material document identifiers/names when necessary;
- byte size/hash/integrity metadata;
- comparison result;
- required contract/workflow/execution/event/provenance references.

Raw document/archive bytes stay owner-local unless a later explicit decision requires otherwise.

### Classification

The source material is treated as external public procurement-source material within the bounded retrieval contour, while secrets, local paths and private runtime identifiers retain stricter handling. Public accessibility is not used as a proxy for unlimited reuse rights.

### Disclosure / sharing

- internal owner-operated evidence use only;
- no cross-Organization sharing;
- no customer-facing redistribution;
- no public evidence package containing unnecessary raw source content;
- any future disclosure requires a separate rights/purpose check.

### Retention / deletion

- preserve minimized governed comparison/reconstruction evidence according to existing internal governance needs;
- raw owner-local artifacts may be deleted under the applicable retention rules when no longer needed;
- retained canonical history must honestly expose when underlying raw content is no longer available;
- deletion/minimization never rewrites already admitted historical facts.

### Export

A repository/governance export may contain minimized metadata and immutable references only. Reusable credentials/private keys are always omitted and must be reprovisioned separately.

## 8. Rights boundary

Current canonical evidence supports only a narrow internal read-only technical validation contour. It does not establish a comprehensive legal opinion or general EIS redistribution/service right.

Therefore unresolved rights remain explicitly denied for:

- redistribution;
- external customer delivery of source content;
- cross-Organization reuse;
- automated mutation/submission/signature;
- public stable connector service;
- support/availability commitments.

If the local P8.04 attempt requires any such widening, it must stop rather than silently expand scope.

## 9. Privileged/support-access boundary

- No ambient admin access to all product/platform content is created.
- Local troubleshooting may use owner-approved privileged access only within the existing M7 contour and must preserve attribution.
- Support/debug access must not expose secrets into Git, canonical payload or model prompts.
- No external support party is introduced by this case.

## 10. Failure-closed matrix

| Unresolved condition | Required behavior |
|---|---|
| Organization/tenant ambiguous | deny / stop |
| Actor/service identity unavailable | deny / stop |
| TLS verification cannot be established | fail closed |
| credential/authentication fails | fail closed |
| authorization exceeds read-only notice scope | deny |
| rights/purpose need widening | stop for governance decision |
| secret would need canonical persistence | refuse / redesign |
| source authority cannot be preserved | fail / no Native substitution |
| cross-Organization access requested | deny unless separately governed |
| evidence path cannot reconstruct exact observation | incomplete / fail closed |

## 11. Cross-review

### Iteration 1 — security

No new IAM/auth protocol was introduced; trust and secret controls remain bounded to the existing owner-operated contour.

### Iteration 2 — authority

Authentication, Authorization and Organizational Authority are explicitly separate; A8 does not become an unlimited operation grant.

### Iteration 3 — data governance

Public accessibility is not treated as unlimited rights; disclosure/export and retention remain minimized and purpose-bound.

### Iteration 4 — cross-Organization semantics

The document states explicitly that only one Organization is validated. Phase 8 activation does not imply multi-Organization evidence.

**Result:** `PASS`; no material objection remains.

## 12. Handoff

P8.02 exit criteria are satisfied.

Next canonical action:

> **P8.03 — External Product Contract / integration-contract boundary + stable-surface disposition.**
