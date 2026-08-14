from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import p6_05_l3_diagnose_unverified_env_owner as DIAG


AI_REMOTE = "https://github.com/arvectum/ai-corporation.git"
OS_REMOTE = "https://github.com/arvectum/arvectum-os.git"
OTHER_REMOTE = "https://github.com/example/other.git"
SYNTHETIC_SECRET = "synthetic-never-read-secret"


class P605L3UnverifiedOwnerDiagnosticTests(unittest.TestCase):
    def _git(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

    def _repo(self, root: Path, remote: str | None) -> Path:
        root.mkdir(parents=True)
        self._git(root, "init", "-q")
        self._git(root, "config", "user.email", "test@example.invalid")
        self._git(root, "config", "user.name", "P6.05 test")
        marker = root / "tracked.txt"
        marker.write_text("baseline\n", encoding="utf-8")
        self._git(root, "add", "tracked.txt")
        self._git(root, "commit", "-q", "-m", "baseline")
        if remote is not None:
            self._git(root, "remote", "add", "origin", remote)
        return root.resolve()

    def _env(self, root: Path, name: str = "legacy.env", *, tracked: bool = False) -> Path:
        path = root / name
        path.write_text(f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SYNTHETIC_SECRET}\n", encoding="utf-8")
        if tracked:
            self._git(root, "add", name)
            self._git(root, "commit", "-q", "-m", "track env")
        return path.resolve()

    def _manifest(self, root: Path, checkout: Path, envs: list[Path]) -> Path:
        manifest = root / "discovery.txt"
        lines = [f"AI_CORPORATION_CHECKOUT={checkout}"]
        lines.extend(f"ENV_WITH_EIS_KEY={env}" for env in envs)
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return manifest

    def _run_case(self, owner_remote: str | None, *, tracked: bool = False):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            supplied = self._repo(base / "supplied", AI_REMOTE)
            supplied_env = self._env(supplied)
            owner = self._repo(base / "owner", owner_remote)
            foreign_env = self._env(owner, tracked=tracked)
            manifest = self._manifest(base, supplied, [supplied_env, foreign_env])

            rc, lines = DIAG.diagnose(
                manifest,
                expected_checkout_count=1,
                expected_env_count=2,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 0)
            self.assertIn("p6_05_l3_unverified_owner_diagnostic_status=PASS", output)
            self.assertIn("repo_local_source_count=1", output)
            self.assertIn("standalone_source_count=0", output)
            self.assertIn("unverified_git_owned_source_count=1", output)
            self.assertNotIn(SYNTHETIC_SECRET, output)
            self.assertNotIn(str(supplied), output)
            self.assertNotIn(str(owner), output)
            if owner_remote is not None:
                self.assertNotIn(owner_remote, output)
            self.assertIn("env_contents_read=false", output)
            self.assertIn("secret_values_read=false", output)
            self.assertIn("filesystem_modified=false", output)
            return output

    def test_unlisted_ai_corporation_checkout_is_classified_without_remote_output(self):
        output = self._run_case(AI_REMOTE)
        self.assertIn("unverified_owner_ai_corporation_count=1", output)
        self.assertIn("unverified_owner_arvectum_os_count=0", output)
        self.assertIn("unverified_owner_other_remote_count=0", output)
        self.assertIn("unverified_owner_no_origin_count=0", output)
        self.assertIn("unverified_owner_untracked_env_count=1", output)

    def test_arvectum_os_owner_is_distinguished_and_tracked_state_is_safe_count_only(self):
        output = self._run_case(OS_REMOTE, tracked=True)
        self.assertIn("unverified_owner_ai_corporation_count=0", output)
        self.assertIn("unverified_owner_arvectum_os_count=1", output)
        self.assertIn("unverified_owner_tracked_env_count=1", output)
        self.assertIn("unverified_owner_untracked_env_count=0", output)

    def test_other_remote_is_not_accepted_as_ai_corporation(self):
        output = self._run_case(OTHER_REMOTE)
        self.assertIn("unverified_owner_other_remote_count=1", output)
        self.assertIn("unverified_owner_ai_corporation_count=0", output)
        self.assertIn("unverified_owner_untracked_env_count=1", output)

    def test_repo_without_origin_is_reported_without_guessing_owner(self):
        output = self._run_case(None)
        self.assertIn("unverified_owner_no_origin_count=1", output)
        self.assertIn("unverified_owner_ai_corporation_count=0", output)
        self.assertIn("unverified_owner_untracked_env_count=1", output)


if __name__ == "__main__":
    unittest.main()
