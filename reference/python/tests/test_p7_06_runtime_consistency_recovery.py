import json
import os
import plistlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import p7_06_runtime_consistency_recovery as r


SHA_A = "a" * 40
SHA_B = "b" * 40


class RuntimeConsistencyRecoveryTests(unittest.TestCase):
    def test_validate_sha_and_decision_ref(self):
        self.assertEqual(r._validate_sha(SHA_A, "x"), SHA_A)
        with self.assertRaises(r.RecoveryError):
            r._validate_sha("abc", "x")
        self.assertEqual(r._validate_decision_ref("owner-approved"), "owner-approved")
        with self.assertRaises(r.RecoveryError):
            r._validate_decision_ref("bad\nref")

    def test_current_release_requires_exact_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "releases" / SHA_A
            target.mkdir(parents=True)
            (root / "current").symlink_to(target)
            self.assertEqual(r._current_release(root), SHA_A)
            (root / "current").unlink()
            (root / "current").write_text("not-a-link", encoding="utf-8")
            with self.assertRaises(r.RecoveryError):
                r._current_release(root)

    def test_runtime_plist_extracts_exact_release(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            py = root / "venvs" / SHA_A / "bin/python"
            script = root / "releases" / SHA_A / "source/reference/python/p7_02_persistent_runtime.py"
            payload = {
                "ProgramArguments": [
                    str(py),
                    str(script),
                    "run",
                    "--runtime-root",
                    str(root),
                    "--release-sha",
                    SHA_A,
                    "--heartbeat-seconds",
                    "5",
                ]
            }
            self.assertEqual(r._runtime_release_from_plist(root, payload), SHA_A)
            payload["ProgramArguments"][0] = str(root / "venvs" / SHA_B / "bin/python")
            with self.assertRaises(r.RecoveryError):
                r._runtime_release_from_plist(root, payload)

    def test_observer_plist_extracts_exact_release(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            py = root / "venvs" / SHA_A / "bin/python"
            script = root / "releases" / SHA_A / "source/reference/python/p7_05_operational_visibility.py"
            payload = {
                "ProgramArguments": [
                    str(py),
                    str(script),
                    "observe",
                    "--runtime-root",
                    str(root),
                    "--max-age-seconds",
                    "20",
                ]
            }
            self.assertEqual(r._observer_release_from_plist(root, payload), SHA_A)
            payload["ProgramArguments"][1] = str(
                root / "releases" / SHA_B / "source/reference/python/p7_05_operational_visibility.py"
            )
            with self.assertRaises(r.RecoveryError):
                r._observer_release_from_plist(root, payload)

    def test_load_plist_requires_owner_only_and_label(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "service.plist"
            with path.open("wb") as handle:
                plistlib.dump({"Label": r.RUNTIME_LABEL, "ProgramArguments": ["x"]}, handle)
            os.chmod(path, 0o600)
            value = r._load_plist(path, r.RUNTIME_LABEL)
            self.assertEqual(value["Label"], r.RUNTIME_LABEL)
            with self.assertRaises(r.RecoveryError):
                r._load_plist(path, r.OBSERVER_LABEL)

    def test_verify_manifest_is_exact(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            release = root / "releases" / SHA_A
            (release / "source/reference/python").mkdir(parents=True)
            (root / "venvs" / SHA_A / "bin").mkdir(parents=True)
            py = root / "venvs" / SHA_A / "bin/python"
            py.write_text("#!/bin/sh\n", encoding="utf-8")
            os.chmod(py, 0o700)
            (release / "source/reference/python/p7_02_persistent_runtime.py").write_text("", encoding="utf-8")
            (release / "source/reference/python/p7_05_operational_visibility.py").write_text("", encoding="utf-8")
            (release / "release-manifest.json").write_text(
                json.dumps({"canonical_repository": r.CANONICAL_REPO, "release_sha": SHA_A}),
                encoding="utf-8",
            )
            r._verify_release_manifest(root, SHA_A)
            (release / "release-manifest.json").write_text(
                json.dumps({"canonical_repository": r.CANONICAL_REPO, "release_sha": SHA_B}),
                encoding="utf-8",
            )
            with self.assertRaises(r.RecoveryError):
                r._verify_release_manifest(root, SHA_A)

    def test_health_must_match_launchd_pid(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            py = root / "venvs" / SHA_A / "bin/python"
            runtime = root / "releases" / SHA_A / "source/reference/python/p7_02_persistent_runtime.py"
            py.parent.mkdir(parents=True)
            runtime.parent.mkdir(parents=True)
            py.write_text("", encoding="utf-8")
            runtime.write_text("", encoding="utf-8")
            with mock.patch.object(
                r,
                "_run",
                return_value=(0, json.dumps({"release_sha": SHA_A, "pid": 123}), ""),
            ):
                value = r._verify_runtime_health(root, SHA_A, 123)
                self.assertEqual(value["pid"], 123)
            with mock.patch.object(
                r,
                "_run",
                return_value=(0, json.dumps({"release_sha": SHA_A, "pid": 999}), ""),
            ):
                with self.assertRaises(r.RecoveryError):
                    r._verify_runtime_health(root, SHA_A, 123)

    def test_atomic_replace_current_only_changes_pointer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = root / "releases" / SHA_A
            new = root / "releases" / SHA_B
            old.mkdir(parents=True)
            new.mkdir(parents=True)
            (root / "current").symlink_to(old)
            r._atomic_replace_current(root, SHA_B)
            self.assertEqual(r._current_release(root), SHA_B)
            self.assertTrue(old.is_dir())
            self.assertTrue(new.is_dir())

    def test_protected_digests_detect_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "state/governed").mkdir(parents=True)
            (root / "state/checkpoints").mkdir(parents=True)
            (root / "config").mkdir()
            (root / "secrets/p7-04").mkdir(parents=True)
            (root / "state/governed/x").write_text("one", encoding="utf-8")
            (root / "config/p7-04-access.json").write_text("{}", encoding="utf-8")
            before3 = r._p703_digest(root)
            before4 = r._p704_digest(root)
            (root / "state/governed/x").write_text("two", encoding="utf-8")
            self.assertNotEqual(before3, r._p703_digest(root))
            (root / "secrets/p7-04/x.secret").write_text("secret", encoding="utf-8")
            self.assertNotEqual(before4, r._p704_digest(root))

    def test_evidence_is_owner_only_and_secret_free_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = {
                "schema": "arvectum.p7_06.runtime-consistency-recovery/1",
                "reusable_secret_emitted": False,
                "canonical_state_mutated": False,
            }
            path, digest = r._write_evidence(root, value)
            self.assertTrue(path.is_file())
            self.assertEqual(len(digest), 64)
            if os.name != "nt":
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("secret_value", text)

    def test_recovery_source_has_no_ui3_or_rollback_invocation(self):
        text = Path(r.__file__).read_text(encoding="utf-8")
        self.assertNotIn("rollback-last", text)
        self.assertNotIn("recover-interrupted-latest", text)
        self.assertNotIn("p7_06_ui3", text)
        self.assertIn("p7-06-deploy.lock", text)
        self.assertIn("runtime and observer exact-release pins disagree", text)
        self.assertIn("runtime health pid does not match launchd pid", text)


if __name__ == "__main__":
    unittest.main()
