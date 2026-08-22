# INT-B2 — Functional Cross-Review

Status: `Complete`
Reviewed artifact: [`INT-B2 — Domain-Neutral Connector Boundary Pattern`](../architecture/INT-B2-domain-neutral-connector-boundary-pattern.md) `1.0.0`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Iterations: `3 of maximum 7`
Result: `PASS after bounded reconciliation`

## 1. Review scope

The review tested INT-B2 against Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, INT-B1 and the canonical roadmap, with particular attention to:

- external authority preservation;
- product/platform boundary;
- identity and credential semantics;
- separation of authentication, authorization, Organizational Authority and Data Governance;
- Governed Execution for consequential effects;
- duplicate/retry/replay/uncertainty/reconciliation behavior;
- Event admission and provenance;
- domain-neutrality and avoidance of a speculative generic connector framework;
- lifecycle, portability and termination;
- accidental public/API/capability/commercial commitments.

Functional review is not RFC/ADR acceptance, Product Contract stabilization, Platform Capability promotion or operational-readiness approval.

## 2. Iteration 1 — architecture and authority review

### Findings

1. A shared connector abstraction could accidentally become a universal business-object model.
2. External-system identifiers could be mistaken for Arvectum OS identities.
3. A technically supported external API write could be mistaken for an authorized organizational operation.
4. Timeout/retry behavior could create duplicate external effects if transport failure were interpreted as confirmed no-effect.

### Reconciliation

The reviewed artifact explicitly:

- limits the shared abstraction to the Connector Boundary Envelope;
- keeps 1С/CRM/СЭД/ЭДО business semantics system/product/customer-owned;
- treats external identifiers as governed aliases/references rather than automatic Subject Identities;
- requires explicit operation/effect contracts before writes/effects;
- separates technical credentials from authorization and Organizational Authority;
- introduces outcome uncertainty and reconciliation rather than unsafe blind retry.

Result: material objections closed.

## 3. Iteration 2 — security, execution and event review

### Findings

1. Credential storage could leak reusable secrets into canonical history, logs or AI prompts.
2. Webhooks/source occurrences could be over-promoted into canonical Events.
3. Historical replay could accidentally repeat an external effect.
4. Product reliance could bypass the RFC-0004 Product Contract boundary through adapter internals.

### Reconciliation

The reviewed artifact explicitly:

- makes credentials indirect references and prohibits convenience copying of reusable secrets/private keys/tokens into ordinary canonical state, Events, prompts and logs;
- distinguishes source occurrence/transport receipt from RFC-0006 Event admission;
- prohibits historical replay from repeating external effects without a new authorized Governed Execution;
- requires Product Contracts before governed platform reliance and forbids hidden dependencies on private tables, undocumented endpoints, internal imports, private topics and incidental logs.

Result: material objections closed.

## 4. Iteration 3 — lifecycle, proportionality and anti-overengineering review

### Findings

1. Connector lifecycle terminology could be confused with Platform Capability or Product Contract lifecycle.
2. “Rollback” could falsely imply reversal of an external business effect.
3. INT-B2 could prematurely force a shared runtime, broker, secrets manager, schema registry or SDK.
4. Low-consequence reads could be burdened with unnecessary canonical/runtime state.

### Reconciliation

The reviewed artifact explicitly:

- separates connector implementation/governance state from Platform Capability and Product Contract lifecycle;
- defines connector rollback as implementation/configuration rollback and requires a new governed compensation/reversal action for external effects;
- selects no shared runtime/transport/broker/secrets technology and defines clear ADR triggers for future materially constraining choices;
- permits lighter operational representation for low-consequence reads while preserving attribution and security/data-governance requirements.

Result: no remaining material objection.

## 5. Higher-authority compatibility

- **Constitution 1.2.0:** compatible.
- **RFC-0001:** compatible; external authority and domain-neutral platform boundaries preserved.
- **RFC-0002:** compatible; Identity/Canonical Record/external identifier/version semantics preserved without imposing physical schema.
- **RFC-0003:** compatible; least privilege, secret minimization, Organization scope and authority separation preserved.
- **RFC-0004:** compatible; Product Contract required before governed platform reliance and hidden coupling prohibited.
- **RFC-0005:** compatible; consequential effects use Governed Execution and explicit idempotency/uncertainty/reconciliation semantics.
- **RFC-0006:** compatible; source occurrence is distinct from canonical Event admission and replay is side-effect safe.
- **RFC-0007 / RFC-0008:** no new Knowledge/Memory or document-authority promotion semantics introduced.

No Accepted ADR conflict was found. INT-B2 itself requires no new ADR because it makes no durable shared technology/topology choice.

## 6. Final result

**PASS after bounded reconciliation — 3 of maximum 7 iterations.**

INT-B2 is fit to close as `Complete / architecture baseline`.

Closure does not create an Active Platform Capability, Stable Product Contract, public/stable connector API/SDK, connector marketplace, customer Production scope, SLA/support/certification promise or approval for a concrete external effect.

Next integration-lane action: `INT-B3 — 1С first-candidate design`, constrained to one concrete 1С configuration/deployment and one bounded organizational outcome.
