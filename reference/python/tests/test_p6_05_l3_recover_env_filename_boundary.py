from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import p6_05_l3_recover_discovered_sources as MODULE


SECRET = "TEST_EIS_SECRET_ENV_SUFFIX_BOUNDARY_6f4f31"


class P605L3RecoverEnvFilenameBoundaryTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def test_filename_boundary_matches_discovery_scope(self) -> None:
        for name in (".env", ".env.local", "legacy.env", "operator.env"):
            with self.subTest(name=name):
                self.assertTrue(MODULE._supported_legacy_env_filename(Path(name)))

        for name in (
            ".zshrc",
            ".bash_profile",
            ".env.production",
            "config.txt",
            "legacy.env.backup",
            "environment",
        ):
            with self.subTest(name=name):
                self.assertFalse(MODULE._supported_legacy_env_filename(Path(name)))

    def test_named_star_env_source_is_recovered_without_secret_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            checkout = root / "product"
            local_secrets = root / "local-secrets"
            arvectum.mkdir(mode=0o700)
            checkout.mkdir(mode=0o700)
            local_secrets.mkdir(mode=0o700)

            self.assertEqual(self._git(checkout, "init", "-b", "main").returncode, 0)
            self.assertEqual(self._git(checkout, "config", "user.name", "Test").returncode, 0)
            self.assertEqual(
                self._git(checkout, "config", "user.email", "test@example.invalid").returncode,
                0,
            )
            self.assertEqual(
                self._git(
                    checkout,
                    "remote",
                    "add",
                    "origin",
                    "https://github.com/arvectum/ai-corporation.git",
                ).returncode,
                0,
            )

            tracked = checkout / "tracked.txt"
            tracked.write_text("baseline\n", encoding="utf-8")
            self.assertEqual(self._git(checkout, "add", "tracked.txt").returncode, 0)
            self.assertEqual(self._git(checkout, "commit", "-m", "baseline").returncode, 0)

            env = checkout / "legacy-secrets.env"
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
            destination = local_secrets / "eis-soap-token"

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
            self.assertIn("source_env_untracked_count=1", output)
            self.assertIn("source_envs_with_eis_key_remaining=0", output)
            self.assertIn("tracked_state_unchanged=true", output)
            self.assertIn("tracked_head_unchanged=true", output)
            self.assertIn("p6_05_l3_secret_migration_status=PASS", output)
            self.assertNotIn(SECRET, output)
            self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
            self.assertNotIn(
                "ZAKUPKI_GOV_RU_SOAP_TOKEN",
                env.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
