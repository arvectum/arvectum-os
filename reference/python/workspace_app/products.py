from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol

from .access import AccessContext
import p7_03_durable_state as p703
import p7_08_discount_parser_cross_host as p708

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


class ProductSurfacesProvider(Protocol):
    def project(self, access: AccessContext) -> ProductSurfacesProjection: ...


_TENDER_BOUNDARY = ProductContractBoundary(
    contract="P6.02 — Tender Operator",
    governance_ref="docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md",
    version="0.1.0",
    lifecycle="Provisional",
    compatibility_line="restricted-paid-pilot/44fz-prebid-v1",
    dependencies=("CAP-001", "CAP-004"),
    explicitly_omitted_dependencies=("CAP-002", "CAP-003"),
)

_DISCOUNT_BOUNDARY = ProductContractBoundary(
    contract="P6.06 — Discount Parser",
    governance_ref="docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md",
    version="0.1.0",
    lifecycle="Provisional",
    compatibility_line="mvp-v1/controlled-telegram-publication",
    dependencies=("CAP-004",),
    explicitly_omitted_dependencies=("CAP-001", "CAP-002", "CAP-003"),
)


def _unavailable_tender(code: str) -> ProductSurface:
    return ProductSurface(
        product_id="tender-operator",
        name="Tender Operator",
        purpose="44-ФЗ pre-bid review",
        evidence_state="unavailable",
        evidence_code=code,
        source="ЕИС / zakupki.gov.ru",
        authority_mode="External Reference",
        summary="Current retained Tender Operator reliance could not be revalidated; no product data is shown.",
        work=(),
        boundary=_TENDER_BOUNDARY,
        operational_contour="P7.07",
        evidence_classification="governed retained evidence",
    )


def _unavailable_discount(code: str) -> ProductSurface:
    return ProductSurface(
        product_id="discount-parser",
        name="Discount Parser",
        purpose="Controlled Telegram publication reconstruction",
        evidence_state="unavailable",
        evidence_code=code,
        source="Discount Parser + Telegram external evidence",
        authority_mode="Derived reconstruction / External Reference",
        summary="Current retained Discount Parser reconstruction could not be revalidated; no product data is shown.",
        work=(),
        boundary=_DISCOUNT_BOUNDARY,
        operational_contour="P7.08",
        evidence_classification="non-canonical operational evidence",
    )


def _verified_tender_surface(runtime_root: Path) -> ProductSurface:
    try:
        status = p703.verify_store(runtime_root)
        if status.get("integrity") != "PASS":
            return _unavailable_tender("TENDER_STORE_UNAVAILABLE")
        items_root = runtime_root / "state" / "governed" / "items"
        candidates: list[Mapping[str, Any]] = []
        for child in sorted(items_root.iterdir()):
            manifest = p703.verify_item(child)
            metadata = manifest.get("metadata", {})
            if not isinstance(metadata, Mapping):
                continue
            if metadata.get("operational_contour") != "P7.07":
                continue
            if metadata.get("state_class") != "canonical-governed-state":
                continue
            candidates.append(metadata)
        if not candidates:
            return _unavailable_tender("TENDER_RETAINED_EVIDENCE_NOT_FOUND")
        metadata = candidates[0]
        required = {
            "product_contract_version": "0.1.0",
            "authority_mode": "External Reference",
            "authoritative_source": "ЕИС / zakupki.gov.ru",
            "rehydratable_cap001_document": True,
            "raw_document_bytes_included": False,
            "external_actions": False,
        }
        if any(metadata.get(key) != value for key, value in required.items()):
            return _unavailable_tender("TENDER_BOUNDARY_REVALIDATION_FAILED")
        return ProductSurface(
            product_id="tender-operator",
            name="Tender Operator",
            purpose="44-ФЗ pre-bid review",
            evidence_state="available",
            evidence_code="PASS_RETAINED_P7_07_RELIANCE",
            source="ЕИС / zakupki.gov.ru",
            authority_mode="External Reference",
            summary="A real retained EIS-backed pre-bid evidence set is available through the P6.02 Product Contract boundary.",
            work=(
                ProductWorkItem(
                    "Tender notice",
                    "0344100006426000005",
                    "Human entry point for the retained EIS-backed case; platform Subject/Version identities are not required here.",
                ),
                ProductWorkItem(
                    "Current product work",
                    "Pre-bid review",
                    "Tender interpretation, risks, RFQ/TKP and recommendation semantics remain owned by Tender Operator.",
                ),
                ProductWorkItem(
                    "Shared reliance",
                    "CAP-001 exact document/artifact + CAP-004 reconstruction",
                    "The platform governs exact evidence and reconstruction only; it does not own procurement meaning.",
                ),
            ),
            boundary=_TENDER_BOUNDARY,
            operational_contour="P7.07",
            evidence_classification="governed retained evidence",
        )
    except (OSError, p703.P703Error, ValueError, TypeError):
        return _unavailable_tender("TENDER_REVALIDATION_UNAVAILABLE")


def _read_verified_json(json_path: Path, digest_path: Path) -> dict[str, Any]:
    if json_path.is_symlink() or digest_path.is_symlink():
        raise ProductSurfacesError("symlinked product evidence is not accepted")
    raw = json_path.read_bytes()
    if len(raw) <= 0 or len(raw) > 2 * 1024 * 1024:
        raise ProductSurfacesError("product evidence size outside bounded limit")
    digest = hashlib.sha256(raw).hexdigest()
    sidecar = digest_path.read_text(encoding="utf-8").strip().split()
    if len(sidecar) != 2 or sidecar[0] != digest or sidecar[1] != json_path.name:
        raise ProductSurfacesError("product evidence digest mismatch")
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ProductSurfacesError("product evidence root must be an object")
    return value


