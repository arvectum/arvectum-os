from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
import p7_06_ui4_owner_preflight as ui4
from workspace_app.access import AccessContext
from workspace_app.config import WorkspaceSettings
from workspace_app.governed import (
    GovernedExperienceError,
    GovernedExperienceProjection,
    GovernedGateView,
    GovernedPreflightResult,
    RuntimeGovernedExperienceProvider,
    project_owner_preflight,
)
from workspace_app.main import CSRF_HEADER, RELEASE_HEADER, create_app
from workspace_app.release import load_release


def real_shape_preflight(*, outcome: str = "Waiting", gate_state: str = "Waiting") -> ui4.UI4OwnerPreflight:
    gates = tuple(
        ui4.UI4GateView(name, gate_state, f"{name} basis from governed evidence")
        for name in ("Authorization", "Organizational Authority", "Data Governance", "Consequential Approval")
    )
    return ui4.UI4OwnerPreflight(
        release_sha="a" * 40,
        organization_id="organization:org-a [platform]",
        actor_id="principal:owner [org-a]",
        storage_item_id="storage-real-eis",
        subject_identity="document-subject/eis-real",
        version_identity="document-version/eis-real-v1",
        semantic_type="platform.document",
        authority_mode="External Reference",
        authority_scope="EIS exact notice attachment evidence",
        authoritative_source="ЕИС / zakupki.gov.ru",
        execution_subject="execution-subject/eis-real",
        execution_version="execution-version/eis-real-v5",
        event_version="event-version/eis-real-v1",
        checkpoint_id="checkpoint-real",
        provenance_refs=("execution-version/eis-real-v5", "event-version/eis-real-v1"),
        validation_status="CAP-004 reconstruction complete",
        gates=gates,
        outcome=outcome,
    )


class GovernedProjectionTests(unittest.TestCase):
    def test_real_preflight_projects_human_context_and_four_independent_decisions(self) -> None:
        payload = project_owner_preflight(real_shape_preflight()).to_payload()
        self.assertEqual(payload["schema"], "arvectum.workspace.governed-experience/1")
        self.assertEqual(payload["presentation"]["source"], "ЕИС / zakupki.gov.ru")
        self.assertEqual(payload["presentation"]["authority_mode"], "External Reference")
        self.assertEqual(payload["execution"]["status"], "Waiting")
        self.assertEqual(
            payload["execution"]["waiting_decisions"],
            ["Authorization", "Organizational Authority", "Data Governance", "Consequential Approval"],
        )
        self.assertEqual([row["state"] for row in payload["decisions"]], ["Waiting"] * 4)
        self.assertFalse(payload["action"]["consequential"])
        self.assertFalse(payload["action"]["authority_provided"])
        self.assertFalse(payload["scope"]["visibility_implies_permission"])
        self.assertEqual(payload["technical"]["execution_version"], "execution-version/eis-real-v5")

    def test_runtime_action_rebuilds_preflight_and_records_only_existing_noncanonical_receipt(self) -> None:
        access = AccessContext(
            organization=Identity("organization", "org-a", "platform"),
            actor=Identity("principal", "owner", "org-a"),
            principal_kind="human",
            credential_id="credential-a",
            grant_id="grant-a",
        )
        provider = RuntimeGovernedExperienceProvider(Path("/runtime"))
        preflight = real_shape_preflight()
        receipt = ui4.UI4EvidenceReceipt(Path("/runtime/evidence/preflight.json"), "b" * 64, preflight)
        with patch.object(ui4, "build_owner_preflight", return_value=preflight) as build, patch.object(
            ui4, "record_browser_preflight", return_value=receipt
        ) as record:
            result = provider.run_preflight(access).to_payload()
        self.assertEqual(result["outcome"], "Waiting")
        self.assertFalse(result["canonical_mutation_requested"])
        self.assertFalse(result["canonical_mutation_performed"])
        self.assertFalse(result["external_effect_requested"])
        self.assertFalse(result["organizational_authority_provided"])
        self.assertEqual(result["evidence"]["sha256"], "b" * 64)
        build.assert_called_once()
        record.assert_called_once_with(Path("/runtime"), preflight)

    def test_non_waiting_case_fails_closed_before_receipt_write(self) -> None:
        access = AccessContext(
            organization=Identity("organization", "org-a", "platform"),
            actor=Identity("principal", "owner", "org-a"),
            principal_kind="human",
            credential_id="credential-a",
            grant_id="grant-a",
        )
        provider = RuntimeGovernedExperienceProvider(Path("/runtime"))
        with patch.object(ui4, "build_owner_preflight", return_value=real_shape_preflight(outcome="Ready", gate_state="Allow")), patch.object(
            ui4, "record_browser_preflight"
        ) as record:
            with self.assertRaises(GovernedExperienceError):
                provider.run_preflight(access)
        record.assert_not_called()


