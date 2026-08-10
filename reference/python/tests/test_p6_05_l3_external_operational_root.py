from __future__ import annotations

import importlib.util
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "p6_05_l3_prepare_external_operational_root.py"
SPEC = importlib.util.spec_from_file_location("p6_05_l3_prepare_external_operational_root", MODULE_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class P605L3ExternalOperationalRootTests(unittest.TestCase):
    def test_prepares_owner_only_root_and_exact_nonsecret_config_outside_git(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "arvectum-os"
            repo.mkdir()
            git(repo, "init")
            target = base / "external" / "p6-05-l3"
            target.parent.mkdir()

            rc, lines = MOD.prepare(target, arvectum_repo_root=repo)

            self.assertEqual(rc, 0)
            output = "\n".join(lines)
            self.assertIn("p6_05_l3_external_operational_root_status=PASS", output)
            self.assertIn("operational_root_outside_git=true", output)
            self.assertIn("config_exact_expected_nonsecret_content=true", output)
            self.assertIn("secret_destination_exists=false", output)
            self.assertEqual((target / "local-config" / "p6-05-l3.env").read_text(), MOD.EXPECTED_CONFIG)
            for path in [target, target / "local-config", target / "local-secrets", target / "evidence", target / "evidence" / "p6-05-l3"]:
                self.assertEqual(stat.S_IMODE(path.stat().st_mode) & 0o077, 0)
            self.assertEqual(stat.S_IMODE((target / "local-config" / "p6-05-l3.env").stat().st_mode) & 0o077, 0)

    def test_target_inside_git_worktree_fails_before_creation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            repo.mkdir()
            git(repo, "init")
            target = repo / "local" / "p6-05-l3"

            rc, lines = MOD.prepare(target, arvectum_repo_root=base / "other-arvectum")

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=TARGET_ROOT_INSIDE_GIT_WORKTREE", lines)
            self.assertFalse(target.exists())

    def test_existing_wrong_config_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "arvectum-os"
            repo.mkdir()
            git(repo, "init")
            target = base / "external" / "p6-05-l3"
            config_dir = target / "local-config"
            secret_dir = target / "local-secrets"
            evidence_dir = target / "evidence" / "p6-05-l3"
            config_dir.mkdir(parents=True)
            secret_dir.mkdir()
            evidence_dir.mkdir(parents=True)
            for path in [target, config_dir, secret_dir, target / "evidence", evidence_dir]:
                os.chmod(path, 0o700)
            config = config_dir / "p6-05-l3.env"
            config.write_text("WRONG=1\n")
            os.chmod(config, 0o600)

            rc, lines = MOD.prepare(target, arvectum_repo_root=repo)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=CONFIG_CONTENT_MISMATCH", lines)
            self.assertEqual(config.read_text(), "WRONG=1\n")

    def test_existing_secret_symlink_fails_without_secret_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "arvectum-os"
            repo.mkdir()
            git(repo, "init")
            target = base / "external" / "p6-05-l3"
            target.mkdir(parents=True)
            os.chmod(target, 0o700)
            for child in ["local-config", "local-secrets", "evidence"]:
                (target / child).mkdir()
                os.chmod(target / child, 0o700)
            (target / "evidence" / "p6-05-l3").mkdir()
            os.chmod(target / "evidence" / "p6-05-l3", 0o700)
            config = target / "local-config" / "p6-05-l3.env"
            config.write_text(MOD.EXPECTED_CONFIG)
            os.chmod(config, 0o600)
            outside = base / "outside-secret"
            outside.write_text("do-not-read")
            (target / "local-secrets" / "eis-soap-token").symlink_to(outside)

            rc, lines = MOD.prepare(target, arvectum_repo_root=repo)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=SECRET_DESTINATION_SYMLINK_NOT_ALLOWED", lines)
            self.assertIn("secret_values_read=false", lines)


if __name__ == "__main__":
    unittest.main()
