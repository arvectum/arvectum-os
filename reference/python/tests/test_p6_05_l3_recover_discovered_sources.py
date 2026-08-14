from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import p6_05_l3_recover_discovered_sources as MODULE


SECRET = "TEST_EIS_SECRET_BASELINE_AWARE_81f32a"
OTHER_SECRET = "TEST_EIS_SECRET_DIFFERENT_1d0e44"


class P605L3RecoverDiscoveredSourcesTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def _make_checkout(
        self,
        root: Path,
        name: str,
        secret: str = SECRET,
        *,
        dirty_tracked: bool = False,
        track_env: bool = False,
        remote: str = "https://github.com/arvectum/ai-corporation.git",
    ) -> tuple[Path, Path, Path]:
        repo = root / name
        repo.mkdir(mode=0o700)
        self.assertEqual(self._git(repo, "init", "-b", "main").returncode, 0)
        self.assertEqual(self._git(repo, "config", "user.name", "Test").returncode, 0)
        self.assertEqual(self._git(repo, "config", "user.email", "test@example.invalid").returncode, 0)
        self.assertEqual(self._git(repo, "remote", "add", "origin", remote).returncode, 0)

        tracked = repo / "tracked.txt"
        tracked.write_text("baseline\n", encoding="utf-8")
        env = repo / ".env.local"
        env.write_text(
            "LOCAL_DEBUG=false\n"
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={secret}\n",
            encoding="utf-8",
        )
        os.chmod(env, 0o600)

        self.assertEqual(self._git(repo, "add", "tracked.txt").returncode, 0)
        if track_env:
            self.assertEqual(self._git(repo, "add", ".env.local").returncode, 0)
        self.assertEqual(self._git(repo, "commit", "-m", "baseline").returncode, 0)

        if dirty_tracked:
            tracked.write_text("preexisting local work\n", encoding="utf-8")

        return repo, env, tracked

    def _layout(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        arvectum = root / "arvectum-os"
        local_secrets = root / "local-secrets"
        arvectum.mkdir(mode=0o700)
        local_secrets.mkdir(mode=0o700)
        os.chmod(arvectum, 0o700)
        os.chmod(local_secrets, 0o700)
        destination = local_secrets / "eis-soap-token"
        discovery = root / "discovery-local-only.txt"
        return root, arvectum, destination, discovery

    def _write_discovery(
        self,
        discovery: Path,
        checkouts: list[Path],
        envs: list[Path],
    ) -> None:
        lines: list[str] = []
        for checkout in checkouts:
            lines.append(f"AI_CORPORATION_CHECKOUT={checkout}")
        for env in envs:
            lines.append(f"ENV_WITH_EIS_KEY={env}")
        discovery.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_seven_sources_allow_preexisting_tracked_dirtiness_when_unchanged(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkouts: list[Path] = []
        envs: list[Path] = []
        tracked_files: list[Path] = []
        for index in range(7):
            checkout, env, tracked = self._make_checkout(
                root,
                f"product-{index}",
                dirty_tracked=(index == 3),
            )
            checkouts.append(checkout)
            envs.append(env)
            tracked_files.append(tracked)
        self._write_discovery(discovery, checkouts, envs)
        dirty_before = self._git(checkouts[3], "status", "--porcelain=v1", "--untracked-files=no").stdout

        rc, lines = MODULE.recover_discovered_sources(
            discovery,
            destination,
            expected_checkout_count=7,
            expected_env_count=7,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_discovered_source_recovery_status=PASS", output)
        self.assertIn("source_remote_verified_count=7", output)
        self.assertIn("source_env_untracked_count=7", output)
        self.assertIn("tracked_dirty_before_count=1", output)
        self.assertIn("tracked_state_unchanged=true", output)
        self.assertIn("tracked_head_unchanged=true", output)
        self.assertIn("source_envs_with_eis_key_remaining=0", output)
        self.assertIn("p6_05_l3_secret_migration_status=PASS", output)
        self.assertNotIn(SECRET, output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertEqual(
            self._git(checkouts[3], "status", "--porcelain=v1", "--untracked-files=no").stdout,
            dirty_before,
        )
        self.assertEqual(tracked_files[3].read_text(encoding="utf-8"), "preexisting local work\n")
        for env in envs:
            self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", env.read_text(encoding="utf-8"))

    def test_tracked_legacy_env_fails_before_migration(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkout, env, _ = self._make_checkout(root, "product", track_env=True)
        self._write_discovery(discovery, [checkout], [env])

        rc, lines = MODULE.recover_discovered_sources(
            discovery,
            destination,
            expected_checkout_count=1,
            expected_env_count=1,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=LEGACY_ENV_TRACKED_BY_GIT", output)
        self.assertFalse(destination.exists())
        self.assertNotIn(SECRET, output)

    def test_wrong_remote_fails_without_printing_remote_or_paths(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkout, env, _ = self._make_checkout(
            root,
            "product",
            remote="https://github.com/example/unrelated.git",
        )
        self._write_discovery(discovery, [checkout], [env])

        rc, lines = MODULE.recover_discovered_sources(
            discovery,
            destination,
            expected_checkout_count=1,
            expected_env_count=1,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=AI_CORPORATION_REMOTE_NOT_VERIFIED", output)
        self.assertNotIn("example/unrelated", output)
        self.assertNotIn(str(checkout), output)
        self.assertNotIn(SECRET, output)

    def test_historical_arutyunoveth_remote_rejected_for_current_path(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkout, env, _ = self._make_checkout(
            root,
            "product",
            remote="https://github.com/arutyunoveth/ai-corporation.git",
        )
        self._write_discovery(discovery, [checkout], [env])

        rc, lines = MODULE.recover_discovered_sources(
            discovery,
            destination,
            expected_checkout_count=1,
            expected_env_count=1,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=AI_CORPORATION_REMOTE_NOT_VERIFIED", output)
        self.assertNotIn("arutyunoveth", output)
        self.assertNotIn(SECRET, output)

    def test_active_arvectum_ssh_remotes_accepted(self) -> None:
        for remote_url in [
            "git@github.com:arvectum/ai-corporation.git",
            "ssh://git@github.com/arvectum/ai-corporation.git",
            "https://github.com/arvectum/ai-corporation",
        ]:
            with self.subTest(remote=remote_url):
                root, arvectum, destination, discovery = self._layout()
                checkout, env, _ = self._make_checkout(
                    root,
                    "product",
                    remote=remote_url,
                )
                self._write_discovery(discovery, [checkout], [env])

                rc, lines = MODULE.recover_discovered_sources(
                    discovery,
                    destination,
                    expected_checkout_count=1,
                    expected_env_count=1,
                    arvectum_repo_root=arvectum,
                )
                output = "\n".join(lines)
                self.assertEqual(rc, 0)
                self.assertIn("p6_05_l3_discovered_source_recovery_status=PASS", output)

    def test_count_change_fails_closed(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkout, env, _ = self._make_checkout(root, "product")
        self._write_discovery(discovery, [checkout], [env])

        rc, lines = MODULE.recover_discovered_sources(
            discovery,
            destination,
            expected_checkout_count=7,
            expected_env_count=7,
            arvectum_repo_root=arvectum,
        )

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SOURCE_CHECKOUT_COUNT_CHANGED", "\n".join(lines))
        self.assertFalse(destination.exists())

    def test_differing_secrets_preserve_tracked_baseline_and_fail_closed(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkout1, env1, _ = self._make_checkout(root, "product-1", SECRET, dirty_tracked=True)
        checkout2, env2, _ = self._make_checkout(root, "product-2", OTHER_SECRET)
        self._write_discovery(discovery, [checkout1, checkout2], [env1, env2])

        rc, lines = MODULE.recover_discovered_sources(
            discovery,
            destination,
            expected_checkout_count=2,
            expected_env_count=2,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CANONICAL_MIGRATION_FAILED", output)
        self.assertIn("failure_code=SOURCE_SECRETS_DIFFER", output)
        self.assertIn("tracked_state_unchanged=true", output)
        self.assertIn("tracked_head_unchanged=true", output)
        self.assertIn("source_envs_with_eis_key_remaining=2", output)
        self.assertFalse(destination.exists())
        self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", env1.read_text(encoding="utf-8"))
        self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", env2.read_text(encoding="utf-8"))
        self.assertNotIn(SECRET, output)
        self.assertNotIn(OTHER_SECRET, output)

    def test_new_tracked_change_during_migration_is_detected(self) -> None:
        root, arvectum, destination, discovery = self._layout()
        checkout, env, tracked = self._make_checkout(root, "product")
        self._write_discovery(discovery, [checkout], [env])
        original = MODULE.MIGRATION.migrate_secret_set

        def mutating_migration(*args, **kwargs):
            result = original(*args, **kwargs)
            tracked.write_text("concurrent tracked change\n", encoding="utf-8")
            return result

        with mock.patch.object(
            MODULE.MIGRATION,
            "migrate_secret_set",
            side_effect=mutating_migration,
        ):
            rc, lines = MODULE.recover_discovered_sources(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=1,
                arvectum_repo_root=arvectum,
            )

        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=TRACKED_STATE_CHANGED_DURING_MIGRATION", output)
        self.assertIn("tracked_state_unchanged=false", output)
        self.assertNotIn(SECRET, output)


if __name__ == "__main__":
    unittest.main()
