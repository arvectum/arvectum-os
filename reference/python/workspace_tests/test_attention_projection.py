from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
import p7_05_operational_visibility as p705
import p7_06_ui4_owner_preflight as ui4
from workspace_app.access import AccessContext, WorkspaceAccessError
from workspace_app.attention import (
    AttentionItem,
    AttentionKind,
    AttentionProjection,
    AttentionProjectionError,
    AttentionUrgency,
    ProjectionFreshness,
    ProjectionHealth,
    RuntimeAttentionProvider,
    scenario_item,
)
from workspace_app.config import WorkspaceSettings
from workspace_app.main import RELEASE_HEADER, create_app
from workspace_app.release import load_release


class FakeResolver:
    def __init__(self) -> None:
        self.denied = False
        self.organization = Identity("organization", "org-a", "platform")
        self.actor = Identity("principal", "actor-a", "org-a")

    def authorize(self) -> AccessContext:
        if self.denied:
            raise WorkspaceAccessError("revoked for test")
        return AccessContext(
            organization=self.organization,
            actor=self.actor,
            principal_kind="human",
            credential_id="credential-test",
            grant_id="grant-test",
        )


class FakeProvider:
    def __init__(self, projection: AttentionProjection) -> None:
        self.projection = projection
        self.seen: list[AccessContext] = []

    def project(self, access: AccessContext) -> AttentionProjection:
        self.seen.append(access)
        return self.projection


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


def _fresh_projection(*items: AttentionItem) -> AttentionProjection:
    return AttentionProjection(
        generated_at="2026-08-21T10:00:00Z",
        health=ProjectionHealth(
            ProjectionFreshness.FRESH,
            "OK",
            "Attention sources were evaluated against current governed state.",
            "2026-08-21T10:00:00Z",
            1.5,
        ),
        items=tuple(items),
    )


class AttentionContractTests(unittest.TestCase):
    def test_normalized_attention_kinds_cover_j1_without_implying_authority(self) -> None:
        kinds = (
            AttentionKind.WAITING_APPROVAL,
            AttentionKind.WAITING_INPUT,
            AttentionKind.RECONCILIATION_REQUIRED,
            AttentionKind.GUARDED_ACTION_FAILED,
            AttentionKind.RECOVERABLE_SYSTEM_CONDITION,
            AttentionKind.RECENT_OUTCOME,
            AttentionKind.INFORMATIONAL,
        )
        items = tuple(
            scenario_item(
                source_fingerprint=kind.value,
                kind=kind,
                urgency=AttentionUrgency.MEDIUM,
                title=f"Scenario {kind.value}",
                reason="Controlled acceptance reason.",
                source_label="P9.04 controlled acceptance fixture",
                next_step="Inspect the source context only.",
                observed_at="2026-08-21T10:00:00Z",
            )
            for kind in kinds
        )
        payload = _fresh_projection(*items).to_payload()
        self.assertEqual(len(payload["items"]), len(kinds))
        serialized = json.dumps(payload)
        self.assertIn('"evidence_mode": "scenario"', serialized)
        self.assertIn('"interaction": "inspect-only"', serialized)
        self.assertIn('"canonical_authority": false', serialized)
        self.assertIn('"organizational_authority_provided": false', serialized)
        self.assertIn('"visibility_implies_permission": false', serialized)

    def test_item_deep_link_is_bounded_and_opaque(self) -> None:
        item = scenario_item(
            source_fingerprint="raw/execution/version?secret=1",
            kind=AttentionKind.WAITING_INPUT,
            urgency=AttentionUrgency.HIGH,
            title="Input required",
            reason="A governed input is missing.",
            source_label="Controlled scenario",
            next_step="Inspect the blocker.",
        )
        payload = item.to_payload()
        self.assertRegex(item.attention_id, r"^[0-9a-f]{20}$")
        self.assertEqual(payload["open_href"], f"/my-work?focus={item.attention_id}")
        self.assertNotIn("execution", json.dumps(payload))
        self.assertFalse(payload["authority_provided"])

    def test_duplicate_attention_ids_fail_closed(self) -> None:
        item = scenario_item(
            source_fingerprint="same",
            kind=AttentionKind.INFORMATIONAL,
            urgency=AttentionUrgency.LOW,
            title="Information",
            reason="Informational projection.",
            source_label="Controlled scenario",
            next_step="No action required.",
        )
        with self.assertRaises(AttentionProjectionError):
            _fresh_projection(item, item)


