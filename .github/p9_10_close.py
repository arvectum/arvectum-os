from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one match in {path}, found {count}: {old[:120]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: str, marker: str, addition: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if marker in text:
        raise RuntimeError(f"marker already exists in {path}: {marker}")
    target.write_text(text.rstrip() + "\n\n" + addition.rstrip() + "\n", encoding="utf-8")


master = "docs/roadmap/ROADMAP.md"
phase = "docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md"
review = "docs/reviews/P9-10-arvectum-organization-composition.md"

# Master roadmap.
replace_once(master, "Version: `2.84.0`", "Version: `2.85.0`")
replace_once(
    master,
    "Version `2.84.0` closes **`P9.09 — Activity, notifications and attention routing`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`P9.10 — ООО «Арвектум» organization composition`**.",
    "Version `2.85.0` closes **`P9.10 — ООО «Арвектум» organization composition`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`R31 — Product Composition / AI Safety Review`**.",
)
replace_once(
    master,
    "P9.09 final implementation/test evidence: head `c335e293022193de93b349fa5d86325501c74e4f`; Productive Workspace CI `#103` / run `32555963482` and Reference Python CI `#335` / run `32555963477` passed; functional cross-review completed 3 iterations with no material objection after one UI styling remediation. Activity remains a non-authoritative read-side projection, alerts reuse P9.04 attention semantics, and no notification/read-receipt authority is created. Product Contracts and Platform Capabilities remain unchanged.",
    "P9.10 final implementation/test evidence: post-remediation head `98cc9c0b0f42bc401ba2dd5c8eedc73e3516e73a`; Productive Workspace CI `#111` / run `32557218451` and Reference Python CI `#343` / run `32557218465` passed; functional cross-review completed 3 iterations with no remaining material objection. Organization composition remains a rebuildable non-authoritative read side over existing authorized product, project-lens, knowledge and work projections; project lenses are explicitly non-canonical, RFC-0007 Knowledge-role distinctions remain explicit, and no company/product semantics or Organizational Authority move into Kernel. Product Contracts and Platform Capabilities remain unchanged.",
)
replace_once(master, "`Active 1.11.0`", "`Active 1.12.0`")
replace_once(master, "| **`P9.10`** | **ООО «Арвектум» organization composition** | **🟨 Current** |", "| `P9.10` | ООО «Арвектум» organization composition | 🟩 Complete / PASS |")
replace_once(master, "| `R31` | Product Composition / AI Safety Review | ⬜ gate |", "| **`R31`** | **Product Composition / AI Safety Review** | **🟨 Current gate** |")
replace_once(
    master,
    "P9.10 company organization composition                    CURRENT\n```",
    "P9.10 company organization composition                 PASS\n        ↓\nR31 Product Composition / AI Safety Review                CURRENT GATE\n```",
)
replace_once(
    master,
    "M9-alpha is achieved, and P9.07–P9.09 are now complete. The owner can continue using the Workspace as the primary validation loop while P9.10–P9.12 add company-level composition, real daily-use dogfooding and final hardening.",
    "M9-alpha is achieved, and P9.07–P9.10 are now complete. The owner can continue using the Workspace as the primary validation loop while R31 reviews composition/AI boundaries before P9.11 daily-use dogfooding and the remaining hardening/closure work.",
)
replace_once(
    master,
    "> **P9.10 — ООО «Арвектум» organization composition.**\n\nCompose company-level navigation over products, projects, knowledge and work through explicit boundaries without moving product/company semantics into Kernel authority. Preserve Organization scope, source authority, provenance, product ownership and Governed Execution boundaries.\n\nP9.08 is complete within its exact internal scope. Product Contract and Platform Capability lifecycle states remain unchanged unless separately transitioned through their own governed decisions. Full M9 remains open through P9.09–P9.12 and R31/R32.",
    "> **R31 — Product Composition / AI Safety Review.**\n\nReview the integrated P9.07–P9.10 product-composition, Copilot, activity and organization-composition surfaces for product leakage, hidden coupling, authority escalation, source/provenance loss and unsafe AI-to-action shortcuts. Treat this as a review gate, not lifecycle promotion or product/platform expansion.\n\nP9.10 is complete within its exact internal scope. Product Contract and Platform Capability lifecycle states remain unchanged unless separately transitioned through their own governed decisions. Full M9 remains open through R31, P9.11, R32 and P9.12.",
)

# Detailed Phase 9 roadmap.
replace_once(phase, "Version: `1.11.0`", "Version: `1.12.0`")
replace_once(phase, "| **`P9.10`** | **ООО «Арвектум» organization composition** | **🟨 Current** | company-level navigation over products/projects/knowledge/work |", "| `P9.10` | ООО «Арвектум» organization composition | 🟩 Complete / PASS | company-level navigation over products/projects/knowledge/work |")
replace_once(phase, "| `R31` | Product Composition / AI Safety Review | ⬜ gate | no product leakage, hidden coupling or AI authority escalation |", "| **`R31`** | **Product Composition / AI Safety Review** | **🟨 Current gate** | no product leakage, hidden coupling or AI authority escalation |")
replace_once(
    phase,
    "> **P9.10 — ООО «Арвектум» organization composition.**\n\nCompose company-level navigation over products, projects, knowledge and work through explicit boundaries without moving product/company semantics into Kernel authority. Preserve Organization scope, source authority, provenance, product ownership and Governed Execution boundaries.\n\nP9.09 is complete within the exact private internal scope. M9 remains open; P9.10–P9.12 and R31/R32 still govern company composition, dogfooding and hardening work.",
    "> **R31 — Product Composition / AI Safety Review.**\n\nReview the integrated P9.07–P9.10 product-owned composition, AI assistance, activity and company-level organization composition for product leakage, hidden coupling, source/provenance loss, AI authority escalation and unsafe bypass of Governed Execution. No lifecycle transition is implied by passing the review.\n\nP9.10 is complete within the exact private internal scope. M9 remains open; R31, P9.11, R32 and P9.12 still govern composition safety, dogfooding, hardening and final closure.",
)
append_once(
    phase,
    "## 21. P9.10 closure result",
    '''## 21. P9.10 closure result

Status: `Complete / PASS` within the exact private internal scope.

P9.10 adds an `Organization` Workspace surface backed by `arvectum.workspace.organization-composition/1`. The projection composes existing authorized Products, non-canonical project lenses, Knowledge context and Work/attention context without introducing a company database, canonical Project source of truth or company/product semantics in Kernel.

Closure evidence: [`P9-10-arvectum-organization-composition.md`](../reviews/P9-10-arvectum-organization-composition.md). Post-remediation implementation/review head `98cc9c0b0f42bc401ba2dd5c8eedc73e3516e73a`; Productive Workspace CI `#111` / run `32557218451` and Reference Python CI `#343` / run `32557218465` passed. Functional cross-review completed 3 iterations; the first two identified and repaired explicit RFC-0007 semantic preservation and minimized BFF structural-error handling, and the third found no remaining material objection.

Products remain product-owned behind P9.07/Product Contract boundaries. Project lenses are navigation-only and explicitly non-canonical. Knowledge keeps Observation / Organizational Memory / Knowledge Candidate / validated Knowledge distinctions visible. Work/attention grants no Authorization, Organizational Authority or approval and exposes no consequential action. Organization/Actor scope remains server-resolved and current access is revalidated at the BFF boundary.

Workspace release is `p9.10.1`, internal application contract `8`, still `bounded-internal-provisional` and non-public. No Product Contract or Platform Capability lifecycle promotion, public/stable API, customer Production, SLA/support/certification or broader conformance claim is introduced.''',
)

# Finalize canonical review evidence.
replace_once(review, "Status: `Implementation review checkpoint — roadmap closure pending`", "Status: `Complete / PASS`")
replace_once(review, "Two iterations completed so far, within the maximum of 7.", "Three iterations completed, within the maximum of 7.")
replace_once(
    review,
    "2. **RFC-0007 / BFF failure semantics.** Found that the first implementation preserved Knowledge-role distinctions mainly through summary prose and let a structural composition error fall through as a generic server error. Remediation added explicit `semantic_note` presentation and a minimized `ORGANIZATION_COMPOSITION_UNAVAILABLE` 503 boundary. Bounded backend/frontend verification and exact-release rebuild passed after remediation.\n\nA final post-CI implementation review and canonical roadmap synchronization remain before `Complete / PASS`.",
    "2. **RFC-0007 / BFF failure semantics.** Found that the first implementation preserved Knowledge-role distinctions mainly through summary prose and let a structural composition error fall through as a generic server error. Remediation added explicit `semantic_note` presentation and a minimized `ORGANIZATION_COMPOSITION_UNAVAILABLE` 503 boundary. Bounded backend/frontend verification and exact-release rebuild passed after remediation.\n3. **Post-remediation integrated review.** Re-read the complete PR diff after independent CI, including composition source boundaries, Organization/Actor scope, project-lens truthfulness, Knowledge-role preservation, attention routing, BFF error minimization, frontend presentation, tests and exact release assets. No remaining material architecture, security, product-boundary, authority, provenance, AI-safety, reproducibility or maintainability objection was found.\n\nFunctional cross-review is implementation evidence, not RFC/ADR acceptance, lifecycle promotion or delegated Organizational Authority.",
)
replace_once(review, "## Verification checkpoint", "## Verification evidence")
replace_once(
    review,
    "A clean ordinary PR head will be used for the independent post-remediation merge gate.",
    "Post-remediation implementation/review head `98cc9c0b0f42bc401ba2dd5c8eedc73e3516e73a` then passed the independent merge gates: Productive Workspace CI `#111` / run `32557218451` — `SUCCESS`; Reference Python CI `#343` / run `32557218465` — `SUCCESS`. Canonical roadmaps are synchronized by closure-only documentation changes to master `2.85.0` / Phase 9 `1.12.0`, with `R31 — Product Composition / AI Safety Review` as the next action.",
)

print("P9.10 canonical closure applied")
