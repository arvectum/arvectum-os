import json
import os
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from arvectum_os_ref.identity import Identity
import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_05_operational_visibility as p705


SHA = "a" * 40


class P705OperationalVisibilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "runtime"
        self.root.mkdir(mode=0o700)
        (self.root / "run").mkdir(mode=0o700)
        self.health_path = self.root / "run" / "health.json"
        self.write_health()

    def tearDown(self):
        self.tmp.cleanup()

    def write_health(self, *, state="healthy", heartbeat_at=None, pid=None):
        payload = {
            "schema": "arvectum.p7_02.runtime-health/1",
            "classification": "non-canonical operational telemetry",
            "release_sha": SHA,
            "pid": os.getpid() if pid is None else pid,
            "heartbeat_at": heartbeat_at or p705._utc_now(),
            "state": state,
            "network_listener_mode": "none",
            "product_effects_enabled": False,
            "canonical_state_written": False,
        }
        self.health_path.write_text(json.dumps(payload), encoding="utf-8")
        if os.name != "nt":
            self.health_path.chmod(0o600)

    def test_health_distinguishes_healthy_degraded_down_and_action(self):
        healthy = p705.classify_health(self.root)
        self.assertEqual(healthy.state, "healthy")
        self.assertIn("no operator action", healthy.action)

        future = (p705._utc_now_dt() + timedelta(seconds=30)).isoformat().replace("+00:00", "Z")
        self.write_health(heartbeat_at=future)
        degraded = p705.classify_health(self.root)
        self.assertEqual((degraded.state, degraded.code), ("degraded", "CLOCK_SKEW"))
        self.assertTrue(degraded.action)

        stale = (p705._utc_now_dt() - timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
        self.write_health(heartbeat_at=stale)
        down = p705.classify_health(self.root, max_age_seconds=20)
        self.assertEqual((down.state, down.code), ("down", "HEARTBEAT_STALE"))
        self.assertIn("restart", down.action)

    def test_structured_logging_is_noncanonical_owner_only_and_minimized(self):
        record = p705.emit_telemetry(
            self.root, event="runtime.observed",
            attributes={"component": "p7-02", "status": "healthy", "count": 1},
        )
        self.assertFalse(record["canonical_authority"])
        log = self.root / "logs" / "p7-05" / "telemetry.jsonl"
        line = json.loads(log.read_text(encoding="utf-8").strip())
        self.assertEqual(line["schema"], p705.TELEMETRY_SCHEMA)
        self.assertEqual(line["attributes"]["status"], "healthy")
        if os.name != "nt":
            self.assertEqual(log.stat().st_mode & 0o777, 0o600)

        with self.assertRaises(p705.BoundaryError):
            p705.emit_telemetry(self.root, event="bad", attributes={"token": "do-not-log"})
        with self.assertRaises(p705.BoundaryError):
            p705.emit_telemetry(self.root, event="bad", attributes={"payload": "business data"})
        with self.assertRaises(p705.BoundaryError):
            p705.emit_telemetry(self.root, event="bad", attributes={"free_text": "not allow-listed"})

    def test_alert_is_actionable_noncanonical_and_cleared_by_healthy_status(self):
        degraded = p705.HealthStatus(
            "degraded", "TEST_DEGRADED", "proof condition", "inspect the runtime", SHA, 2.0
        )
        alert = p705.publish_health_signal(self.root, degraded)
        self.assertIsNotNone(alert)
        self.assertFalse(alert["canonical_authority"])
        self.assertEqual(alert["operator_action"], "inspect the runtime")
        self.assertTrue((self.root / "run" / "p7-05-alert.json").exists())

        healthy = p705.HealthStatus("healthy", "OK", "healthy", "no operator action required", SHA, 1.0)
        self.assertIsNone(p705.publish_health_signal(self.root, healthy))
        self.assertFalse((self.root / "run" / "p7-05-alert.json").exists())

    def _authorized_audit_decision(self):
        org = Identity("organization", "org-arvectum", "platform")
        human = Identity("principal", "owner", org.value)
        p704.initialize_access_store(self.root, org)
        p704.register_principal(self.root, human, kind="human")
        issued = p704.issue_credential(self.root, human)
        secret = p704.read_credential_secret(Path(issued["secret_path"]))
        p704.grant_access(
            self.root, human, operation="audit.inspect", resource="state:governed",
            access_paths=("local",),
        )
        decision = p704.authorize(
            self.root, organization=org, principal=human,
            credential_id=issued["credential_id"], credential_secret=secret,
            operation="audit.inspect", resource="state:governed", access_path="local",
        )
        return decision

    def test_audit_visibility_requires_exact_access_and_never_copies_payload(self):
        p703.persist_governed_item(
            self.root, SHA, b'{"material":"audit-body-must-not-be-copied"}',
            {
                "state_class": "canonical-governed-state",
                "organization_scope": p703.ORGANIZATION_SCOPE,
                "semantic_type": "Event",
                "schema_version": "1",
                "classification": "internal audit",
                "retention_policy_ref": "test-retention",
                "source_release_sha": SHA,
                "subject_identity": "event:test-1",
                "version_identity": "event:test-1:v1",
                "authority_mode": "Native",
                "authority_scope": "test",
                "governed_admission_ref": "execution:test",
                "provenance_refs": ["test:source"],
                "canonical_authority": True,
                "contains_reusable_secret": False,
            },
        )
        decision = self._authorized_audit_decision()
        projection = p705.audit_visibility(self.root, decision)
        self.assertEqual(projection["count"], 1)
        self.assertFalse(projection["payload_bytes_exposed"])
        self.assertNotIn("audit-body-must-not-be-copied", json.dumps(projection))
        self.assertEqual(projection["items"][0]["semantic_type"], "Event")

        denied = p704.AccessDecision(
            False, "NO_EXPLICIT_GRANT", decision.organization, decision.principal,
            decision.principal_kind, decision.credential_id, None,
            "audit.inspect", "state:governed", "local",
        )
        with self.assertRaises(p705.BoundaryError):
            p705.audit_visibility(self.root, denied)

    def test_retention_cleanup_removes_old_telemetry_and_preserves_governed_and_evidence(self):
        protected = self.root / "state" / "governed" / "sentinel.bin"
        protected.parent.mkdir(parents=True, mode=0o700)
        protected.write_bytes(b"canonical-or-governed-sentinel")
        evidence = self.root / "evidence" / "audit.json"
        evidence.parent.mkdir(mode=0o700)
        evidence.write_text('{"keep":true}', encoding="utf-8")
        old = (p705._utc_now_dt() - timedelta(hours=p705.DEFAULT_RETENTION_HOURS + 1)).isoformat().replace("+00:00", "Z")
        p705.emit_telemetry(self.root, event="old", recorded_at=old, attributes={"status": "old"})
        p705.emit_telemetry(self.root, event="new", attributes={"status": "new"})

        result = p705.cleanup(self.root)
        self.assertEqual(result["removed_telemetry_records"], 1)
        self.assertEqual(result["kept_telemetry_records"], 1)
        self.assertEqual(protected.read_bytes(), b"canonical-or-governed-sentinel")
        self.assertEqual(evidence.read_text(encoding="utf-8"), '{"keep":true}')
        self.assertFalse(result["canonical_state_deleted"])
        self.assertFalse(result["evidence_deleted"])

    def test_tampered_policy_cannot_expand_cleanup_or_canonical_authority(self):
        policy = p705.initialize(self.root)
        path = self.root / "config" / "p7-05-retention.json"
        policy["telemetry_authority"] = "canonical"
        path.write_text(json.dumps(policy), encoding="utf-8")
        if os.name != "nt":
            path.chmod(0o600)
        with self.assertRaises(p705.IntegrityError):
            p705.load_policy(self.root)


if __name__ == "__main__":
    unittest.main()
