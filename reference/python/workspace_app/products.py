from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

import p7_03_durable_state as p703

from .access import AccessContext


class ProductCompositionError(RuntimeError):
    """Product composition evidence is unavailable, unsafe, or inconsistent."""


@dataclass(frozen=True, slots=True)
class ProductSurface:
    product_id: str
    label: str
    repository: str
    product_contract: str
    product_contract_version: str
    product_contract_lifecycle: str
    contour: str
    operating_scope: str
    status: str
    summary: str
    shared_dependencies: tuple[str, ...]
    source_authority: str
    interaction: str
    technical_refs: tuple[str, ...]
    product_release_sha: str | None = None

    def to_payload(self) -> dict[str, Any]:
        return {
            "id": self.product_id,
            "label": self.label,
            "ownership": "product-owned",
            "repository": self.repository,
            "product_contract": {
                "id": self.product_contract,
                "version": self.product_contract_version,
                "lifecycle": self.product_contract_lifecycle,
            },
            "contour": {
                "id": self.contour,
                "operating_scope": self.operating_scope,
                "status": self.status,
                "summary": self.summary,
                "shared_dependencies": list(self.shared_dependencies),
                "source_authority": self.source_authority,
            },
            "interaction": {
                "kind": self.interaction,
                "product_specific_work_stays_product_owned": True,
                "authority_provided": False,
                "canonical_mutation_available": False,
                "external_effect_available": False,
            },
            "technical": {
                "product_release_sha": self.product_release_sha,
                "evidence_refs": list(self.technical_refs),
            },
        }


@dataclass(frozen=True, slots=True)
class ProductCompositionProjection:
    products: tuple[ProductSurface, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "schema": "arvectum.workspace.product-composition/1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "product_semantics_owned_by_platform": False,
                "organizational_authority_provided": False,
                "cross_product_business_relationship_inferred": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "current_access_revalidated": True,
                "switching_products_broadens_authorization": False,
            },
            "products": [item.to_payload() for item in self.products],
        }


class ProductCompositionProvider(Protocol):
    def project(self, access: AccessContext) -> ProductCompositionProjection: ...


_MAX_JSON_BYTES = 2 * 1024 * 1024
_TENDER_CONFIG_SCHEMA = "arvectum.p7_07.tender-operator-contour-config/1"
_DISCOUNT_REPORT_SCHEMA = "arvectum-os.p7-08.discount-parser-cap004-reconstruction"
_DISCOUNT_RECEIPT_SCHEMA = "arvectum-os.p7-08.discount-parser-reconstruction-receipt"


