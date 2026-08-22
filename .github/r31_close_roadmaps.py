from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, *, count: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != count:
        raise RuntimeError(f"{path}: expected {count} matches, found {actual}: {old[:140]!r}")
    target.write_text(text.replace(old, new, count), encoding="utf-8")


def append_once(path: str, marker: str, text: str) -> None:
    target = ROOT / path
    current = target.read_text(encoding="utf-8")
    if marker in current:
        raise RuntimeError(f"{path}: marker already exists: {marker}")
    target.write_text(current.rstrip() + "\n\n" + text.rstrip() + "\n", encoding="utf-8")


master = "docs/roadmap/ROADMAP.md"
phase = "docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md"

# Master roadmap closure and sequencing.
replace(master, "Version: `2.85.0`", "Version: `2.86.0`")
replace(
    master,
    "Version `2.85.0` closes **`P9.10 — ООО «Арвектум» organization composition`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`R31 — Product Composition / AI Safety Review`**.",
    "Version `2.86.0` closes **`R31 — Product Composition / AI Safety Review`** as `Complete / PASS` after three functional cross-review iterations and advances Phase 9 to **`P9.11 — Real daily-use dogfooding + friction/backlog closure`**.",
)
replace(
    master,
    "P9.10 final implementation/test evidence: post-remediation head `98cc9c0b0f42bc401ba2dd5c8eedc73e3516e73a`; Productive Workspace CI `#111` / run `32557218451` and Reference Python CI `#343` / run `32557218465` passed; functional cross-review completed 3 iterations with no remaining material objection. Organization composition remains a rebuildable non-authoritative read side over existing authorized product, project-lens, knowledge and work projections; project lenses are explicitly non-canonical, RFC-0007 Knowledge-role distinctions remain explicit, and no company/product semantics or Organizational Authority move into Kernel. Product Contracts and Platform Capabilities remain unchanged.",
    "R31 final implementation/review evidence: clean post-remediation head `022db6e18a8e7128c1984e6f46908d48351c54e8`; Productive Workspace CI `#125` / run `32559626999` and Reference Python CI `#356` / run `32559627003` passed. R31 found and closed two material P9.08 integration findings: unvalidated Knowledge roles are now presented as `source-context` rather than `sourced-fact`, and Copilot no longer provides a generic unbound `/governed` shortcut. Follow-up is evidence-first and requires a context-bound governed continuation. Product boundaries, source/provenance semantics, Activity non-authority, Organization scope, Product Contract lifecycle and Platform Capability lifecycle remain unchanged.",
)
replace(master, "`Active 1.12.0`", "`Active 1.13.0`", count=2)
replace(master, "| **`R31`** | **Product Composition / AI Safety Review** | **🟨 Current gate** |", "| `R31` | Product Composition / AI Safety Review | 🟩 Complete / PASS |")
replace(master, "| `P9.11` | Real daily-use dogfooding + friction/backlog closure | ⬜ |", "| **`P9.11`** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current** |")
replace(
    master,
    "R31 Product Composition / AI Safety Review             CURRENT GATE\n```",
    "R31 Product Composition / AI Safety Review             PASS\n        ↓\nP9.11 real daily-use dogfooding + friction closure          CURRENT\n```",
)
replace(
    master,
    "M9-alpha is achieved, and P9.07–P9.10 are now complete. The owner can continue using the Workspace as the primary validation loop while R31 reviews composition/AI boundaries before P9.11 daily-use dogfooding and the remaining hardening/closure work.",
    "M9-alpha is achieved, P9.07–P9.10 are complete and R31 has passed after closing its two material AI-safety findings. Phase 9 now moves to real owner daily-use dogfooding; usability friction discovered there remains evidence to be dispositioned before R32 hardening and P9.12 closure.",
)
replace(
    master,
    "> **R31 — Product Composition / AI Safety Review.**\n\nReview the integrated P9.07–P9.10 product-composition, Copilot, activity and organization-composition surfaces for product leakage, hidden coupling, authority escalation, source/provenance loss and unsafe AI-to-action shortcuts. Treat this as a review gate, not lifecycle promotion or product/platform expansion.\n\nP9.10 is complete within its exact internal scope. Product Contract and Platform Capability lifecycle states remain unchanged unless separately transitioned through their own governed decisions. Full M9 remains open through R31, P9.11, R32 and P9.12.",
    "> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**\n\nUse the private Productive Workspace as the primary interface for real owner working sessions. Capture recurring friction and incomplete journeys as evidence, distinguish usability defects from product-specific or governance gaps, repair material blockers without weakening security/authority boundaries, and disposition the resulting backlog before R32.\n\nR31 is complete within its exact private internal scope. Product Contract and Platform Capability lifecycle states remain unchanged. Full M9 remains open through P9.11, R32 and P9.12.",
)

