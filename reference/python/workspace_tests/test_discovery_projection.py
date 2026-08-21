from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
import p7_06_ui4_owner_preflight as ui4
from workspace_app.access import AccessContext, WorkspaceAccessError
from workspace_app.config import WorkspaceSettings
from workspace_app.discovery import (
    DiscoveryKind,
    DiscoverySourceContext,
    DiscoverySourceItem,
    ObjectUnavailable,
    inspect_discovery,
    project_discovery,
)
from workspace_app.main import RELEASE_HEADER, create_app
from workspace_app.release import load_release


F1_SUBJECT = "document-subject/eis-0344100006426000005-exact-attachment-evidence@aa4e760c379c8952aba6c6c335f3e233"
F1_VERSION = "document-version/eis-0344100006426000005-74e943d855406b04@aa4e760c379c8952aba6c6c335f3e233"


def _document_item() -> DiscoverySourceItem:
    return DiscoverySourceItem(
        semantic_type="platform.document",
        schema_version="1",
        subject_identity=F1_SUBJECT,
        version_identity=F1_VERSION,
        authority_mode="External Reference",
        authority_scope="EIS exact notice attachment evidence",
        authoritative_source="ЕИС / zakupki.gov.ru",
        classification="internal",
        lifecycle_status="admitted",
        validation_status="CAP-004 reconstruction complete",
        provenance_refs=("execution-version/exact", "event-version/admitted"),
        source_release_sha="release-sha",
    )


def _knowledge_item() -> DiscoverySourceItem:
    return DiscoverySourceItem(
        semantic_type="platform.observation",
        schema_version="1",
        subject_identity="observation-subject/customer-signal",
        version_identity="observation-version/customer-signal-v1",
        authority_mode="Native",
        authority_scope="organization",
        authoritative_source=None,
        classification="internal",
        lifecycle_status="retained",
        validation_status="observed",
        provenance_refs=("event-version/source",),
        source_release_sha="release-sha",
    )


def _preflight() -> ui4.UI4OwnerPreflight:
    return ui4.UI4OwnerPreflight(
        release_sha="release-sha",
        organization_id="org-a",
        actor_id="actor-a",
        storage_item_id="storage-internal",
        subject_identity=F1_SUBJECT,
        version_identity=F1_VERSION,
        semantic_type="platform.document",
        authority_mode="External Reference",
        authority_scope="EIS exact notice attachment evidence",
        authoritative_source="ЕИС / zakupki.gov.ru",
        execution_subject="execution-subject/p7-ui4",
        execution_version="execution-version/p7-ui4-v5",
        event_version="event-version/document-admitted-v1",
        checkpoint_id="checkpoint-p7-ui4",
        provenance_refs=("execution-version/p7-ui4-v5", "event-version/document-admitted-v1"),
        validation_status="CAP-004 reconstruction complete",
        gates=(
            ui4.UI4GateView("Authorization", "Waiting", "missing"),
            ui4.UI4GateView("Organizational Authority", "Waiting", "missing"),
            ui4.UI4GateView("Data Governance", "Waiting", "missing"),
            ui4.UI4GateView("Consequential Approval", "Waiting", "missing"),
        ),
    )


def _source(*items: DiscoverySourceItem) -> DiscoverySourceContext:
    return DiscoverySourceContext(
        items=tuple(items),
        observed_at="2026-08-21T12:00:00Z",
        release_sha="release-sha",
        preflight=_preflight(),
    )


class DiscoveryProjectionTests(unittest.TestCase):
    def test_real_f1_is_findable_by_human_notice_without_exposing_internal_ids_in_results(self) -> None:
        projection = project_discovery(_source(_document_item()), query="0344100006426000005")
        payload = projection.to_payload()
        self.assertEqual(len(payload["results"]), 1)
        result = payload["results"][0]
        self.assertEqual(result["kind"], "document")
        self.assertEqual(result["source"], "ЕИС / zakupki.gov.ru")
        self.assertEqual(result["authority_mode"], "External Reference")
        self.assertRegex(result["id"], r"^[0-9a-f]{20}$")
        self.assertEqual(result["open_href"], f"/objects/{result['id']}")
        self.assertFalse(result["authority_provided"])
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn(F1_SUBJECT, serialized)
        self.assertNotIn(F1_VERSION, serialized)
        self.assertNotIn("storage-internal", serialized)
        self.assertFalse(payload["projection"]["canonical_authority"])
        self.assertFalse(payload["projection"]["search_result_is_authority"])
        self.assertFalse(payload["scope"]["denied_result_counts_exposed"])

    def test_documents_and_knowledge_can_be_filtered_without_semantic_flattening(self) -> None:
        source = _source(_document_item(), _knowledge_item())
        documents = project_discovery(source, kind=DiscoveryKind.DOCUMENT).to_payload()
        knowledge = project_discovery(source, kind=DiscoveryKind.KNOWLEDGE).to_payload()
        self.assertEqual([item["kind"] for item in documents["results"]], ["document"])
        self.assertEqual([item["kind"] for item in knowledge["results"]], ["knowledge"])
        self.assertEqual(knowledge["results"][0]["knowledge_role"], "Observation — not validated Knowledge")
        self.assertNotEqual(knowledge["results"][0]["knowledge_role"], "Knowledge")

    def test_opened_object_is_human_first_with_exact_technical_drill_down_and_waiting_gates(self) -> None:
        source = _source(_document_item())
        opaque = source.items[0].object_id
        payload = inspect_discovery(source, opaque).to_payload()
        self.assertEqual(payload["source"], "ЕИС / zakupki.gov.ru")
        self.assertEqual(payload["authority"]["mode"], "External Reference")
        self.assertFalse(payload["authority"]["organizational_authority_provided"])
        self.assertFalse(payload["context"]["consequential_action_available"])
        self.assertEqual(payload["technical"]["subject_identity"], F1_SUBJECT)
        self.assertEqual(payload["technical"]["version_identity"], F1_VERSION)
        self.assertEqual(payload["technical"]["related_execution_version"], "execution-version/p7-ui4-v5")
        self.assertEqual(payload["governed_preflight"]["outcome"], "Waiting")
        self.assertEqual(len(payload["governed_preflight"]["waiting_gates"]), 4)
        self.assertTrue(payload["projection"]["current_source_revalidated"])

    def test_unknown_or_malformed_opaque_reference_is_minimized(self) -> None:
        source = _source(_document_item())
        with self.assertRaisesRegex(ObjectUnavailable, "object is unavailable"):
            inspect_discovery(source, "document-subject/secret")
        with self.assertRaisesRegex(ObjectUnavailable, "object is unavailable"):
            inspect_discovery(source, "0" * 20)

    def test_query_bound_is_fail_closed(self) -> None:
        with self.assertRaisesRegex(Exception, "outside the bounded application contract"):
            project_discovery(_source(_document_item()), query="x" * 161)


