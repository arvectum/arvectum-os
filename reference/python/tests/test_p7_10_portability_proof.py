import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import p7_03_durable_state as p703
import p7_10_portability_proof as p710

TOOL_SHA = "a" * 40
SOURCE_SHA = "b" * 40


class P710PortabilityProofTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        if os.name != "nt":
            self.base.chmod(0o700)
        self.source = self.base / "source-runtime"
        self.package = self.base / "off-host-package"
        self.target = self.base / "clean-target"
        p703.initialize_store(self.source, TOOL_SHA)
        self.item_id = p703.persist_governed_item(
            self.source,
            TOOL_SHA,
            b"historical-governed-record",
            {
                "state_class": "canonical-governed-state",
                "organization_scope": p703.ORGANIZATION_SCOPE,
                "semantic_type": "p7.10.test.record",
                "schema_version": "1",
                "classification": "internal",
                "retention_policy_ref": "p7.10-test-retention",
                "source_release_sha": SOURCE_SHA,
                "canonical_authority": True,
                "contains_reusable_secret": False,
                "subject_identity": "subject:p7-10:test",
                "version_identity": "version:p7-10:test:1",
                "authority_mode": "Native",
                "authority_scope": "p7.10-test",
                "governed_admission_ref": "execution:p7-10:test:1",
                "provenance_refs": ["event:p7-10:test:1"],
            },
        )
        p703.create_checkpoint(
            self.source,
            TOOL_SHA,
            execution_subject_identity="execution:p7-10:test",
            execution_version_identity="execution:p7-10:test:v1",
            governed_storage_item_ids=[self.item_id],
            classification="internal",
            retention_policy_ref="p7.10-test-retention",
            reason="P7.10 portability fixture checkpoint",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _prepare(self):
        return p710.prepare_handoff(
            self.source,
            self.package,
            TOOL_SHA,
            host_marker="source-host",
        )

    def test_host_loss_restore_on_clean_environment_preserves_semantics(self):
        before = p710.governed_state_digest(self.source)
        historical = p710.selected_historical_evidence(self.source)
        manifest = self._prepare()
        self.assertEqual(manifest["semantic_evidence"]["governed_state_sha256"], before)

        # Simulate primary-host loss: only the transferred package survives.
        shutil.rmtree(self.source)
        self.assertFalse(self.source.exists())
        receipt = p710.restore_on_clean_environment(
            self.package,
            self.target,
            TOOL_SHA,
            host_marker="clean-secondary-host",
        )
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["governed_state_sha256"], before)
        self.assertEqual(receipt["selected_historical_record"], historical)
        self.assertEqual(p710.governed_state_digest(self.target), before)
        self.assertFalse(receipt["external_effect_replay_performed"])
        self.assertFalse(receipt["organizational_authority_granted_by_restore"])
        self.assertFalse(receipt["reusable_secrets_restored"])

    def test_off_host_handoff_preserves_explicit_exclusions(self):
        for name in ("run", "logs", "cache", "secrets"):
            path = self.source / name
            path.mkdir(parents=True, exist_ok=True)
            if os.name != "nt":
                path.chmod(0o700)
            file = path / "must-not-transfer.txt"
            file.write_text("excluded", encoding="utf-8")
            if os.name != "nt":
                file.chmod(0o600)

        self._prepare()
        shutil.rmtree(self.source)
        receipt = p710.restore_on_clean_environment(
            self.package,
            self.target,
            TOOL_SHA,
            host_marker="clean-secondary-host",
        )
        self.assertEqual(receipt["result"], "PASS")
        for name in ("run", "logs", "cache", "secrets"):
            self.assertFalse((self.target / name).exists())

    def test_restore_requires_release_identity_match(self):
        self._prepare()
        with self.assertRaises(p710.PortabilityError):
            p710.restore_on_clean_environment(
                self.package,
                self.target,
                "c" * 40,
                host_marker="clean-secondary-host",
            )

    def test_restore_requires_distinct_host_marker(self):
        self._prepare()
        with self.assertRaises(p710.PortabilityError):
            p710.restore_on_clean_environment(
                self.package,
                self.target,
                TOOL_SHA,
                host_marker="source-host",
            )

    def test_restore_requires_absent_clean_target(self):
        self._prepare()
        self.target.mkdir()
        if os.name != "nt":
            self.target.chmod(0o700)
        with self.assertRaises(p710.PortabilityError):
            p710.restore_on_clean_environment(
                self.package,
                self.target,
                TOOL_SHA,
                host_marker="clean-secondary-host",
            )

    def test_handoff_must_be_physically_outside_source_root(self):
        nested = self.source / "handoff"
        with self.assertRaises(p710.PortabilityError):
            p710.prepare_handoff(
                self.source,
                nested,
                TOOL_SHA,
                host_marker="source-host",
            )

    def test_tampered_handoff_manifest_fails_closed(self):
        self._prepare()
        manifest_path = self.package / p710.MANIFEST_NAME
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["authority_and_exclusions"]["external_effect_replay_authorized"] = True
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        if os.name != "nt":
            manifest_path.chmod(0o600)
        with self.assertRaises(p710.PortabilityError):
            p710.verify_handoff(self.package)

    @unittest.skipIf(os.name == "nt", "symlink setup differs on Windows without Developer Mode")
    def test_lexical_var_style_alias_is_compared_by_filesystem_identity(self):
        physical_parent = self.base / "private" / "var"
        physical_runtime = physical_parent / "lib" / "arvectum-os"
        physical_runtime.mkdir(parents=True)
        alias = self.base / "var"
        alias.symlink_to(physical_parent, target_is_directory=True)
        lexical_runtime = alias / "lib" / "arvectum-os"

        identity = p710.path_identity(lexical_runtime)
        self.assertNotEqual(identity["lexical"], identity["physical"])
        self.assertTrue(identity["lexical_differs_from_physical"])
        self.assertTrue(p710.paths_refer_same_location(lexical_runtime, physical_runtime))


if __name__ == "__main__":
    unittest.main()
