from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, *, count: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"missing expected closure fragment in {path}: {old[:100]!r}")
    target.write_text(text.replace(old, new, count), encoding="utf-8")


review = '''# P9.09 — Activity, notifications and attention routing

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
'''
(ROOT / "docs/reviews/P9-09-activity-notifications-attention-routing.md").write_text(review, encoding="utf-8")

phase = "docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md"
replace(phase, "Version: `1.10.0`", "Version: `1.11.0`")
replace(
    phase,
    '| **`P9.09`** | **Activity, notifications and attention routing** | **🟨 Current** | human-readable operational timeline/alerts projection |\n| `P9.10` | ООО «Арвектум» organization composition | ⬜ | company-level navigation over products/projects/knowledge/work |',
    '| `P9.09` | Activity, notifications and attention routing | 🟩 Complete / PASS | non-authoritative observed timeline + current attention routing |\n| **`P9.10`** | **ООО «Арвектум» organization composition** | **🟨 Current** | company-level navigation over products/projects/knowledge/work |',
)
replace(
    phase,
    '> **P9.09 — Activity, notifications and attention routing.**\n\nAdd a human-readable operational activity/notification projection that routes attention without turning telemetry, derived timelines or notification delivery into canonical authority. Preserve the P9.04 attention semantics, P9.05 provenance/source distinctions, P9.06 Governed Execution boundary, P9.07 product ownership boundary and P9.08 AI authority/grounding guarantees.\n\nP9.08 is complete within the exact private internal scope. M9 remains open; P9.09–P9.12 and R31/R32 still govern the remaining activity, company composition, dogfooding and hardening work.',
    '> **P9.10 — ООО «Арвектум» organization composition.**\n\nCompose company-level navigation over products, projects, knowledge and work through explicit boundaries without moving product/company semantics into Kernel authority. Preserve Organization scope, source authority, provenance, product ownership and Governed Execution boundaries.\n\nP9.09 is complete within the exact private internal scope. M9 remains open; P9.10–P9.12 and R31/R32 still govern company composition, dogfooding and hardening work.',
)
phase_path = ROOT / phase
phase_text = phase_path.read_text(encoding="utf-8")
if "## 20. P9.09 closure result" not in phase_text:
    phase_text += '''\n\n## 20. P9.09 closure result\n\nStatus: `Complete / PASS` within the exact private internal scope.\n\nP9.09 adds Activity as a non-authoritative observed timeline and current attention-routing surface. Alerts reuse P9.04 My Work semantics; projection timestamps are not represented as canonical Event occurrence; no durable read/unread state, notification authority or new consequential action path is created.\n\nClosure evidence: [`P9-09-activity-notifications-attention-routing.md`](../reviews/P9-09-activity-notifications-attention-routing.md). Final implementation head `c335e293022193de93b349fa5d86325501c74e4f`; Productive Workspace CI `#103` / run `32555963482` and Reference Python CI `#335` / run `32555963477` passed. Workspace release is `p9.09.1`, internal application contract `7`, still `bounded-internal-provisional` and non-public.\n\nNo Product Contract or Platform Capability lifecycle promotion occurred. No email/push channel, durable read receipt, public notification API or customer-facing Production/support commitment is established.\n'''
phase_path.write_text(phase_text, encoding="utf-8")

roadmap = "docs/roadmap/ROADMAP.md"
replace(roadmap, "Version: `2.83.0`", "Version: `2.84.0`")
replace(
    roadmap,
    'Version `2.83.0` closes **`P9.08 — Arvectum AI Copilot + source-grounded organizational assistance`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`P9.09 — Activity, notifications and attention routing`**.',
    'Version `2.84.0` closes **`P9.09 — Activity, notifications and attention routing`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`P9.10 — ООО «Арвектум» organization composition`**.',
)
replace(
    roadmap,
    'P9.08 final implementation/test evidence: head `e5bedffa778cd2487929f826f10359071c1f0b76`; Productive Workspace CI `#90` / run `32553258369` and Reference Python CI `#322` / run `32553258317` passed; functional cross-review completed 3 iterations with no material objection; P9.01 J6 implementation acceptance passed. Product Contracts and Platform Capabilities remain unchanged.',
    'P9.09 final implementation/test evidence: head `c335e293022193de93b349fa5d86325501c74e4f`; Productive Workspace CI `#103` / run `32555963482` and Reference Python CI `#335` / run `32555963477` passed; functional cross-review completed 3 iterations with no material objection after one UI styling remediation. Activity remains a non-authoritative read-side projection, alerts reuse P9.04 attention semantics, and no notification/read-receipt authority is created. Product Contracts and Platform Capabilities remain unchanged.',
)
# The detailed Phase 9 version occurs in both the version note and active-phase section.
roadmap_path = ROOT / roadmap
roadmap_text = roadmap_path.read_text(encoding="utf-8").replace("`Active 1.10.0`", "`Active 1.11.0`")
roadmap_path.write_text(roadmap_text, encoding="utf-8")
replace(
    roadmap,
    '| **`P9.09`** | **Activity, notifications and attention routing** | **🟨 Current** |\n| `P9.10` | ООО «Арвектум» organization composition | ⬜ |',
    '| `P9.09` | Activity, notifications and attention routing | 🟩 Complete / PASS |\n| **`P9.10`** | **ООО «Арвектум» organization composition** | **🟨 Current** |',
)
replace(
    roadmap,
    'P9.09 activity / notifications / attention routing     CURRENT',
    'P9.09 activity / notifications / attention routing     PASS\n        ↓\nP9.10 company organization composition                    CURRENT',
)
replace(
    roadmap,
    'M9-alpha is achieved, and P9.07/P9.08 are now complete. The owner can continue using the Workspace as the primary validation loop while P9.09–P9.12 add activity/notifications, company-level composition, real daily-use dogfooding and final hardening.',
    'M9-alpha is achieved, and P9.07–P9.09 are now complete. The owner can continue using the Workspace as the primary validation loop while P9.10–P9.12 add company-level composition, real daily-use dogfooding and final hardening.',
)
replace(
    roadmap,
    '> **P9.09 — Activity, notifications and attention routing.**\n\nAdd a human-readable operational activity/notification projection that routes attention without turning telemetry, derived timelines or notification delivery into canonical authority. Preserve P9.04 attention semantics, P9.05 provenance/source distinctions, P9.06 Governed Execution, P9.07 product ownership and P9.08 AI grounding/authority boundaries.',
    '> **P9.10 — ООО «Арвектум» organization composition.**\n\nCompose company-level navigation over products, projects, knowledge and work through explicit boundaries without moving product/company semantics into Kernel authority. Preserve Organization scope, source authority, provenance, product ownership and Governed Execution boundaries.',
)
