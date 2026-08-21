from __future__ import annotations

from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def sync_master() -> None:
    path = Path("docs/roadmap/ROADMAP.md")
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, "Version: `2.78.0`", "Version: `2.79.0`", "master version")

    section_start = text.index("## 2. Version note\n")
    section_end = text.index("## 3. Architecture and governance baseline\n")
    version_note = """## 2. Version note

Version `2.79.0` closes **`P9.05 — Human-friendly Records / Documents / Knowledge + global search`** as `Complete / PASS` after two functional cross-review iterations and advances Phase 9 to **`P9.06 — Executions / Decisions / governed actions UX`**.

P9.05 adds the first human-first governed discovery/context layer through the Accepted ADR-0001 / P9.03 application boundary:

1. internal `arvectum.workspace.discovery/1` and `arvectum.workspace.object-context/1` derived read contracts with no canonical or Organizational Authority;
2. persistent global search plus dedicated Records, Documents and Knowledge browser surfaces;
3. current server-side Organization/Actor scope and access/source revalidation before protected result/object disclosure;
4. opaque browser object references and human-readable ordinary-path title/source/authority/state/context, with exact Subject/Version/provenance exposed only on demand;
5. fail-closed degraded behavior and minimized denial semantics that do not expose protected denied-result counts or stale protected details as current;
6. preservation of `Observation ≠ validated Knowledge` and Document `External Reference` authority-source semantics;
7. direct P9.01 F1 evidence: real EIS notice `0344100006426000005` is discoverable without internal identifier knowledge and opens into human-first context;
8. no durable search source of truth, no mutation/governed-action path and no permission/authority inference from search visibility.

The first review iteration found only the expected stale committed-SPA-asset mismatch after source gates passed; exact CI-built assets were reconciled through a bounded one-shot helper that was removed before closure. The second clean iteration passed Productive Workspace CI run `32477614572` and Reference Python CI run `32477614687` with no remaining material objection.

Canonical P9.05 evidence: [`P9-05-human-friendly-records-documents-knowledge-global-search.md`](../reviews/P9-05-human-friendly-records-documents-knowledge-global-search.md). Detailed Phase 9 roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) `Active 1.6.0`.

The intermediate milestone remains **`M9-alpha — Usable Internal Workspace`** and is **not yet achieved**. P9.06 and R30 remain necessary for a real governed action and full P9.01 J1–J4 ordinary-path usability evidence.

P9.05 closure does not create public/customer Production, Stable Product Contracts, Active Platform Capabilities, public/stable API/SDK/browser compatibility, SLA/support/certification, broader conformance or Organizational/AI authority.

"""
    text = text[:section_start] + version_note + text[section_end:]
    text = replace_once(
        text,
        "Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.5.0`.",
        "Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.6.0`.",
        "master detailed roadmap version",
    )
    text = replace_once(
        text,
        "| **`P9.05`** | **Human-friendly Records / Documents / Knowledge + global search** | **🟨 Current** |\n| `P9.06` | Executions / Decisions / governed actions UX | ⬜ |",
        "| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS |\n| **`P9.06`** | **Executions / Decisions / governed actions UX** | **🟨 Current** |",
        "master work breakdown",
    )
    text = replace_once(
        text,
        "P9.05 human-friendly Records/Documents/Knowledge/search CURRENT\n        ↓\nP9.06 Executions/Decisions/governed actions",
        "P9.05 human-friendly Records/Documents/Knowledge/search PASS\n        ↓\nP9.06 Executions/Decisions/governed actions             CURRENT",
        "master critical path",
    )
    action_start = text.index("## 9. Current canonical action\n")
    action = """## 9. Current canonical action

> **P9.06 — Executions / Decisions / governed actions UX.**

Build the next owner-facing governed-action layer through the existing ADR-0001 Productive Workspace boundary. The operator must be able to inspect one real Execution/Decision in human terms and perform at least one bounded real governed interaction without the UI itself becoming Authorization, Organizational Authority or Consequential Approval; all consequential canonical change/effects remain subject to Governed Execution and current command-boundary gates.

P9.06 does not itself achieve M9-alpha. The remaining critical sequence is `P9.06 → R30 → M9-alpha`.
"""
    path.write_text(text[:action_start] + action, encoding="utf-8")


