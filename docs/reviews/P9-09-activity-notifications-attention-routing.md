# P9.09 — Activity, notifications and attention routing

Status: `Complete / PASS`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance`
Predecessor: `P9.08 — Complete / PASS`

## Canonical baseline checked

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- direct task checks: RFC-0003, RFC-0005, RFC-0006;
- ADR-0001 — `Accepted` for the exact Phase 9 Productive Workspace topology;
- canonical roadmap `2.83.0` and Phase 9 roadmap `1.10.0` before closure.

No higher-authority conflict was found. No new RFC, ADR, Product Contract lifecycle transition or Platform Capability promotion is required by this bounded implementation.

## Implemented scope

P9.09 adds an internal Activity surface over already-authorized Productive Workspace projections:

- `Activity` is available in the Workspace navigation;
- current alerts reuse the existing P9.04 My Work groups `decision-required`, `blocked-failed` and `reconciliation-required` rather than defining a competing priority model;
- the timeline aggregates currently visible My Work observations plus current Governed Execution presentation state;
- projection timestamps are explicitly presented as observation times and are not represented as canonical Event occurrence time;
- scenario evidence remains visibly marked as scenario evidence;
- links route only to existing inspectable My Work or Governed Execution context;
- source loading is fail-closed: if a required protected projection cannot be safely revalidated, partial retained activity is not presented;
- no durable read/unread state, acknowledgment authority, email/push delivery channel, approval state, canonical Event, canonical mutation or external effect is introduced;
- Workspace release advances to `p9.09.1`, internal application contract `7`, still `bounded-internal-provisional` with `public_api: false`.

## Functional cross-review

Three iterations were completed, within the maximum of 7.

1. **Architecture / security / governance.** Required non-authoritative read-side semantics, reuse of P9.04 attention taxonomy, no notification authority, no pseudo-Event history, no read/unread canonical state, fail-closed current-source handling, and no new consequential action path.
2. **Product / UX / engineering.** Reviewed the actual PR diff; found one concrete Activity styling defect caused by undefined CSS variables. Replaced it with explicit Workspace-compatible styling and rebuilt committed production assets.
3. **Final implementation review.** Re-read the post-remediation Activity surface, routing, release boundary, tests and changed-file set after independent CI. No material architecture, security, product-boundary, authority, provenance, reproducibility or maintainability objection remains.

Functional cross-review is not RFC/ADR acceptance, lifecycle promotion, owner approval delegation or a public readiness claim.

## Verification evidence

Final implementation head before closure documentation: `c335e293022193de93b349fa5d86325501c74e4f`.

- Productive Workspace CI `#103` / run `32555963482` — `SUCCESS`;
  - BFF security/context tests — PASS;
  - TypeScript typecheck — PASS;
  - frontend interaction tests — PASS;
  - Web Storage rejection gate — PASS;
  - production asset rebuild/reproducibility gate — PASS;
  - release-pinned production asset boundary — PASS.
- Reference Python CI `#335` / run `32555963477` — `SUCCESS`;
  - generated-artifact rejection — PASS;
  - full architecture/reference fitness suite — PASS.
- Bounded implementation/reconciliation workflows also passed backend and frontend suites before the independent gates; temporary helper workflows/scripts are absent from the closure state.

## Explicit limitations

- Activity is not the RFC-0006 canonical Event history or an audit log.
- `observed_at` / projection generation timestamps are not asserted to be business-event occurrence timestamps.
- Alert visibility, ordering and routing grant neither Authorization nor Organizational Authority.
- No email, push, external notification provider, durable inbox, delivery receipt or read/unread persistence is claimed.
- No notification itself can approve, retry, mutate canonical state or repeat an external effect.
- Product-specific notification rules remain product-owned; P9.09 only establishes domain-neutral Workspace composition of existing governed signals.
- This remains private internal bounded evidence; it creates no public/stable API/browser/SDK surface, SLA/support/certification promise, Stable Product Contract, Active Platform Capability or broader conformance claim.