class FakeResolver:
    def __init__(self) -> None:
        self.denied = False
        self.organization = Identity("organization", "org-a", "platform")
        self.actor = Identity("principal", "actor-a", "org-a")

    def authorize(self) -> AccessContext:
        if self.denied:
            raise WorkspaceAccessError("revoked")
        return AccessContext(
            organization=self.organization,
            actor=self.actor,
            principal_kind="human",
            credential_id="credential-test",
            grant_id="grant-test",
        )


class FakeDiscoveryProvider:
    def __init__(self, source: DiscoverySourceContext) -> None:
        self.source = source
        self.seen: list[AccessContext] = []

    def search(self, access: AccessContext, *, query: str = "", kind: DiscoveryKind | None = None):  # type: ignore[no-untyped-def]
        self.seen.append(access)
        return project_discovery(self.source, query=query, kind=kind)

    def inspect(self, access: AccessContext, object_id: str):  # type: ignore[no-untyped-def]
        self.seen.append(access)
        return inspect_discovery(self.source, object_id)


class FakeAttentionProvider:
    def project(self, access: AccessContext):  # type: ignore[no-untyped-def]
        raise AssertionError("P9.05 discovery test must not invoke My Work")


def _settings(root: Path) -> WorkspaceSettings:
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


class DiscoveryBffTests(unittest.TestCase):
    def _client(self):  # type: ignore[no-untyped-def]
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        static = root / "dist"
        static.mkdir()
        (static / "index.html").write_text("<!doctype html><div id='root'></div>", encoding="utf-8")
        (static / "assets").mkdir()
        resolver = FakeResolver()
        provider = FakeDiscoveryProvider(_source(_document_item(), _knowledge_item()))
        client = TestClient(
            create_app(
                _settings(root),
                access_resolver=resolver,
                attention_provider=FakeAttentionProvider(),
                discovery_provider=provider,
                static_dir=static,
            ),
            base_url="http://127.0.0.1:8769",
            client=("127.0.0.1", 50000),
        )
        release = load_release().release_id
        headers = {RELEASE_HEADER: release}
        response = client.post(
            "/api/app/v1/session/bootstrap",
            headers={**headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(response.status_code, 200)
        return temp, client, resolver, provider, headers

    def test_search_ignores_browser_supplied_organization_and_actor_scope(self) -> None:
        temp, client, resolver, provider, headers = self._client()
        try:
            response = client.get(
                "/api/app/v1/discovery?q=0344100006426000005&organization=foreign&actor=attacker",
                headers={**headers, "X-Organization": "foreign", "X-Actor": "attacker"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(provider.seen), 1)
            self.assertEqual(provider.seen[0].organization, resolver.organization)
            self.assertEqual(provider.seen[0].actor, resolver.actor)
            serialized = json.dumps(response.json(), ensure_ascii=False)
            self.assertNotIn("foreign", serialized)
            self.assertNotIn("attacker", serialized)
            self.assertNotIn(F1_SUBJECT, serialized)
        finally:
            client.close()
            temp.cleanup()

    def test_object_endpoint_revalidates_current_context_and_unknown_reference_is_generic(self) -> None:
        temp, client, resolver, provider, headers = self._client()
        try:
            object_id = provider.source.items[0].object_id
            response = client.get(f"/api/app/v1/objects/{object_id}", headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["technical"]["version_identity"], F1_VERSION)
            resolver.denied = True
            denied = client.get(f"/api/app/v1/objects/{object_id}", headers=headers)
            self.assertEqual(denied.status_code, 403)
            self.assertEqual(denied.json()["detail"], "ACCESS_DENIED")
        finally:
            client.close()
            temp.cleanup()

    def test_malformed_kind_is_rejected_without_source_disclosure(self) -> None:
        temp, client, _, _, headers = self._client()
        try:
            response = client.get("/api/app/v1/discovery?kind=secret-type", headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["detail"], "DISCOVERY_QUERY_INVALID")
        finally:
            client.close()
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
