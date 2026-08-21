from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.config import WorkspaceSettings
from workspace_app.main import RELEASE_HEADER, create_app
from workspace_app.products import (
    ProductCompositionError,
    ProductCompositionProjection,
    ProductSurface,
)


class FakeResolver:
    def authorize(self) -> AccessContext:
        return AccessContext(
            organization=Identity("organization", "org-a", "platform"),
            actor=Identity("principal", "owner", "org-a"),
            principal_kind="human",
            credential_id="credential-a",
            grant_id="grant-a",
        )


class FakeProducts:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.calls = 0

    def project(self, access: AccessContext) -> ProductCompositionProjection:
        self.calls += 1
        if self.fail:
            raise ProductCompositionError("unavailable")
        return ProductCompositionProjection(
            (
                ProductSurface(
                    "tender-operator",
                    "Tender Operator",
                    "arvectum/tender-agent",
                    "P6.02",
                    "0.1.0",
                    "Provisional",
                    "P7.07",
                    "Persistent Internal / owner-operated",
                    "verified-retained-context",
                    "Tender context",
                    ("CAP-001",),
                    "ЕИС / zakupki.gov.ru — External Reference",
                    "inspect-product-context",
                    ("governed-item:x",),
                ),
                ProductSurface(
                    "discount-parser",
                    "Discount Parser",
                    "arvectum/discount-parser",
                    "P6.06",
                    "0.1.0",
                    "Provisional",
                    "P7.08",
                    "Persistent Internal / owner-operated",
                    "verified-retained-context",
                    "Discount context",
                    ("CAP-004",),
                    "Product-owned external-outcome evidence; platform reconstruction is read-only",
                    "inspect-product-context",
                    ("execution:y",),
                ),
            )
        )


def settings(root: Path) -> WorkspaceSettings:
    return WorkspaceSettings(
        runtime_root=root,
        public_origin="http://127.0.0.1:8769",
        bind_host="127.0.0.1",
        bind_port=8769,
        allowed_hosts=("127.0.0.1:8769",),
        organization_label="ООО «Арвектум»",
        actor_label="Owner operator",
        session_idle_seconds=60,
        session_absolute_seconds=300,
        allow_loopback_http=True,
    )


class ProductCompositionBffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        static = root / "dist"
        static.mkdir()
        (static / "index.html").write_text("ok", encoding="utf-8")
        self.provider = FakeProducts()
        self.client = TestClient(
            create_app(
                settings(root),
                access_resolver=FakeResolver(),
                product_provider=self.provider,
                static_dir=static,
            ),
            base_url="http://127.0.0.1:8769",
        )
        self.headers = {RELEASE_HEADER: "p9.07.1"}
        response = self.client.post(
            "/api/app/v1/session/bootstrap",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_products_returns_only_non_authoritative_explicit_composition(self) -> None:
        response = self.client.get("/api/app/v1/products", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["projection"]["canonical_authority"])
        self.assertFalse(payload["projection"]["product_semantics_owned_by_platform"])
        self.assertFalse(payload["projection"]["cross_product_business_relationship_inferred"])
        self.assertFalse(payload["scope"]["switching_products_broadens_authorization"])
        self.assertEqual(
            [item["product_contract"]["lifecycle"] for item in payload["products"]],
            ["Provisional", "Provisional"],
        )
        self.assertTrue(all(not item["interaction"]["authority_provided"] for item in payload["products"]))
        self.assertTrue(all(not item["interaction"]["canonical_mutation_available"] for item in payload["products"]))
        self.assertEqual(self.provider.calls, 1)

    def test_product_composition_requires_current_session(self) -> None:
        other = TestClient(
            create_app(
                settings(Path(self.temp.name)),
                access_resolver=FakeResolver(),
                product_provider=self.provider,
                static_dir=Path(self.temp.name) / "dist",
            ),
            base_url="http://127.0.0.1:8769",
        )
        response = other.get("/api/app/v1/products", headers=self.headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "SESSION_REQUIRED")

    def test_unavailable_product_evidence_fails_closed(self) -> None:
        failing = TestClient(
            create_app(
                settings(Path(self.temp.name)),
                access_resolver=FakeResolver(),
                product_provider=FakeProducts(fail=True),
                static_dir=Path(self.temp.name) / "dist",
            ),
            base_url="http://127.0.0.1:8769",
        )
        boot = failing.post(
            "/api/app/v1/session/bootstrap",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(boot.status_code, 200)
        response = failing.get("/api/app/v1/products", headers=self.headers)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "PRODUCT_COMPOSITION_UNAVAILABLE")


class ProductCompositionPayloadTests(unittest.TestCase):
    def test_neutral_projection_does_not_define_product_domain_fields(self) -> None:
        surface = ProductSurface(
            "discount-parser",
            "Discount Parser",
            "arvectum/discount-parser",
            "P6.06",
            "0.1.0",
            "Provisional",
            "P7.08",
            "Persistent Internal / owner-operated",
            "verified-retained-context",
            "Verified read-only reconstruction",
            ("CAP-004",),
            "Product-owned external-outcome evidence",
            "inspect-product-context",
            ("execution:x",),
        )
        raw = json.dumps(ProductCompositionProjection((surface,)).to_payload(), sort_keys=True)
        for forbidden in (
            "offer_id",
            "publication_id",
            "template_version",
            "telegram_message_id",
            "tender_id",
            "bid",
        ):
            self.assertNotIn(forbidden, raw)


if __name__ == "__main__":
    unittest.main()
