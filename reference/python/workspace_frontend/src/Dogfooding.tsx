import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";
import {
  dispositionDogfoodingObservation,
  loadDogfoodingBacklog,
  recordDogfoodingObservation,
  WorkspaceApiError,
} from "./api";
import type {
  DogfoodingBacklog,
  DogfoodingClassification,
  DogfoodingDisposition,
  DogfoodingJourney,
  DogfoodingObservation,
  DogfoodingObservationInput,
  DogfoodingSeverity,
  DogfoodingSurface,
} from "./dogfoodingTypes";
import "./Dogfooding.css";

const journeyLabels: Record<DogfoodingJourney, string> = {
  J1: "J1 · answer what needs attention now",
  J2: "J2 · understand one object in context",
  J3: "J3 · discover records, documents and knowledge",
  J4: "J4 · ask Arvectum with inspectable evidence",
  J5: "J5 · inspect or continue governed work",
  J6: "J6 · inspect product context without hidden coupling",
  other: "Other ordinary Workspace journey",
};

const surfaceLabels: Record<DogfoodingSurface, string> = {
  home: "Home",
  organization: "Organization",
  "my-work": "My Work",
  activity: "Activity",
  search: "Search",
  "records-documents-knowledge": "Records / Documents / Knowledge",
  "ask-arvectum": "Ask Arvectum",
  "governed-actions": "Governed actions",
  products: "Products",
  other: "Other",
};

const classificationLabels: Record<DogfoodingClassification, string> = {
  "workspace-usability": "Workspace usability defect",
  "product-specific": "Product-specific gap",
  governance: "Governance / contract gap",
  "security-authority": "Security / authority concern",
};

const dispositionLabels: Record<DogfoodingDisposition, string> = {
  resolved: "Resolved and rechecked",
  "routed-product": "Routed to product-owned backlog",
  "routed-governance": "Routed to governance work",
  "not-reproducible": "Not reproducible after recheck",
  deferred: "Deferred with explicit rationale",
};

function allowedDispositions(item: DogfoodingObservation): DogfoodingDisposition[] {
  const allowed: DogfoodingDisposition[] = ["resolved", "not-reproducible"];
  if (item.classification === "product-specific") allowed.push("routed-product");
  if (item.classification === "governance" || item.classification === "security-authority") allowed.push("routed-governance");
  if (item.severity !== "blocker" && item.classification !== "security-authority") allowed.push("deferred");
  return allowed;
}

type LoadState =
  | { kind: "loading" }
  | { kind: "ready"; backlog: DogfoodingBacklog }
  | { kind: "error"; code: string };

