import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import p7_03_durable_state as p703
import p7_03_selected_mac_proof as selected

TOOL_SHA = "a" * 40
RUNTIME_SHA = "b" * 40


class P703SelectedMacProofTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "runtime"
        run = self.root / "run"
        run.mkdir(parents=True)
        if os.name != "nt":
            self.root.chmod(0o700)
            run.chmod(0o700)

    def tearDown(self):
        self.tmp.cleanup()

    def write_health(self, state="healthy"):
        path = self.root / "run" / "health.json"
        path.write_text(
            json.dumps(
                {
                    "release_sha": RUNTIME_SHA,
                    "state": state,
                    "canonical_state_written": False,
                    "product_effects_enabled": False,
                }
            ),
            encoding="utf-8",
        )
        if os.name != "nt":
            path.chmod(0o600)

    def test_selected_mac_attestation_enforces_healthy_runtime_and_core_contract(self):
        self.write_health()
        result = selected.run_selected_mac_proof(self.root, TOOL_SHA)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["required_runtime_enforced"])
        self.assertEqual(result["persistent_runtime_state_before"], "healthy")
        self.assertEqual(result["persistent_runtime_state_after"], "healthy")
        self.assertEqual(result["persistent_runtime_release_sha_before"], RUNTIME_SHA)
        self.assertEqual(result["persistent_runtime_release_sha_after"], RUNTIME_SHA)
        self.assertFalse(result["reusable_secrets_in_backup"])
        self.assertFalse(result["telemetry_in_backup"])
        self.assertFalse(result["cache_in_backup"])
        self.assertFalse(result["checkpoint_canonical_authority"])
        self.assertFalse(result["external_effect_replay_authorized"])
        self.assertFalse(result["proof_fixture_canonical_authority"])
        self.assertTrue((self.root / "evidence" / result["attestation_basename"]).is_file())

    def test_selected_mac_attestation_fails_closed_for_stopped_runtime(self):
        self.write_health(state="stopped")
        with self.assertRaises(p703.IntegrityError):
            selected.run_selected_mac_proof(self.root, TOOL_SHA)

    def test_selected_mac_attestation_rejects_core_summary_runtime_mismatch(self):
        self.write_health()
        fake_core = {
            "status": "PASS",
            "persistent_runtime_observed": True,
            "persistent_runtime_state": "stopped",
            "persistent_runtime_release_sha": RUNTIME_SHA,
            "summary_basename": "summary.json",
            "live_backup_basename": "backup.tar.gz",
            "live_backup_sha256": "c" * 64,
            "live_restore_integrity": "PASS",
            "live_state_digest_matches_restore": True,
            "fixture_backup_integrity": "PASS",
            "fixture_restore_integrity": "PASS",
            "tamper_detection_fail_closed": True,
            "explicit_exclusions_absent": True,
            "reusable_secrets_in_backup": False,
            "telemetry_in_backup": False,
            "cache_in_backup": False,
            "checkpoint_canonical_authority": False,
            "external_effect_replay_authorized": False,
            "proof_fixture_canonical_authority": False,
        }
        with mock.patch.object(p703, "run_proof", return_value=fake_core):
            with self.assertRaises(p703.IntegrityError):
                selected.run_selected_mac_proof(self.root, TOOL_SHA)


if __name__ == "__main__":
    unittest.main()
