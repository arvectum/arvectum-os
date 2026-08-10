from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "p6_05_l3_classify_known_legacy_owner.py"
spec = importlib.util.spec_from_file_location("p6_05_l3_classify_known_legacy_owner", MODULE_PATH)
assert spec and spec.loader
MOD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MOD)


def git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *args], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def init_repo(path: Path, remote: str | None) -> None:
    path.mkdir(parents=True)
    git(path, "init")
    git(path, "config", "user.email", "synthetic@example.test")
    git(path, "config", "user.name", "Synthetic")
    (path / "tracked.txt").write_text("synthetic\n", encoding="utf-8")
    git(path, "add", "tracked.txt")
    git(path, "commit", "-m", "init")
    if remote:
        git(path, "remote", "add", "origin", remote)


class P605L3KnownLegacyOwnerTests(unittest.TestCase):
    def run_case(self, other_remote: str, expected_key: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checkouts = []
            envs = []
            for i in range(7):
                repo = root / f"product-{i}"
                init_repo(repo, "https://github.com/arutyunoveth/ai-corporation.git")
                checkouts.append(repo)
            for i in range(2):
                env = checkouts[i] / f"legacy{i}.env"
                env.write_text("SYNTHETIC_ONLY=1\n", encoding="utf-8")
                envs.append(env)
            for i in range(4):
                d = root / f"standalone-{i}"
                d.mkdir()
                env = d / f"legacy{i}.env"
                env.write_text("SYNTHETIC_ONLY=1\n", encoding="utf-8")
                envs.append(env)
            other = root / "other"
            init_repo(other, other_remote)
            other_env = other / "legacy.env"
            synthetic_secret = "SYNTHETIC_SECRET_MUST_NOT_APPEAR"
            other_env.write_text(f"ZAKUPKI_GOV_RU_SOAP_TOKEN={synthetic_secret}\n", encoding="utf-8")
            envs.append(other_env)

            manifest = root / "manifest.txt"
            lines = [*(f"AI_CORPORATION_CHECKOUT={p}" for p in checkouts), *(f"ENV_WITH_EIS_KEY={p}" for p in envs)]
            manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

            rc, output_lines = MOD.diagnose(manifest, expected_checkout_count=7, expected_env_count=7)
            output = "\n".join(output_lines)
            self.assertEqual(rc, 0)
            self.assertIn("repo_local_source_count=2", output)
            self.assertIn("standalone_source_count=4", output)
            self.assertIn("unverified_git_owned_source_count=1", output)
            self.assertIn(f"{expected_key}=1", output)
            self.assertIn("unverified_owner_untracked_env_count=1", output)
            self.assertIn("env_contents_read=false", output)
            self.assertIn("secret_values_read=false", output)
            self.assertNotIn(synthetic_secret, output)
            self.assertNotIn(str(other), output)
            self.assertNotIn(other_remote, output)
            return rc, output

    def test_tender_app_is_bounded_known_category(self) -> None:
        self.run_case("https://github.com/arutyunoveth/tender-app.git", "known_owner_tender_app_count")

    def test_tender_ai_is_bounded_known_category(self) -> None:
        self.run_case("git@github.com:arutyunoveth/tender-ai.git", "known_owner_tender_ai_count")

    def test_same_account_unrelated_repo_is_not_legacy_tender(self) -> None:
        self.run_case("https://github.com/arutyunoveth/discount-parser.git", "known_owner_same_account_other_count")

    def test_external_repo_remains_external_other(self) -> None:
        self.run_case("https://github.com/example/example.git", "known_owner_external_other_count")


if __name__ == "__main__":
    unittest.main()
