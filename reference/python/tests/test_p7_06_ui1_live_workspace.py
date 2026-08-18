from __future__ import annotations

import hashlib
import http.client
import json
import os
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.identity import Identity

import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_06_ui1_live_workspace as ui1


RELEASE = "a" * 40


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class P706UI1LiveWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "runtime"
        self.org = Identity("organization", "org-ui1", "platform")
        self.human = Identity("principal", "owner-ui1", self.org.value)
        self.service = Identity("principal", "service-ui1", self.org.value)

        p704.initialize_access_store(self.root, self.org)
        p704.register_principal(self.root, self.human, kind="human")
        p704.register_principal(self.root, self.service, kind="service")
        self.issued = p704.issue_credential(self.root, self.human)
        self.credential_id = self.issued["credential_id"]
        self.credential_file = Path(self.issued["secret_path"])
        self.grant_id = p704.grant_access(
            self.root,
            self.human,
            operation=ui1.WORKSPACE_OPERATION,
            resource=ui1.WORKSPACE_RESOURCE,
            access_paths=("local",),
        )

        self.item_id = p703.persist_governed_item(
            self.root,
            RELEASE,
            b'{"live":"governed"}',
            {
                "state_class": "canonical-governed-state",
                "organization_scope": p703.ORGANIZATION_SCOPE,
                "semantic_type": "execution-context",
                "schema_version": "1.0.0",
                "classification": "internal",
                "retention_policy_ref": "retention:ui1",
                "source_release_sha": RELEASE,
                "subject_identity": "subject-live-001",
                "version_identity": "version-live-001",
                "authority_mode": "Native",
                "authority_scope": "org-ui1",
                "authoritative_source": "native-governed-store",
                "governed_admission_ref": "admission:ui1-001",
                "provenance_refs": ["event:ui1-001"],
                "lifecycle_status": "effective",
                "validation_status": "validated",
                "canonical_authority": True,
                "contains_reusable_secret": False,
            },
        )
        self.fixture_id = p703.persist_governed_item(
            self.root,
            RELEASE,
            b'{"fixture":true}',
            {
                "state_class": "governed-test-fixture",
                "organization_scope": p703.ORGANIZATION_SCOPE,
                "semantic_type": "fixture-only",
                "schema_version": "1.0.0",
                "classification": "test",
                "retention_policy_ref": "retention:test",
                "source_release_sha": RELEASE,
                "canonical_authority": False,
                "contains_reusable_secret": False,
            },
        )
        p703.create_checkpoint(
            self.root,
            RELEASE,
            execution_subject_identity="execution-subject-ui1",
            execution_version_identity="execution-version-ui1",
            governed_storage_item_ids=(self.item_id,),
            classification="internal",
            retention_policy_ref="retention:ui1",
            reason="UI1 recovery evidence",
        )

        health = {
            "schema": "arvectum.p7_02.runtime-health/1",
            "classification": "non-canonical operational telemetry",
            "operating_mode": "Persistent Internal / owner-operated",
            "organization_scope": p703.ORGANIZATION_SCOPE,
            "operating_role": "Arvectum OS Owner-Operator",
            "network_listener_mode": "none",
            "product_effects_enabled": False,
            "canonical_state_written": False,
            "release_sha": RELEASE,
            "instance_id": "ui1-test-runtime",
            "previous_instance_id": None,
            "generation": 1,
            "pid": os.getpid(),
            "started_at": _now(),
            "heartbeat_at": _now(),
            "state": "healthy",
            "semantic_imports_ok": True,
            "semantic_modules": [],
            "python_version": "test",
            "platform_system": "test",
        }
        health_path = self.root / "run" / "health.json"
        health_path.parent.mkdir(parents=True, exist_ok=True)
        health_path.write_text(json.dumps(health), encoding="utf-8")
        if os.name != "nt":
            health_path.chmod(0o600)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _snapshot(self) -> ui1.LiveWorkspaceSnapshot:
        with patch.object(ui1, "_verify_exact_release", return_value=RELEASE):
            return ui1.build_live_snapshot(
                self.root,
                organization=self.org,
                principal=self.human,
                credential_id=self.credential_id,
                credential_file=self.credential_file,
            )

    def _content_digest(self) -> str:
        digest = hashlib.sha256()
        for path in sorted(self.root.rglob("*"), key=lambda value: str(value)):
            rel = path.relative_to(self.root).as_posix()
            digest.update(rel.encode())
            if path.is_symlink():
                digest.update(b"SYMLINK")
                digest.update(os.readlink(path).encode())
            elif path.is_file():
                digest.update(path.read_bytes())
        return digest.hexdigest()

    def test_authorized_snapshot_is_live_read_only_and_excludes_fixtures(self) -> None:
        before = self._content_digest()
        snapshot = self._snapshot()
        after = self._content_digest()

        self.assertEqual(before, after)
        self.assertEqual(snapshot.organization_id, self.org.value)
        self.assertEqual(snapshot.actor_id, self.human.value)
        self.assertEqual(snapshot.release_sha, RELEASE)
        self.assertEqual(snapshot.health_state, "healthy")
        self.assertEqual(snapshot.access_grant_id, self.grant_id)
        self.assertEqual(len(snapshot.items), 1)
        self.assertEqual(snapshot.items[0].subject_identity, "subject-live-001")
        self.assertEqual(snapshot.items[0].version_identity, "version-live-001")
        self.assertEqual(len(snapshot.checkpoints), 1)
        rendered = ui1.render_live_workspace_html(snapshot)
        self.assertIn("subject-live-001", rendered)
        self.assertIn("version-live-001", rendered)
        self.assertNotIn("fixture-only", rendered)
        self.assertNotIn(self.fixture_id, rendered)

    def test_all_required_information_architecture_surfaces_are_renderable(self) -> None:
        snapshot = self._snapshot()
        for destination in ui1.WORKSPACE_DESTINATIONS:
            with self.subTest(destination=destination):
                html = ui1.render_live_workspace_html(
                    snapshot, destination=destination
                )
                self.assertIn(f"<h2>{destination.value}</h2>", html)
                self.assertIn("Organization:", html)
                self.assertIn("Actor:", html)
                self.assertIn("Exact runtime release:", html)
                self.assertIn("Subject", html)
                self.assertIn("Exact Version", html)

        evidence = ui1.render_live_workspace_html(
            snapshot, destination=ui1.WorkspaceDestination.EVIDENCE
        )
        self.assertIn("admission:ui1-001", evidence)
        self.assertIn("event:ui1-001", evidence)
        self.assertIn("Non-authoritative recovery state", evidence)

    def test_missing_optional_authority_lifecycle_validation_is_not_inferred(self) -> None:
        minimal_id = p703.persist_governed_item(
            self.root,
            RELEASE,
            b"minimal",
            {
                "state_class": "canonical-governed-state",
                "organization_scope": p703.ORGANIZATION_SCOPE,
                "semantic_type": "canonical-record",
                "schema_version": "1",
                "classification": "internal",
                "retention_policy_ref": "retention:minimal",
                "source_release_sha": RELEASE,
                "subject_identity": "subject-minimal",
                "version_identity": "version-minimal",
                "authority_mode": "External Reference",
                "authority_scope": "external:registry",
                "governed_admission_ref": "admission:minimal",
                "provenance_refs": ["external:source"],
                "canonical_authority": True,
                "contains_reusable_secret": False,
            },
        )
        snapshot = self._snapshot()
        self.assertTrue(any(item.storage_item_id == minimal_id for item in snapshot.items))
        html = ui1.render_live_workspace_html(
            snapshot, destination=ui1.WorkspaceDestination.RECORDS
        )
        self.assertIn("Authoritative source: not declared in retained metadata", html)
        self.assertIn("Lifecycle: not declared in retained metadata", html)
        self.assertIn("Validation: not declared in retained metadata", html)

    def test_wrong_or_unresolved_organization_fails_before_governed_state_read(self) -> None:
        other_org = Identity("organization", "other-org", "platform")
        other_principal = Identity("principal", self.human.value, other_org.value)
        with patch.object(
            ui1, "_live_items", side_effect=AssertionError("must not read governed state")
        ):
            with self.assertRaises(ui1.UI1AccessDenied):
                ui1.build_live_snapshot(
                    self.root,
                    organization=other_org,
                    principal=other_principal,
                    credential_id=self.credential_id,
                    credential_file=self.credential_file,
                )

    def test_missing_grant_fails_before_governed_state_read(self) -> None:
        p704.revoke_grant(self.root, self.grant_id)
        with patch.object(
            ui1, "_live_items", side_effect=AssertionError("must not read governed state")
        ):
            with self.assertRaises(ui1.UI1AccessDenied):
                ui1.build_live_snapshot(
                    self.root,
                    organization=self.org,
                    principal=self.human,
                    credential_id=self.credential_id,
                    credential_file=self.credential_file,
                )

    def test_service_principal_is_not_accepted_for_ui1_human_operator_scope(self) -> None:
        service_issued = p704.issue_credential(self.root, self.service)
        p704.grant_access(
            self.root,
            self.service,
            operation=ui1.WORKSPACE_OPERATION,
            resource=ui1.WORKSPACE_RESOURCE,
            access_paths=("local",),
        )
        with self.assertRaises(ui1.UI1AccessDenied):
            ui1.build_live_snapshot(
                self.root,
                organization=self.org,
                principal=self.service,
                credential_id=service_issued["credential_id"],
                credential_file=Path(service_issued["secret_path"]),
            )

    def test_runtime_release_mismatch_fails_closed_without_governed_content(self) -> None:
        with patch.object(ui1, "_verify_exact_release", return_value="b" * 40):
            with patch.object(
                ui1, "_live_items", side_effect=AssertionError("must not read governed state")
            ):
                with self.assertRaises(ui1.UI1IntegrityError):
                    ui1.build_live_snapshot(
                        self.root,
                        organization=self.org,
                        principal=self.human,
                        credential_id=self.credential_id,
                        credential_file=self.credential_file,
                    )

    def test_server_is_loopback_only_get_head_only_and_reauthorizes_each_request(self) -> None:
        with patch.object(ui1, "_verify_exact_release", return_value=RELEASE):
            server = ui1.make_server(
                host="127.0.0.1",
                port=0,
                root=self.root,
                organization=self.org,
                principal=self.human,
                credential_id=self.credential_id,
                credential_file=self.credential_file,
            )
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            host, port = server.server_address[:2]
            try:
                connection = http.client.HTTPConnection(host, port, timeout=5)
                connection.request("GET", "/?view=records")
                response = connection.getresponse()
                body = response.read().decode()
                self.assertEqual(response.status, 200)
                self.assertIn("subject-live-001", body)
                self.assertEqual(response.getheader("Cache-Control"), "no-store, max-age=0")
                self.assertIn("default-src 'none'", response.getheader("Content-Security-Policy"))

                connection.request("POST", "/", body=b"mutation")
                response = connection.getresponse()
                body = response.read().decode()
                self.assertEqual(response.status, 405)
                self.assertNotIn("subject-live-001", body)

                p704.revoke_grant(self.root, self.grant_id)
                connection.request("GET", "/?view=records")
                response = connection.getresponse()
                body = response.read().decode()
                self.assertEqual(response.status, 403)
                self.assertIn("Governed content, protected counts", body)
                self.assertNotIn("subject-live-001", body)
                self.assertNotIn("version-live-001", body)
                connection.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

    def test_non_loopback_bind_is_rejected(self) -> None:
        for host in ("0.0.0.0", "192.0.2.10", "localhost", "::1"):
            with self.subTest(host=host):
                with self.assertRaises(ui1.UI1BoundaryError):
                    ui1._verify_loopback_host(host)

    def test_source_contains_no_ui1_governed_mutation_or_external_effect_path(self) -> None:
        source = Path(ui1.__file__).read_text(encoding="utf-8")
        forbidden_calls = (
            "persist_governed_item(",
            "create_checkpoint(",
            "record_transaction(",
            "grant_access(",
            "revoke_grant(",
            "issue_credential(",
            "rotate_credential(",
            "emit_telemetry(",
            "operational_status(",
        )
        for token in forbidden_calls:
            with self.subTest(token=token):
                self.assertNotIn(token, source)
        for token in ("do_POST = _reject_mutation", "do_PUT = _reject_mutation",
                      "do_PATCH = _reject_mutation", "do_DELETE = _reject_mutation"):
            self.assertIn(token, source)


if __name__ == "__main__":
    unittest.main()