def sync_phase() -> None:
    path = Path("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md")
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, "Version: `1.5.0`", "Version: `1.6.0`", "phase version")
    text = replace_once(
        text,
        "| **`P9.05`** | **Human-friendly Records / Documents / Knowledge + global search** | **🟨 Current** | understandable discovery and object context |\n| `P9.06` | Executions / Decisions / governed actions UX | ⬜ | owner can inspect and perform one real governed action |",
        "| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS | understandable discovery and object context |\n| **`P9.06`** | **Executions / Decisions / governed actions UX** | **🟨 Current** | owner can inspect and perform one real governed action |",
        "phase work breakdown",
    )

    marker = "## 11. M9-alpha exit criteria\n"
    if marker not in text:
        raise SystemExit("phase insertion marker missing")
    p905 = """## 11. P9.05 implementation and closure result

Status: `Complete / PASS`.

Canonical evidence: [`P9-05-human-friendly-records-documents-knowledge-global-search.md`](../reviews/P9-05-human-friendly-records-documents-knowledge-global-search.md).

P9.05 established the first human-friendly discovery and exact-object-context layer through the P9.03/P9.04/ADR-0001 application boundary:

1. internal `arvectum.workspace.discovery/1` derived discovery and `arvectum.workspace.object-context/1` read contracts;
2. persistent global search plus dedicated Records, Documents and Knowledge routes;
3. server-resolved Organization/Actor scope and current protected-read revalidation;
4. human-readable semantic role/title/summary/source/authority/state in the ordinary path;
5. opaque browser object references, with exact Subject/Version/provenance available only through explicit technical drill-down;
6. real P9.01 F1 EIS notice `0344100006426000005` discoverable by human/external context and opened with `ЕИС / zakupki.gov.ru` / `External Reference` semantics intact;
7. `Observation`, Organizational Memory, Knowledge Candidate and validated Knowledge kept semantically distinct;
8. fail-closed degraded search/object behavior with no denied-result cardinality oracle and no stale protected details represented as current;
9. no durable search source of truth in the current implementation and no consequential write/effect path;
10. Workspace release `p9.05.1`, internal application contract `3`, still `bounded-internal-provisional` and non-public.

Functional cross-review completed two iterations. Iteration 1 passed source behavior/typecheck/tests/storage/build gates and found only the expected committed production-asset mismatch; exact CI-built assets were reconciled through a bounded one-shot helper and that helper was removed before closure. Iteration 2 passed Productive Workspace CI run `32477614572` and Reference Python CI run `32477614687` with no remaining material objection.

P9.05 closes the J2/J3 implementation slice for the declared real F1 discovery/context path. It does not claim full M9-alpha: P9.06 must still prove one bounded real governed interaction and R30 must review the complete J1–J4 ordinary path.

P9.05 creates no public/stable API, Product Contract or Platform Capability lifecycle transition, customer Production claim, broader conformance promise or Organizational Authority.

"""
    text = text.replace(marker, p905 + marker, 1)
    text = replace_once(text, "## 11. M9-alpha exit criteria", "## 12. M9-alpha exit criteria", "phase section 12")
    text = replace_once(text, "## 12. M9 exit criteria", "## 13. M9 exit criteria", "phase section 13")
    text = replace_once(text, "## 13. Explicit non-goals", "## 14. Explicit non-goals", "phase section 14")
    current_start = text.index("## 14. Current canonical action\n")
    current = """## 15. Current canonical action

> **P9.06 — Executions / Decisions / governed actions UX.**

Build the next owner-facing governed-action layer on top of the P9.03–P9.05 Productive Workspace. The ordinary path must let the owner inspect one real Execution/Decision in human terms and perform at least one bounded real governed interaction while preserving current Authorization, Organizational Authority, Data Governance, Consequential Approval, provenance, idempotency/retry and no-effect-on-replay invariants at the command boundary.

The remaining near-term sequence is `P9.06 → R30 → M9-alpha`. P9.05 provides human-friendly discovery/context; M9-alpha remains unachieved until the full declared exit set passes.
"""
    path.write_text(text[:current_start] + current, encoding="utf-8")


if __name__ == "__main__":
    sync_master()
    sync_phase()
