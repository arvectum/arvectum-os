from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import p6_05_l3_recover_owner_authorized_tender_app as MODULE


SECRET = "TEST_EIS_SECRET_AUTHORIZED_TENDER_APP_8c91"


class P605L3OwnerAuthorizedTenderAppRecoveryTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def _make_repo(self, path: Path, remote: str) -> None:
        path.mkdir(parents=True, mode=0o700)
        self.assertEqual(self._git(path, "init", "-b", "main").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.name", "Test").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.email", "test@example.invalid").returncode, 0)
        self.assertEqual(self._git(path, "remote", "add", "origin", remote).returncode, 0)
        tracked = path / "tracked.txt"
        tracked.write_text("baseline\n", encoding="utf-8")
        self.assertEqual(self._git(path, "add", "tracked.txt").returncode, 0)
        self.assertEqual(self._git(path, "commit", "-m", "baseline").returncode, 0)

    def _write_env(self, path: Path, value: str = SECRET) -> None:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        path.write_text(f"LOCAL_DEBUG=false\nZAKUPKI_GOV_RU_SOAP_TOKEN={value}\n", encoding="utf-8")
        os.chmod(path, 0o600)

    def _fixture(self, root: Path) -> tuple[Path, Path, Path, Path, Path]:
        arvectum = root / "arvectum-os"
        product = root / "product"
        tender = root / "legacy-tender"
        standalone = root / "standalone" / "legacy.env"
        secret_dir = root / "local-secrets"
        arvectum.mkdir(mode=0o700)
        secret_dir.mkdir(mode=0o700)
        self._make_repo(product, "https://github.com/arutyunoveth/ai-corporation.git")
        self._make_repo(tender, "https://github.com/arutyunoveth/tender-app.git")
        repo_env = product / "product.env"
        tender_env = tender / "legacy.env"
        self._write_env(repo_env)
        self._write_env(tender_env)
        self._write_env(standalone)
        discovery = root / "discovery.txt"
        discovery.write_text(
            f"AI_CORPORATION_CHECKOUT={product}\n"
            f"ENV_WITH_EIS_KEY={repo_env}\n"
            f"ENV_WITH_EIS_KEY={standalone}\n"
            f"ENV_WITH_EIS_KEY={tender_env}\n",
            encoding="utf-8",
        )
        return arvectum, product, tender, discovery, secret_dir / "eis-soap-token"

    def test_explicit_authorization_migrates_and_preserves_both_repo_tracked_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum, product, tender, discovery, destination = self._fixture(root)
            product_head_before = self._git(product, "rev-parse", "HEAD").stdout.strip()
            tender_head_before = self._git(tender, "rev-parse", "HEAD").stdout.strip()

            rc, lines = MODULE.recover(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=3,
                owner_authorization=MODULE.OWNER_AUTHORIZATION_VALUE,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("p6_05_l3_owner_authorized_recovery_status=PASS", output)
            self.assertIn("repo_local_source_count=1", output)
            self.assertIn("standalone_source_count=1", output)
            self.assertIn("authorized_tender_app_source_count=1", output)
            self.assertIn("source_env_untracked_count=3", output)
            self.assertIn("owner_authorization_asserted=true", output)
            self.assertIn("tracked_state_unchanged=true", output)
            self.assertIn("tracked_head_unchanged=true", output)
            self.assertIn("tender_app_tracked_state_unchanged=true", output)
            self.assertIn("tender_app_head_unchanged=true", output)
            self.assertIn("source_envs_with_eis_key_remaining=0", output)
            self.assertEqual(self._git(product, "rev-parse", "HEAD").stdout.strip(), product_head_before)
            self.assertEqual(self._git(tender, "rev-parse", "HEAD").stdout.strip(), tender_head_before)
            self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
            self.assertNotIn(SECRET, output)

    def test_missing_owner_authorization_fails_before_secret_read_or_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum, _product, _tender, discovery, destination = self._fixture(root)

            rc, lines = MODULE.recover(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=3,
                owner_authorization="NOT_APPROVED",
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=TENDER_APP_OWNER_AUTHORIZATION_REQUIRED", output)
            self.assertIn("owner_authorization_asserted=false", output)
            self.assertFalse(destination.exists())
            self.assertNotIn(SECRET, output)
            self.assertNotIn("sources_with_secret_before=", output)

    def test_non_tender_app_git_owner_is_not_authorized_by_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum, _product, tender, discovery, destination = self._fixture(root)
            self.assertEqual(self._git(tender, "remote", "set-url", "origin", "https://github.com/arutyunoveth/tender-ai.git").returncode, 0)

            rc, lines = MODULE.recover(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=3,
                owner_authorization=MODULE.OWNER_AUTHORIZATION_VALUE,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=UNVERIFIED_GIT_OWNER_NOT_AUTHORIZED_TENDER_APP", output)
            self.assertFalse(destination.exists())
            self.assertNotIn(SECRET, output)

    def test_tracked_tender_app_env_fails_before_migration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum, _product, tender, discovery, destination = self._fixture(root)
            tender_env = tender / "legacy.env"
            self.assertEqual(self._git(tender, "add", "legacy.env").returncode, 0)
            self.assertEqual(self._git(tender, "commit", "-m", "track env for negative test").returncode, 0)

            rc, lines = MODULE.recover(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=3,
                owner_authorization=MODULE.OWNER_AUTHORIZATION_VALUE,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=TENDER_APP_LEGACY_ENV_TRACKED_BY_GIT", output)
            self.assertFalse(destination.exists())
            self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", tender_env.read_text(encoding="utf-8"))
            self.assertNotIn(SECRET, output)

    def test_differing_tender_app_secret_fails_before_any_scrub(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum, product, tender, discovery, destination = self._fixture(root)
            tender_env = tender / "legacy.env"
            self._write_env(tender_env, "DIFFERENT_SYNTHETIC_VALUE")
            product_env = product / "product.env"

            rc, lines = MODULE.recover(
                discovery,
                destination,
                expected_checkout_count=1,
                expected_env_count=3,
                owner_authorization=MODULE.OWNER_AUTHORIZATION_VALUE,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("failure_code=SOURCE_SECRETS_DIFFER", output)
            self.assertFalse(destination.exists())
            self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", product_env.read_text(encoding="utf-8"))
            self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", tender_env.read_text(encoding="utf-8"))
            self.assertNotIn(SECRET, output)
            self.assertNotIn("DIFFERENT_SYNTHETIC_VALUE", output)


if __name__ == "__main__":
    unittest.main()
