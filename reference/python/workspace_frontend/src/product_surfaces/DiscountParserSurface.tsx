import type { ProductSurfaceContext } from "../types";

export function DiscountParserSurface({ surface }: { surface: ProductSurfaceContext }) {
  return (
    <section className="hero" aria-labelledby="discount-surface-title">
      <p className="eyebrow">Product-owned surface · {surface.contour.id}</p>
      <h1 id="discount-surface-title">Discount Parser</h1>
      <p>{surface.contour.summary}</p>
      <div className="status-grid">
        <article>
          <span>Product Contract</span>
          <strong>{surface.product_contract.id} · {surface.product_contract.lifecycle} {surface.product_contract.version}</strong>
          <p>Composition does not promote this lifecycle.</p>
        </article>
        <article>
          <span>Shared reliance</span><strong>{surface.contour.shared_dependencies.join(", ")}</strong>
          <p>Platform reconstruction remains read-only.</p>
        </article>
        <article>
          <span>Effect boundary</span><strong>No effect replay</strong>
          <p>Offer/publication/database/template and delivery semantics remain product-owned and are not copied into the shared Workspace contract.</p>
        </article>
      </div>
      <p className="boundary-note">
        This surface exposes a verified retained context only. Product-specific publication work must continue through the product-owned governed boundary; the Workspace grants no authorization, Organizational Authority or approval.
      </p>
      <details>
        <summary>Technical Product Contract and provenance</summary>
        <dl>
          <dt>Repository</dt><dd>{surface.repository}</dd>
          <dt>Product release</dt><dd>{surface.technical.product_release_sha ?? "Not exposed by retained evidence"}</dd>
          <dt>Evidence</dt><dd>{surface.technical.evidence_refs.join(" · ")}</dd>
        </dl>
      </details>
    </section>
  );
}
