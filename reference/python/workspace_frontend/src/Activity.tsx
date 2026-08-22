import { useCallback, useEffect, useMemo, useState } from "react";
import { loadGovernedExperience, loadMyWork, WorkspaceApiError } from "./api";
import type { AttentionItem, GovernedExperienceProjection, MyWorkProjection } from "./types";
import "./Activity.css";

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

// Reuse the already-governed P9.04 attention taxonomy instead of creating a second priority model.
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
