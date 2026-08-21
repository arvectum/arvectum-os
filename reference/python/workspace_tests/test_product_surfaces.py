from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.products import RuntimeProductSurfacesProvider
import p7_08_discount_parser_cross_host as p708


def _access() -> AccessContext:
    return AccessContext(
        organization=Identity("organization", "arvectum", "platform"),
        actor=Identity("principal", "owner", "arvectum"),
        principal_kind="human",
        credential_id="credential-test",
        grant_id="grant-test",
    )


def _write_discount_report(root: Path, *, bad_digest: bool = False, dependencies: list[str] | None = None) -> None:
    reconstruction = root / "product-contours" / "discount-parser" / "runs" / "run-a" / "reconstruction"
    reconstruction.mkdir(parents=True)
    report = {
        "schema": p708.REPORT_SCHEMA,
        "schema_version": p708.REPORT_SCHEMA_VERSION,
        "status": "PASS",
        "scope": "Persistent Internal / owner-operated",
        "execution_id": "run-a",
        "continuity": {
            "product_contract_version": "0.1.0",
            "product_contract_continuity": "PASS",
            "shared_dependencies": dependencies if dependencies is not None else ["CAP-004"],
        },
        "product_evidence": {
            "repository": "arvectum/discount-parser",
            "repository_sha": "a" * 40,
            "offer_id": "offer-42",
            "publication_id": "publication-7",
            "target_ref": "channel-main",
            "template_version": "template-v3",
            "telegram_message_id": "55",
            "external_confirmation": "PASS",
        },
        "cap004": {
            "dependency": "CAP-004",
            "read_only": True,
            "reconstruction_complete": True,
            "gate_decisions_fabricated": False,
            "derived_observation_is_canonical_event": False,
        },
        "containment": {
            "network_calls": 0,
            "telegram_calls": 0,
            "discount_parser_publish_calls": 0,
            "product_database_mutations": 0,
            "external_mutations": 0,
            "canonical_state_mutations": 0,
            "telegram_effect_replayed": False,
        },
    }
    raw = (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    report_path = reconstruction / p708.REPORT_FILENAME
    digest_path = reconstruction / p708.REPORT_DIGEST_FILENAME
    report_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    if bad_digest:
        digest = "0" * 64
    digest_path.write_text(f"{digest}  {p708.REPORT_FILENAME}\n", encoding="utf-8")


class ProductSurfaceProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        item = self.root / "state" / "governed" / "items" / "item-a"
        item.mkdir(parents=True)
        _write_discount_report(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _tender_manifest(self):
        return {
            "metadata": {
                "state_class": "canonical-governed-state",
                "operational_contour": "P7.07",
                "product_contract_version": "0.1.0",
                "authority_mode": "External Reference",
                "authoritative_source": "ЕИС / zakupki.gov.ru",
                "rehydratable_cap001_document": True,
                "raw_document_bytes_included": False,
                "external_actions": False,
                "subject_identity": "must-not-leak",
                "version_identity": "must-not-leak",
                "storage_locator": "must-not-leak",
            }
        }

    def test_real_two_product_projection_is_minimized_and_boundary_explicit(self) -> None:
        with patch("workspace_app.products.p703.verify_store", return_value={"integrity": "PASS"}), patch(
            "workspace_app.products.p703.verify_item", return_value=self._tender_manifest()
        ):
            payload = RuntimeProductSurfacesProvider(self.root).project(_access()).to_payload()

        self.assertEqual(payload["schema"], "arvectum.workspace.product-surfaces/1")
        self.assertFalse(payload["projection"]["canonical_authority"])
        self.assertFalse(payload["projection"]["product_business_logic_in_platform"])
        self.assertFalse(payload["projection"]["hidden_coupling"])
        products = {item["id"]: item for item in payload["products"]}
        self.assertEqual(set(products), {"tender-operator", "discount-parser"})
        tender = products["tender-operator"]
        discount = products["discount-parser"]
        self.assertEqual(tender["evidence_state"], "available")
        self.assertEqual(discount["evidence_state"], "available")
        self.assertEqual(tender["boundary"]["lifecycle"], "Provisional")
        self.assertEqual(tender["boundary"]["dependencies"], ["CAP-001", "CAP-004"])
        self.assertEqual(discount["boundary"]["dependencies"], ["CAP-004"])
        self.assertEqual(discount["work"][0]["value"], "offer-42")
        self.assertEqual(discount["work"][1]["value"], "publication-7")
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("must-not-leak", serialized)
        self.assertNotIn("telegram_message_id", serialized)
        self.assertNotIn("repository_sha", serialized)
        self.assertNotIn("organization_id", serialized)
        self.assertNotIn("principal_id", serialized)

    def test_tampered_discount_report_fails_closed_without_product_work(self) -> None:
        self.temp.cleanup()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "state" / "governed" / "items").mkdir(parents=True)
        _write_discount_report(self.root, bad_digest=True)
        payload = RuntimeProductSurfacesProvider(self.root).project(_access()).to_payload()
        discount = next(item for item in payload["products"] if item["id"] == "discount-parser")
        self.assertEqual(discount["evidence_state"], "unavailable")
        self.assertEqual(discount["work"], [])
        self.assertIn("could not be revalidated", discount["summary"])

    def test_discount_dependency_expansion_fails_closed(self) -> None:
        self.temp.cleanup()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "state" / "governed" / "items").mkdir(parents=True)
        _write_discount_report(self.root, dependencies=["CAP-001", "CAP-004"])
        payload = RuntimeProductSurfacesProvider(self.root).project(_access()).to_payload()
        discount = next(item for item in payload["products"] if item["id"] == "discount-parser")
        self.assertEqual(discount["evidence_code"], "DISCOUNT_DEPENDENCY_BOUNDARY_CHANGED")
        self.assertEqual(discount["work"], [])

    def test_embedded_contract_metadata_matches_canonical_provisional_contracts(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        tender = (repo_root / "docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md").read_text(encoding="utf-8")
        discount = (repo_root / "docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("Status: `Provisional`", tender)
        self.assertIn("Version: `0.1.0`", tender)
        self.assertIn("restricted-paid-pilot/44fz-prebid-v1", tender)
        self.assertIn("Status: `Provisional`", discount)
        self.assertIn("Version: `0.1.0`", discount)
        self.assertIn("mvp-v1/controlled-telegram-publication", discount)


if __name__ == "__main__":
    unittest.main()
