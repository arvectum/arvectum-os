from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

import p6_05_l3_diagnose_destination_boundary as MODULE


class P605L3DestinationBoundaryDiagnosticTests(unittest.TestCase):
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

    def _manifest(self, root: Path, ai: Path, tender: Path) -> Path:
        ai_env = ai / "product.env"
        ai_env.write_text("ZAKUPKI_GOV_RU_SOAP_TOKEN=DO_NOT_READ_AI\n", encoding="utf-8")
        tender_env = tender / "legacy.env"
        tender_env.write_text("ZAKUPKI_GOV_RU_SOAP_TOKEN=DO_NOT_READ_TENDER\n", encoding="utf-8")
        discovery = root / "discovery.txt"
        discovery.write_text(
            f"AI_CORPORATION_CHECKOUT={ai}\n"
            f"ENV_WITH_EIS_KEY={ai_env}\n"
            f"ENV_WITH_EIS_KEY={tender_env}\n",
            encoding="utf-8",
        )
        return discovery

    def test_destination_inside_tender_app_is_classified_without_secret_read(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            ai = root / "ai"
            tender = root / "tender"
            arvectum.mkdir(mode=0o700)
            self._make_repo(ai, "https://github.com/arvectum/ai-corporation.git")
            self._make_repo(tender, "https://github.com/arutyunoveth/tender-app.git")
            discovery = self._manifest(root, ai, tender)
            secret_dir = tender / "local-secrets"
            secret_dir.mkdir(mode=0o700)

            rc, lines = MODULE.diagnose(
                discovery,
                secret_dir / "eis-soap-token",
                expected_checkout_count=1,
                expected_env_count=2,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("destination_inside_tender_app=true", output)
            self.assertIn("destination_inside_ai_corporation_checkout_count=0", output)
            self.assertIn("secret_values_read=false", output)
            self.assertNotIn("DO_NOT_READ_AI", output)
            self.assertNotIn("DO_NOT_READ_TENDER", output)

    def test_destination_inside_ai_checkout_is_classified(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            ai = root / "ai"
            tender = root / "tender"
            arvectum.mkdir(mode=0o700)
            self._make_repo(ai, "https://github.com/arvectum/ai-corporation.git")
            self._make_repo(tender, "https://github.com/arutyunoveth/tender-app.git")
            discovery = self._manifest(root, ai, tender)
            secret_dir = ai / "local-secrets"
            secret_dir.mkdir(mode=0o700)

            rc, lines = MODULE.diagnose(
                discovery,
                secret_dir / "eis-soap-token",
                expected_checkout_count=1,
                expected_env_count=2,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("destination_inside_ai_corporation_checkout_count=1", output)
            self.assertIn("destination_inside_tender_app=false", output)

    def test_destination_outside_git_is_classified_as_no_git_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            ai = root / "ai"
            tender = root / "tender"
            arvectum.mkdir(mode=0o700)
            self._make_repo(ai, "https://github.com/arvectum/ai-corporation.git")
            self._make_repo(tender, "https://github.com/arutyunoveth/tender-app.git")
            discovery = self._manifest(root, ai, tender)
            secret_dir = root / "external-secrets"
            secret_dir.mkdir(mode=0o700)

            rc, lines = MODULE.diagnose(
                discovery,
                secret_dir / "eis-soap-token",
                expected_checkout_count=1,
                expected_env_count=2,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("destination_no_git_owner=true", output)
            self.assertIn("destination_inside_ai_corporation_checkout_count=0", output)
            self.assertIn("destination_inside_tender_app=false", output)
            self.assertIn("destination_inside_arvectum_os=false", output)


if __name__ == "__main__":
    unittest.main()
