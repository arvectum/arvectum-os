import { useEffect, useState } from "react";
import { loadProductComposition, WorkspaceApiError } from "./api";
import { productSurfaceRegistry } from "./product_surfaces/registry";
import type { ProductCompositionProjection } from "./types";

type State =
  | { kind: "loading" }
  | { kind: "ready"; data: ProductCompositionProjection }
  | { kind: "error"; code: string };

function navigateTo(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function Products({ productId }: { productId?: string | null }) {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    let live = true;
    loadProductComposition().then(
      (data) => { if (live) setState({ kind: "ready", data }); },
      (error) => {
        if (live) setState({
          kind: "error",
          code: error instanceof WorkspaceApiError ? error.code : "PRODUCT_COMPOSITION_UNAVAILABLE",
        });
      },
    );
    return () => { live = false; };
  }, []);

  if (state.kind === "loading") {
    return <section className="placeholder" aria-live="polite">Loading product contexts…</section>;
  }
  if (state.kind === "error") {
    return (
      <section className="placeholder" role="alert">
        <h1>Product contexts unavailable</h1>
        <p>Current product evidence could not be revalidated. Nothing is inferred from stale or missing product state.</p>
        <code>{state.code}</code>
      </section>
    );
  }

  if (productId) {
    const surface = state.data.products.find((item) => item.id === productId);
    const contribution = productSurfaceRegistry[productId];
    if (!surface || !contribution || contribution.id !== surface.id) {
      return (
        <section className="placeholder" role="alert">
          <h1>Product surface unavailable</h1>
          <p>The requested product contribution is not registered in this exact Workspace release.</p>
        </section>
      );
    }
    return <>{contribution.render(surface)}</>;
  }

  return (
    <section className="hero" aria-labelledby="products-title">
      <p className="eyebrow">Company workspace · explicit Product Contract boundaries</p>
      <h1 id="products-title">Products</h1>
      <p>Move between real product contexts while each product keeps ownership of its business semantics and execution boundary.</p>
      <div className="status-grid">
        {state.data.products.map((surface) => (
          <article key={surface.id}>
            <span>{surface.ownership}</span>
            <strong>{surface.label}</strong>
            <p>{surface.product_contract.id} · {surface.product_contract.lifecycle} {surface.product_contract.version}</p>
            <p>{surface.contour.summary}</p>
            <a
              href={`/products/${surface.id}`}
              onClick={(event) => {
                event.preventDefault();
                navigateTo(`/products/${surface.id}`);
              }}
            >
              Open {surface.label}
            </a>
          </article>
        ))}
      </div>
      <p className="boundary-note">
        These contexts are composed, not merged: the Workspace does not infer a business relationship between products and switching products does not broaden access or authority.
      </p>
    </section>
  );
}
