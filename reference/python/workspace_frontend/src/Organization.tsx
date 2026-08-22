import { useEffect, useState } from "react";
import { loadOrganizationComposition, WorkspaceApiError } from "./api";
import type { OrganizationCompositionProjection, OrganizationLane } from "./types";
import "./Organization.css";

type State =
  | { kind: "loading" }
  | { kind: "ready"; data: OrganizationCompositionProjection }
  | { kind: "error"; code: string };

function navigate(href: string, event: React.MouseEvent<HTMLAnchorElement>) {
  event.preventDefault();
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function Lane({ lane }: { lane: OrganizationLane }) {
  return (
    <section className="organization-lane" aria-labelledby={`organization-${lane.id}`}>
      <div className="organization-lane-head">
        <div>
          <p className="eyebrow">{lane.source_boundary}</p>
          <h2 id={`organization-${lane.id}`}>{lane.label}</h2>
        </div>
        <span className={`organization-lane-state state-${lane.state}`}>{lane.state}</span>
      </div>
      <p>{lane.summary}</p>
      {lane.items.length ? (
        <div className="organization-items">
          {lane.items.map((item) => (
            <article className="organization-item" key={item.id}>
              <div className="organization-item-meta">
                <span>{item.kind}</span><span>{item.state}</span>
              </div>
              <h3>{item.label}</h3>
              <p>{item.summary}</p>
              <dl>
                <div><dt>Source</dt><dd>{item.source}</dd></div>
                <div><dt>Authority</dt><dd>{item.authority}</dd></div>
                <div><dt>Ownership</dt><dd>{item.ownership}</dd></div>
                {item.semantic_note ? <div><dt>Semantics</dt><dd>{item.semantic_note}</dd></div> : null}
              </dl>
              {item.kind === "project-lens" ? <p className="boundary-note">Navigation lens only · not a canonical Project record.</p> : null}
              <a href={item.href} onClick={(event) => navigate(item.href, event)}>Open context</a>
            </article>
          ))}
        </div>
      ) : (
        <p className="boundary-note">No context is presented from this lane in the current authorized snapshot.</p>
      )}
    </section>
  );
}

export function Organization({ organizationLabel }: { organizationLabel: string }) {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    let live = true;
    void loadOrganizationComposition()
      .then((data) => { if (live) setState({ kind: "ready", data }); })
      .catch((error) => {
        const code = error instanceof WorkspaceApiError ? error.code : "ORGANIZATION_COMPOSITION_UNAVAILABLE";
        if (live) setState({ kind: "error", code });
      });
    return () => { live = false; };
  }, []);

  if (state.kind === "loading") return <section className="organization-page" aria-live="polite">Composing organization context…</section>;
  if (state.kind === "error") {
    return (
      <section className="organization-page" role="alert">
        <p className="eyebrow">Organization composition</p>
        <h1>Organization context is unavailable.</h1>
        <p>Protected source context could not be safely composed.</p>
        <code>{state.code}</code>
      </section>
    );
  }

  return (
    <section className="organization-page" aria-labelledby="organization-title">
      <header className="organization-header">
        <p className="eyebrow">Organization composition</p>
        <h1 id="organization-title">{organizationLabel}</h1>
        <p>One company-level navigation view over already-authorized products, project lenses, knowledge and work.</p>
        <p className="boundary-note">
          This view is rebuildable and non-authoritative. It does not create Organizational Authority, a canonical company database,
          a canonical Project record, or product/company semantics in the Kernel.
        </p>
      </header>
      {state.data.health.state !== "ready" ? (
        <div className="organization-health" role="status">Some source lanes are degraded or unavailable; unavailable context is withheld rather than guessed.</div>
      ) : null}
      <div className="organization-lanes">
        {state.data.lanes.map((lane) => <Lane lane={lane} key={lane.id} />)}
      </div>
    </section>
  );
}
