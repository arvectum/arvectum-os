import { useState } from "react";
import type { ProductSurfaceContext } from "../types";

export function TenderOperatorSurface({ surface }: { surface: ProductSurfaceContext }) {
  const [technicalOpen, setTechnicalOpen] = useState(false);
  return (
    <section className="hero" aria-labelledby="tender-surface-title">
      <p className="eyebrow">Product-owned surface · {surface.contour.id}</p>
      <h1 id="tender-surface-title">Tender Operator</h1>
      <p>{surface.contour.summary}</p>
      <div className="status-grid">
        <article><span>Product Contract</span><strong>{surface.product_contract.id} · {surface.product_contract.lifecycle} {surface.product_contract.version}</strong><p>Composition does not promote this lifecycle.</p></article>
        <article><span>Shared reliance</span><strong>{surface.contour.shared_dependencies.join(", ")}</strong><p>Exact Tender Operator platform reliance remains contract-scoped.</p></article>
        <article><span>Authority</span><strong>{surface.contour.source_authority}</strong><p>The Workspace presentation does not replace the authoritative source.</p></article>
      </div>
      <p className="boundary-note">Tender schemas, procurement rules and product workflows remain owned by Tender Operator. This read-only composition grants no authorization, Organizational Authority or consequential approval.</p>
      <details onToggle={(event) => setTechnicalOpen(event.currentTarget.open)}>
        <summary>Technical Product Contract and provenance</summary>
        {technicalOpen ? (
          <dl>
            <dt>Repository</dt><dd>{surface.repository}</dd>
            <dt>Product release</dt><dd>{surface.technical.product_release_sha ?? "Not exposed by retained evidence"}</dd>
            <dt>Evidence</dt><dd>{surface.technical.evidence_refs.join(" · ")}</dd>
          </dl>
        ) : null}
      </details>
    </section>
  );
}
