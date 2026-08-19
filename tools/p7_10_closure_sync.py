#!/usr/bin/env python3
from pathlib import Path


def one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


roadmap_path = Path("docs/roadmap/ROADMAP.md")
roadmap = roadmap_path.read_text(encoding="utf-8")
roadmap = one(roadmap, "Version: `2.56.2`", "Version: `2.56.3`", "master version")
roadmap = one(
    roadmap,
    "Version `2.56.2` records the repository-side implementation",
    """Version `2.56.3` closes `P7.10 — Portability, host-loss and restore-on-clean-environment proof` as `Complete / PASS` for the declared `Persistent Internal / owner-operated` scope. The unchanged verified four-member handoff from the real selected-Mac P7.03 store crossed the host-loss boundary and restored successfully on a separate clean MacBook Air environment at exact embedded release `fbab170ab337c1631b40d0d36ea58a02f6512f6e`. Archive SHA-256 `074f2a4e84e222bd26d6ed21a829aa0dcc1c91834479345cfa652405b721bfbd`, manifest SHA-256 `fe0d2c7d9460f9da4356a3a3f7419b825b8aef3a8d18123ab35fb0281db3ada9`, restored governed-state SHA-256 `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1`, owner-local receipt basename `p7-10-clean-restore-receipt-attempt-3.json`, receipt SHA-256 `ab7bf132d3d3a1304e3582c25fbd80a783d36c7bee9e5e6439ed4c54780aa341`. P7.03 integrity and selected historical reconstruction passed; reusable secrets, external-effect replay, Organizational Authority grant and excluded runtime/secrets paths remained absent. Attempt 2 remains preserved as `FAIL-CLOSED`; PR `#86` retained the P7.03 owner-only restore-parent boundary and passed `1192 tests / OK`; PR `#87` preserved exact handoff-release binding. Canonical closure: [`P7.10 — Canonical Closure`](../reviews/P7-10-canonical-closure.md).\n\n`P7.10 = Complete / PASS`; M7 criterion 10 is satisfied. Active Phase 7 advances to `1.2.15`; `R23 — Recovery / Portability Review` becomes the current canonical action. No Production/lifecycle/Product Contract/capability/SLA/SLO/RPO/RTO/support/conformance promotion is created.\n\nVersion `2.56.2` records the repository-side implementation""",
    "master version note",
)
roadmap = one(
    roadmap,
    "Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Active 1.2.14`.",
    "Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Active 1.2.15`.",
    "master phase version",
)
roadmap = one(
    roadmap,
    "| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | 🟨 Current | `░░░░░░░░░░ 0%` |",
    "| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | 🟩 Complete / PASS | `██████████ 100%` |",
    "master P7.10 row",
)
roadmap = one(
    roadmap,
    "- `R23 — Recovery / Portability Review` — after P7.10;",
    "- `R23 — Recovery / Portability Review` — 🟨 Current after P7.10;",
    "master R23 gate",
)
roadmap = one(
    roadmap,
    "P7.10 portability / host-loss / clean-environment restore proof ← current\n        ↓\nP7.11–P7.12 readiness disposition + hardening + closure",
    "P7.10 portability / host-loss / clean-environment restore proof — PASS\n        ↓\nR23 Recovery / Portability Review ← current\n        ↓\nP7.11–P7.12 readiness disposition + hardening + closure",
    "master transition",
)
roadmap = one(
    roadmap,
    "\n## 7. M7 milestone definition",
    """\n\nP7.10 is `Complete / PASS`. The actual selected-Mac governed store was re-verified from the unchanged off-host handoff and restored on the clean secondary host at exact release `fbab170ab337c1631b40d0d36ea58a02f6512f6e`; P7.03 integrity, governed-state digest, selected historical reconstruction, exclusions, no-effect-replay and no-authority checks all passed. Canonical closure: [`P7.10 — Canonical Closure`](../reviews/P7-10-canonical-closure.md).\n\n## 7. M7 milestone definition""",
    "master P7.10 summary",
)
marker = "## 11. Current canonical action\n"
if roadmap.count(marker) != 1:
    raise SystemExit("master current-action marker mismatch")
roadmap = roadmap.split(marker, 1)[0] + marker + """

> **R23 — Recovery / Portability Review.**

`P7.10 = Complete / PASS` for the declared `Persistent Internal / owner-operated` scope. The real selected-Mac governed store crossed the host-loss boundary and restored successfully on a clean secondary environment with exact-release, integrity, governed-state, selected-history, exclusion, no-replay and no-authority checks all passing. M7 criterion 10 is satisfied.

R23 now reviews the accumulated P7.03/P7.06/P7.09/P7.10 recovery and portability evidence before P7.11 performs lifecycle, conformance and stable-boundary disposition. Criteria 11–13 remain downstream. R23 is an engineering/governance review, not a Production approval or lifecycle transition.
""".lstrip("\n")
roadmap_path.write_text(roadmap, encoding="utf-8")