class FakeResolver:
    def __init__(self) -> None:
        self.organization = Identity("organization", "org-a", "platform")
        self.actor = Identity("principal", "owner", "org-a")
        self.calls = 0

    def authorize(self) -> AccessContext:
        self.calls += 1
        return AccessContext(
            organization=self.organization,
            actor=self.actor,
            principal_kind="human",
            credential_id="credential-a",
            grant_id="grant-a",
        )


class FakeGovernedProvider:
    def __init__(self) -> None:
        self.inspections = 0
        self.runs = 0

    def inspect(self, access: AccessContext) -> GovernedExperienceProjection:
        self.inspections += 1
        return GovernedExperienceProjection(
            generated_at="2026-08-21T12:00:00Z",
            release_sha="a" * 40,
            source="ЕИС / zakupki.gov.ru",
            authority_mode="External Reference",
            authority_scope="EIS exact notice attachment evidence",
            validation_status="CAP-004 reconstruction complete",
            execution_subject="execution-subject/eis-real",
            execution_version="execution-version/eis-real-v5",
            event_version="event-version/eis-real-v1",
            source_subject="document-subject/eis-real",
            source_version="document-version/eis-real-v1",
            checkpoint_id="checkpoint-real",
            provenance_refs=("event-version/eis-real-v1",),
            gates=tuple(
                GovernedGateView(name, "Waiting", f"{name} remains independently unresolved")
                for name in ("Authorization", "Organizational Authority", "Data Governance", "Consequential Approval")
            ),
            outcome="Waiting",
        )

    def run_preflight(self, access: AccessContext) -> GovernedPreflightResult:
        self.runs += 1
        return GovernedPreflightResult("2026-08-21T12:01:00Z", "Waiting", "b" * 64)


def app_settings(root: Path) -> WorkspaceSettings:
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


class GovernedBffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        static = root / "dist"
        static.mkdir()
        (static / "index.html").write_text("<!doctype html><div id='root'></div>", encoding="utf-8")
        self.resolver = FakeResolver()
        self.provider = FakeGovernedProvider()
        app = create_app(
            app_settings(root),
            access_resolver=self.resolver,
            governed_provider=self.provider,
            static_dir=static,
        )
        self.client = TestClient(app, base_url="http://127.0.0.1:8769", client=("127.0.0.1", 50000))
        self.release = load_release().release_id
        self.headers = {RELEASE_HEADER: self.release}
        response = self.client.post(
            "/api/app/v1/session/bootstrap",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(response.status_code, 200)
        self.csrf = response.json()["session"]["csrf_token"]

    def tearDown(self) -> None:
        self.client.close()
        self.temp.cleanup()

    def test_get_is_server_authorized_and_non_authoritative(self) -> None:
        response = self.client.get("/api/app/v1/governed", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["execution"]["status"], "Waiting")
        self.assertFalse(payload["scope"]["organizational_authority_provided"])
        self.assertEqual(self.provider.inspections, 1)
        self.assertGreaterEqual(self.resolver.calls, 2)

    def test_post_requires_origin_csrf_and_fresh_server_authorization(self) -> None:
        missing_csrf = self.client.post(
            "/api/app/v1/governed/preflight",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(missing_csrf.status_code, 403)
        self.assertEqual(self.provider.runs, 0)

        wrong_origin = self.client.post(
            "/api/app/v1/governed/preflight",
            headers={**self.headers, CSRF_HEADER: self.csrf, "Origin": "https://attacker.invalid"},
        )
        self.assertEqual(wrong_origin.status_code, 403)
        self.assertEqual(self.provider.runs, 0)

        before = self.resolver.calls
        valid = self.client.post(
            "/api/app/v1/governed/preflight",
            headers={**self.headers, CSRF_HEADER: self.csrf, "Origin": "http://127.0.0.1:8769"},
            json={"approval": True, "authority": "browser-must-not-be-consumed"},
        )
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.json()["outcome"], "Waiting")
        self.assertFalse(valid.json()["canonical_mutation_performed"])
        self.assertEqual(self.provider.runs, 1)
        self.assertGreater(self.resolver.calls, before)


if __name__ == "__main__":
    unittest.main()
