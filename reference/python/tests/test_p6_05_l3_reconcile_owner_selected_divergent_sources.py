from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import p6_05_l3_reconcile_owner_selected_divergent_sources as MODULE

SECRET_SELECTED = "TEST_EIS_TOKEN_SELECTED_CLASS_C2_f812a"
SECRET_STALE = "TEST_EIS_TOKEN_STALE_CLASS_C1_39b0d"


class P605L3ReconcileOwnerSelectedDivergentSourcesTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def _make_repo(
        self,
        path: Path,
        remote: str = "https://github.com/arvectum/ai-corporation.git",
    ) -> Path:
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.assertEqual(self._git(path, "init", "-b", "main").returncode, 0)
        self.assertEqual(self._git(path, "config", "user.name", "Test").returncode, 0)
        self.assertEqual(
            self._git(path, "config", "user.email", "test@example.invalid").returncode, 0
        )
        self.assertEqual(self._git(path, "remote", "add", "origin", remote).returncode, 0)
        tracked = path / "tracked.txt"
        tracked.write_text("initial\n", encoding="utf-8")
        self.assertEqual(self._git(path, "add", "tracked.txt").returncode, 0)
        self.assertEqual(self._git(path, "commit", "-m", "init").returncode, 0)
        return path

    def _make_env(self, path: Path, secret: str = SECRET_SELECTED) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        path.write_text(
            f"LOCAL_DEBUG=false\nZAKUPKI_GOV_RU_SOAP_TOKEN={secret}\nEXTRA_KEY=value\n",
            encoding="utf-8",
        )
        os.chmod(path, 0o600)
        return path

    def _write_manifest(
        self,
        manifest_path: Path,
        checkouts: list[Path],
        envs: list[Path],
    ) -> None:
        manifest_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        lines = [f"ai_corporation_checkout_count={len(checkouts)}"]
        for c in checkouts:
            lines.append(f"AI_CORPORATION_CHECKOUT={c}")
        lines.append(f"env_with_eis_key_count={len(envs)}")
        for e in envs:
            lines.append(f"ENV_WITH_EIS_KEY={e}")
        manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.chmod(manifest_path, 0o600)

    def _setup_canonical_layout(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        arvectum = self._make_repo(root / "arvectum-os", "https://github.com/arvectum/arvectum-os.git")
        destination = root / "runtime" / "local-secrets" / "eis-soap-token"
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        manifest = root / "evidence" / "discovery-local-only.txt"

        # 7 ai-corporation checkouts
        checkouts = []
        for i in range(1, 8):
            repo = self._make_repo(root / f"ai-corp-{i}", "https://github.com/arvectum/ai-corporation.git")
            checkouts.append(repo)

        # 1 other local git repo (Category C)
        other_repo = self._make_repo(root / "other-local-repo", "git@github.com:arbitrary/local-repo.git")

        # 7 env files with exact 2 manifest, 4 standalone, 1 other git repo structure:
        # e1: standalone (.env) -> STALE (C1)
        # e2: standalone (.env) -> STALE (C1)
        # e3: standalone (.env.local) -> SELECTED (C2)
        # e4: checkouts[0] (.env.local) -> SELECTED (C2)
        # e5: checkouts[1] (.env.local) -> SELECTED (C2)
        # e6: standalone (.env.local) -> SELECTED (C2)
        # e7: other_repo (.env) -> SELECTED (C2)
        envs = [
            self._make_env(root / "standalone-1" / "legacy.env", SECRET_STALE),
            self._make_env(root / "standalone-2" / "pilot.env", SECRET_STALE),
            self._make_env(root / "standalone-3" / ".env.local", SECRET_SELECTED),
            self._make_env(checkouts[0] / ".env.local", SECRET_SELECTED),
            self._make_env(checkouts[1] / ".env.local", SECRET_SELECTED),
            self._make_env(root / "standalone-4" / ".env.local", SECRET_SELECTED),
            self._make_env(other_repo / ".env", SECRET_SELECTED),
        ]

        self._write_manifest(manifest, checkouts, envs)
        return root, arvectum, destination, manifest, checkouts, other_repo, envs

    def test_reconciles_5_plus_2_pattern_and_scrubs_all_seven_sources(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_divergent_reconciliation_status=PASS", output)
        self.assertIn("owner_authorization_asserted=true", output)
        self.assertIn("distinct_secret_class_count=2", output)
        self.assertIn("dot_env_local_source_count=4", output)
        self.assertIn("selected_secret_source_count=5", output)
        self.assertIn("stale_secret_source_count=2", output)
        self.assertIn("destination_created=true", output)
        self.assertIn("sources_scrubbed=7", output)
        self.assertIn("source_envs_with_eis_key_remaining=0", output)

        # Destination established with selected value
        self.assertTrue(destination.exists())
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET_SELECTED)

        # All 7 sources scrubbed of secret key, other lines preserved
        for env in envs:
            content = env.read_text(encoding="utf-8")
            self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", content)
            self.assertIn("LOCAL_DEBUG=false", content)
            self.assertIn("EXTRA_KEY=value", content)

        # Stale value never written to destination or leaked
        self.assertNotIn(SECRET_SELECTED, output)
        self.assertNotIn(SECRET_STALE, output)

    def test_missing_or_wrong_owner_assertion_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization="WRONG_ASSERTION",
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("p6_05_l3_divergent_reconciliation_status=FAIL", output)
        self.assertIn("failure_code=OWNER_AUTHORIZATION_REQUIRED", output)
        self.assertNotIn("distinct_secret_class_count=", [line for line in lines if not line.startswith("expected_")])
        self.assertNotIn("selected_secret_source_count=", [line for line in lines if not line.startswith("expected_")])
        self.assertNotIn("stale_secret_source_count=", [line for line in lines if not line.startswith("expected_")])
        self.assertFalse(destination.exists())

    def test_distribution_other_than_5_plus_2_fails_closed(self) -> None:
        # 4 + 3 distribution
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        # Change e7 to STALE -> 4 SELECTED, 3 STALE
        envs[6].write_text(f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET_STALE}\n", encoding="utf-8")

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("p6_05_l3_divergent_reconciliation_status=FAIL", output)
        self.assertIn("failure_code=SELECTED_SECRET_CLASS_COUNT_MISMATCH", output)
        self.assertFalse(destination.exists())

    def test_three_distinct_classes_fail_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        third_secret = "TEST_EIS_TOKEN_THIRD_CLASS_999a"
        envs[0].write_text(f"ZAKUPKI_GOV_RU_SOAP_TOKEN={third_secret}\n", encoding="utf-8")

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DISTINCT_SECRET_CLASS_COUNT_MISMATCH", output)
        self.assertFalse(destination.exists())

    def test_dot_env_local_not_all_in_selected_class_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        # e3 (.env.local) given STALE, e1 (.env) given SELECTED -> still 5+2, but only 3 .env.local in selected class
        envs[2].write_text(f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET_STALE}\n", encoding="utf-8")
        envs[0].write_text(f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET_SELECTED}\n", encoding="utf-8")

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DOT_ENV_LOCAL_NOT_ALL_IN_SELECTED_CLASS", output)
        self.assertFalse(destination.exists())

    def test_ai_corporation_wrong_remote_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        self._git(checkouts[0], "remote", "set-url", "origin", "https://github.com/arutyunoveth/ai-corporation.git")

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=AI_CORPORATION_REMOTE_MISMATCH", output)
        self.assertNotIn("distinct_secret_class_count=", [line for line in lines if not line.startswith("expected_")])
        self.assertFalse(destination.exists())

    def test_tracked_env_in_category_c_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        self.assertEqual(self._git(other_repo, "add", ".env").returncode, 0)

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=OTHER_GIT_WORKTREE_ENV_TRACKED_BY_GIT", output)
        self.assertNotIn("distinct_secret_class_count=", [line for line in lines if not line.startswith("expected_")])
        self.assertFalse(destination.exists())

    def test_destination_inside_source_checkout_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        bad_dest = checkouts[0] / "secrets" / "token"
        bad_dest.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=bad_dest,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DESTINATION_INSIDE_SOURCE_CHECKOUT", output)

    def test_destination_inside_arvectum_os_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        bad_dest = arvectum / "secrets" / "token"
        bad_dest.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=bad_dest,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DESTINATION_INSIDE_ARVECTUM_CHECKOUT", output)

    def test_idempotent_retry_passes_and_reuses_destination(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()

        # Run 1: success
        rc1, lines1 = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        self.assertEqual(rc1, 0)
        self.assertIn("destination_created=true", "\n".join(lines1))

        # Run 2: retry (all sources already scrubbed)
        rc2, lines2 = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output2 = "\n".join(lines2)
        self.assertEqual(rc2, 0)
        self.assertIn("destination_reused=true", output2)
        self.assertIn("sources_already_scrubbed_before=7", output2)
        self.assertIn("sources_scrubbed=0", output2)

    def test_partial_retry_scrubs_remaining_sources(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()

        # Simulate destination already created with selected value
        destination.write_text(f"{SECRET_SELECTED}\n", encoding="utf-8")
        os.chmod(destination, 0o600)

        # Scrub first 3 sources manually (2 stale + 1 .env.local; 3 .env.local remain)
        envs[0].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")
        envs[1].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")
        envs[2].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_divergent_reconciliation_status=PASS", output)
        self.assertIn("destination_reused=true", output)
        self.assertIn("sources_already_scrubbed_before=3", output)
        self.assertIn("sources_scrubbed=4", output)
        self.assertIn("source_envs_with_eis_key_remaining=0", output)

    def test_retry_without_remaining_dot_env_local_fails_closed(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()

        # Destination exists with selected value
        destination.write_text(f"{SECRET_SELECTED}\n", encoding="utf-8")
        os.chmod(destination, 0o600)

        # Scrub all 4 .env.local sources (envs[2], envs[3], envs[4], envs[5])
        envs[2].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")
        envs[3].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")
        envs[4].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")
        envs[5].write_text("LOCAL_DEBUG=false\nEXTRA_KEY=value\n", encoding="utf-8")

        # envs[6] (other_repo/.env) still contains SECRET_SELECTED
        # envs[0] and envs[1] still contain SECRET_STALE

        rc, lines = MODULE.reconcile_divergent_sources(
            discovery_file=manifest,
            destination=destination,
            owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("p6_05_l3_divergent_reconciliation_status=FAIL", output)
        self.assertIn("failure_code=RETRY_DOT_ENV_LOCAL_PROOF_REQUIRED", output)

        # Verify destination unchanged, remaining sources unchanged
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET_SELECTED)
        self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", envs[6].read_text(encoding="utf-8"))
        self.assertNotIn(SECRET_SELECTED, output)
        self.assertNotIn(SECRET_STALE, output)

    def test_destination_exclusive_create_prevents_overwrite_race(self) -> None:
        root, arvectum, destination, manifest, checkouts, other_repo, envs = self._setup_canonical_layout()
        initial_dest_content = "EXISTING_CONCURRENT_SECRET_VAL\n"

        # Patch _write_destination_secret_exclusive or simulate concurrent creation
        original_write = MODULE._write_destination_secret_exclusive

        def concurrent_creation(dest: Path, secret_val: str):
            # Simulate another process creating destination right before write
            dest.write_text(initial_dest_content, encoding="utf-8")
            os.chmod(dest, 0o600)
            # Now try exclusive create which must fail
            return original_write(dest, secret_val)

        with mock.patch.object(MODULE, "_write_destination_secret_exclusive", side_effect=concurrent_creation):
            rc, lines = MODULE.reconcile_divergent_sources(
                discovery_file=manifest,
                destination=destination,
                owner_authorization=MODULE.OWNER_AUTHORIZATION_ASSERTION,
                arvectum_repo_root=arvectum,
            )
            output = "\n".join(lines)

            self.assertEqual(rc, 2)
            self.assertIn("p6_05_l3_divergent_reconciliation_status=FAIL", output)
            self.assertIn("failure_code=DESTINATION_ALREADY_EXISTS", output)

            # Destination was not overwritten
            self.assertEqual(destination.read_text(encoding="utf-8"), initial_dest_content)

            # Source envs remain unscrubbed
            for env in envs:
                self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", env.read_text(encoding="utf-8"))

            self.assertNotIn(SECRET_SELECTED, output)
            self.assertNotIn(SECRET_STALE, output)


if __name__ == "__main__":
    unittest.main()
