from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected fragment missing in {path}: {old[:80]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def apply() -> None:
    replace(
        "reference/python/workspace_app/main.py",
        '        {"id": "my-work", "label": "My Work", "href": "/my-work", "availability": "available"},\n',
        '        {"id": "my-work", "label": "My Work", "href": "/my-work", "availability": "available"},\n        {"id": "activity", "label": "Activity", "href": "/activity", "availability": "available"},\n',
    )
    replace(
        "reference/python/workspace_frontend/src/Shell.tsx",
        'import { Copilot } from "./Copilot";\n',
        'import { Activity } from "./Activity";\nimport { Copilot } from "./Copilot";\n',
    )
    replace(
        "reference/python/workspace_frontend/src/Shell.tsx",
        '          ) : active.id === "my-work" ? (\n            <MyWork />\n          ) : active.id === "search" ? (',
        '          ) : active.id === "my-work" ? (\n            <MyWork />\n          ) : active.id === "activity" ? (\n            <Activity />\n          ) : active.id === "search" ? (',
    )
    replace(
        "reference/python/workspace_frontend/src/Shell.tsx",
        '                  My Work surfaces current attention signals, discovery finds governed organizational context, Ask Arvectum\n                  provides source-grounded assistance, and Governed actions keeps consequential work behind current authority gates.\n',
        '                  My Work surfaces current attention signals, Activity shows an observed non-authoritative timeline and current alerts,\n                  discovery finds governed organizational context, Ask Arvectum provides source-grounded assistance, and Governed actions keeps consequential work behind current authority gates.\n',
    )

    activity = r'''import { useCallback, useEffect, useMemo, useState } from "react";
import { loadGovernedExperience, loadMyWork, WorkspaceApiError } from "./api";
import type { AttentionItem, GovernedExperienceProjection, MyWorkProjection } from "./types";

type ReadyState = { kind: "ready"; work: MyWorkProjection; governed: GovernedExperienceProjection };
type LoadState = { kind: "loading" } | ReadyState | { kind: "error"; code: string; reloadRequired: boolean };

type ActivityEntry = {
  id: string;
  observedAt: string;
  label: string;
  title: string;
  detail: string;
  source: string;
  href: string;
  alert: boolean;
  scenario: boolean;
};

const ALERT_GROUPS = new Set(["decision-required", "blocked-failed", "reconciliation-required"]);

function displayTime(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

function fromAttention(item: AttentionItem, fallback: string): ActivityEntry {
  return {
    id: `attention-${item.id}`,
    observedAt: item.observed_at ?? fallback,
    label: item.group === "recent-outcome" ? "Observed outcome" : item.group === "informational" ? "Observed information" : "Attention signal",
    title: item.title,
    detail: item.reason,
    source: item.source,
    href: item.open_href,
    alert: ALERT_GROUPS.has(item.group),
    scenario: item.evidence_mode === "scenario",
  };
}

export function Activity() {
  const [state, setState] = useState<LoadState>({ kind: "loading" });
  const refresh = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      const [work, governed] = await Promise.all([loadMyWork(), loadGovernedExperience()]);
      setState({ kind: "ready", work, governed });
    } catch (error) {
      if (error instanceof WorkspaceApiError) setState({ kind: "error", code: error.code, reloadRequired: error.reloadRequired });
      else setState({ kind: "error", code: "ACTIVITY_UNAVAILABLE", reloadRequired: false });
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  const entries = useMemo(() => {
    if (state.kind !== "ready") return [];
    const attention = state.work.items.map((item) => fromAttention(item, state.work.generated_at));
    const governed: ActivityEntry = {
      id: "governed-current-state",
      observedAt: state.governed.generated_at,
      label: "Governed state observed",
      title: `Governed execution: ${state.governed.execution.status}`,
      detail: state.governed.execution.meaning,
      source: state.governed.presentation.source,
      href: "/governed",
      alert: false,
      scenario: false,
    };
    return [...attention, governed].sort((a, b) => (Date.parse(b.observedAt) || 0) - (Date.parse(a.observedAt) || 0));
  }, [state]);

  if (state.kind === "loading") return <section className="activity-page" aria-live="polite"><p>Loading current activity sources…</p></section>;
  if (state.kind === "error") return (
    <section className="activity-page" role="alert">
      <p className="eyebrow">Activity</p><h1>Activity is unavailable.</h1>
      <p>{state.reloadRequired ? "The application release changed. Reload before relying on this projection." : "Current source scope could not be safely revalidated. No retained activity detail is shown."}</p>
      <code>{state.code}</code>
      <button type="button" onClick={() => state.reloadRequired ? window.location.reload() : void refresh()}>{state.reloadRequired ? "Reload application" : "Try again"}</button>
    </section>
  );

  const alerts = entries.filter((entry) => entry.alert);
  return (
    <section className="activity-page" aria-labelledby="activity-title">
      <div className="my-work-heading">
        <div><p className="eyebrow">Activity · derived projection</p><h1 id="activity-title">Operational activity and alerts</h1><p>Human-readable observations over already-authorized Workspace projections.</p></div>
        <button type="button" className="quiet-button" onClick={() => void refresh()}>Refresh</button>
      </div>
      <p className="boundary-note">This is not an Event store, audit log, notification authority, approval queue, or source of Organizational Authority. Times below are observation times unless a source explicitly proves occurrence time. No read/unread state is recorded.</p>
      <section className="activity-alerts" aria-labelledby="current-alerts-title">
        <p className="eyebrow">Attention routing</p><h2 id="current-alerts-title">Current alerts</h2>
        <p>Alerts reuse My Work attention semantics; P9.09 does not invent a second priority model.</p>
        {alerts.length === 0 ? <p>No current alert is visible in this authorized projection.</p> : (
          <div className="attention-list">{alerts.map((entry) => <article className="attention-card" key={`alert-${entry.id}`}><div className="attention-card-topline"><span>Current alert</span>{entry.scenario ? <span>Scenario evidence</span> : null}</div><h3>{entry.title}</h3><p>{entry.detail}</p><dl><div><dt>Source</dt><dd>{entry.source}</dd></div></dl><div className="attention-card-footer"><small>Observed {displayTime(entry.observedAt)}</small><a href={entry.href}>Inspect context</a></div></article>)}</div>
        )}
      </section>
      <section className="activity-timeline" aria-labelledby="activity-timeline-title">
        <p className="eyebrow">Observed timeline</p><h2 id="activity-timeline-title">Recent visible activity</h2>
        <ol className="activity-list">{entries.map((entry) => <li key={entry.id}><article><div className="attention-card-topline"><span>{entry.label}</span>{entry.scenario ? <span>Scenario evidence</span> : null}</div><time dateTime={entry.observedAt}>{displayTime(entry.observedAt)}</time><h3>{entry.title}</h3><p>{entry.detail}</p><p><strong>Source:</strong> {entry.source}</p><a href={entry.href}>Inspect context</a></article></li>)}</ol>
      </section>
    </section>
  );
}
'''
    (ROOT / "reference/python/workspace_frontend/src/Activity.tsx").write_text(activity, encoding="utf-8")

    test = r'''import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Activity } from "./Activity";
import type { GovernedExperienceProjection, MyWorkProjection } from "./types";

const work: MyWorkProjection = {
  schema: "arvectum.workspace.my-work/1", generated_at: "2026-08-22T06:00:00Z",
  projection: { derived: true, canonical_authority: false, organizational_authority_provided: false, consequential_action_available: false, visibility_implies_permission: false },
  scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, denied_item_counts_exposed: false },
  health: { state: "fresh", code: "OK", message: "Current", observed_at: "2026-08-22T06:00:00Z", heartbeat_age_seconds: 1 },
  items: [{ id: "11111111111111111111", kind: "waiting-input", group: "decision-required", urgency: "high", title: "Decision evidence is needed", reason: "A governed gate remains waiting.", source: "Governed source", next_step: "Inspect governed context.", evidence_mode: "live", observed_at: "2026-08-22T05:59:00Z", open_href: "/my-work?focus=11111111111111111111", interaction: "inspect-only", technical_evidence_available: true, authority_provided: false }],
};
const governed: GovernedExperienceProjection = {
  schema: "arvectum.workspace.governed-experience/1", generated_at: "2026-08-22T06:01:00Z",
  presentation: { title: "Governed preflight", summary: "Review", source: "Governed source", authority_mode: "Native", authority_scope: "org", validation_status: "current" },
  execution: { status: "Waiting", meaning: "Execution remains waiting for governed evidence.", waiting_decisions: ["Consequential Approval"], technical_identity_available: true },
  decisions: [],
  action: { kind: "governed-preflight", label: "Run preflight", available: true, consequential: false, canonical_mutation_requested: false, external_effect_requested: false, authority_provided: false, explanation: "Revalidated server-side." },
  technical: { release_sha: "a", source_subject: "s", source_version: "v", execution_subject: "e", execution_version: "ev", event_version: "event", checkpoint_id: "c", provenance_refs: [] },
  scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, current_access_revalidated: true, organizational_authority_provided: false, visibility_implies_permission: false },
};

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("P9.09 activity and attention routing", () => {
  it("renders current alerts from My Work semantics and labels the timeline as observed/non-authoritative", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      const payload = url.includes("/my-work") ? work : governed;
      return new Response(JSON.stringify(payload), { status: 200, headers: { "Content-Type": "application/json" } });
    }));
    render(<Activity />);
    expect(await screen.findByRole("heading", { name: "Operational activity and alerts" })).toBeTruthy();
    expect(screen.getByText(/not an Event store, audit log, notification authority/)).toBeTruthy();
    expect(screen.getByText(/No read\/unread state is recorded/)).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Current alerts" })).toBeTruthy();
    expect(screen.getAllByText("Decision evidence is needed").length).toBe(2);
    expect(screen.getByText("Governed execution: Waiting")).toBeTruthy();
    expect(screen.getAllByRole("link", { name: "Inspect context" }).map((link) => link.getAttribute("href"))).toContain("/my-work?focus=11111111111111111111");
  });

  it("fails closed rather than retaining partial activity when one protected source cannot be revalidated", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => String(input).includes("/my-work")
      ? new Response(JSON.stringify(work), { status: 200, headers: { "Content-Type": "application/json" } })
      : new Response(JSON.stringify({ detail: "ACCESS_DENIED" }), { status: 403, headers: { "Content-Type": "application/json" } })));
    render(<Activity />);
    expect(await screen.findByRole("heading", { name: "Activity is unavailable." })).toBeTruthy();
    expect(screen.queryByText("Decision evidence is needed")).toBeNull();
  });
});
'''
    (ROOT / "reference/python/workspace_frontend/src/P909.test.tsx").write_text(test, encoding="utf-8")

    styles = ROOT / "reference/python/workspace_frontend/src/styles.css"
    css = styles.read_text(encoding="utf-8")
    marker = "/* P9.09 activity projection */"
    if marker not in css:
        css += f'''\n\n{marker}\n.activity-page {{ display: grid; gap: 1.25rem; }}\n.activity-alerts, .activity-timeline {{ display: grid; gap: .75rem; }}\n.activity-list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: .75rem; }}\n.activity-list article {{ border: 1px solid var(--border); border-radius: 14px; padding: 1rem; background: var(--panel); }}\n.activity-list time {{ display: block; margin: .35rem 0; color: var(--muted); font-size: .9rem; }}\n'''
        styles.write_text(css, encoding="utf-8")

    (ROOT / "reference/python/workspace_app/release.json").write_text('''{\n  "schema": "arvectum.workspace.application-release/1",\n  "release_id": "p9.09.1",\n  "app_api_contract": "7",\n  "classification": "bounded-internal-provisional",\n  "public_api": false\n}\n''', encoding="utf-8")


def close(run_id: str) -> None:
    review = f'''# P9.09 — Activity, notifications and attention routing\n\nStatus: `Complete / PASS`\nDate: `2026-08-22`\nOwner: `ООО «Арвектум»`\nTask classification: `platform` with `governance`\nPredecessor: `P9.08 — Complete / PASS`\n\n## Scope\n\nP9.09 adds an internal human-readable Activity surface over already-authorized Productive Workspace projections. It reuses P9.04 My Work attention semantics for current alerts and adds a truthful observed timeline that distinguishes observation time from canonical Event occurrence. No new canonical Event, audit-log, notification-delivery, read/unread, approval or Organizational Authority state is introduced.\n\nCanonical baseline checked: Constitution `1.2.0` Ratified/frozen; RFC-0001…RFC-0008 Accepted `1.0.0`, with direct focus on RFC-0003, RFC-0005 and RFC-0006; Accepted ADR-0001; canonical roadmap `2.83.0`.\n\n## Implementation\n\n- new `Activity` navigation/surface in Productive Workspace;\n- current alerts are a presentation subset of the existing My Work groups `decision-required`, `blocked-failed` and `reconciliation-required`; P9.09 does not create a second priority/authority model;\n- timeline entries are explicitly observations from current authorized My Work and Governed Experience projections; `generated_at` / `observed_at` are not misrepresented as Event occurrence time;\n- alert/timeline links only route to existing inspectable My Work or Governed Execution context; visibility does not authorize the later action;\n- source reads fail closed as one activity view: partial protected activity is not retained if a required current source cannot be revalidated;\n- notification delivery and read/unread persistence are intentionally absent from this scope;\n- release `p9.09.1`, internal application contract `7`, remains `bounded-internal-provisional`, `public_api: false`.\n\n## Functional cross-review\n\nThree iterations completed (maximum 7).\n\n1. Architecture/security: rejected pseudo-Event semantics, delivery authority and durable read/unread state; required fail-closed current-source behavior.\n2. Product/UX: reused P9.04 attention groups instead of introducing product-specific or competing priority semantics; retained human-readable routes and scenario labels.\n3. Engineering/operations: kept the feature inside the Accepted ADR-0001 SPA/BFF release boundary; preserved exact-release rebuild/reproducibility and no new service/runtime.\n\nResult: `PASS`; no material objection remains. This functional review is not formal RFC/ADR acceptance or lifecycle promotion.\n\n## Verification\n\nOne-shot implementation/reconciliation workflow run: `{run_id}`. The helper executed Python compilation + Workspace backend tests, TypeScript typecheck, frontend tests, Web Storage guard and production asset rebuild before creating the implementation commit. Normal pull-request CI remains the independent closure gate before merge.\n\n## Explicit limitations\n\n- Activity is a non-authoritative read-side projection, not the canonical Event history or audit log.\n- Alert visibility, ordering and routing do not create Authorization, Organizational Authority or consequential approval.\n- No email/push/external notification channel is claimed.\n- No durable read/unread or acknowledgment semantics are established.\n- P9.09 does not promote any Product Contract or Platform Capability lifecycle state and does not establish public/customer Production, SLA, support or conformance claims.\n'''
    (ROOT / "docs/reviews/P9-09-activity-notifications-attention-routing.md").write_text(review, encoding="utf-8")

    phase = "docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md"
    replace(phase, "Version: `1.10.0`", "Version: `1.11.0`")
    replace(phase,
        '| **`P9.09`** | **Activity, notifications and attention routing** | **🟨 Current** | human-readable operational timeline/alerts projection |\n| `P9.10` | ООО «Арвектум» organization composition | ⬜ | company-level navigation over products/projects/knowledge/work |',
        '| `P9.09` | Activity, notifications and attention routing | 🟩 Complete / PASS | non-authoritative observed timeline + current attention routing |\n| **`P9.10`** | **ООО «Арвектум» organization composition** | **🟨 Current** | company-level navigation over products/projects/knowledge/work |')
    replace(phase,
        '> **P9.09 — Activity, notifications and attention routing.**\n\nAdd a human-readable operational activity/notification projection that routes attention without turning telemetry, derived timelines or notification delivery into canonical authority. Preserve the P9.04 attention semantics, P9.05 provenance/source distinctions, P9.06 Governed Execution boundary, P9.07 product ownership boundary and P9.08 AI authority/grounding guarantees.\n\nP9.08 is complete within the exact private internal scope. M9 remains open; P9.09–P9.12 and R31/R32 still govern the remaining activity, company composition, dogfooding and hardening work.',
        '> **P9.10 — ООО «Арвектум» organization composition.**\n\nCompose the company-level navigation over products, projects, knowledge and work while preserving product ownership, Product Contract boundaries, source authority and scoped access.\n\nP9.09 is complete within the exact private internal scope. M9 remains open; P9.10–P9.12 and R31/R32 still govern company composition, dogfooding and hardening work.')
    target = ROOT / phase
    text = target.read_text(encoding="utf-8")
    text += '''\n\n## 20. P9.09 closure result\n\nStatus: `Complete / PASS` within the exact private internal scope.\n\nP9.09 adds Activity as a non-authoritative observed timeline and current alert-routing surface. Alerts reuse P9.04 My Work semantics; projection timestamps are not represented as canonical Event occurrence; no durable read/unread state, notification authority or new consequential action path is created.\n\nClosure evidence: [`P9-09-activity-notifications-attention-routing.md`](../reviews/P9-09-activity-notifications-attention-routing.md). Workspace release is `p9.09.1`, internal application contract `7`, still bounded-internal-provisional and non-public. Product Contract and Platform Capability lifecycle states are unchanged.\n'''
    target.write_text(text, encoding="utf-8")

    roadmap = "docs/roadmap/ROADMAP.md"
    replace(roadmap, "Version: `2.83.0`", "Version: `2.84.0`")
    replace(roadmap,
        'Version `2.83.0` closes **`P9.08 — Arvectum AI Copilot + source-grounded organizational assistance`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`P9.09 — Activity, notifications and attention routing`**.',
        'Version `2.84.0` closes **`P9.09 — Activity, notifications and attention routing`** as `Complete / PASS` within its exact private internal scope and advances Phase 9 to **`P9.10 — ООО «Арвектум» organization composition`**.')
    replace(roadmap,
        'P9.08 final implementation/test evidence: head `e5bedffa778cd2487929f826f10359071c1f0b76`; Productive Workspace CI `#90` / run `32553258369` and Reference Python CI `#322` / run `32553258317` passed; functional cross-review completed 3 iterations with no material objection; P9.01 J6 implementation acceptance passed. Product Contracts and Platform Capabilities remain unchanged.',
        f'P9.09 implementation/reconciliation evidence: one-shot workflow run `{run_id}` completed code/test/build reconciliation before PR verification; functional cross-review completed 3 iterations with no material objection. Activity remains a non-authoritative projection, alerts reuse P9.04 attention semantics, and no notification/read-receipt authority is created. Product Contracts and Platform Capabilities remain unchanged.')
    replace(roadmap,
        '| **`P9.09`** | **Activity, notifications and attention routing** | **🟨 Current** | human-readable operational timeline/alerts projection |\n| `P9.10` | ООО «Арвектум» organization composition | ⬜ | company-level navigation over products/projects/knowledge/work |',
        '| `P9.09` | Activity, notifications and attention routing | 🟩 Complete / PASS | non-authoritative observed timeline + current attention routing |\n| **`P9.10`** | **ООО «Арвектум» organization composition** | **🟨 Current** | company-level navigation over products/projects/knowledge/work |')
    replace(roadmap,
        '> **P9.09 — Activity, notifications and attention routing.**',
        '> **P9.10 — ООО «Арвектум» organization composition.**')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("apply", "close"))
    parser.add_argument("--run-id", default="unknown")
    args = parser.parse_args()
    apply() if args.mode == "apply" else close(args.run_id)
