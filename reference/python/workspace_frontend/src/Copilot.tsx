import { useState } from "react";
import type { FormEvent } from "react";
import { askCopilot, WorkspaceApiError } from "./api";
import type { CopilotAnswer, CopilotClaimKind } from "./types";

const starters = [
  "What is the current status of EIS notice 0344100006426000005 and which source is authoritative?",
  "Why is Tender Operator context available in the current workspace, and what evidence supports it?",
  "What Discount Parser reconstruction context is retained, and what uncertainty or reconciliation limits remain?",
];

const claimLabels: Record<CopilotClaimKind, string> = {
  "sourced-fact": "Sourced fact",
  synthesis: "AI synthesis",
  uncertainty: "Uncertainty",
  "unavailable-evidence": "Unavailable evidence",
};

export function Copilot({ csrfToken }: { csrfToken: string }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<CopilotAnswer | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const normalized = question.trim();
    if (!normalized || loading) return;
    setLoading(true);
    setError(null);
    try {
      setAnswer(await askCopilot(normalized, csrfToken));
    } catch (caught) {
      setAnswer(null);
      setError(caught instanceof WorkspaceApiError ? caught.code : "COPILOT_UNAVAILABLE");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="copilot" aria-labelledby="copilot-title">
      <div className="copilot-heading">
        <p className="eyebrow">Arvectum AI Copilot</p>
        <h1 id="copilot-title">Ask the organization, then inspect the evidence.</h1>
        <p>
          Ask a natural-language question. Arvectum separates sourced facts, AI synthesis, uncertainty and unavailable
          evidence. The answer is a transient output: it is not validated Knowledge, permission, approval or authority.
        </p>
      </div>

      <div className="copilot-starters" aria-label="Example grounded questions">
        {starters.map((starter) => (
          <button key={starter} type="button" onClick={() => setQuestion(starter)}>{starter}</button>
        ))}
      </div>

      <form className="copilot-form" onSubmit={(event) => void submit(event)}>
        <label htmlFor="copilot-question">Question</label>
        <textarea
          id="copilot-question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          maxLength={800}
          rows={5}
          placeholder="Ask about organizational records, evidence, product context, provenance or current governed state…"
        />
        <div className="copilot-form-footer">
          <small>Only the current server-authorized Workspace scope is eligible for retrieval.</small>
          <button type="submit" disabled={!question.trim() || loading}>{loading ? "Grounding answer…" : "Ask Arvectum"}</button>
        </div>
      </form>

      {error ? (
        <div className="copilot-unavailable" role="alert">
          <strong>Copilot unavailable</strong>
          <p>The request could not be answered safely in the current Workspace context.</p>
          <code>{error}</code>
        </div>
      ) : null}

      {answer ? (
        <div className="copilot-answer" aria-live="polite">
          <div className="copilot-answer-heading">
            <div>
              <p className="eyebrow">Grounded response</p>
              <h2>Answer</h2>
            </div>
            <span className="transient-badge">Transient · not validated Knowledge</span>
          </div>

          <div className="claim-list">
            {answer.claims.map((claim, index) => (
              <article className={`claim-card claim-${claim.kind}`} key={`${claim.kind}-${index}`}>
                <span className="claim-kind">{claimLabels[claim.kind]}</span>
                <p>{claim.text}</p>
              </article>
            ))}
          </div>

          <section className="copilot-sources" aria-labelledby="copilot-sources-title">
            <h2 id="copilot-sources-title">Inspectable evidence</h2>
            {answer.sources.length ? (
              <div className="source-list">
                {answer.sources.map((source) => (
                  <article className="source-card" key={source.id}>
                    <div className="source-card-topline">
                      <span>{source.semantic_role}</span><span>{source.freshness}</span>
                    </div>
                    <h3>{source.label}</h3>
                    <p>{source.summary}</p>
                    <dl>
                      <div><dt>Authority / source</dt><dd>{source.authority}</dd></div>
                      {source.knowledge_role ? <div><dt>Knowledge role</dt><dd>{source.knowledge_role}</dd></div> : null}
                    </dl>
                    <a href={source.open_href}>Open evidence in Workspace</a>
                  </article>
                ))}
              </div>
            ) : <p className="boundary-note">No inspectable evidence was sufficient to ground this question.</p>}
          </section>

          <div className="copilot-boundary-grid">
            <article>
              <span className="eyebrow">Model</span>
              <strong>{answer.model.used ? `${answer.model.provider} · ${answer.model.model}` : "No synthesis used"}</strong>
              <p>{answer.model.failure ? `Model limitation: ${answer.model.failure}` : "Free-form model output can only appear as synthesis, never as sourced fact."}</p>
            </article>
            <article>
              <span className="eyebrow">Authority</span>
              <strong>Not provided</strong>
              <p>Asking a question cannot grant authorization, Organizational Authority or consequential approval.</p>
            </article>
            <article>
              <span className="eyebrow">Persistence</span>
              <strong>Transient response</strong>
              <p>The question and answer are not silently promoted into Memory, validated Knowledge or canonical state.</p>
            </article>
          </div>

          <div className="copilot-follow-up">
            <div>
              <strong>Need a consequential follow-up?</strong>
              <p>Review the current governed execution/decision gates. Copilot does not execute the consequence itself.</p>
            </div>
            <a className="quiet-link" href={answer.follow_up.href}>{answer.follow_up.label}</a>
          </div>
        </div>
      ) : null}
    </section>
  );
}
