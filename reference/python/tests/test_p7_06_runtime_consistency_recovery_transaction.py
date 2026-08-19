import tempfile
import unittest
from pathlib import Path
from unittest import mock

import p7_06_runtime_consistency_recovery as r


SHA_OLD_POINTER = "a" * 40
SHA_LIVE = "b" * 40
SHA_CANONICAL = "c" * 40


class RuntimeConsistencyRecoveryTransactionTests(unittest.TestCase):
    def test_post_reconciliation_failure_restores_exact_original_pointer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            runtime_root = root / "runtime"
            repo.mkdir()
            (runtime_root / "run").mkdir(parents=True)
            old_dir = runtime_root / "releases" / SHA_OLD_POINTER
            live_dir = runtime_root / "releases" / SHA_LIVE
            old_dir.mkdir(parents=True)
            live_dir.mkdir(parents=True)
            (runtime_root / "current").symlink_to(old_dir)

            runtime_plist = {"ProgramArguments": ["runtime"]}
            observer_plist = {"ProgramArguments": ["observer"]}

            with (
                mock.patch.object(r.sys, "platform", "darwin"),
                mock.patch.object(r, "_canonical_head", return_value=SHA_CANONICAL),
                mock.patch.object(r, "_load_plist", side_effect=[runtime_plist, observer_plist]),
                mock.patch.object(r, "_runtime_release_from_plist", return_value=SHA_LIVE),
                mock.patch.object(r, "_observer_release_from_plist", return_value=SHA_LIVE),
                mock.patch.object(r, "_verify_release_manifest"),
                mock.patch.object(r, "_launchd_pid", return_value=1234),
                mock.patch.object(
                    r,
                    "_verify_runtime_health",
                    return_value={"release_sha": SHA_LIVE, "pid": 1234},
                ),
                mock.patch.object(r, "_p703_digest", return_value="p703-stable"),
                mock.patch.object(r, "_p704_digest", return_value="p704-stable"),
                mock.patch.object(r, "_run", return_value=(7, "", "forced post-check failure")),
                mock.patch.object(r, "_write_evidence", return_value=(runtime_root / "failure.json", "f" * 64)),
            ):
                with self.assertRaises(r.RecoveryError):
                    r.recover(runtime_root, repo, "transaction-regression")

            self.assertEqual(r._current_release(runtime_root), SHA_OLD_POINTER)
            self.assertFalse((runtime_root / "run" / "p7-06-deploy.lock").exists())


if __name__ == "__main__":
    unittest.main()
