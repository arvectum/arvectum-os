import io
import json
import os
import shutil
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p7_03_durable_state as p703

TOOL_SHA = "a" * 40
SOURCE_SHA = "b" * 40
RUNTIME_SHA = "c" * 40


class P703DurableStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "runtime"

    def tearDown(self):
        self.tmp.cleanup()

    def metadata(self, *, canonical=True, source_sha=SOURCE_SHA):
        base = {
            "state_class": "canonical-governed-state" if canonical else "governed-test-fixture",
            "organization_scope": p703.ORGANIZATION_SCOPE,
            "semantic_type": "test.record",
            "schema_version": "1",
            "classification": "internal",
            "retention_policy_ref": "test-retention",
            "source_release_sha": source_sha,
            "canonical_authority": canonical,
            "contains_reusable_secret": False,
        }
        if canonical:
            base.update(
                subject_identity="subject:test",
                version_identity="version:test:1",
                authority_mode="Native",
                authority_scope="test",
                governed_admission_ref="execution:test:1",
                provenance_refs=["event:test:1"],
            )
        return base

    def write_runtime_health(self, *, state="healthy"):
        run = self.root / "run"
        run.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            run.chmod(0o700)
        health = {
            "release_sha": RUNTIME_SHA,
            "state": state,
            "canonical_state_written": False,
            "product_effects_enabled": False,
        }
        (run / "health.json").write_text(json.dumps(health), encoding="utf-8")
        if os.name != "nt":
            (run / "health.json").chmod(0o600)

    def test_init_separates_scope_and_records_exclusions(self):
        cfg = p703.initialize_store(self.root, TOOL_SHA)
        self.assertEqual(cfg["explicit_exclusions"], ["run/", "logs/", "cache/", "secrets/"])
        self.assertFalse(cfg["reusable_secrets_in_governed_backup"])
        self.assertEqual(p703.verify_store(self.root)["integrity"], "PASS")

    def test_persist_accepts_historical_source_release_and_is_immutable(self):
        item = p703.persist_governed_item(self.root, TOOL_SHA, b"governed", self.metadata())
        self.assertEqual(len(item), 64)
        item_dir = self.root / "state" / "governed" / "items" / item
        manifest = p703.verify_item(item_dir)
        self.assertEqual(manifest["metadata"]["source_release_sha"], SOURCE_SHA)
        self.assertEqual(p703.persist_governed_item(self.root, TOOL_SHA, b"governed", self.metadata()), item)
        (item_dir / "payload.bin").write_bytes(b"tampered")
        with self.assertRaises(p703.IntegrityError):
            p703.verify_store(self.root)

    def test_secret_declared_payload_is_refused(self):
        metadata = self.metadata()
        metadata["contains_reusable_secret"] = True
        with self.assertRaises(p703.BoundaryError):
            p703.persist_governed_item(self.root, TOOL_SHA, b"secret-ish", metadata)

    def test_checkpoint_is_non_authoritative_and_replay_safe(self):
        item = p703.persist_governed_item(self.root, TOOL_SHA, b"governed", self.metadata())
        checkpoint = p703.create_checkpoint(
            self.root,
            TOOL_SHA,
            execution_subject_identity="execution:test",
            execution_version_identity="execution:test:v1",
            governed_storage_item_ids=[item],
            classification="internal",
            retention_policy_ref="test-retention",
            reason="recovery point",
        )
        doc = p703.verify_checkpoint(self.root, self.root / "state" / "checkpoints" / f"{checkpoint}.json")
        self.assertFalse(doc["canonical_authority"])
        self.assertFalse(doc["external_effect_replay_authorized"])

    def test_backup_excludes_telemetry_cache_and_secrets_and_restores(self):
        item = p703.persist_governed_item(self.root, TOOL_SHA, b"governed", self.metadata())
        p703.create_checkpoint(
            self.root, TOOL_SHA,
            execution_subject_identity="execution:test",
            execution_version_identity="execution:test:v1",
            governed_storage_item_ids=[item],
            classification="internal",
            retention_policy_ref="test-retention",
            reason="recovery point",
        )
        for dirname in ("run", "logs", "cache", "secrets"):
            d = self.root / dirname
            d.mkdir(exist_ok=True)
            if os.name != "nt": d.chmod(0o700)
            f = d / "excluded.txt"
            f.write_text("must-not-back-up", encoding="utf-8")
            if os.name != "nt": f.chmod(0o600)
        archive, _ = p703.create_backup(self.root, TOOL_SHA)
        check = p703.verify_backup(archive)
        self.assertFalse(check["reusable_secrets_included"])
        with tarfile.open(archive, "r:gz") as tf:
            names = tf.getnames()
        self.assertFalse(any(n.startswith(("run/", "logs/", "cache/", "secrets/")) for n in names))
        restored = self.root / "evidence" / "isolated-restore"
        result = p703.restore_backup(archive, restored)
        self.assertEqual(result["integrity"], "PASS")
        self.assertEqual(p703._tree_digest(self.root / "state"), p703._tree_digest(restored / "state"))

    def test_backup_checksum_tamper_fails_closed(self):
        p703.initialize_store(self.root, TOOL_SHA)
        archive, _ = p703.create_backup(self.root, TOOL_SHA)
        with archive.open("ab") as handle:
            handle.write(b"tamper")
        with self.assertRaises(p703.IntegrityError):
            p703.verify_backup(archive)

    def test_restore_rejects_existing_target(self):
        p703.initialize_store(self.root, TOOL_SHA)
        archive, _ = p703.create_backup(self.root, TOOL_SHA)
        target = self.root / "evidence" / "existing"
        target.mkdir()
        if os.name != "nt": target.chmod(0o700)
        with self.assertRaises(p703.BoundaryError):
            p703.restore_backup(archive, target)

    def test_safe_member_rejects_traversal_and_backslash(self):
        for name in ("../escape", "/absolute", "..\\escape"):
            with self.assertRaises(p703.IntegrityError):
                p703._safe_member_name(name)

    def test_proof_does_not_add_fixture_to_live_governed_state(self):
        result = p703.run_proof(self.root, TOOL_SHA)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["live_store_before_backup"]["governed_items"], 0)
        self.assertEqual(p703.verify_store(self.root)["governed_items"], 0)
        self.assertTrue(result["tamper_detection_fail_closed"])
        self.assertTrue(result["explicit_exclusions_absent"])

    def test_selected_runtime_observation_is_recorded_and_can_be_required(self):
        self.write_runtime_health()
        result = p703.run_proof(self.root, TOOL_SHA, require_persistent_runtime=True)
        self.assertTrue(result["persistent_runtime_observed"])
        self.assertEqual(result["persistent_runtime_release_sha"], RUNTIME_SHA)
        backup = next((self.root / "backups").glob("*.tar.gz"))
        manifest, payloads = p703._read_backup_members(backup)
        cfg = json.loads(payloads["config/p7-03-recovery.json"])
        self.assertEqual(cfg["persistent_runtime_release_sha"], RUNTIME_SHA)

    def test_required_runtime_fails_closed_when_unobserved_or_unhealthy(self):
        with self.assertRaises(p703.IntegrityError):
            p703.run_proof(self.root, TOOL_SHA, require_persistent_runtime=True)
        shutil.rmtree(self.root)
        self.write_runtime_health(state="stopped")
        with self.assertRaises(p703.IntegrityError):
            p703.run_proof(self.root, TOOL_SHA, require_persistent_runtime=True)

    def test_backup_output_cannot_escape_owner_local_backup_directory(self):
        p703.initialize_store(self.root, TOOL_SHA)
        outside = Path(self.tmp.name) / "outside.tar.gz"
        with self.assertRaises(p703.BoundaryError):
            p703.create_backup(self.root, TOOL_SHA, outside)


if __name__ == "__main__":
    unittest.main()
