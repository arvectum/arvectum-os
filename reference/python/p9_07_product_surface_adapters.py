from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import p7_03_durable_state as p703
import p7_08_discount_parser_cross_host as p708
from workspace_app.access import AccessContext
from workspace_app.products import (
    ComposedProductSurfacesProvider,
    ProductContractBoundary,
    ProductSurface,
    ProductSurfacesError,
    ProductWorkItem,
)

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


class TenderOperatorSurfaceAdapter:
    """P6.02-owned presentation adapter over the already-proven P7.07 platform evidence contour."""

    def __init__(self, runtime_root: Path) -> None:
        self._runtime_root = runtime_root.expanduser().resolve()

    def project(self, access: AccessContext) -> ProductSurface:
        del access  # Organization/actor access has already been resolved by the BFF; it is not a selector here.
        try:
            status = p703.verify_store(self._runtime_root)
            if status.get("integrity") != "PASS":
                return _unavailable_tender("TENDER_STORE_UNAVAILABLE")
            items_root = self._runtime_root / "state" / "governed" / "items"
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
            if len(candidates) != 1:
                return _unavailable_tender("TENDER_RETAINED_EVIDENCE_AMBIGUOUS")
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


class DiscountParserSurfaceAdapter:
    """P6.06-owned presentation adapter over the already-proven P7.08 CAP-004 reconstruction contour."""

    def __init__(self, runtime_root: Path) -> None:
        self._runtime_root = runtime_root.expanduser().resolve()

    def project(self, access: AccessContext) -> ProductSurface:
        del access  # Organization/actor access has already been resolved by the BFF; it is not a selector here.
        reports_root = self._runtime_root / "product-contours" / "discount-parser" / "runs"
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
            continuity = value.get("continuity")
            product_evidence = value.get("product_evidence")
            cap004 = value.get("cap004")
            containment = value.get("containment")
            if not all(isinstance(item, Mapping) for item in (continuity, product_evidence, cap004, containment)):
                return _unavailable_discount("DISCOUNT_REPORT_INCOMPLETE")
            assert isinstance(continuity, Mapping)
            assert isinstance(product_evidence, Mapping)
            assert isinstance(cap004, Mapping)
            assert isinstance(containment, Mapping)
            if continuity.get("product_contract_version") != "0.1.0" or continuity.get("product_contract_continuity") != "PASS":
                return _unavailable_discount("DISCOUNT_CONTRACT_REVALIDATION_FAILED")
            if continuity.get("shared_dependencies") != ["CAP-004"]:
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
            required_product_fields = ("offer_id", "publication_id", "template_version")
            if product_evidence.get("external_confirmation") != "PASS" or any(
                not isinstance(product_evidence.get(key), str) or not str(product_evidence.get(key)).strip()
                for key in required_product_fields
            ):
                return _unavailable_discount("DISCOUNT_EXTERNAL_EVIDENCE_REVALIDATION_FAILED")

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
                        str(product_evidence["offer_id"]),
                        "Product-owned offer identity; Offer schema, classification and eligibility remain inside Discount Parser.",
                    ),
                    ProductWorkItem(
                        "Publication",
                        str(product_evidence["publication_id"]),
                        "Product-owned publication reference reconstructed from retained evidence.",
                    ),
                    ProductWorkItem(
                        "External outcome",
                        "Telegram confirmation retained",
                        "Telegram remains authoritative for the external message; the Workspace shows derived reconstruction evidence only.",
                    ),
                    ProductWorkItem(
                        "Template",
                        str(product_evidence["template_version"]),
                        "The rendering/template semantics remain product-owned and are referenced only for reconstruction.",
                    ),
                ),
                boundary=_DISCOUNT_BOUNDARY,
                operational_contour="P7.08",
                evidence_classification="non-canonical operational evidence",
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ProductSurfacesError, ValueError, TypeError):
            return _unavailable_discount("DISCOUNT_REVALIDATION_UNAVAILABLE")


def build_product_surfaces_provider(runtime_root: Path) -> ComposedProductSurfacesProvider:
    """Build the exact P9.07 internal composition without importing product repositories or mutable product stores."""

    root = runtime_root.expanduser().resolve()
    return ComposedProductSurfacesProvider(
        adapters=(
            TenderOperatorSurfaceAdapter(root),
            DiscountParserSurfaceAdapter(root),
        )
    )


__all__ = [
    "DiscountParserSurfaceAdapter",
    "TenderOperatorSurfaceAdapter",
    "build_product_surfaces_provider",
]