def _verified_discount_surface(runtime_root: Path) -> ProductSurface:
    reports_root = runtime_root / "product-contours" / "discount-parser" / "runs"
    try:
        candidates: list[tuple[Path, Path]] = []
        if reports_root.is_dir() and not reports_root.is_symlink():
            for run_dir in sorted(reports_root.iterdir(), key=lambda path: path.name):
                if not run_dir.is_dir() or run_dir.is_symlink():
                    continue
                reconstruction = run_dir / "reconstruction"
                report = reconstruction / p708.REPORT_FILENAME
                digest = reconstruction / p708.REPORT_DIGEST_FILENAME
                if report.is_file() and digest.is_file():
                    candidates.append((report, digest))
        if not candidates:
            return _unavailable_discount("DISCOUNT_RETAINED_EVIDENCE_NOT_FOUND")
        report, digest = candidates[-1]
        value = _read_verified_json(report, digest)
        if value.get("schema") != p708.REPORT_SCHEMA or value.get("schema_version") != p708.REPORT_SCHEMA_VERSION:
            return _unavailable_discount("DISCOUNT_REPORT_SCHEMA_MISMATCH")
        boundary = value.get("boundary")
        product_evidence = value.get("product_evidence")
        cap004 = value.get("cap004")
        containment = value.get("containment")
        if not all(isinstance(item, Mapping) for item in (boundary, product_evidence, cap004, containment)):
            return _unavailable_discount("DISCOUNT_REPORT_INCOMPLETE")
        assert isinstance(boundary, Mapping)
        assert isinstance(product_evidence, Mapping)
        assert isinstance(cap004, Mapping)
        assert isinstance(containment, Mapping)
        if boundary.get("product_contract_version") != "0.1.0" or boundary.get("product_contract_continuity") != "PASS":
            return _unavailable_discount("DISCOUNT_CONTRACT_REVALIDATION_FAILED")
        if boundary.get("shared_dependencies") != ["CAP-004"]:
            return _unavailable_discount("DISCOUNT_DEPENDENCY_BOUNDARY_CHANGED")
        if cap004.get("read_only") is not True or cap004.get("reconstruction_complete") is not True:
            return _unavailable_discount("DISCOUNT_RECONSTRUCTION_INCOMPLETE")
        expected_zero = (
            "network_calls",
            "telegram_calls",
            "discount_parser_publish_calls",
            "product_database_mutations",
            "external_mutations",
            "canonical_state_mutations",
        )
        if any(containment.get(key) != 0 for key in expected_zero) or containment.get("telegram_effect_replayed") is not False:
            return _unavailable_discount("DISCOUNT_CONTAINMENT_REVALIDATION_FAILED")

        def text(key: str) -> str:
            value_raw = product_evidence.get(key)
            return str(value_raw) if value_raw is not None else "Not exposed"

        return ProductSurface(
            product_id="discount-parser",
            name="Discount Parser",
            purpose="Controlled Telegram publication reconstruction",
            evidence_state="available",
            evidence_code="PASS_RETAINED_P7_08_RECONSTRUCTION",
            source="Discount Parser product evidence + Telegram external confirmation",
            authority_mode="Derived reconstruction / External Reference",
            summary="A real retained publication outcome is reconstructable through the P6.06 CAP-004-only Product Contract boundary without replaying the Telegram effect.",
            work=(
                ProductWorkItem(
                    "Offer",
                    text("offer_id"),
                    "Product-owned offer identity; Offer schema, classification and eligibility remain inside Discount Parser.",
                ),
                ProductWorkItem(
                    "Publication",
                    text("publication_id"),
                    "Product-owned publication reference reconstructed from retained evidence.",
                ),
                ProductWorkItem(
                    "External outcome",
                    "Telegram confirmation retained",
                    "Telegram remains authoritative for the external message; the Workspace shows derived reconstruction evidence only.",
                ),
                ProductWorkItem(
                    "Template",
                    text("template_version"),
                    "The rendering/template semantics remain product-owned and are referenced only for reconstruction.",
                ),
            ),
            boundary=_DISCOUNT_BOUNDARY,
            operational_contour="P7.08",
            evidence_classification="non-canonical operational evidence",
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ProductSurfacesError, ValueError, TypeError):
        return _unavailable_discount("DISCOUNT_REVALIDATION_UNAVAILABLE")


class RuntimeProductSurfacesProvider:
    """Read-only P9.07 composition over explicit P7.07/P7.08 platform evidence boundaries."""

    def __init__(self, runtime_root: Path) -> None:
        self._runtime_root = runtime_root.expanduser().resolve()

    def project(self, access: AccessContext) -> ProductSurfacesProjection:
        # Access is resolved/revalidated by the BFF before this provider is called.
        # It is intentionally not used as a selector: browser/client input cannot choose
        # another Organization or product evidence scope.
        if not access.organization.value or not access.actor.value:
            raise ProductSurfacesError("attributable server-resolved access context required")
        return ProductSurfacesProjection(
            generated_at=datetime.now(UTC),
            products=(
                _verified_tender_surface(self._runtime_root),
                _verified_discount_surface(self._runtime_root),
            ),
        )


__all__ = [
    "ProductContractBoundary",
    "ProductSurface",
    "ProductSurfacesError",
    "ProductSurfacesProjection",
    "ProductSurfacesProvider",
    "ProductWorkItem",
    "RuntimeProductSurfacesProvider",
]
