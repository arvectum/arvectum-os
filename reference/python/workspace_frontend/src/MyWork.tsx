import { useCallback, useEffect, useState } from "react";
import { loadMyWork, WorkspaceApiError } from "./api";
import type {
  AttentionGroup,
  AttentionItem,
  AttentionUrgency,
  MyWorkProjection,
} from "./types";

type LoadState =
  | { kind: "loading" }
  | { kind: "ready"; projection: MyWorkProjection }
  | { kind: "error"; code: string; reloadRequired: boolean };

const groupLabels: Record<AttentionGroup, string> = {
  "decision-required": "Decision / input required",
  "blocked-failed": "Blocked / failed",
  "reconciliation-required": "Awaiting reconciliation",
  "recent-outcome": "Recent important outcome",
  informational: "Informational",
};

const kindLabels: Record<AttentionItem["kind"], string> = {
  "waiting-approval": "Waiting approval",
  "waiting-input": "Waiting input",
  "reconciliation-required": "Reconciliation required",
  "guarded-action-failed": "Guarded action failed",
  "recoverable-system-condition": "System condition",
  "recent-outcome": "Recent outcome",
  informational: "Informational",
};

const urgencyOrder: Record<AttentionUrgency, number> = { high: 0, medium: 1, low: 2 };

function displayTime(value: string | null): string {
  if (!value) return "Observation time unavailable";
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

function currentFocus(): string | null {
  return new URLSearchParams(window.location.search).get("focus");
}

function pushWorkspaceHref(href: string): void {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function MyWork({ embedded = false }: { embedded?: boolean }) {
  const [state, setState] = useState<LoadState>({ kind: "loading" });
  const [group, setGroup] = useState<AttentionGroup | "all">("all");
  const [urgency, setUrgency] = useState<AttentionUrgency | "all">("all");
  const [sort, setSort] = useState<"urgency" | "newest">("urgency");

  const refresh = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      setState({ kind: "ready", projection: await loadMyWork() });
    } catch (error) {
      if (error instanceof WorkspaceApiError) {
        setState({ kind: "error", code: error.code, reloadRequired: error.reloadRequired });
      } else {
        setState({ kind: "error", code: "MY_WORK_UNAVAILABLE", reloadRequired: false });
      }
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  const focusId = embedded ? null : currentFocus();
  const titleId = embedded ? "home-my-work-title" : "my-work-title";
  const Heading = embedded ? "h2" : "h1";

  if (state.kind === "loading") {
    return (
      <section className={`my-work${embedded ? " my-work-embedded" : ""}`} aria-live="polite">
        <p>Loading current attention sources…</p>
      </section>
    );
  }
  if (state.kind === "error") {
    return (
      <section className={`my-work my-work-error${embedded ? " my-work-embedded" : ""}`} role="alert">
        <p className="eyebrow">My Work</p>
        <Heading>Needs attention is unavailable.</Heading>
        <p>
          {state.reloadRequired
            ? "The application release changed. Reload before relying on this projection."
            : "Current source scope could not be safely resolved. No protected work-item detail is shown."}
        </p>
        <code>{state.code}</code>
        <button type="button" onClick={() => state.reloadRequired ? window.location.reload() : void refresh()}>
          {state.reloadRequired ? "Reload application" : "Try again"}
        </button>
      </section>
    );
  }

  const projection = state.projection;
  const filtered = projection.items
    .filter((item) => group === "all" || item.group === group)
    .filter((item) => urgency === "all" || item.urgency === urgency)
    .sort((left, right) => {
      if (sort === "urgency") {
        const urgencyDelta = urgencyOrder[left.urgency] - urgencyOrder[right.urgency];
        if (urgencyDelta !== 0) return urgencyDelta;
      }
      return (Date.parse(right.observed_at ?? "") || 0) - (Date.parse(left.observed_at ?? "") || 0);
    });
  const visible = embedded ? filtered.slice(0, 3) : filtered;
  const focused = focusId ? projection.items.find((item) => item.id === focusId) : undefined;

  const navigateTo = (item: AttentionItem) => (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    if (!item.open_href.startsWith("/my-work?focus=")) return;
    pushWorkspaceHref(item.open_href);
  };

  return (
    <section className={`my-work${embedded ? " my-work-embedded" : ""}`} aria-labelledby={titleId}>
      <div className="my-work-heading">
        <div>
          <p className="eyebrow">My Work · derived projection</p>
          <Heading id={titleId}>Needs attention</Heading>
          <p>Current owner-facing signals, filtered server-side before they reach the browser.</p>
        </div>
        {embedded ? (
          <a className="quiet-link" href="/my-work" onClick={(event) => {
            event.preventDefault();
            pushWorkspaceHref("/my-work");
          }}>Open My Work</a>
        ) : (
          <button type="button" className="quiet-button" onClick={() => void refresh()}>Refresh</button>
        )}
      </div>

      <div className={`projection-health projection-health-${projection.health.state}`} role="status">
        <strong>{projection.health.state === "fresh" ? "Current" : projection.health.state === "stale" ? "Stale" : "Degraded"}</strong>
        <span>{projection.health.message}</span>
        <small>Checked {displayTime(projection.health.observed_at)}</small>
      </div>

      <p className="boundary-note">
        This queue is non-authoritative. Visibility does not grant permission, Organizational Authority,
        approval, or a right to retry an uncertain external effect.
      </p>

      {!embedded && focused ? (
        <article className="attention-detail" aria-labelledby="focused-attention-title">
          <p className="eyebrow">Focused work item · {kindLabels[focused.kind]}</p>
          <h2 id="focused-attention-title">{focused.title}</h2>
          <p>{focused.reason}</p>
          <dl>
            <div><dt>Source</dt><dd>{focused.source}</dd></div>
            <div><dt>Why now</dt><dd>{groupLabels[focused.group]}</dd></div>
            <div><dt>Legitimate next step</dt><dd>{focused.next_step}</dd></div>
            <div><dt>Interaction</dt><dd>Inspect only — current authority is revalidated elsewhere.</dd></div>
            {focused.technical_evidence_available ? (
              <div><dt>Technical evidence</dt><dd>Available in the governed source; exact identity/provenance drill-down is handled by the context surfaces activated after P9.04.</dd></div>
            ) : null}
          </dl>
          {focused.evidence_mode === "scenario" ? <p className="scenario-note">Controlled scenario evidence — not a live occurrence.</p> : null}
          <a href="/my-work" onClick={(event) => {
            event.preventDefault();
            pushWorkspaceHref("/my-work");
          }}>Back to queue</a>
        </article>
      ) : !embedded && focusId ? (
        <div className="attention-unavailable" role="status">
          <strong>Work item unavailable in the current projection.</strong>
          <p>It may no longer be visible, current, or authorized. No protected existence detail is disclosed.</p>
          <a href="/my-work" onClick={(event) => {
            event.preventDefault();
            pushWorkspaceHref("/my-work");
          }}>Back to queue</a>
        </div>
      ) : null}

      {!embedded ? (
        <div className="queue-toolbar" aria-label="My Work filters">
          <label>
            Work state
            <select value={group} onChange={(event) => setGroup(event.target.value as AttentionGroup | "all")}>
              <option value="all">All visible work</option>
              {Object.entries(groupLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
            </select>
          </label>
          <label>
            Urgency
            <select value={urgency} onChange={(event) => setUrgency(event.target.value as AttentionUrgency | "all")}>
              <option value="all">All urgency</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </label>
          <label>
            Sort
            <select value={sort} onChange={(event) => setSort(event.target.value as "urgency" | "newest")}>
              <option value="urgency">Urgency first</option>
              <option value="newest">Newest first</option>
            </select>
          </label>
        </div>
      ) : null}

      <div className="queue-summary" aria-live="polite">
        {embedded && projection.items.length > visible.length
          ? `Showing ${visible.length} of ${projection.items.length} visible items`
          : `${visible.length} visible item${visible.length === 1 ? "" : "s"}`}
      </div>
      {visible.length === 0 ? (
        <div className="empty-queue">
          <strong>No visible items match this view.</strong>
          <p>This does not assert that no protected work exists outside the current authorized projection.</p>
        </div>
      ) : (
        <div className="attention-list">
          {visible.map((item) => (
            <article className="attention-card" key={item.id}>
              <div className="attention-card-topline">
                <span className={`urgency urgency-${item.urgency}`}>{item.urgency} urgency</span>
                <span>{kindLabels[item.kind]}</span>
                {item.evidence_mode === "scenario" ? <span>Scenario evidence</span> : null}
              </div>
              <h2>{item.title}</h2>
              <p>{item.reason}</p>
              <dl>
                <div><dt>Source</dt><dd>{item.source}</dd></div>
                <div><dt>Next step</dt><dd>{item.next_step}</dd></div>
              </dl>
              <div className="attention-card-footer">
                <small>{displayTime(item.observed_at)}</small>
                <a href={item.open_href} onClick={navigateTo(item)}>Inspect</a>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