def _read_json(path: Path, *, label: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ProductCompositionError(f"{label} missing or unsafe")
    try:
        if path.stat().st_size <= 0 or path.stat().st_size > _MAX_JSON_BYTES:
            raise ProductCompositionError(f"{label} outside bounded size")
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductCompositionError(f"{label} unreadable") from exc
    if not isinstance(value, dict):
        raise ProductCompositionError(f"{label} must be a JSON object")
    return value


def _verify_sidecar(json_path: Path, digest_path: Path, *, label: str) -> str:
    _read_json(json_path, label=label)
    try:
        raw = json_path.read_bytes()
        line = digest_path.read_text(encoding="utf-8").strip()
        digest, filename = line.split(maxsplit=1)
    except (OSError, ValueError) as exc:
        raise ProductCompositionError(f"{label} digest unavailable") from exc
    actual = hashlib.sha256(raw).hexdigest()
    if digest != actual or filename.strip() != json_path.name:
        raise ProductCompositionError(f"{label} digest mismatch")
    return actual


class RuntimeProductCompositionProvider:
    """Read-only composition over already-proven P7.07/P7.08 evidence.

    This adapter does not load product code, product databases, external effect
    clients, or product domain models. It exposes only a minimal product-neutral
    envelope required for Workspace composition and leaves detailed semantics to
    compile-time product-owned contributions.
    """

    def __init__(self, runtime_root: Path) -> None:
        self.runtime_root = runtime_root.expanduser().resolve()

    def _tender(self) -> ProductSurface:
        config = _read_json(
            self.runtime_root / "config" / "p7-07-tender-operator.json",
            label="P7.07 Tender Operator routing evidence",
        )
        if config.get("schema") != _TENDER_CONFIG_SCHEMA:
            raise ProductCompositionError("P7.07 Tender Operator routing schema mismatch")
        expected = {
            "product_id": "arvectum-tender-operator",
            "product_contract_version": "0.1.0",
            "external_authority": "ЕИС / zakupki.gov.ru",
            "raw_document_bytes_required": False,
            "external_actions_enabled": False,
        }
        for key, value in expected.items():
            if config.get(key) != value:
                raise ProductCompositionError(f"P7.07 Tender Operator boundary mismatch: {key}")
        item_id = config.get("storage_item_id")
        if not isinstance(item_id, str) or len(item_id) != 64 or any(ch not in "0123456789abcdef" for ch in item_id):
            raise ProductCompositionError("P7.07 Tender Operator item reference invalid")
        try:
            manifest = p703.verify_item(self.runtime_root / "state" / "governed" / "items" / item_id)
        except Exception as exc:
            raise ProductCompositionError("P7.07 governed item integrity verification failed") from exc
        metadata = manifest.get("metadata")
        if not isinstance(metadata, dict):
            raise ProductCompositionError("P7.07 governed item metadata missing")
        required_metadata = {
            "operational_contour": "P7.07",
            "product_contract_version": "0.1.0",
            "authority_mode": "External Reference",
            "authoritative_source": "ЕИС / zakupki.gov.ru",
            "rehydratable_cap001_document": True,
            "external_actions": False,
        }
        for key, value in required_metadata.items():
            if metadata.get(key) != value:
                raise ProductCompositionError(f"P7.07 governed item boundary mismatch: {key}")
        release_sha = metadata.get("source_release_sha")
        if not isinstance(release_sha, str) or len(release_sha) != 40:
            release_sha = None
        return ProductSurface(
            product_id="tender-operator",
            label="Tender Operator",
            repository="arvectum/tender-agent",
            product_contract="P6.02",
            product_contract_version="0.1.0",
            product_contract_lifecycle="Provisional",
            contour="P7.07",
            operating_scope="Persistent Internal / owner-operated",
            status="verified-retained-context",
            summary="Persistent Tender Operator context is available through its declared CAP-001 Product Contract reliance. EIS remains externally authoritative.",
            shared_dependencies=("CAP-001",),
            source_authority="ЕИС / zakupki.gov.ru — External Reference",
            interaction="inspect-product-context",
            technical_refs=(f"governed-item:{item_id}",),
            product_release_sha=release_sha,
        )

    def _discount(self) -> ProductSurface:
        runs_root = self.runtime_root / "product-contours" / "discount-parser" / "runs"
        if runs_root.is_symlink() or not runs_root.is_dir():
            raise ProductCompositionError("P7.08 Discount Parser retained contour unavailable")
        candidates: list[tuple[str, dict[str, Any], str]] = []
        for run_dir in sorted(runs_root.iterdir(), key=lambda path: path.name):
            if run_dir.is_symlink() or not run_dir.is_dir():
                continue
            root = run_dir / "reconstruction"
            report_path = root / "p7-08-discount-parser-reconstruction.json"
            report_digest = root / "p7-08-discount-parser-reconstruction.sha256"
            receipt_path = root / "p7-08-discount-parser-reconstruction-receipt.json"
            receipt_digest = root / "p7-08-discount-parser-reconstruction-receipt.sha256"
            if not all(path.is_file() and not path.is_symlink() for path in (report_path, report_digest, receipt_path, receipt_digest)):
                continue
            report_sha = _verify_sidecar(report_path, report_digest, label="P7.08 reconstruction report")
            _verify_sidecar(receipt_path, receipt_digest, label="P7.08 reconstruction receipt")
            report = _read_json(report_path, label="P7.08 reconstruction report")
            receipt = _read_json(receipt_path, label="P7.08 reconstruction receipt")
            if report.get("schema") != _DISCOUNT_REPORT_SCHEMA or receipt.get("schema") != _DISCOUNT_RECEIPT_SCHEMA:
                continue
            if report.get("status") != "PASS" or receipt.get("reconstruction_complete") is not True:
                continue
            if receipt.get("report_sha256") != report_sha or receipt.get("external_effect_replayed") is not False:
                continue
            continuity = report.get("continuity")
            containment = report.get("containment")
            product = report.get("product_evidence")
            if not isinstance(continuity, dict) or not isinstance(containment, dict) or not isinstance(product, dict):
                continue
            if continuity.get("product_contract_version") != "0.1.0" or continuity.get("shared_dependencies") != ["CAP-004"]:
                continue
            if containment.get("external_mutations") != 0 or containment.get("telegram_effect_replayed") is not False:
                continue
            execution_id = report.get("execution_id")
            if not isinstance(execution_id, str) or not execution_id:
                continue
            candidates.append((execution_id, report, report_sha))
        if not candidates:
            raise ProductCompositionError("no verified P7.08 Discount Parser reconstruction is retained")
        execution_id, report, report_sha = candidates[-1]
        product = report["product_evidence"]
        release_sha = product.get("repository_sha")
        if not isinstance(release_sha, str) or len(release_sha) != 40:
            release_sha = None
        return ProductSurface(
            product_id="discount-parser",
            label="Discount Parser",
            repository="arvectum/discount-parser",
            product_contract="P6.06",
            product_contract_version="0.1.0",
            product_contract_lifecycle="Provisional",
            contour="P7.08",
            operating_scope="Persistent Internal / owner-operated",
            status="verified-retained-context",
            summary="A verified Discount Parser CAP-004 reconstruction context is retained. Reconstruction is read-only and does not replay a historical external effect.",
            shared_dependencies=("CAP-004",),
            source_authority="Product-owned external-outcome evidence; platform reconstruction is read-only",
            interaction="inspect-product-context",
            technical_refs=(f"execution:{execution_id}", f"report-sha256:{report_sha}"),
            product_release_sha=release_sha,
        )

    def project(self, access: AccessContext) -> ProductCompositionProjection:
        del access
        return ProductCompositionProjection((self._tender(), self._discount()))
