from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext, WorkspaceAccessError
from workspace_app.config import WorkspaceSettings
from workspace_app.copilot import (
    CopilotAnswer,
    CopilotClaim,
    CopilotEvidence,
    CopilotModelError,
    ModelDescriptor,
    RuntimeCopilotProvider,
)
from workspace_app.discovery import (
    DiscoveryFreshness,
    DiscoveryHealth,
    DiscoveryKind,
    DiscoveryProjection,
    DiscoveryResult,
)
from workspace_app.main import CSRF_HEADER, RELEASE_HEADER, create_app
from workspace_app.products import ProductCompositionProjection, ProductSurface
from workspace_app.release import load_release


ACCESS = AccessContext(
    organization=Identity("organization", "org-a", "platform"),
    actor=Identity("principal", "actor-a", "org-a"),
    principal_kind="human",
    credential_id="credential-a",
    grant_id="grant-a",
)


class FakeDiscovery:
    def __init__(self, results: tuple[DiscoveryResult, ...]) -> None:
        self.results = results

    def search(self, access: AccessContext, *, query: str = "", kind: DiscoveryKind | None = None) -> DiscoveryProjection:
        self.last_access = access
        results = self.results
        if kind is not None:
            results = tuple(item for item in results if item.kind is kind)
        if query.strip():
            needle = query.casefold()
            results = tuple(
                item
                for item in results
                if needle in " ".join((item.title, item.summary, item.source_label, item.semantic_role)).casefold()
                or query == "0344100006426000005"
            )
        return DiscoveryProjection(
            generated_at="2026-08-22T00:00:00Z",
            query=query,
            kind_filter=kind,
            health=DiscoveryHealth(
                DiscoveryFreshness.FRESH,
                "OK",
                "Current authorized source snapshot.",
                "2026-08-22T00:00:00Z",
            ),
            results=results,
        )

    def inspect(self, access: AccessContext, object_id: str):  # pragma: no cover - Copilot uses links, not hidden detail reads
        raise AssertionError("Copilot must not bypass the ordinary inspectable source link boundary")


class FakeProducts:
    def __init__(self, products: tuple[ProductSurface, ...]) -> None:
        self.products = products

    def project(self, access: AccessContext) -> ProductCompositionProjection:
        self.last_access = access
        return ProductCompositionProjection(self.products)


class FakeModel:
    descriptor = ModelDescriptor("test-model-adapter", "bounded-test-model")

    def synthesize(self, question: str, evidence: tuple[CopilotEvidence, ...]) -> str:
        self.question = question
        self.evidence = evidence
        return "The retained evidence supports the displayed status; verify the cited source before consequential reliance."


class FailingModel(FakeModel):
    def synthesize(self, question: str, evidence: tuple[CopilotEvidence, ...]) -> str:
        raise CopilotModelError("test outage")


def notice_result() -> DiscoveryResult:
    return DiscoveryResult(
        object_id="a" * 20,
        kind=DiscoveryKind.DOCUMENT,
        semantic_role="Document",
        title="EIS notice 0344100006426000005",
        summary="A governed External Reference to the EIS notice is available from ЕИС / zakupki.gov.ru.",
        source_label="ЕИС / zakupki.gov.ru",
        authority_mode="External Reference",
        state_label="retained · current",
    )


def tender_product() -> ProductSurface:
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
        summary="Persistent Tender Operator context is available through declared CAP-001 Product Contract reliance.",
        shared_dependencies=("CAP-001",),
        source_authority="ЕИС / zakupki.gov.ru — External Reference",
        interaction="inspect-product-context",
        technical_refs=("governed-item:secret-technical-ref",),
        product_release_sha="1" * 40,
    )


