# INT-B4 — Functional Cross-Review

Status: `Complete`
Reviewed artifact: [`INT-B4 — CRM Designs`](../architecture/INT-B4-crm-designs.md) `1.0.0`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Iterations: `3 of maximum 7`
Result: `PASS after bounded reconciliation`

## 1. Review scope

The review tested INT-B4 against Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, INT-B1, INT-B2, INT-B3 and the canonical roadmap.

Review focus:

- keeping Битрикс24 and amoCRM as separate concrete designs;
- preserving external CRM authority;
- vendor-specific authentication and account/portal scope;
- least privilege and secret handling;
- external identity mapping;
- bounded read-first operation scope;
- webhook/source-occurrence semantics;
- product-owned CRM interpretation;
- Product Contract boundary;
- write-side admission controls;
- failure/reconciliation/termination;
- ADR triggers and avoidance of premature CRM platformization.

Functional review is not RFC/ADR acceptance, Product Contract stabilization, Platform Capability promotion, security certification or operational-readiness approval.

## 2. Iteration 1 — system separation and authority review

### Findings

1. A common “CRM connector” could collapse materially different authentication, API and business semantics.
2. Pipeline/stage concepts could be falsely normalized across Битрикс24 and amoCRM.
3. Workspace attention labels derived from CRM data could be mistaken for CRM-authoritative state.
4. External entity IDs could be reused incorrectly as Arvectum Subject Identities.

### Reconciliation

The artifact explicitly:

- defines separate Bitrix24 and amoCRM connector designs;
- shares only the INT-B2 governance envelope;
- keeps pipeline/stage/custom-field/task semantics vendor/account/product-owned;
- keeps both CRM systems authoritative for their declared source data;
- treats Arvectum attention/prioritization as product/native interpretation rather than vendor truth;
- treats vendor IDs as external aliases/references scoped to the bound portal/account.

Result: material objections closed.

## 3. Iteration 2 — security, webhooks and mutation review

### Findings

1. Bitrix24 incoming-webhook credentials can carry user-context permissions and could be overprivileged.
2. amoCRM OAuth tokens/scopes could be mistaken for Organizational Authority.
3. Vendor APIs expose write methods, creating a risk that implementation would admit mutations by transport capability rather than governance decision.
4. Webhook delivery could be over-promoted into canonical Event state or trusted as a complete source of truth.
5. Subscription creation/deletion is itself an external administrative mutation.

### Reconciliation

The artifact now:

- requires dedicated least-privilege integration contexts and indirect secret references;
- states that credentials/API permission/scopes do not establish Organizational Authority;
- enumerates read-first business operations and explicitly excludes business writes;
- treats webhook delivery as source occurrence requiring normal Event admission/reconciliation rules;
- classifies amoCRM webhook subscribe/unsubscribe as explicit `manage_subscription` administrative operations, not reads;
- requires a separate write-side admission process before any future CRM mutation.

Result: material objections closed.

## 4. Iteration 3 — product/platform, lifecycle and proportionality review

### Findings

1. A Product Contract could be required too early merely because architecture designs exist.
2. Failure/pagination semantics could allow partial CRM state to appear complete/current.
3. Connector disable/termination could be confused with deletion of authoritative CRM data or historical Arvectum evidence.
4. A shared OAuth worker/webhook runtime/common CRM DTO could be accidentally fixed without ADR/evidence.

### Reconciliation

The artifact explicitly:

- requires Product Contract before governed product/shared-platform reliance, not for retention of design documents;
- exposes freshness, incomplete pagination, stale/unavailable and webhook-gap states;
- defines termination as stopping integration/revoking credentials/unsubscribing/removing non-authoritative caches while leaving CRM authority untouched and preserving lawful historical attribution;
- makes shared runtime/token-store/webhook-ingress/common DTO choices explicit ADR triggers rather than INT-B4 decisions.

Result: no remaining material objection.

## 5. External feasibility evidence review

Official vendor documentation checked on `2026-08-22` supports the bounded feasibility assumptions:

- Bitrix24 REST supports portal-specific HTTP methods, incoming-webhook and OAuth authorization, user-context permissions, and CRM deal listing;
- amoCRM API v4 exposes CRM entities/tasks, OAuth 2.0 is the current integration authorization model, and webhook subscriptions are supported through API v4.

Vendor documentation is evidence only and does not override Arvectum OS governance. Exact portal/account features, tariffs, fields, permissions, limits and event behavior remain deployment-discovery requirements.

## 6. Higher-authority compatibility

- **Constitution 1.2.0:** compatible; domain boundaries, external authority, security and proportionality preserved.
- **RFC-0001:** compatible; no competing source of truth and no speculative generic CRM capability admitted.
- **RFC-0002:** compatible; vendor IDs remain aliases/references and no physical schema is prescribed.
- **RFC-0003:** compatible; least privilege, secret minimization, Organization scope and authority separation preserved.
- **RFC-0004:** compatible; Product Contract required before governed platform reliance and hidden coupling prohibited.
- **RFC-0005:** compatible; business writes are not admitted; future external mutations require explicit Governed Execution/effect semantics.
- **RFC-0006:** compatible; webhook deliveries are source occurrences, not automatic canonical Events; replay does not repeat effects.
- **RFC-0007 / RFC-0008:** no automatic Knowledge/Memory or document-authority promotion introduced.

No Accepted ADR conflict was found. No new ADR is required because the design uses vendor-specific APIs without selecting a shared connector runtime/topology.

## 7. Final result

**PASS after bounded reconciliation — 3 of maximum 7 iterations.**

INT-B4 is fit to close as `Complete / concrete integration design baseline`.

Closure does not create a generic CRM connector/schema, Stable Product Contract, Active Platform Capability, public API/SDK, customer Production scope or authorization for CRM business mutations.

Next integration-lane action: `INT-B5 — СЭД/ECM/ЭДО design`, beginning from named concrete deployment/provider profiles and preserving document/signature/retention authority.
