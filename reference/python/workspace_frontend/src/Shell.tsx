import { MyWork } from "./MyWork";
import type { NavigationItem, WorkspaceContext } from "./types";

const plannedCopy: Record<string, string> = {
  search: "Human-friendly records and search arrive in P9.05.",
  governed: "Governed action UX arrives in P9.06.",
  products: "Product-owned surfaces arrive in P9.07 through explicit boundaries.",
};

function activeItem(items: NavigationItem[]): NavigationItem {
  const current = window.location.pathname;
  return items.find((item) => item.href === current) ?? items[0];
}

export function Shell({ context, onLogout }: { context: WorkspaceContext; onLogout: () => void }) {
  const active = activeItem(context.navigation);
  const navigate = (item: NavigationItem) => (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    window.history.pushState({}, "", item.href);
    window.dispatchEvent(new PopStateEvent("popstate"));
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
          <button type="button" className="quiet-button" onClick={onLogout}>Sign out</button>
        </header>

        <main id="workspace-main" tabIndex={-1}>
          {active.id === "home" ? (
            <section className="hero" aria-labelledby="home-title">
              <p className="eyebrow">Productive Workspace</p>
              <h1 id="home-title">Your organization context is established.</h1>
              <p>
                The application boundary is active, and My Work now adds a bounded,
                non-authoritative projection of current attention signals.
              </p>
              <div className="status-grid">
                <article><span>Context</span><strong>Server resolved</strong><p>Browser input cannot choose the Organization or actor.</p></article>
                <article><span>Protected reads</span><strong>Revalidated</strong><p>Current least-privilege access is checked before protected projections are returned.</p></article>
                <article><span>Authority</span><strong>Not implied</strong><p>Session and queue visibility do not create Organizational Authority.</p></article>
              </div>
            </section>
          ) : active.id === "my-work" ? (
            <MyWork />
          ) : (
            <section className="placeholder" aria-labelledby="placeholder-title">
              <p className="eyebrow">Navigation spine</p>
              <h1 id="placeholder-title">{active.label}</h1>
              <p>{plannedCopy[active.id] ?? "This surface is not activated in the current release."}</p>
              <p className="boundary-note">No product or canonical business data is exposed by this placeholder.</p>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}
