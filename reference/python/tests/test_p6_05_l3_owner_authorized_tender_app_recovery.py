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
        self._make_repo(product, "https://github.com/arvectum/ai-corporation.git")
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

    def test_direct_invocation_fails_closed_as_superseded(self) -> None:
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
                owner_authorization="OWNER_APPROVES_TENDER_APP_LEGACY_SECRET_SCRUB",
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("p6_05_l3_owner_authorized_recovery_status=FAIL", output)
            self.assertIn("failure_code=LEGACY_GITHUB_IDENTITY_PATH_SUPERSEDED", output)
            self.assertIn("replacement_helper=p6_05_l3_reconcile_owner_selected_divergent_sources.py", output)
            self.assertIn("secret_values_read=false", output)
            self.assertIn("filesystem_modified=false", output)
            self.assertIn("network_invoked=false", output)
            self.assertFalse(destination.exists())
            self.assertEqual(self._git(product, "rev-parse", "HEAD").stdout.strip(), product_head_before)
            self.assertEqual(self._git(tender, "rev-parse", "HEAD").stdout.strip(), tender_head_before)
            self.assertNotIn(SECRET, output)


if __name__ == "__main__":
    unittest.main()