class RuntimeAttentionProviderTests(unittest.TestCase):
    def test_stale_runtime_withholds_work_items_and_surfaces_recoverable_condition(self) -> None:
        calls = {"preflight": 0}

        def health(_: Path) -> p705.HealthStatus:
            return p705.HealthStatus("down", "HEARTBEAT_STALE", "secret diagnostic", "restart", "sha", 120.0)

        def preflight(*args, **kwargs):  # type: ignore[no-untyped-def]
            calls["preflight"] += 1
            raise AssertionError("stale projection must not inspect protected work sources")

        provider = RuntimeAttentionProvider(Path("/tmp/runtime"), health_reader=health, preflight_builder=preflight)
        access = AccessContext(
            Identity("organization", "org-a", "platform"),
            Identity("principal", "actor-a", "org-a"),
            "human",
            "cred",
            "grant",
        )
        payload = provider.project(access).to_payload()
        self.assertEqual(calls["preflight"], 0)
        self.assertEqual(payload["health"]["state"], "stale")
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual(payload["items"][0]["kind"], "recoverable-system-condition")
        self.assertNotIn("secret diagnostic", json.dumps(payload))

    def test_source_denial_is_minimized_to_no_visible_item(self) -> None:
        def health(_: Path) -> p705.HealthStatus:
            return p705.HealthStatus("healthy", "OK", "healthy", "none", "sha", 1.0)

        def denied(*args, **kwargs):  # type: ignore[no-untyped-def]
            raise ui4.ui2.UI2AccessDenied("protected object exists but is denied")

        provider = RuntimeAttentionProvider(Path("/tmp/runtime"), health_reader=health, preflight_builder=denied)
        access = AccessContext(
            Identity("organization", "org-a", "platform"),
            Identity("principal", "actor-a", "org-a"),
            "human",
            "cred",
            "grant",
        )
        payload = provider.project(access).to_payload()
        self.assertEqual(payload["health"]["state"], "fresh")
        self.assertEqual(payload["items"], [])
        self.assertNotIn("protected object exists", json.dumps(payload))

    def test_real_ui4_waiting_state_becomes_live_waiting_input_without_raw_identity(self) -> None:
        def health(_: Path) -> p705.HealthStatus:
            return p705.HealthStatus("healthy", "OK", "healthy", "none", "sha", 1.0)

        preflight = ui4.UI4OwnerPreflight(
            release_sha="release-secret",
            organization_id="org-secret",
            actor_id="actor-secret",
            storage_item_id="storage-secret",
            subject_identity="document-subject/secret",
            version_identity="document-version/secret",
            semantic_type="platform.document",
            authority_mode="External Reference",
            authority_scope="EIS notice",
            authoritative_source="ЕИС / zakupki.gov.ru",
            execution_subject="execution-secret",
            execution_version="execution-version-secret",
            event_version="event-version-secret",
            checkpoint_id="checkpoint-secret",
            provenance_refs=("execution-secret", "event-version-secret"),
            validation_status="CAP-004 reconstruction complete",
            gates=(
                ui4.UI4GateView("Authorization", "Waiting", "missing"),
                ui4.UI4GateView("Organizational Authority", "Waiting", "missing"),
                ui4.UI4GateView("Data Governance", "Waiting", "missing"),
                ui4.UI4GateView("Consequential Approval", "Waiting", "missing"),
            ),
        )
        provider = RuntimeAttentionProvider(Path("/tmp/runtime"), health_reader=health, preflight_builder=lambda *a, **k: preflight)
        access = AccessContext(
            Identity("organization", "org-a", "platform"),
            Identity("principal", "actor-a", "org-a"),
            "human",
            "cred",
            "grant",
        )
        payload = provider.project(access).to_payload()
        self.assertEqual(payload["items"][0]["kind"], "waiting-input")
        self.assertEqual(payload["items"][0]["source"], "ЕИС / zakupki.gov.ru")
        self.assertEqual(payload["items"][0]["evidence_mode"], "live")
        serialized = json.dumps(payload)
        for forbidden in (
            "org-secret",
            "actor-secret",
            "storage-secret",
            "document-subject/secret",
            "document-version/secret",
            "execution-secret",
            "execution-version-secret",
            "event-version-secret",
            "checkpoint-secret",
            "release-secret",
        ):
            self.assertNotIn(forbidden, serialized)


class MyWorkBffTests(unittest.TestCase):
    def test_endpoint_uses_current_server_authorized_context_and_minimized_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            static = root / "dist"
            static.mkdir()
            (static / "index.html").write_text("<!doctype html><div id='root'></div>", encoding="utf-8")
            (static / "assets").mkdir()
            projection = _fresh_projection(
                scenario_item(
                    source_fingerprint="one",
                    kind=AttentionKind.RECONCILIATION_REQUIRED,
                    urgency=AttentionUrgency.HIGH,
                    title="External outcome is uncertain",
                    reason="Reconciliation is required before any retry.",
                    source_label="Controlled P8.05 scenario",
                    next_step="Reconcile the external outcome; do not retry blindly.",
                )
            )
            provider = FakeProvider(projection)
            resolver = FakeResolver()
            client = TestClient(
                create_app(
                    _settings(root),
                    access_resolver=resolver,
                    attention_provider=provider,
                    static_dir=static,
                ),
                base_url="http://127.0.0.1:8769",
                client=("127.0.0.1", 50000),
            )
            release = load_release().release_id
            headers = {RELEASE_HEADER: release}
            bootstrap = client.post(
                "/api/app/v1/session/bootstrap",
                headers={**headers, "Origin": "http://127.0.0.1:8769"},
            )
            self.assertEqual(bootstrap.status_code, 200)
            response = client.get(
                "/api/app/v1/my-work?organization=foreign&actor=attacker",
                headers={**headers, "X-Organization": "foreign", "X-Actor": "attacker"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(provider.seen), 1)
            self.assertEqual(provider.seen[0].organization, resolver.organization)
            self.assertEqual(provider.seen[0].actor, resolver.actor)
            payload = response.json()
            self.assertFalse(payload["projection"]["canonical_authority"])
            self.assertFalse(payload["projection"]["visibility_implies_permission"])
            self.assertFalse(payload["scope"]["denied_item_counts_exposed"])
            serialized = json.dumps(payload)
            self.assertNotIn("foreign", serialized)
            self.assertNotIn("attacker", serialized)
            self.assertNotIn("org-a", serialized)
            self.assertNotIn("actor-a", serialized)
            client.close()


if __name__ == "__main__":
    unittest.main()