function DispositionForm({
  item,
  csrfToken,
  onChanged,
}: {
  item: DogfoodingObservation;
  csrfToken: string;
  onChanged: () => Promise<void>;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const allowed = allowedDispositions(item);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setBusy(true);
    setError(null);
    const form = new FormData(event.currentTarget);
    try {
      await dispositionDogfoodingObservation(
        item.id,
        String(form.get("disposition")) as DogfoodingDisposition,
        String(form.get("rationale") ?? ""),
        csrfToken,
      );
      await onChanged();
    } catch (caught) {
      setError(caught instanceof WorkspaceApiError ? caught.code : "DOGFOODING_DISPOSITION_FAILED");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="dogfood-disposition" onSubmit={(event) => void submit(event)}>
      <label>
        Disposition
        <select name="disposition" defaultValue={allowed[0]}>
          {allowed.map((value) => (
            <option key={value} value={value}>{dispositionLabels[value]}</option>
          ))}
        </select>
      </label>
      <label>
        Rationale
        <input
          name="rationale"
          required
          maxLength={500}
          placeholder="What changed, where it was routed, or why it is deferred"
        />
      </label>
      <button type="submit" disabled={busy}>{busy ? "Saving…" : "Disposition"}</button>
      {error ? <p className="dogfood-error" role="alert">{error}</p> : null}
    </form>
  );
}

export function Dogfooding({ csrfToken }: { csrfToken: string }) {
  const [state, setState] = useState<LoadState>({ kind: "loading" });
  const [captureBusy, setCaptureBusy] = useState(false);
  const [captureError, setCaptureError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setState({ kind: "ready", backlog: await loadDogfoodingBacklog() });
    } catch (caught) {
      setState({ kind: "error", code: caught instanceof WorkspaceApiError ? caught.code : "DOGFOODING_UNAVAILABLE" });
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  const capture = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    const input: DogfoodingObservationInput = {
      journey: String(form.get("journey")) as DogfoodingJourney,
      surface: String(form.get("surface")) as DogfoodingSurface,
      severity: String(form.get("severity")) as DogfoodingSeverity,
      classification: String(form.get("classification")) as DogfoodingClassification,
      summary: String(form.get("summary") ?? ""),
      details: String(form.get("details") ?? ""),
    };
    setCaptureBusy(true);
    setCaptureError(null);
    try {
      await recordDogfoodingObservation(input, csrfToken);
      formElement.reset();
      await refresh();
    } catch (caught) {
      setCaptureError(caught instanceof WorkspaceApiError ? caught.code : "DOGFOODING_CAPTURE_FAILED");
    } finally {
      setCaptureBusy(false);
    }
  };

  return (
    <section className="dogfood-page" aria-labelledby="dogfood-title">
      <p className="eyebrow">P9.11 · Real daily-use dogfooding</p>
      <h1 id="dogfood-title">Capture friction where the work actually happens.</h1>
      <p className="dogfood-boundary">
        Entries are bounded, owner-operated observations only. They are not canonical Events, validated Knowledge,
        authorization, Organizational Authority, or approval. Do not paste secrets or unnecessary protected content.
      </p>

      <form className="dogfood-capture" onSubmit={(event) => void capture(event)}>
        <div className="dogfood-grid">
          <label>
            Journey
            <select name="journey" defaultValue="J1">
              {(Object.keys(journeyLabels) as DogfoodingJourney[]).map((value) => (
                <option key={value} value={value}>{journeyLabels[value]}</option>
              ))}
            </select>
          </label>
          <label>
            Surface
            <select name="surface" defaultValue="my-work">
              {(Object.keys(surfaceLabels) as DogfoodingSurface[]).map((value) => (
                <option key={value} value={value}>{surfaceLabels[value]}</option>
              ))}
            </select>
          </label>
          <label>
            Severity
            <select name="severity" defaultValue="material">
              <option value="blocker">Blocker · ordinary work cannot continue</option>
              <option value="material">Material · recurring or costly friction</option>
              <option value="minor">Minor · usable but unnecessarily awkward</option>
            </select>
          </label>
          <label>
            Classification
            <select name="classification" defaultValue="workspace-usability">
              {(Object.keys(classificationLabels) as DogfoodingClassification[]).map((value) => (
                <option key={value} value={value}>{classificationLabels[value]}</option>
              ))}
            </select>
          </label>
        </div>
        <label>
          Short observation
          <input name="summary" required maxLength={240} placeholder="Describe the friction in one sentence" />
        </label>
        <label>
          Minimal supporting detail
          <textarea name="details" maxLength={600} rows={3} placeholder="Only what is needed to reproduce or understand it" />
        </label>
        <div className="dogfood-actions">
          <button type="submit" disabled={captureBusy}>{captureBusy ? "Recording…" : "Record observation"}</button>
          <span>Retention: 90 days · capacity: 200 entries · expired entries pruned on access</span>
        </div>
        {captureError ? <p className="dogfood-error" role="alert">{captureError}</p> : null}
      </form>

      {state.kind === "loading" ? <p aria-live="polite">Loading current friction backlog…</p> : null}
      {state.kind === "error" ? <p className="dogfood-error" role="alert">{state.code}</p> : null}
      {state.kind === "ready" ? (
        <section aria-labelledby="dogfood-backlog-title">
          <div className="dogfood-summary">
            <div><span>Total retained</span><strong>{state.backlog.summary.total}</strong></div>
            <div><span>Open observations</span><strong>{state.backlog.summary.open}</strong></div>
            <div><span>P9.11 closure-blocking</span><strong>{state.backlog.summary.closure_blocking}</strong></div>
          </div>
          <h2 id="dogfood-backlog-title">Friction backlog</h2>
          {state.backlog.items.length === 0 ? <p>No observations captured yet. Real owner sessions are still required for P9.11 closure.</p> : null}
          {state.backlog.summary.closure_blocking > 0 ? (
            <p className="dogfood-boundary">Blocker/material observations that are open or deferred still block P9.11 friction-backlog closure.</p>
          ) : null}
          <div className="dogfood-list">
            {state.backlog.items.map((item) => (
              <article key={item.id} className="dogfood-item">
                <div className="dogfood-item-head">
                  <strong>{item.summary}</strong>
                  <span>{item.status === "open" ? "Open" : dispositionLabels[item.disposition!]}</span>
                </div>
                <p>{item.details || "No additional detail recorded."}</p>
                <dl>
                  <div><dt>Journey</dt><dd>{item.journey}</dd></div>
                  <div><dt>Surface</dt><dd>{surfaceLabels[item.surface]}</dd></div>
                  <div><dt>Severity</dt><dd>{item.severity}</dd></div>
                  <div><dt>Classification</dt><dd>{classificationLabels[item.classification]}</dd></div>
                  <div><dt>Release</dt><dd>{item.release_id}</dd></div>
                </dl>
                {item.status === "open" ? (
                  <DispositionForm item={item} csrfToken={csrfToken} onChanged={refresh} />
                ) : (
                  <p className="dogfood-rationale"><strong>Rationale:</strong> {item.disposition_rationale}</p>
                )}
              </article>
            ))}
          </div>
        </section>
      ) : null}
    </section>
  );
}
