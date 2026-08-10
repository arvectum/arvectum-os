from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import p6_05_l3_recover_verified_containers as MODULE


SECRET = "TEST_EIS_SECRET_VERIFIED_CONTAINER_7c91d2"


class P605L3VerifiedContainerRecoveryTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def _make_repo(self, path: Path) -> None:
        path.mkdir(parents=True, mode=0o700)
        self.assertEqual(self._git(path, "init", "-b", "main").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.name", "Test").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.email", "test@example.invalid").returncode, 0)
        self.assertEqual(
            self._git(
                path,
                "remote",
                "add",
                "origin",
                "https://github.com/arutyunoveth/ai-corporation.git",
            ).returncode,
            0,
        )
        tracked = path / "tracked.txt"
        tracked.write_text("baseline\n", encoding="utf-8")
        self.assertEqual(self._git(path, "add", "tracked.txt").returncode, 0)
        self.assertEqual(self._git(path, "commit", "-m", "baseline").returncode, 0)

    def _layout(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        arvectum = root / "arvectum-os"
        local_secrets = root / "local-secrets"
        arvectum.mkdir(mode=0o700)
        local_secrets.mkdir(mode=0o700)
        return root, arvectum, local_secrets / "eis-soap-token"

    def test_orphaned_nested_git_marker_does_not_block_explicit_untracked_source(self) -> None:
        root, arvectum, destination = self._layout()
        checkout = root / "product"
        self._make_repo(checkout)

        legacy_dir = checkout / "copied-worktree"
        legacy_dir.mkdir(mode=0o700)
        (legacy_dir / ".git").write_text(
            "gitdir: /definitely/missing/p6-05-l3-test-gitdir\n",
            encoding="utf-8",
        )
        env = legacy_dir / "legacy.env"
        env.write_text(
            "LOCAL_DEBUG=false\n"
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            encoding="utf-8",
        )
        os.chmod(env, 0o600)

        discovery = root / "discovery-local-only.txt"
        discovery.write_text(
            f"AI_CORPORATION_CHECKOUT={checkout}\n"
            f"ENV_WITH_EIS_KEY={env}\n",
            encoding="utf-8",
        )

        rc, lines = MODULE.recover_verified_containers(
            discovery,
            destination,
            expected_checkout_count=1,
            expected_env_count=1,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_discovered_source_recovery_status=PASS", output)
        self.assertIn("source_env_untracked_count=1", output)
        self.assertIn("tracked_state_unchanged=true", output)
        self.assertIn("tracked_head_unchanged=true", output)
        self.assertIn("source_envs_with_eis_key_remaining=0", output)
        self.assertIn("p6_05_l3_secret_migration_status=PASS", output)
        self.assertNotIn(SECRET, output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", env.read_text(encoding="utf-8"))

    def test_valid_unsupplied_nested_repo_still_fails_closed(self) -> None:
        root, arvectum, destination = self._layout()
        outer = root / "outer"
        hidden = outer / "nested" / "hidden"
        self._make_repo(outer)
        self._make_repo(hidden)

        env = hidden / "legacy.env"
        env.write_text(
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            encoding="utf-8",
        )
        os.chmod(env, 0o600)

        discovery = root / "discovery-local-only.txt"
        discovery.write_text(
            f"AI_CORPORATION_CHECKOUT={outer}\n"
            f"ENV_WITH_EIS_KEY={env}\n",
            encoding="utf-8",
        )

        rc, lines = MODULE.recover_verified_containers(
            discovery,
            destination,
            expected_checkout_count=1,
            expected_env_count=1,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=ENV_GIT_OWNER_NOT_IN_DISCOVERY", output)
        self.assertFalse(destination.exists())
        self.assertNotIn(SECRET, output)
        self.assertNotIn(str(outer), output)
        self.assertNotIn(str(hidden), output)

    def test_ambient_git_location_variables_do_not_change_verified_mapping(self) -> None:
        root, arvectum, destination = self._layout()
        checkout = root / "product"
        nested_dir = checkout / "config" / "legacy"
        self._make_repo(checkout)
        nested_dir.mkdir(parents=True, mode=0o700)

        env = nested_dir / "operator.env"
        env.write_text(
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            encoding="utf-8",
        )
        os.chmod(env, 0o600)

        discovery = root / "discovery-local-only.txt"
        discovery.write_text(
            f"AI_CORPORATION_CHECKOUT={checkout}\n"
            f"ENV_WITH_EIS_KEY={env}\n",
            encoding="utf-8",
        )

        poisoned = {
            "GIT_DIR": str(root / "missing-git-dir"),
            "GIT_WORK_TREE": str(root / "wrong-work-tree"),
            "GIT_CEILING_DIRECTORIES": str(nested_dir),
        }
        with mock.patch.dict(os.environ, poisoned, clear=False):
            rc, lines = MODULE.recover_verified_containers(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=1,
                arvectum_repo_root=arvectum,
            )

        output = "\n".join(lines)
        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_discovered_source_recovery_status=PASS", output)
        self.assertIn("source_remote_verified_count=1", output)
        self.assertIn("source_env_untracked_count=1", output)
        self.assertNotIn(SECRET, output)


if __name__ == "__main__":
    unittest.main()