class CopilotGroundingTests(unittest.TestCase):
    def test_real_question_shape_keeps_facts_synthesis_sources_and_authority_distinct(self) -> None:
        discovery = FakeDiscovery((notice_result(),))
        products = FakeProducts((tender_product(),))
        model = FakeModel()
        answer = RuntimeCopilotProvider(discovery, products, model=model).answer(
            ACCESS,
            "Каков текущий статус закупки 0344100006426000005 и какой источник авторитетен?",
        )
        payload = answer.to_payload()
        kinds = [claim["kind"] for claim in payload["claims"]]
        self.assertIn("source-context", kinds)
        self.assertIn("synthesis", kinds)
        self.assertTrue(payload["model"]["used"])
        self.assertEqual(payload["model"]["output_role"], "synthesis-only")
        self.assertTrue(payload["generation"]["transient_output"])
        self.assertFalse(payload["generation"]["validated_knowledge"])
        self.assertFalse(payload["generation"]["canonical_state_changed"])
        self.assertFalse(payload["generation"]["external_effect_performed"])
        self.assertFalse(payload["generation"]["organizational_authority_provided"])
        self.assertFalse(payload["follow_up"]["routes_to_governed_execution"])
        self.assertEqual(payload["follow_up"]["kind"], "inspect-evidence-first")
        self.assertEqual(payload["follow_up"]["href"], "/objects/" + "a" * 20)
        self.assertTrue(payload["follow_up"]["context_bound_governed_continuation_required"])
        self.assertEqual(discovery.last_access, ACCESS)
        self.assertEqual(products.last_access, ACCESS)
        serialized_model_evidence = " ".join(item.summary for item in model.evidence)
        self.assertNotIn("secret-technical-ref", serialized_model_evidence)
        self.assertTrue(all(source["inspectable_in_workspace"] for source in payload["sources"]))

    def test_unvalidated_knowledge_role_is_source_context_not_fact(self) -> None:
        observation = DiscoveryResult(
            object_id="b" * 20,
            kind=DiscoveryKind.KNOWLEDGE,
            semantic_role="Observation",
            title="Supplier observation",
            summary="Observation — not validated Knowledge. Governed observation context is available.",
            source_label="Arvectum OS governed state",
            authority_mode="Native",
            state_label="retained · unvalidated",
            knowledge_role="Observation — not validated Knowledge",
        )
        payload = RuntimeCopilotProvider(FakeDiscovery((observation,)), FakeProducts(())).answer(
            ACCESS, "Что известно про supplier observation?"
        ).to_payload()
        source_claims = [claim for claim in payload["claims"] if claim["kind"] == "source-context"]
        self.assertTrue(source_claims)
        self.assertTrue(all(claim["kind"] != "sourced-fact" for claim in payload["claims"]))
        self.assertEqual(payload["sources"][0]["knowledge_role"], "Observation — not validated Knowledge")
        self.assertTrue(payload["semantics"]["unvalidated_knowledge_not_presented_as_fact"])

    def test_model_outage_never_replaces_missing_synthesis_with_invented_certainty(self) -> None:
        answer = RuntimeCopilotProvider(
            FakeDiscovery((notice_result(),)),
            FakeProducts(()),
            model=FailingModel(),
        ).answer(ACCESS, "Что известно про 0344100006426000005?")
        payload = answer.to_payload()
        self.assertFalse(payload["model"]["used"])
        self.assertEqual(payload["model"]["failure"], "MODEL_UNAVAILABLE")
        self.assertTrue(any(claim["kind"] == "uncertainty" for claim in payload["claims"]))
        self.assertTrue(any(claim["kind"] == "source-context" for claim in payload["claims"]))

    def test_unknown_question_returns_unavailable_evidence_instead_of_guessing(self) -> None:
        answer = RuntimeCopilotProvider(FakeDiscovery(()), FakeProducts(())).answer(
            ACCESS,
            "Расскажи про объект, которого нет в разрешённом контексте",
        )
        payload = answer.to_payload()
        self.assertEqual(payload["sources"], [])
        self.assertTrue(any(claim["kind"] == "unavailable-evidence" for claim in payload["claims"]))
        self.assertFalse(payload["generation"]["validated_knowledge"])

    def test_reconciliation_question_surfaces_uncertainty(self) -> None:
        product = ProductSurface(
            product_id="discount-parser",
            label="Discount Parser",
            repository="arvectum/discount-parser",
            product_contract="P6.06",
            product_contract_version="0.1.0",
            product_contract_lifecycle="Provisional",
            contour="P7.08",
            operating_scope="Persistent Internal / owner-operated",
            status="verified-retained-context",
            summary="A verified CAP-004 reconstruction context is retained; replay of the historical external effect is disabled.",
            shared_dependencies=("CAP-004",),
            source_authority="Product-owned external-outcome evidence; platform reconstruction is read-only",
            interaction="inspect-product-context",
            technical_refs=("execution:hidden",),
        )
        answer = RuntimeCopilotProvider(FakeDiscovery(()), FakeProducts((product,))).answer(
            ACCESS,
            "Какой выбран контекст Discount Parser и есть ли неопределённость или reconciliation?",
        )
        payload = answer.to_payload()
        self.assertTrue(any(claim["kind"] == "uncertainty" for claim in payload["claims"]))
        self.assertEqual(payload["sources"][0]["open_href"], "/products/discount-parser")


