from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import p6_05_l3_recover_discovered_sources as MODULE


SECRET = "TEST_EIS_SECRET_NESTED_CHECKOUT_4bf2b7"


class P605L3NestedCheckoutMappingTests(unittest.TestCase):
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
                "https://github.com/arvectum/ai-corporation.git",
            ).returncode,
            0,
        )
        tracked = path / "tracked.txt"
        tracked.write_text("baseline\n", encoding="utf-8")
        self.assertEqual(self._git(path, "add", "tracked.txt").returncode, 0)
        self.assertEqual(self._git(path, "commit", "-m", "baseline").returncode, 0)

    def test_nested_verified_checkouts_use_nearest_git_worktree_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            local_secrets = root / "local-secrets"
            outer = root / "outer"
            inner = outer / "nested" / "inner"
            arvectum.mkdir(mode=0o700)
            local_secrets.mkdir(mode=0o700)
            self._make_repo(outer)
            self._make_repo(inner)

            outer_env = outer / "outer.env"
            inner_env = inner / "inner.env"
            for env in (outer_env, inner_env):
                env.write_text(
                    "LOCAL_DEBUG=false\n"
                    f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
                    encoding="utf-8",
                )
                os.chmod(env, 0o600)

            discovery = root / "discovery-local-only.txt"
            discovery.write_text(
                f"AI_CORPORATION_CHECKOUT={outer}\n"
                f"AI_CORPORATION_CHECKOUT={inner}\n"
                f"ENV_WITH_EIS_KEY={outer_env}\n"
                f"ENV_WITH_EIS_KEY={inner_env}\n",
                encoding="utf-8",
            )
            destination = local_secrets / "eis-soap-token"

            rc, lines = MODULE.recover_discovered_sources(
                discovery,
                destination,
                expected_checkout_count=2,
                expected_env_count=2,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("p6_05_l3_discovered_source_recovery_status=PASS", output)
            self.assertIn("source_env_untracked_count=2", output)
            self.assertIn("tracked_state_unchanged=true", output)
            self.assertIn("tracked_head_unchanged=true", output)
            self.assertIn("source_envs_with_eis_key_remaining=0", output)
            self.assertNotIn(SECRET, output)

    def test_env_owned_by_unsupplied_nested_repo_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arvectum = root / "arvectum-os"
            local_secrets = root / "local-secrets"
            outer = root / "outer"
            hidden_inner = outer / "nested" / "hidden"
            arvectum.mkdir(mode=0o700)
            local_secrets.mkdir(mode=0o700)
            self._make_repo(outer)
            self._make_repo(hidden_inner)

            env = hidden_inner / "legacy.env"
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
            destination = local_secrets / "eis-soap-token"

            rc, lines = MODULE.recover_discovered_sources(
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
            self.assertNotIn(str(hidden_inner), output)


if __name__ == "__main__":
    unittest.main()