# Detailed Phase 9 roadmap.
replace(phase, "Version: `1.12.0`", "Version: `1.13.0`")
replace(phase, "| **`R31`** | **Product Composition / AI Safety Review** | **🟨 Current gate** | no product leakage, hidden coupling or AI authority escalation |", "| `R31` | Product Composition / AI Safety Review | 🟩 Complete / PASS | no product leakage, hidden coupling or AI authority escalation |")
replace(phase, "| `P9.11` | Real daily-use dogfooding + friction/backlog closure | ⬜ | real working sessions completed primarily through Workspace |", "| **`P9.11`** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current** | real working sessions completed primarily through Workspace |")
replace(
    phase,
    "> **R31 — Product Composition / AI Safety Review.**\n\nReview the integrated P9.07–P9.10 product-owned composition, AI assistance, activity and company-level organization composition for product leakage, hidden coupling, source/provenance loss, AI authority escalation and unsafe bypass of Governed Execution. No lifecycle transition is implied by passing the review.\n\nP9.10 is complete within the exact private internal scope. M9 remains open; R31, P9.11, R32 and P9.12 still govern composition safety, dogfooding, hardening and final closure.",
    "> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**\n\nUse the private Productive Workspace as the primary interface for real owner working sessions. Capture recurring friction and incomplete journeys, distinguish Workspace usability defects from product-specific or governance gaps, repair material blockers without weakening security/authority boundaries, and disposition the resulting backlog before R32.\n\nR31 is complete within the exact private internal scope. M9 remains open; P9.11, R32 and P9.12 still govern real daily-use evidence, hardening and final closure.",
)
append_once(
    phase,
    "## 22. R31 closure result",
    '''## 22. R31 closure result

Status: `Complete / PASS` within the exact private internal scope after three functional cross-review iterations.

Canonical evidence: [`R31-product-composition-ai-safety-review.md`](../reviews/R31-product-composition-ai-safety-review.md).

R31 reviewed the integrated P9.07–P9.10 product composition, AI Copilot, Activity/attention and organization-composition surfaces against Constitution `1.2.0`, Accepted RFC-0001…RFC-0008, Accepted ADR-0001 and the P6.02/P6.06 Provisional Product Contracts.

Two material AI-safety findings were found and remediated before PASS:

1. Copilot's previous `sourced-fact` presentation could visually overstate Observation / Organizational Memory / Knowledge Candidate context despite preserved Knowledge-role notes. The internal response contract is now `arvectum.workspace.copilot-answer/2`; the presentation role is `source-context`, and unvalidated Knowledge roles are explicitly not presented as fact.
2. Copilot's previous generic `Review governed actions → /governed` follow-up was not causally bound to the cited evidence and could route unrelated product/Knowledge questions to the retained EIS preflight. Follow-up is now `inspect-evidence-first`, links only to cited Workspace context, does not route directly to Governed Execution, and requires any later governed continuation to be context-bound to the relevant Execution/Decision.

Product adapters remain explicit/release-scoped over declared retained evidence and do not import product databases or domain models. Tender and Discount semantics remain product-owned under P6.02/P6.06. Activity remains a non-authoritative observed projection rather than canonical Event/audit authority. Organization composition remains rebuildable, Organization-scoped and non-canonical; project lenses remain non-canonical.

Clean post-remediation implementation/review head `022db6e18a8e7128c1984e6f46908d48351c54e8` passed Productive Workspace CI `#125` / run `32559626999` and Reference Python CI `#356` / run `32559627003`. Workspace release is `p9.10.2`, internal application contract `9`, still `bounded-internal-provisional` and non-public.

R31 creates no Product Contract or Platform Capability lifecycle promotion, no public/stable interface, no AI authority, no new canonical source of truth and no customer Production/SLA/support/conformance expansion.''',
)

print("R31 roadmap closure applied")
