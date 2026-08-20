# P8.00-A5 — Platform-Responsibility Necessity Test

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Roadmap work item: `P8.00-A5 — Platform-responsibility necessity test`
Selected outcome: [`P8.00-A3`](P8-00-A3-bounded-external-outcome-selection.md)
Boundary map: [`P8.00-A4`](P8-00-A4-organization-authority-data-rights-map.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**Disposition: `PLATFORM_REQUIRED`, narrowly scoped.**

Platform responsibility is required for the **governed external-authority reliance envelope** around the selected EIS revalidation outcome.

Platform responsibility is **not** justified for the EIS connector, procurement discovery logic, SOAP details, archive parsing or Tender Operator business semantics. Those remain product-owned.

## 2. Necessity test

### 2.1 Reuse across products/integrations

Current evidence does not yet prove repeated EIS-specific reuse across products. This criterion alone is insufficient.

However, the selected pressure is not EIS-specific: any product that relies consequentially on an external authoritative system needs domain-neutral semantics for external authority, observation freshness, exact-version reliance, provenance, stale/unavailable evidence and reconstruction.

**Result:** supportive strategically, but not the sole basis.

### 2.2 Shared identity/security/Organization isolation

The selected case uses one Organization only, so multi-Organization isolation is not the activation justification.

Shared platform semantics are still required to keep Organization scope, Actor attribution, authorization, Organizational Authority and data-governance evaluation distinct from product credentials and external identifiers.

**Result:** materially relevant but bounded.

### 2.3 Shared provenance/reconstruction safety

This criterion is materially true.

A later governed execution must be able to distinguish:

- the P6 external observation;
- the fresh Phase 8 external observation;
- the external authority that each observation represents;
- exact source/document evidence relied upon;
- observation/freshness time;
- change/no-change comparison result;
- missing/stale/ambiguous evidence;
- the immutable historical execution that relied on an earlier observation.

If these semantics exist only in Tender Operator local tables/logs, Arvectum OS cannot reconstruct consequential platform-backed reliance without hidden product coupling.

**Result:** `YES`.

### 2.4 Governed portability/interoperability

The experiment does not yet require a customer handover format. But preserving semantic authority/freshness/provenance independent of the current EIS adapter and local file layout is required by the Accepted architecture.

**Result:** relevant at the semantic level; no stable external export format required now.

### 2.5 Hidden-coupling risk

This criterion is materially true.

Without a platform-governed envelope, later Arvectum OS executions could implicitly depend on:

- product-local cache/current-state assumptions;
- transient EIS retrieval timestamps;
- local manifest formats;
- private file paths;
- product logs;
- unversioned source freshness decisions.

That would make product-local implementation details an undeclared platform dependency.

**Result:** `YES`.

### 2.6 Constitutional / Accepted RFC invariants

This criterion is materially true.

Accepted architecture requires Arvectum OS to preserve:

- external authoritative source rather than creating competing truth;
- exact versions for consequential reliance;
- Organization/authority boundaries;
- provenance and reconstructability;
- explicit incomplete/uncertain evidence;
- Document/Artifact external authority and exact-version semantics where applicable.

The platform must therefore own the domain-neutral governance semantics of reliance even when the connector stays in the product.

**Result:** `YES`.

## 3. Exact responsibility split

### Platform-owned responsibility

Arvectum OS is responsible for the reusable governed semantics needed to:

- identify the external authority and authority mode;
- represent a time-bounded external observation/reference;
- preserve or reference exact materially relied-upon source/document evidence;
- attribute observation/freshness/provenance to an Execution Context;
- distinguish historical observations from later observations;
- expose stale/missing/ambiguous evidence honestly;
- reconstruct which exact observation/version a governed execution relied upon;
- prevent later source change from rewriting historical governed evidence.

This responsibility should reuse existing Kernel/RFC semantics and Incubating capabilities where sufficient; A5 does not create a new Platform Capability automatically.

### Product-owned responsibility

Tender Operator remains responsible for:

- EIS discovery and retrieval implementation;
- SOAP method selection and request details;
- EIS-specific token handling within approved secret controls;
- archive download/extraction implementation;
- procurement-domain document expectations;
- tender/document business semantics;
- procurement workflow and UX;
- product-specific retry/network behavior beyond the explicit shared contract;
- product-local caches and diagnostics.

## 4. Why `PRODUCT_LOCAL` is insufficient

A purely product-local implementation can fetch and compare files, but it cannot satisfy the Phase 8 objective if Arvectum OS later relies on the result without an explicit governed boundary.

Keeping **all** freshness/version/provenance semantics product-local would either:

1. force Arvectum OS to trust undocumented product-local state; or
2. make product logs/manifests/private internals de facto platform contracts.

Both outcomes violate the explicit-contract and reconstructability direction of Accepted RFC-0001/RFC-0004/RFC-0006/RFC-0008.

## 5. Why this is not connector platformization

`PLATFORM_REQUIRED` applies to the governance envelope, not the adapter.

A5 explicitly rejects:

- generic EIS connector capability admission;
- platform-owned procurement parsing;
- universal government connector abstractions;
- public/stable connector protocols;
- migration of Tender Operator source code into Arvectum OS merely for reuse optics.

If later evidence shows that the existing platform envelope cannot support the outcome without EIS-specific special cases, the correct response is to contain or revise the boundary, not to force product logic into the platform.

## 6. Lifecycle effect

None.

A5 does not:

- create a `Candidate` capability;
- promote CAP-001 through CAP-004;
- make a Product Contract `Stable`;
- establish Production or external support;
- approve a public interface.

## 7. Cross-review

### Iteration 1 — platform architecture

**Finding:** `PLATFORM_REQUIRED` could be overread as connector ownership.

**Revision:** responsibility split now names only domain-neutral external-authority/freshness/provenance/reconstruction semantics as platform-owned.

### Iteration 2 — product

**Finding:** procurement-specific document-set expectations belong to Tender Operator.

**Revision:** document expectation, SOAP/archive and procurement semantics remain explicitly product-owned.

### Iteration 3 — proportionality

**Finding:** the outcome might motivate a new capability prematurely.

**Revision:** A5 requires reuse of existing Kernel/RFC/capability semantics first and creates no capability lifecycle transition.

**Result:** `PASS`; no material objection remains.

## 8. Handoff

A5 exit criterion is satisfied with `PLATFORM_REQUIRED` for the narrow governed reliance envelope.

Next canonical action:

> **P8.00-A6 — Stable/readiness/ADR gate scan.**
