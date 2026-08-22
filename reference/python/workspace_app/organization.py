from __future__ import annotations

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
    if not normalized or len(normalized) > limit or "\x00" in normalized:
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
    semantic_note: str | None = None
    canonical_project_record: bool = False

    def __post_init__(self) -> None:
        for name in ("item_id", "kind", "label", "summary", "source", "authority", "ownership", "state"):
            _bounded(getattr(self, name), field=name, limit=1024)
        href = _bounded(self.href, field="href", limit=1024)
        if not href.startswith("/") or href.startswith("//"):
            raise OrganizationCompositionError("organization navigation href must stay inside Workspace")
        if self.semantic_note is not None:
            _bounded(self.semantic_note, field="semantic_note", limit=1024)
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
            "semantic_note": self.semantic_note,
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
                semantic_note=item.knowledge_role or item.semantic_role,
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