phase_path = Path("docs/roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md")
phase = phase_path.read_text(encoding="utf-8")
phase = one(phase, "Version: `1.2.14`", "Version: `1.2.15`", "phase version")
phase = one(
    phase,
    "| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | Mac mini + secondary clean environment + GitHub | 🟨 Current | `░░░░░░░░░░ 0%` |",
    "| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | Mac mini + secondary clean environment + GitHub | 🟩 Complete / PASS | `██████████ 100%` |",
    "phase P7.10 row",
)
phase = one(
    phase,
    "| `R23 — Recovery / Portability Review` | after `P7.10`, before lifecycle/readiness decisions | ⬜ | verify backup/restore, host-loss recovery, semantic portability, exact identities/versions/provenance and absence of host-specific hidden authority |",
    "| `R23 — Recovery / Portability Review` | after `P7.10`, before lifecycle/readiness decisions | 🟨 `Current` | verify backup/restore, host-loss recovery, semantic portability, exact identities/versions/provenance and absence of host-specific hidden authority |",
    "phase R23 row",
)
start = phase.index("### P7.10 — Portability, host-loss and restore-on-clean-environment proof")
end = phase.index("### P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition")
phase_p710 = """### P7.10 — Portability, host-loss and restore-on-clean-environment proof

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.10 — Implementation Readiness Review`](../reviews/P7-10-implementation-readiness.md) — repository implementation and automated mechanism proof;
- [`P7.10 — Selected-Mac Operational Attempt 2`](../reviews/P7-10-selected-mac-attempt-2-clean-parent-failure.md) — preserved fail-closed secondary-parent failure;
- [`P7.10 — Canonical Closure`](../reviews/P7-10-canonical-closure.md) — final operational closure;
- implementation PR `#83`, merge `393cc5bff98cc87553b96d282f4bf618621fd87a`;
- restore-parent remediation PR `#86`, merge `16621a1abc814a92e8fed0d0a3451946be6f8303`, final full CI `1192 tests / OK`;
- exact-release procedure correction PR `#87`, merge `de59771281ce1b4c58d943bd003560384e332270`;
- exact retained handoff/tool release `fbab170ab337c1631b40d0d36ea58a02f6512f6e`;
- archive SHA-256 `074f2a4e84e222bd26d6ed21a829aa0dcc1c91834479345cfa652405b721bfbd`;
- handoff manifest SHA-256 `fe0d2c7d9460f9da4356a3a3f7419b825b8aef3a8d18123ab35fb0281db3ada9`;
- owner-local receipt basename `p7-10-clean-restore-receipt-attempt-3.json`, SHA-256 `ab7bf132d3d3a1304e3582c25fbd80a783d36c7bee9e5e6439ed4c54780aa341`.

The actual selected-Mac P7.03 governed store crossed the host-loss boundary through the unchanged verified four-member handoff and restored successfully on a separate clean MacBook Air environment. P7.03 integrity remained `PASS`; governed-state SHA-256 `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1` matched the source handoff; selected historical reconstruction passed; two governed items and two checkpoints were retained; reusable secrets, excluded runtime paths, external-effect replay and Organizational Authority grant remained absent.

Attempt 2 remains fail-closed evidence: a target directly beneath a macOS home directory with mode `0750` was rejected before publication. Closure used a dedicated non-symlink `0700` immediate restore parent without weakening the home-directory policy. The same handoff was restored at its exact embedded release rather than rebuilt or relabelled after documentation/test-only corrections.

The P7.09 `/var` versus `/private/var` discrepancy is dispositioned as a host path-presentation/environment issue only when physical filesystem identity proves equivalence. Lexical aliases resolving to different objects remain material and fail closed where same-location identity is required. The actual selected-Mac persistent source was the established owner-local runtime root, not `/var/lib/arvectum-os`.

P7.10 satisfies M7 criterion 10. Host/service-manager paths, machine-local credentials/secrets, network/proxy/TLS configuration and OS-specific ownership plumbing remain target-environment reprovisioning responsibilities rather than portable semantic state.

P7.10 closure creates no Production claim, lifecycle promotion, Stable Product Contract, Active Platform Capability, public/stable recovery/export format, permanent persistence technology, SLA/SLO/RPO/RTO/support commitment or broader conformance claim.

**R23 follows P7.10 and is now Current.**

"""
phase = phase[:start] + phase_p710 + phase[end:]
phase = one(
    phase,
    "M7 criterion 9 is satisfied by P7.09 for the declared `Persistent Internal / owner-operated` scope. Criteria 10–13 remain downstream.",
    "M7 criteria 9 and 10 are satisfied by P7.09 and P7.10 respectively for the declared `Persistent Internal / owner-operated` scope. Criteria 11–13 remain downstream.",
    "phase criteria",
)
marker = "## 8. Current canonical action\n"
if phase.count(marker) != 1:
    raise SystemExit("phase current-action marker mismatch")
phase = phase.split(marker, 1)[0] + marker + """

> **R23 — Recovery / Portability Review.**

P7.10 is `Complete / PASS`: the real selected-Mac governed store was handed off beyond the host-loss boundary and restored on a separate clean secondary environment with exact-release binding, P7.03 integrity, governed-state digest, selected historical reconstruction, exclusions, no-effect-replay and no-authority checks all passing. M7 criterion 10 is satisfied.

R23 now reviews the accumulated recovery/portability evidence before P7.11 performs scoped operational-readiness, lifecycle, conformance and stable-boundary disposition. R23 does not itself promote a capability, stabilize a Product Contract or approve Production.
""".lstrip("\n")
phase_path.write_text(phase, encoding="utf-8")
