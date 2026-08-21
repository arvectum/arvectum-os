import { useEffect, useState } from "react";
import { loadProductSurfaces, WorkspaceApiError } from "./api";
import type { ProductSurface, ProductSurfacesProjection } from "./types";

type State =
  | { kind: "loading" }
  | { kind: "ready"; projection: ProductSurfacesProjection }
  | { kind: "error"; code: string };

function ProductCard({ product }: { product: ProductSurface }) {
  return (
    <article className="context-panel" aria-labelledby={`product-${product.id}`}>
      <p className="eyebrow">{product.purpose}</p>
      <h2 id={`product-${product.id}`}>{product.name}</h2>
      <p>{product.summary}</p>
      <dl>
        <div><dt>Evidence</dt><dd>{product.evidence_state === "available" ? "Current retained evidence revalidated" : "Unavailable / withheld"}</dd></div>
        <div><dt>Source</dt><dd>{product.source}</dd></div>
        <div><dt>Authority</dt><dd>{product.authority_mode}</dd></div>
      </dl>

      {product.evidence_state === "available" ? (
        <section aria-label={`${product.name} work`}>
          <h3>Product work</h3>
          <dl>
            {product.work.map((item) => (
              <div key={`${product.id}-${item.label}`}>
                <dt>{item.label}</dt>
                <dd><strong>{item.value}</strong><br /><small>{item.meaning}</small></dd>
              </div>
            ))}
          </dl>
        </section>
      ) : (
        <p className="semantic-warning" role="status">
          Product-specific work is withheld because the current retained boundary evidence could not be revalidated.
        </p>
      )}

      <details className="technical-details">
        <summary>Product Contract boundary</summary>
        <p>
          This is an inspectable interoperability boundary, not an authority grant and not a transfer of product business logic into Arvectum OS.
        </p>
        <dl>
          <div><dt>Contract</dt><dd>{product.boundary.contract}</dd></div>
          <div><dt>Version / lifecycle</dt><dd>{product.boundary.version} · {product.boundary.lifecycle}</dd></div>
          <div><dt>Compatibility line</dt><dd>{product.boundary.compatibility_line}</dd></div>
          <div><dt>Shared dependencies</dt><dd>{product.boundary.dependencies.join(", ") || "None"}</dd></div>
          <div><dt>Explicitly omitted</dt><dd>{product.boundary.explicitly_omitted_dependencies.join(", ") || "None"}</dd></div>
          <div><dt>Semantic owner</dt><dd>Product-owned; platform business-logic ownership = false</dd></div>
        </dl>
      </details>

      <details className="technical-details">
        <summary>Technical evidence boundary</summary>
        <dl>
          <div><dt>Operational contour</dt><dd>{product.technical.operational_contour}</dd></div>
          <div><dt>Evidence class</dt><dd>{product.technical.evidence_classification}</dd></div>
          <div><dt>Raw product state</dt><dd>Not exposed</dd></div>
          <div><dt>Platform internal identifiers</dt><dd>Not exposed</dd></div>
        </dl>
      </details>
    </article>
  );
}

export function Products() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    let active = true;
    void loadProductSurfaces().then(
      (projection) => { if (active) setState({ kind: "ready", projection }); },
      (error) => {
        if (!active) return;
        setState({ kind: "error", code: error instanceof WorkspaceApiError ? error.code : "PRODUCT_SURFACES_UNAVAILABLE" });
      },
    );
    return () => { active = false; };
  }, []);

  if (state.kind === "loading") {
    return <section className="object-context" aria-live="polite"><p>Loading product surfaces…</p></section>;
  }
  if (state.kind === "error") {
    return (
      <section className="object-context" role="alert">
        <p className="eyebrow">Products</p>
        <h1>Product surfaces unavailable</h1>
        <p>Current Organization-scoped product evidence could not be safely projected.</p>
        <code>{state.code}</code>
      </section>
    );
  }

  return (
    <section className="object-context" aria-labelledby="products-title">
      <div className="object-heading">
        <div>
          <p className="eyebrow">Products</p>
          <h1 id="products-title">Work across products without merging their domains.</h1>
          <p>
            Tender Operator and Discount Parser remain separate product-owned contexts. This Workspace view is a read-only,
            non-authoritative composition over their explicit governed boundaries.
          </p>
        </div>
      </div>
      <p className="boundary-note">
        Product visibility is not authorization or Organizational Authority. No product database, raw evidence, product secret,
        cross-Organization state or consequential action is exposed by this surface.
      </p>
      <div className="product-surfaces">
        {state.projection.products.map((product) => <ProductCard key={product.id} product={product} />)}
      </div>
    </section>
  );
}