class FakeResolver:
    def __init__(self) -> None:
        self.denied = False

    def authorize(self) -> AccessContext:
        if self.denied:
            raise WorkspaceAccessError("revoked")
        return ACCESS


class RecordingCopilot:
    def __init__(self) -> None:
        self.calls: list[tuple[AccessContext, str]] = []

    def answer(self, access: AccessContext, question: str) -> CopilotAnswer:
        self.calls.append((access, question))
        source = CopilotEvidence(
            source_id="object:" + "a" * 20,
            label="EIS notice",
            summary="Inspectable governed evidence.",
            authority="External Reference · ЕИС / zakupki.gov.ru",
            freshness="fresh",
            open_href="/objects/" + "a" * 20,
            semantic_role="Document",
        )
        return CopilotAnswer(
            generated_at="2026-08-22T00:00:00Z",
            claims=(CopilotClaim("source-context", "Inspectable governed evidence.", (source.source_id,)),),
            sources=(source,),
            model_provider="test",
            model_name="test",
            model_used=False,
            model_failure=None,
        )


class CopilotBffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        static = root / "dist"
        static.mkdir()
        (static / "index.html").write_text("<!doctype html><div id='root'></div>", encoding="utf-8")
        self.resolver = FakeResolver()
        self.copilot = RecordingCopilot()
        settings = WorkspaceSettings(
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
        app = create_app(settings, access_resolver=self.resolver, copilot_provider=self.copilot, static_dir=static)
        self.client = TestClient(app, base_url="http://127.0.0.1:8769", client=("127.0.0.1", 50000))
        self.release = load_release().release_id
        self.base_headers = {RELEASE_HEADER: self.release, "Origin": "http://127.0.0.1:8769"}
        bootstrap = self.client.post("/api/app/v1/session/bootstrap", headers=self.base_headers)
        self.assertEqual(bootstrap.status_code, 200)
        self.csrf = bootstrap.json()["session"]["csrf_token"]

    def tearDown(self) -> None:
        self.client.close()
        self.temp.cleanup()

    def test_copilot_post_requires_csrf_and_reuses_server_access_context(self) -> None:
        missing = self.client.post(
            "/api/app/v1/copilot/ask",
            headers=self.base_headers,
            json={"question": "Что известно?"},
        )
        self.assertEqual(missing.status_code, 403)
        response = self.client.post(
            "/api/app/v1/copilot/ask",
            headers={**self.base_headers, CSRF_HEADER: self.csrf},
            json={"question": "Что известно?"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.copilot.calls, [(ACCESS, "Что известно?")])
        payload = response.json()
        self.assertFalse(payload["generation"]["canonical_state_changed"])
        self.assertFalse(payload["generation"]["organizational_authority_provided"])

    def test_browser_cannot_supply_scope_authority_or_hidden_context(self) -> None:
        response = self.client.post(
            "/api/app/v1/copilot/ask",
            headers={**self.base_headers, CSRF_HEADER: self.csrf},
            json={"question": "Что известно?", "organization": "evil", "authority": "approved"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "COPILOT_INPUT_REJECTED")
        self.assertEqual(self.copilot.calls, [])

    def test_current_access_is_revalidated_before_question_reaches_copilot(self) -> None:
        self.resolver.denied = True
        response = self.client.post(
            "/api/app/v1/copilot/ask",
            headers={**self.base_headers, CSRF_HEADER: self.csrf},
            json={"question": "Что известно?"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.copilot.calls, [])


if __name__ == "__main__":
    unittest.main()
