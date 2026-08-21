import { FormEvent, useEffect, useState } from "react";
import { loadDiscovery, WorkspaceApiError } from "./api";
import type { DiscoveryKind, DiscoveryProjection, DiscoveryResult } from "./types";

const surfaceCopy: Record<string, { eyebrow: string; title: string; intro: string }> = {
  search: {
    eyebrow: "Global discovery",
    title: "Find organizational context",
    intro: "Search current governed Records, Documents and Knowledge by human context. Search is a non-authoritative projection; opening a result revalidates the current source before context is shown.",
  },
  record: {
    eyebrow: "Records",
    title: "Governed records",
    intro: "Browse current governed records without learning Subject or Version identifiers. Technical identity remains available only inside an opened object.",
  },
  document: {
    eyebrow: "Documents",
    title: "Documents and artifacts",
    intro: "Find governed Document context while preserving the declared authority source and exact-version evidence behind the human view.",
  },
  knowledge: {
    eyebrow: "Knowledge",
    title: "Knowledge and organizational memory",
    intro: "Browse knowledge-related governed records without treating Observations, Memory or candidates as validated Knowledge.",
  },
};

function navigate(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function ResultCard({ item }: { item: DiscoveryResult }) {
  return (
    <article className="discovery-card">
      <div className="discovery-card-topline">
        <span>{item.kind}</span>
        <span>{item.semantic_role}</span>
        <span>{item.authority_mode}</span>
      </div>
      <h2>{item.title}</h2>
      {item.knowledge_role ? <p className="semantic-warning">{item.knowledge_role}</p> : null}
      <p>{item.summary}</p>
      <dl>
        <div><dt>Source</dt><dd>{item.source}</dd></div>
        <div><dt>State</dt><dd>{item.state}</dd></div>
      </dl>
      <div className="discovery-card-footer">
        <small>Search result · non-authoritative · inspect only</small>
        <a
          href={item.open_href}
          onClick={(event) => {
            event.preventDefault();
            navigate(item.open_href);
          }}
        >
          Open context
        </a>
      </div>
    </article>
  );
}

export function Discovery({ kind }: { kind?: DiscoveryKind }) {
  const routeQuery = new URLSearchParams(window.location.search).get("q") ?? "";
  const [query, setQuery] = useState(routeQuery);
  const [projection, setProjection] = useState<DiscoveryProjection | null>(null);
  const [error, setError] = useState<string | null>(null);
  const copy = surfaceCopy[kind ?? "search"];

  useEffect(() => {
    let cancelled = false;
    setError(null);
    setProjection(null);
    void loadDiscovery(routeQuery, kind)
      .then((value) => { if (!cancelled) setProjection(value); })
      .catch((reason) => {
        if (cancelled) return;
        setError(reason instanceof WorkspaceApiError ? reason.code : "DISCOVERY_UNAVAILABLE");
      });
    return () => { cancelled = true; };
  }, [routeQuery, kind]);

  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = query.trim();
    const base = kind === "record" ? "/records" : kind === "document" ? "/documents" : kind === "knowledge" ? "/knowledge" : "/search";
    navigate(trimmed ? `${base}?q=${encodeURIComponent(trimmed)}` : base);
  };

  return (
    <section className="discovery" aria-labelledby="discovery-title">
      <div className="discovery-heading">
        <p className="eyebrow">{copy.eyebrow}</p>
        <h1 id="discovery-title">{copy.title}</h1>
        <p>{copy.intro}</p>
      </div>

      <form className="discovery-search" role="search" onSubmit={submit}>
        <label htmlFor="discovery-query">Search by name, source, external reference or meaningful context</label>
        <div>
          <input
            id="discovery-query"
            type="search"
            value={query}
            maxLength={160}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="e.g. notice number, source or document context"
          />
          <button type="submit">Search</button>
        </div>
      </form>

      {error ? (
        <div className="discovery-unavailable" role="alert">
          <h2>Discovery unavailable</h2>
          <p>Current protected discovery state could not be read safely. No protected result details are shown.</p>
          <code>{error}</code>
        </div>
      ) : projection ? (
        <>
          <div className={`discovery-health discovery-health-${projection.health.state}`} role="status">
            <strong>{projection.health.state}</strong>
            <span>{projection.health.message}</span>
            <small>Derived search · never canonical authority</small>
          </div>
          {projection.health.state === "degraded" ? (
            <div className="discovery-unavailable">
              <h2>Results withheld</h2>
              <p>The current governed source could not be revalidated. Refresh after source health/access is restored.</p>
            </div>
          ) : projection.results.length === 0 ? (
            <div className="empty-discovery">
              <h2>No accessible matches</h2>
              <p>No current authorized result matches this view. This message does not reveal whether denied objects exist.</p>
            </div>
          ) : (
            <>
              <p className="discovery-summary">{projection.results.length} accessible result{projection.results.length === 1 ? "" : "s"}</p>
              <div className="discovery-list">
                {projection.results.map((item) => <ResultCard key={item.id} item={item} />)}
              </div>
            </>
          )}
        </>
      ) : (
        <p aria-live="polite">Reading current authorized governed sources…</p>
      )}
    </section>
  );
}
