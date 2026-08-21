import { useEffect, useState } from "react";
import { loadObjectContext, WorkspaceApiError } from "./api";
import type { ObjectContext } from "./types";

function navigate(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function backToDiscovery() {
  navigate("/search");
}

function TechnicalDetails({ item }: { item: ObjectContext }) {
  return (
    <details className="technical-details">
      <summary>Exact technical identity and provenance</summary>
      <p>These identifiers are evidence for exact reconstruction. They are not required for ordinary navigation.</p>
      <dl>
        <div><dt>Subject identity</dt><dd><code>{item.technical.subject_identity}</code></dd></div>
        <div><dt>Version identity</dt><dd><code>{item.technical.version_identity}</code></dd></div>
        <div><dt>Schema version</dt><dd><code>{item.technical.schema_version}</code></dd></div>
        <div><dt>Source release</dt><dd><code>{item.technical.source_release_sha}</code></dd></div>
        {item.technical.related_execution_subject ? <div><dt>Execution subject</dt><dd><code>{item.technical.related_execution_subject}</code></dd></div> : null}
        {item.technical.related_execution_version ? <div><dt>Execution version</dt><dd><code>{item.technical.related_execution_version}</code></dd></div> : null}
        {item.technical.related_event_version ? <div><dt>Related event</dt><dd><code>{item.technical.related_event_version}</code></dd></div> : null}
        {item.technical.related_checkpoint ? <div><dt>Recovery checkpoint</dt><dd><code>{item.technical.related_checkpoint}</code></dd></div> : null}
      </dl>
      <h3>Provenance references</h3>
      {item.technical.provenance_refs.length ? (
        <ul className="provenance-list">
          {item.technical.provenance_refs.map((ref) => <li key={ref}><code>{ref}</code></li>)}
        </ul>
      ) : <p>No provenance references are declared in the current retained source.</p>}
    </details>
  );
}

export function ObjectDetail({ objectId }: { objectId: string }) {
  const [item, setItem] = useState<ObjectContext | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setItem(null);
    setError(null);
    void loadObjectContext(objectId)
      .then((value) => { if (!cancelled) setItem(value); })
      .catch((reason) => {
        if (cancelled) return;
        setError(reason instanceof WorkspaceApiError ? reason.code : "OBJECT_UNAVAILABLE");
      });
    return () => { cancelled = true; };
  }, [objectId]);

  if (error) {
    return (
      <section className="object-context object-unavailable" role="alert">
        <p className="eyebrow">Object context</p>
        <h1>Object unavailable</h1>
        <p>The current source could not be revalidated or the opaque reference no longer resolves. No protected existence or historical details are inferred.</p>
        <code>{error}</code>
        <button type="button" className="quiet-button" onClick={backToDiscovery}>Back to search</button>
      </section>
    );
  }

  if (!item) return <p aria-live="polite">Revalidating current governed object context…</p>;

  return (
    <article className="object-context" aria-labelledby="object-title">
      <div className="object-heading">
        <div>
          <p className="eyebrow">{item.kind} · {item.semantic_role}</p>
          <h1 id="object-title">{item.title}</h1>
          <p>{item.summary}</p>
        </div>
        <button type="button" className="quiet-button" onClick={backToDiscovery}>Back to search</button>
      </div>

      {item.knowledge_role ? <p className="semantic-warning">{item.knowledge_role}</p> : null}

      <section className="context-panel" aria-labelledby="meaning-title">
        <h2 id="meaning-title">What this is</h2>
        <p>{item.context.meaning}</p>
        <dl>
          <div><dt>Authoritative source</dt><dd>{item.authority.authoritative_source}</dd></div>
          <div><dt>Authority mode</dt><dd>{item.authority.mode}</dd></div>
          <div><dt>Authority scope</dt><dd>{item.authority.scope}</dd></div>
          <div><dt>Lifecycle</dt><dd>{item.state.lifecycle ?? "Not declared in retained metadata"}</dd></div>
          <div><dt>Validation</dt><dd>{item.state.validation ?? "Not declared in retained metadata"}</dd></div>
        </dl>
      </section>

      <section className="context-panel" aria-labelledby="process-title">
        <h2 id="process-title">Context and next step</h2>
        <p>{item.context.process}</p>
        <p><strong>Next step:</strong> {item.context.next_step}</p>
        <p className="boundary-note">This read-only view grants no Authorization, Organizational Authority or consequential approval.</p>
      </section>

      {item.governed_preflight ? (
        <section className="context-panel" aria-labelledby="preflight-title">
          <h2 id="preflight-title">Governed preflight context</h2>
          <p><strong>Outcome: {item.governed_preflight.outcome ?? "Not declared"}.</strong> The Workspace does not turn technical access into approval.</p>
          {item.governed_preflight.waiting_gates.length ? (
            <>
              <p>Waiting gates:</p>
              <ul>{item.governed_preflight.waiting_gates.map((gate) => <li key={gate}>{gate}</li>)}</ul>
            </>
          ) : null}
          <a
            className="context-action-link"
            href="/governed"
            onClick={(event) => {
              event.preventDefault();
              navigate("/governed");
            }}
          >
            Open related execution and governed action
          </a>
        </section>
      ) : null}

      <TechnicalDetails item={item} />
    </article>
  );
}
