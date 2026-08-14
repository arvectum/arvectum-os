from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import p6_05_l3_recover_mixed_legacy_sources as MODULE


SECRET = "TEST_EIS_SECRET_MIXED_71f4"


class P605L3MixedLegacySourceTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def _make_repo(self, path: Path, remote: str = "https://github.com/arvectum/ai-corporation.git") -> None:
        path.mkdir(parents=True, mode=0o700)
        self.assertEqual(self._git(path, "init", "-b", "main").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.name", "Test").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.email", "test@example.invalid").returncode, 0)
        self.assertEqual(self._git(path, "remote", "add", "origin", remote).returncode, 0)
        tracked = path / "tracked.txt"
        tracked.write_text("baseline\n", encoding="utf-8")
        self.assertEqual(self._git(path, "add", "tracked.txt").returncode, 0)
        self.assertEqual(self._git(path, "commit", "-m", "baseline").returncode, 0)

    def _write_env(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        path.write_text(f"LOCAL_DEBUG=false\nZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n", encoding="utf-8")
        os.chmod(path, 0o600)

    def test_repo_local_and_standalone_sources_migrate_together(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            product = root / "product"
            standalone_dir = root / "legacy-local"
            secret_dir = root / "local-secrets"
            arvectum.mkdir(mode=0o700)
            secret_dir.mkdir(mode=0o700)
            self._make_repo(product)

            repo_env = product / "repo.env"
            standalone_env = standalone_dir / "standalone.env"
            self._write_env(repo_env)
            self._write_env(standalone_env)

            discovery = root / "discovery.txt"
            discovery.write_text(
                f"AI_CORPORATION_CHECKOUT={product}\n"
                f"ENV_WITH_EIS_KEY={repo_env}\n"
                f"ENV_WITH_EIS_KEY={standalone_env}\n",
                encoding="utf-8",
            )
            destination = secret_dir / "eis-soap-token"

            rc, lines = MODULE.recover_mixed_legacy_sources(
                discovery, destination,
                expected_checkout_count=1,
                expected_env_count=2,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("repo_local_source_count=1", output)
            self.assertIn("standalone_source_count=1", output)
            self.assertIn("source_env_untracked_count=2", output)
            self.assertIn("tracked_state_unchanged=true", output)
            self.assertIn("tracked_head_unchanged=true", output)
            self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
            self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", repo_env.read_text(encoding="utf-8"))
            self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", standalone_env.read_text(encoding="utf-8"))
            self.assertNotIn(SECRET, output)

    def test_standalone_source_inside_unverified_git_repo_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            product = root / "product"
            foreign = root / "foreign"
            secret_dir = root / "local-secrets"
            arvectum.mkdir(mode=0o700)
            secret_dir.mkdir(mode=0o700)
            self._make_repo(product)
            self._make_repo(foreign, "https://github.com/example/other.git")

            env = foreign / "foreign.env"
            self._write_env(env)
            discovery = root / "discovery.txt"
            discovery.write_text(
                f"AI_CORPORATION_CHECKOUT={product}\nENV_WITH_EIS_KEY={env}\n",
                encoding="utf-8",
            )
            destination = secret_dir / "eis-soap-token"

            rc, lines = MODULE.recover_mixed_legacy_sources(
                discovery, destination,
                expected_checkout_count=1,
                expected_env_count=1,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=STANDALONE_ENV_OWNED_BY_UNVERIFIED_GIT_REPO", output)
            self.assertFalse(destination.exists())
            self.assertNotIn(SECRET, output)

    def test_differing_repo_local_and_standalone_values_fail_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            product = root / "product"
            secret_dir = root / "local-secrets"
            arvectum.mkdir(mode=0o700)
            secret_dir.mkdir(mode=0o700)
            self._make_repo(product)

            repo_env = product / "repo.env"
            self._write_env(repo_env)
            standalone_env = root / "legacy" / "standalone.env"
            standalone_env.parent.mkdir(mode=0o700)
            standalone_env.write_text("ZAKUPKI_GOV_RU_SOAP_TOKEN=DIFFERENT_TEST_VALUE\n", encoding="utf-8")
            os.chmod(standalone_env, 0o600)

            discovery = root / "discovery.txt"
            discovery.write_text(
                f"AI_CORPORATION_CHECKOUT={product}\n"
                f"ENV_WITH_EIS_KEY={repo_env}\n"
                f"ENV_WITH_EIS_KEY={standalone_env}\n",
                encoding="utf-8",
            )
            destination = secret_dir / "eis-soap-token"

            rc, lines = MODULE.recover_mixed_legacy_sources(
                discovery, destination,
                expected_checkout_count=1,
                expected_env_count=2,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=SOURCE_SECRETS_DIFFER", output)
            self.assertFalse(destination.exists())
            self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", repo_env.read_text(encoding="utf-8"))
            self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", standalone_env.read_text(encoding="utf-8"))
            self.assertNotIn(SECRET, output)


if __name__ == "__main__":
    unittest.main()
