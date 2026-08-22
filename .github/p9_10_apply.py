from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one match in {path}, found {count}: {old[:100]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


write(
    "reference/python/workspace_app/organization.py",
    '''from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol
from urllib.parse import quote

from .access import AccessContext
from .attention import AttentionProjectionError, AttentionProvider, ProjectionFreshness
from .discovery import DiscoveryError, DiscoveryKind, DiscoveryProvider, DiscoveryFreshness
from .products import ProductCompositionError, ProductCompositionProvider


class OrganizationCompositionError(RuntimeError):
    """Organization composition cannot be produced safely."""


class LaneState(str, Enum):
    READY = "ready"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bounded(value: str, *, field: str, limit: int = 480) -> str:
    if not isinstance(value, str):
        raise OrganizationCompositionError(f"{field} must be text")
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > limit or "\\x00" in normalized:
        raise OrganizationCompositionError(f"{field} is outside the bounded presentation contract")
    return normalized


@dataclass(frozen=True, slots=True)
class OrganizationNavItem:
    item_id: str
    kind: str
    label: str
    summary: str
    href: str
    source: str
    authority: str
    ownership: str
    state: str
    provenance_available: bool
    canonical_project_record: bool = False

    def __post_init__(self) -> None:
        for name in ("item_id", "kind", "label", "summary", "source", "authority", "ownership", "state"):
            _bounded(getattr(self, name), field=name, limit=1024)
        href = _bounded(self.href, field="href", limit=1024)
        if not href.startswith("/") or href.startswith("//"):
            raise OrganizationCompositionError("organization navigation href must stay inside Workspace")
        if not isinstance(self.provenance_available, bool) or not isinstance(self.canonical_project_record, bool):
            raise OrganizationCompositionError("organization navigation truth flags must be explicit")

    def to_payload(self) -> dict[str, Any]:
        return {
            "id": self.item_id,
            "kind": self.kind,
            "label": self.label,
            "summary": self.summary,
            "href": self.href,
            "source": self.source,
            "authority": self.authority,
            "ownership": self.ownership,
            "state": self.state,
            "provenance_available": self.provenance_available,
            "canonical_project_record": self.canonical_project_record,
            "interaction": "navigate-and-inspect",
            "authority_provided": False,
            "consequential_action_available": False,
        }


@dataclass(frozen=True, slots=True)
class OrganizationLane:
    lane_id: str
    label: str
    summary: str
    state: LaneState
    source_boundary: str
    items: tuple[OrganizationNavItem, ...]

    def __post_init__(self) -> None:
        for name in ("lane_id", "label", "summary", "source_boundary"):
            _bounded(getattr(self, name), field=name, limit=1024)
        if not isinstance(self.state, LaneState):
            raise OrganizationCompositionError("lane state must be explicit")
        if not isinstance(self.items, tuple) or any(not isinstance(item, OrganizationNavItem) for item in self.items):
            raise OrganizationCompositionError("lane items must be immutable OrganizationNavItem values")

    def to_payload(self) -> dict[str, Any]:
        return {
            "id": self.lane_id,
            "label": self.label,
            "summary": self.summary,
            "state": self.state.value,
            "source_boundary": self.source_boundary,
            "items": [item.to_payload() for item in self.items],
        }


@dataclass(frozen=True, slots=True)
class OrganizationCompositionProjection:
    generated_at: str
    lanes: tuple[OrganizationLane, ...]

    def to_payload(self) -> dict[str, Any]:
        overall = "ready" if all(lane.state is LaneState.READY for lane in self.lanes) else "degraded"
        return {
            "schema": "arvectum.workspace.organization-composition/1",
            "generated_at": self.generated_at,
            "health": {"state": overall},
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "organizational_authority_provided": False,
                "company_semantics_promoted_to_kernel": False,
                "project_lenses_are_canonical_records": False,
                "source_projection_authority_preserved": True,
                "canonical_mutation_available": False,
                "external_effect_available": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "current_access_revalidated": True,
                "cross_organization_aggregation": False,
                "denied_source_counts_exposed": False,
            },
            "lanes": [lane.to_payload() for lane in self.lanes],
        }


class OrganizationCompositionProvider(Protocol):
    def project(self, access: AccessContext) -> OrganizationCompositionProjection: ...


class RuntimeOrganizationCompositionProvider:
    """Company-level navigation over existing authorized Workspace projections.

    The composition is intentionally rebuildable and non-authoritative. Products
    stay product-owned, knowledge/work retain their source semantics, and the
    project lane is only a navigation lens over declared product operating
    contours. It never creates a canonical Project record or a company-specific
    Kernel type.
    """

    def __init__(
        self,
        products: ProductCompositionProvider,
        discovery: DiscoveryProvider,
        attention: AttentionProvider,
    ) -> None:
        self.products = products
        self.discovery = discovery
        self.attention = attention

    def _product_lanes(self, access: AccessContext) -> tuple[OrganizationLane, OrganizationLane]:
        try:
            projection = self.products.project(access)
        except ProductCompositionError:
            note = "Product-owned composition could not be revalidated; no product or project-lens context is presented."
            return (
                OrganizationLane("products", "Products", note, LaneState.UNAVAILABLE, "P9.07 product-owned composition", ()),
                OrganizationLane("projects", "Project lenses", note, LaneState.UNAVAILABLE, "Derived only from declared product contours", ()),
            )

        product_items = tuple(
            OrganizationNavItem(
                item_id=f"product:{item.product_id}",
                kind="product",
                label=item.label,
                summary=item.summary,
                href=f"/products/{quote(item.product_id, safe='')}",
                source=item.contour,
                authority=item.source_authority,
                ownership="product-owned",
                state=item.status,
                provenance_available=bool(item.technical_refs),
            )
            for item in projection.products
        )
        project_items = tuple(
            OrganizationNavItem(
                item_id=f"project-lens:{item.product_id}",
                kind="project-lens",
                label=f"{item.label} operating contour",
                summary=(
                    f"Navigation lens over declared {item.contour} product context. "
                    "This is not a canonical Project record and does not infer a new cross-product business relationship."
                ),
                href=f"/products/{quote(item.product_id, safe='')}",
                source=item.contour,
                authority=item.source_authority,
                ownership="product-owned source; Workspace navigation lens",
                state=item.status,
                provenance_available=bool(item.technical_refs),
                canonical_project_record=False,
            )
            for item in projection.products
        )
        return (
            OrganizationLane(
                "products",
                "Products",
                "Product-owned contexts exposed through explicit Product Contract boundaries.",
                LaneState.READY,
                "P9.07 product-owned composition",
                product_items,
            ),
            OrganizationLane(
                "projects",
                "Project lenses",
                "Human navigation over declared operating contours; no separate project source of truth is created.",
                LaneState.READY,
                "Derived only from declared product contours",
                project_items,
            ),
        )

    def _knowledge_lane(self, access: AccessContext) -> OrganizationLane:
        try:
            projection = self.discovery.search(access, kind=DiscoveryKind.KNOWLEDGE)
        except DiscoveryError:
            return OrganizationLane(
                "knowledge",
                "Knowledge",
                "Authorized knowledge context could not be revalidated and is withheld.",
                LaneState.UNAVAILABLE,
                "P9.05 authorized Discovery projection",
                (),
            )
        lane_state = LaneState.READY if projection.health.state is DiscoveryFreshness.FRESH else LaneState.DEGRADED
        items = tuple(
            OrganizationNavItem(
                item_id=f"knowledge:{item.object_id}",
                kind="knowledge",
                label=item.title,
                summary=item.summary,
                href=item.open_href,
                source=item.source_label,
                authority=item.authority_mode,
                ownership="source-owned governed context",
                state=item.state_label,
                provenance_available=True,
            )
            for item in projection.results[:12]
        )
        return OrganizationLane(
            "knowledge",
            "Knowledge",
            "Authorized knowledge-related context with Observation/Memory/Candidate/Knowledge distinctions preserved.",
            lane_state,
            "P9.05 authorized Discovery projection",
            items,
        )

    def _work_lane(self, access: AccessContext) -> OrganizationLane:
        try:
            projection = self.attention.project(access)
        except AttentionProjectionError:
            return OrganizationLane(
                "work",
                "Work",
                "Current work/attention context could not be revalidated and is withheld.",
                LaneState.UNAVAILABLE,
                "P9.04/P9.09 attention projection",
                (),
            )
        lane_state = LaneState.READY if projection.health.state is ProjectionFreshness.FRESH else LaneState.DEGRADED
        items = tuple(
            OrganizationNavItem(
                item_id=f"work:{item.attention_id}",
                kind="work",
                label=item.title,
                summary=item.reason,
                href=item.open_href,
                source=item.source_label,
                authority="Visibility does not imply permission, Organizational Authority or approval",
                ownership="governed source; Workspace attention projection",
                state=f"{item.group.value} · {item.urgency.value}",
                provenance_available=item.technical_evidence_available,
            )
            for item in projection.items[:12]
        )
        return OrganizationLane(
            "work",
            "Work",
            "Current derived attention context; consequential continuation remains behind Governed Execution gates.",
            lane_state,
            "P9.04/P9.09 attention projection",
            items,
        )

    def project(self, access: AccessContext) -> OrganizationCompositionProjection:
        if not isinstance(access, AccessContext):
            raise OrganizationCompositionError("server-authorized AccessContext is required")
        products, projects = self._product_lanes(access)
        knowledge = self._knowledge_lane(access)
        work = self._work_lane(access)
        return OrganizationCompositionProjection(_utc_now(), (products, projects, knowledge, work))


__all__ = [
    "LaneState",
    "OrganizationCompositionError",
    "OrganizationCompositionProjection",
    "OrganizationCompositionProvider",
    "OrganizationLane",
    "OrganizationNavItem",
    "RuntimeOrganizationCompositionProvider",
]
''',
)

write(
    "reference/python/workspace_tests/test_organization_composition.py",
    '''from __future__ import annotations

import unittest
from types import SimpleNamespace

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.attention import AttentionProjectionError, ProjectionFreshness
from workspace_app.discovery import DiscoveryError, DiscoveryFreshness
from workspace_app.organization import RuntimeOrganizationCompositionProvider
from workspace_app.products import ProductCompositionError


ACCESS = AccessContext(
    organization=Identity("organization", "arvectum", "test"),
    actor=Identity("actor", "owner", "test"),
    principal_kind="human",
    credential_id="cred",
    grant_id="grant",
)


class Products:
    def project(self, access: AccessContext):
        self.access = access
        return SimpleNamespace(products=(SimpleNamespace(
            product_id="tender-operator",
            label="Tender Operator",
            summary="Verified retained product context.",
            contour="P7.07",
            source_authority="ЕИС — External Reference",
            status="verified-retained-context",
            technical_refs=("evidence",),
        ),))


class Discovery:
    def search(self, access: AccessContext, *, query: str = "", kind=None):
        self.access = access
        self.kind = kind
        return SimpleNamespace(
            health=SimpleNamespace(state=DiscoveryFreshness.FRESH),
            results=(SimpleNamespace(
                object_id="a" * 20,
                title="Knowledge — governed source",
                summary="Knowledge. Governed context is available.",
                open_href="/objects/" + "a" * 20,
                source_label="Arvectum OS governed state",
                authority_mode="Native",
                state_label="validated",
            ),),
        )

    def inspect(self, access: AccessContext, object_id: str):  # pragma: no cover - protocol completeness
        raise NotImplementedError


class Attention:
    def project(self, access: AccessContext):
        self.access = access
        return SimpleNamespace(
            health=SimpleNamespace(state=ProjectionFreshness.FRESH),
            items=(SimpleNamespace(
                attention_id="b" * 20,
                title="Decision evidence is needed",
                reason="A governed gate remains waiting.",
                open_href="/my-work?focus=" + "b" * 20,
                source_label="Governed source",
                group=SimpleNamespace(value="decision-required"),
                urgency=SimpleNamespace(value="high"),
                technical_evidence_available=True,
            ),),
        )


class FailingProducts:
    def project(self, access: AccessContext):
        raise ProductCompositionError("protected product source unavailable")


class FailingDiscovery(Discovery):
    def search(self, access: AccessContext, *, query: str = "", kind=None):
        raise DiscoveryError("protected discovery source unavailable")


class FailingAttention:
    def project(self, access: AccessContext):
        raise AttentionProjectionError("protected attention source unavailable")


class OrganizationCompositionTests(unittest.TestCase):
    def test_composes_existing_authorized_sources_without_creating_project_authority(self) -> None:
        projection = RuntimeOrganizationCompositionProvider(Products(), Discovery(), Attention()).project(ACCESS).to_payload()
        self.assertEqual(projection["schema"], "arvectum.workspace.organization-composition/1")
        self.assertFalse(projection["projection"]["canonical_authority"])
        self.assertFalse(projection["projection"]["company_semantics_promoted_to_kernel"])
        self.assertFalse(projection["projection"]["project_lenses_are_canonical_records"])
        self.assertFalse(projection["scope"]["cross_organization_aggregation"])
        lanes = {lane["id"]: lane for lane in projection["lanes"]}
        self.assertEqual(set(lanes), {"products", "projects", "knowledge", "work"})
        self.assertEqual(lanes["products"]["items"][0]["href"], "/products/tender-operator")
        project = lanes["projects"]["items"][0]
        self.assertEqual(project["kind"], "project-lens")
        self.assertFalse(project["canonical_project_record"])
        self.assertIn("not a canonical Project record", project["summary"])
        self.assertEqual(lanes["knowledge"]["items"][0]["href"], "/objects/" + "a" * 20)
        self.assertEqual(lanes["work"]["items"][0]["href"], "/my-work?focus=" + "b" * 20)
        self.assertFalse(lanes["work"]["items"][0]["authority_provided"])

    def test_fails_closed_per_lane_without_inventing_company_state(self) -> None:
        projection = RuntimeOrganizationCompositionProvider(
            FailingProducts(), FailingDiscovery(), FailingAttention()
        ).project(ACCESS).to_payload()
        self.assertEqual(projection["health"]["state"], "degraded")
        lanes = {lane["id"]: lane for lane in projection["lanes"]}
        self.assertEqual(lanes["products"]["state"], "unavailable")
        self.assertEqual(lanes["projects"]["state"], "unavailable")
        self.assertEqual(lanes["knowledge"]["state"], "unavailable")
        self.assertEqual(lanes["work"]["state"], "unavailable")
        self.assertTrue(all(not lane["items"] for lane in lanes.values()))
        self.assertNotIn("protected product source unavailable", str(projection))
        self.assertNotIn("protected discovery source unavailable", str(projection))
        self.assertNotIn("protected attention source unavailable", str(projection))


if __name__ == "__main__":
    unittest.main()
''',
)

write(
    "reference/python/workspace_frontend/src/Organization.tsx",
    '''import { useEffect, useState } from "react";
import { loadOrganizationComposition, WorkspaceApiError } from "./api";
import type { OrganizationCompositionProjection, OrganizationLane } from "./types";
import "./Organization.css";

type State =
  | { kind: "loading" }
  | { kind: "ready"; data: OrganizationCompositionProjection }
  | { kind: "error"; code: string };

function navigate(href: string, event: React.MouseEvent<HTMLAnchorElement>) {
  event.preventDefault();
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function Lane({ lane }: { lane: OrganizationLane }) {
  return (
    <section className="organization-lane" aria-labelledby={`organization-${lane.id}`}>
      <div className="organization-lane-head">
        <div>
          <p className="eyebrow">{lane.source_boundary}</p>
          <h2 id={`organization-${lane.id}`}>{lane.label}</h2>
        </div>
        <span className={`organization-lane-state state-${lane.state}`}>{lane.state}</span>
      </div>
      <p>{lane.summary}</p>
      {lane.items.length ? (
        <div className="organization-items">
          {lane.items.map((item) => (
            <article className="organization-item" key={item.id}>
              <div className="organization-item-meta">
                <span>{item.kind}</span><span>{item.state}</span>
              </div>
              <h3>{item.label}</h3>
              <p>{item.summary}</p>
              <dl>
                <div><dt>Source</dt><dd>{item.source}</dd></div>
                <div><dt>Authority</dt><dd>{item.authority}</dd></div>
                <div><dt>Ownership</dt><dd>{item.ownership}</dd></div>
              </dl>
              {item.kind === "project-lens" ? <p className="boundary-note">Navigation lens only · not a canonical Project record.</p> : null}
              <a href={item.href} onClick={(event) => navigate(item.href, event)}>Open context</a>
            </article>
          ))}
        </div>
      ) : (
        <p className="boundary-note">No context is presented from this lane in the current authorized snapshot.</p>
      )}
    </section>
  );
}

export function Organization({ organizationLabel }: { organizationLabel: string }) {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    let live = true;
    void loadOrganizationComposition()
      .then((data) => { if (live) setState({ kind: "ready", data }); })
      .catch((error) => {
        const code = error instanceof WorkspaceApiError ? error.code : "ORGANIZATION_COMPOSITION_UNAVAILABLE";
        if (live) setState({ kind: "error", code });
      });
    return () => { live = false; };
  }, []);

  if (state.kind === "loading") return <section className="organization-page" aria-live="polite">Composing organization context…</section>;
  if (state.kind === "error") {
    return (
      <section className="organization-page" role="alert">
        <p className="eyebrow">Organization composition</p>
        <h1>Organization context is unavailable.</h1>
        <p>Protected source context could not be safely composed.</p>
        <code>{state.code}</code>
      </section>
    );
  }

  return (
    <section className="organization-page" aria-labelledby="organization-title">
      <header className="organization-header">
        <p className="eyebrow">Organization composition</p>
        <h1 id="organization-title">{organizationLabel}</h1>
        <p>One company-level navigation view over already-authorized products, project lenses, knowledge and work.</p>
        <p className="boundary-note">
          This view is rebuildable and non-authoritative. It does not create Organizational Authority, a canonical company database,
          a canonical Project record, or product/company semantics in the Kernel.
        </p>
      </header>
      {state.data.health.state !== "ready" ? (
        <div className="organization-health" role="status">Some source lanes are degraded or unavailable; unavailable context is withheld rather than guessed.</div>
      ) : null}
      <div className="organization-lanes">
        {state.data.lanes.map((lane) => <Lane lane={lane} key={lane.id} />)}
      </div>
    </section>
  );
}
''',
)

write(
    "reference/python/workspace_frontend/src/Organization.css",
    '''.organization-page { display: grid; gap: 1.25rem; }
.organization-header { max-width: 72rem; }
.organization-header h1 { margin: .15rem 0 .6rem; }
.organization-health { border: 1px solid var(--line, #d5d9e0); border-radius: .75rem; padding: .85rem 1rem; }
.organization-lanes { display: grid; gap: 1rem; }
.organization-lane { border: 1px solid var(--line, #d5d9e0); border-radius: 1rem; padding: 1rem; background: var(--surface, #fff); }
.organization-lane-head { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; }
.organization-lane-head h2 { margin: .1rem 0; }
.organization-lane-state { font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; border: 1px solid currentColor; border-radius: 999px; padding: .25rem .5rem; }
.organization-items { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: .8rem; margin-top: .9rem; }
.organization-item { border: 1px solid var(--line, #d5d9e0); border-radius: .8rem; padding: .9rem; min-width: 0; }
.organization-item h3 { margin: .4rem 0; }
.organization-item-meta { display: flex; flex-wrap: wrap; gap: .5rem; font-size: .78rem; opacity: .8; }
.organization-item dl { display: grid; gap: .35rem; margin: .8rem 0; font-size: .85rem; }
.organization-item dl div { display: grid; grid-template-columns: 5.5rem 1fr; gap: .5rem; }
.organization-item dt { font-weight: 700; }
.organization-item dd { margin: 0; overflow-wrap: anywhere; }
@media (max-width: 720px) { .organization-lane-head { display: grid; } .organization-item dl div { grid-template-columns: 1fr; } }
''',
)

write(
    "reference/python/workspace_frontend/src/P910.test.tsx",
    '''import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Organization } from "./Organization";
import type { OrganizationCompositionProjection } from "./types";

const composition: OrganizationCompositionProjection = {
  schema: "arvectum.workspace.organization-composition/1",
  generated_at: "2026-08-22T07:00:00Z",
  health: { state: "ready" },
  projection: {
    derived: true, canonical_authority: false, organizational_authority_provided: false,
    company_semantics_promoted_to_kernel: false, project_lenses_are_canonical_records: false,
    source_projection_authority_preserved: true, canonical_mutation_available: false, external_effect_available: false,
  },
  scope: {
    organization_resolved_server_side: true, actor_resolved_server_side: true, current_access_revalidated: true,
    cross_organization_aggregation: false, denied_source_counts_exposed: false,
  },
  lanes: [
    { id: "products", label: "Products", summary: "Explicit product boundaries.", state: "ready", source_boundary: "P9.07 product-owned composition", items: [
      { id: "product:tender", kind: "product", label: "Tender Operator", summary: "Product context", href: "/products/tender-operator", source: "P7.07", authority: "ЕИС — External Reference", ownership: "product-owned", state: "verified", provenance_available: true, canonical_project_record: false, interaction: "navigate-and-inspect", authority_provided: false, consequential_action_available: false },
    ] },
    { id: "projects", label: "Project lenses", summary: "Navigation lenses.", state: "ready", source_boundary: "Declared product contours", items: [
      { id: "project-lens:tender", kind: "project-lens", label: "Tender Operator operating contour", summary: "Not a canonical Project record.", href: "/products/tender-operator", source: "P7.07", authority: "ЕИС — External Reference", ownership: "product-owned source; Workspace navigation lens", state: "verified", provenance_available: true, canonical_project_record: false, interaction: "navigate-and-inspect", authority_provided: false, consequential_action_available: false },
    ] },
    { id: "knowledge", label: "Knowledge", summary: "Governed context.", state: "ready", source_boundary: "P9.05 Discovery", items: [] },
    { id: "work", label: "Work", summary: "Attention context.", state: "ready", source_boundary: "P9.04/P9.09 attention", items: [] },
  ],
};

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("P9.10 organization composition", () => {
  it("presents company-level navigation while keeping project lenses explicitly non-canonical", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(composition), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<Organization organizationLabel={'ООО «Арвектум»'} />);
    expect(await screen.findByRole("heading", { name: 'ООО «Арвектум»' })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Products" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Project lenses" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Knowledge" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Work" })).toBeTruthy();
    expect(screen.getAllByText(/not a canonical Project record/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/does not create Organizational Authority/)).toBeTruthy();
    expect(screen.getAllByRole("link", { name: "Open context" }).map((link) => link.getAttribute("href"))).toContain("/products/tender-operator");
  });

  it("does not retain company context when the protected composition endpoint is denied", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ detail: "ACCESS_DENIED" }), { status: 403, headers: { "Content-Type": "application/json" } })));
    render(<Organization organizationLabel={'ООО «Арвектум»'} />);
    expect(await screen.findByRole("heading", { name: "Organization context is unavailable." })).toBeTruthy();
    expect(screen.queryByText("Tender Operator")).toBeNull();
  });
});
''',
)

# Backend wiring.
replace_once(
    "reference/python/workspace_app/main.py",
    "from .governed import GovernedExperienceError, GovernedExperienceProvider, RuntimeGovernedExperienceProvider\nfrom .products import ProductCompositionError, ProductCompositionProvider, RuntimeProductCompositionProvider\n",
    "from .governed import GovernedExperienceError, GovernedExperienceProvider, RuntimeGovernedExperienceProvider\nfrom .organization import OrganizationCompositionProvider, RuntimeOrganizationCompositionProvider\nfrom .products import ProductCompositionError, ProductCompositionProvider, RuntimeProductCompositionProvider\n",
)
replace_once(
    "reference/python/workspace_app/main.py",
    '        {"id": "home", "label": "Home", "href": "/", "availability": "available"},\n',
    '        {"id": "home", "label": "Home", "href": "/", "availability": "available"},\n        {"id": "organization", "label": "Organization", "href": "/organization", "availability": "available"},\n',
)
replace_once(
    "reference/python/workspace_app/main.py",
    "    product_provider: ProductCompositionProvider | None = None,\n    copilot_provider: CopilotProvider | None = None,\n",
    "    product_provider: ProductCompositionProvider | None = None,\n    organization_provider: OrganizationCompositionProvider | None = None,\n    copilot_provider: CopilotProvider | None = None,\n",
)
replace_once(
    "reference/python/workspace_app/main.py",
    "    products = product_provider or RuntimeProductCompositionProvider(settings.runtime_root)\n    model = (\n",
    "    products = product_provider or RuntimeProductCompositionProvider(settings.runtime_root)\n    organization = organization_provider or RuntimeOrganizationCompositionProvider(products, discovery, attention)\n    model = (\n",
)
replace_once(
    "reference/python/workspace_app/main.py",
    "    app.state.product_provider = products\n    app.state.copilot_provider = copilot\n",
    "    app.state.product_provider = products\n    app.state.organization_provider = organization\n    app.state.copilot_provider = copilot\n",
)
replace_once(
    "reference/python/workspace_app/main.py",
    '''    @app.get("/api/app/v1/products")
    async def read_product_composition(
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            return products.project(access).to_payload()
        except ProductCompositionError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="PRODUCT_COMPOSITION_UNAVAILABLE") from None

''',
    '''    @app.get("/api/app/v1/products")
    async def read_product_composition(
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            return products.project(access).to_payload()
        except ProductCompositionError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="PRODUCT_COMPOSITION_UNAVAILABLE") from None

    @app.get("/api/app/v1/organization")
    async def read_organization_composition(
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, Any]:
        _, access = current
        return organization.project(access).to_payload()

''',
)

# Frontend contract + API.
replace_once(
    "reference/python/workspace_frontend/src/api.ts",
    "  ObjectContext,\n  ProductCompositionProjection,\n  WorkspaceContext,\n",
    "  ObjectContext,\n  OrganizationCompositionProjection,\n  ProductCompositionProjection,\n  WorkspaceContext,\n",
)
replace_once(
    "reference/python/workspace_frontend/src/api.ts",
    '''export async function loadProductComposition(): Promise<ProductCompositionProjection> {
  return request<ProductCompositionProjection>("/api/app/v1/products");
}

''',
    '''export async function loadProductComposition(): Promise<ProductCompositionProjection> {
  return request<ProductCompositionProjection>("/api/app/v1/products");
}

export async function loadOrganizationComposition(): Promise<OrganizationCompositionProjection> {
  return request<OrganizationCompositionProjection>("/api/app/v1/organization");
}

''',
)

types_path = ROOT / "reference/python/workspace_frontend/src/types.ts"
types_text = types_path.read_text(encoding="utf-8")
if "export type OrganizationCompositionProjection" in types_text:
    raise RuntimeError("organization types already exist")
types_text += '''\nexport type OrganizationLaneState = "ready" | "degraded" | "unavailable";\n\nexport type OrganizationNavItem = {\n  id: string;\n  kind: "product" | "project-lens" | "knowledge" | "work";\n  label: string;\n  summary: string;\n  href: string;\n  source: string;\n  authority: string;\n  ownership: string;\n  state: string;\n  provenance_available: boolean;\n  canonical_project_record: false;\n  interaction: "navigate-and-inspect";\n  authority_provided: false;\n  consequential_action_available: false;\n};\n\nexport type OrganizationLane = {\n  id: "products" | "projects" | "knowledge" | "work";\n  label: string;\n  summary: string;\n  state: OrganizationLaneState;\n  source_boundary: string;\n  items: OrganizationNavItem[];\n};\n\nexport type OrganizationCompositionProjection = {\n  schema: "arvectum.workspace.organization-composition/1";\n  generated_at: string;\n  health: { state: "ready" | "degraded" };\n  projection: {\n    derived: true;\n    canonical_authority: false;\n    organizational_authority_provided: false;\n    company_semantics_promoted_to_kernel: false;\n    project_lenses_are_canonical_records: false;\n    source_projection_authority_preserved: true;\n    canonical_mutation_available: false;\n    external_effect_available: false;\n  };\n  scope: {\n    organization_resolved_server_side: true;\n    actor_resolved_server_side: true;\n    current_access_revalidated: true;\n    cross_organization_aggregation: false;\n    denied_source_counts_exposed: false;\n  };\n  lanes: OrganizationLane[];\n};\n'''
types_path.write_text(types_text, encoding="utf-8")

replace_once(
    "reference/python/workspace_frontend/src/Shell.tsx",
    'import { ObjectDetail } from "./ObjectDetail";\nimport { Products } from "./Products";\n',
    'import { ObjectDetail } from "./ObjectDetail";\nimport { Organization } from "./Organization";\nimport { Products } from "./Products";\n',
)
replace_once(
    "reference/python/workspace_frontend/src/Shell.tsx",
    '''          ) : active.id === "my-work" ? (
            <MyWork />
''',
    '''          ) : active.id === "organization" ? (
            <Organization organizationLabel={context.organization.label} />
          ) : active.id === "my-work" ? (
            <MyWork />
''',
)

release_path = ROOT / "reference/python/workspace_app/release.json"
release = json.loads(release_path.read_text(encoding="utf-8"))
if release.get("release_id") != "p9.09.1" or release.get("app_api_contract") != "7":
    raise RuntimeError(f"unexpected P9.10 base release: {release}")
release["release_id"] = "p9.10.1"
release["app_api_contract"] = "8"
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("P9.10 source implementation applied")
