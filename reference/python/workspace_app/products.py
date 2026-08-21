from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from .access import AccessContext

UTC = timezone.utc


class ProductSurfacesError(RuntimeError):
    """Product-surface evidence is unavailable, unsafe, or inconsistent."""


@dataclass(frozen=True, slots=True)
class ProductContractBoundary:
    contract: str
    governance_ref: str
    version: str
    lifecycle: str
    compatibility_line: str
    dependencies: tuple[str, ...]
    explicitly_omitted_dependencies: tuple[str, ...]

    def to_payload(self) -> dict[str, object]:
        return {
            "contract": self.contract,
            "governance_ref": self.governance_ref,
            "version": self.version,
            "lifecycle": self.lifecycle,
            "compatibility_line": self.compatibility_line,
            "dependencies": list(self.dependencies),
            "explicitly_omitted_dependencies": list(self.explicitly_omitted_dependencies),
            "product_semantics_owner": "product",
            "platform_business_logic_owner": False,
            "inspectable": True,
        }


@dataclass(frozen=True, slots=True)
class ProductWorkItem:
    label: str
    value: str
    meaning: str

    def to_payload(self) -> dict[str, str]:
        return {"label": self.label, "value": self.value, "meaning": self.meaning}


@dataclass(frozen=True, slots=True)
class ProductSurface:
    product_id: str
    name: str
    purpose: str
    evidence_state: str
    evidence_code: str
    source: str
    authority_mode: str
    summary: str
    work: tuple[ProductWorkItem, ...]
    boundary: ProductContractBoundary
    operational_contour: str
    evidence_classification: str

    def to_payload(self) -> dict[str, object]:
        return {
            "id": self.product_id,
            "name": self.name,
            "purpose": self.purpose,
            "evidence_state": self.evidence_state,
            "evidence_code": self.evidence_code,
            "source": self.source,
            "authority_mode": self.authority_mode,
            "summary": self.summary,
            "work": [item.to_payload() for item in self.work],
            "boundary": self.boundary.to_payload(),
            "technical": {
                "operational_contour": self.operational_contour,
                "evidence_classification": self.evidence_classification,
                "raw_product_state_exposed": False,
                "raw_platform_identifiers_exposed": False,
            },
        }


@dataclass(frozen=True, slots=True)
class ProductSurfacesProjection:
    generated_at: datetime
    products: tuple[ProductSurface, ...]

    def to_payload(self) -> dict[str, object]:
        return {
            "schema": "arvectum.workspace.product-surfaces/1",
            "generated_at": self.generated_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "product_business_logic_in_platform": False,
                "hidden_coupling": False,
                "consequential_action_available": False,
                "visibility_implies_permission": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "current_access_revalidated": True,
                "cross_organization_composition": False,
            },
            "products": [product.to_payload() for product in self.products],
        }


class ProductSurfaceAdapter(Protocol):
    def project(self, access: AccessContext) -> ProductSurface: ...


class ProductSurfacesProvider(Protocol):
    def project(self, access: AccessContext) -> ProductSurfacesProjection: ...


class ComposedProductSurfacesProvider:
    """Generic read-only composition over explicit product-owned surface adapters."""

    def __init__(self, adapters: tuple[ProductSurfaceAdapter, ...]) -> None:
        self._adapters = adapters

    def project(self, access: AccessContext) -> ProductSurfacesProjection:
        if not access.organization.value or not access.actor.value:
            raise ProductSurfacesError("attributable server-resolved access context required")
        return ProductSurfacesProjection(
            generated_at=datetime.now(UTC),
            products=tuple(adapter.project(access) for adapter in self._adapters),
        )


__all__ = [
    "ComposedProductSurfacesProvider",
    "ProductContractBoundary",
    "ProductSurface",
    "ProductSurfaceAdapter",
    "ProductSurfacesError",
    "ProductSurfacesProjection",
    "ProductSurfacesProvider",
    "ProductWorkItem",
]
