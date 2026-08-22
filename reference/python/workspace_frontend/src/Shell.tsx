import { Copilot } from "./Copilot";
import { Discovery } from "./Discovery";
import { Governed } from "./Governed";
import { MyWork } from "./MyWork";
import { ObjectDetail } from "./ObjectDetail";
import { Products } from "./Products";
import type { NavigationItem, WorkspaceContext } from "./types";

function activeItem(items: NavigationItem[]): NavigationItem {
  const current = window.location.pathname;
  if (current.startsWith("/objects/")) return items.find((item) => item.id === "search") ?? items[0];
  if (current.startsWith("/products/")) return items.find((item) => item.id === "products") ?? items[0];
  return items.find((item) => item.href === current) ?? items[0];
}

function navigateTo(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function Shell({ context, onLogout }: { context: WorkspaceContext; onLogout: () => void }) {
  const active = activeItem(context.navigation);
  const currentPath = window.location.pathname;
  const objectId = currentPath.startsWith("/objects/") ? decodeURIComponent(currentPath.slice("/objects/".length)) : null;
  const productId = currentPath.startsWith("/products/") ? decodeURIComponent(currentPath.slice("/products/".length)) : null;
  const navigate = (item: NavigationItem) => (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    navigateTo(item.href);
  };

  return (
    <div className="app-shell">
      <a className="skip-link" href="#workspace-main">Skip to content</a>
      <aside className="sidebar" aria-label="Workspace navigation">
        <div className="brand" aria-label="Arvectum OS">
          <span className="brand-mark">A</span><span>Arvectum OS</span>
        </div>
        <nav aria-label="Workspace navigation">
          <ul>
            {context.navigation.map((item) => (
              <li key={item.id}>
                <a href={item.href} onClick={navigate(item)} aria-current={item.id === active.id ? "page" : undefined}>
                  <span>{item.label}</span>
                  {item.availability !== "available" ? <small>planned</small> : null}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <div className="sidebar-footnote">Internal workspace · {context.release.id}</div>
      </aside>

      <div className="workspace-column">
        <header className="topbar">
          <div className="context-chip" aria-label={`Organization: ${context.organization.label}`}>
            <span className="eyebrow">Organization</span><strong>{context.organization.label}</strong>
          </div>
          <div className="context-chip" aria-label={`Authenticated actor: ${context.actor.label}`}>
            <span className="eyebrow">Authenticated actor</span><strong>{context.actor.label}</strong>
          </div>
          <form
            className="global-search"
            role="search"
            onSubmit={(event) => {
              event.preventDefault();
              const form = new FormData(event.currentTarget);
              const query = String(form.get("q") ?? "").trim();
              navigateTo(query ? `/search?q=${encodeURIComponent(query)}` : "/search");
            }}
          >
            <label className="visually-hidden" htmlFor="global-search-query">Global search</label>
            <input id="global-search-query" name="q" type="search" maxLength={160} placeholder="Search records, documents, knowledge" />
            <button type="submit">Search</button>
          </form>
          <button type="button" className="quiet-button" onClick={onLogout}>Sign out</button>
        </header>

        <main id="workspace-main" tabIndex={-1}>
          {objectId ? (
            <ObjectDetail objectId={objectId} />
          ) : active.id === "home" ? (
            <>
              <section className="hero" aria-labelledby="home-title">
                <p className="eyebrow">Productive Workspace</p>
                <h1 id="home-title">Your organization context is established.</h1>
                <p>
                  My Work surfaces current attention signals, discovery finds governed organizational context, Ask Arvectum
                  provides source-grounded assistance, and Governed actions keeps consequential work behind current authority gates.
                </p>
                <div className="status-grid">
                  <article><span>Context</span><strong>Server resolved</strong><p>Browser input cannot choose the Organization or actor.</p></article>
                  <article><span>AI assistance</span><strong>Grounded, transient</strong><p>Sourced facts, synthesis and uncertainty stay distinguishable and inspectable.</p></article>
                  <article><span>Authority</span><strong>Not implied</strong><p>Session, search results, Copilot answers and action buttons do not create Organizational Authority.</p></article>
                </div>
              </section>
              <MyWork embedded />
            </>
          ) : active.id === "my-work" ? (
            <MyWork />
          ) : active.id === "search" ? (
            <Discovery />
          ) : active.id === "records" ? (
            <Discovery kind="record" />
          ) : active.id === "documents" ? (
            <Discovery kind="document" />
          ) : active.id === "knowledge" ? (
            <Discovery kind="knowledge" />
          ) : active.id === "copilot" ? (
            <Copilot csrfToken={context.session.csrf_token} />
          ) : active.id === "governed" ? (
            <Governed csrfToken={context.session.csrf_token} />
          ) : active.id === "products" ? (
            <Products productId={productId} />
          ) : (
            <section className="placeholder" aria-labelledby="placeholder-title">
              <p className="eyebrow">Navigation spine</p>
              <h1 id="placeholder-title">{active.label}</h1>
              <p>This surface is not activated in the current release.</p>
              <p className="boundary-note">No product or canonical business data is exposed by this placeholder.</p>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}
