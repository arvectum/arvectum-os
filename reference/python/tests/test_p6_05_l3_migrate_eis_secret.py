from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

import p6_05_l3_migrate_eis_secret as MODULE


SECRET = "TEST_EIS_SECRET_DO_NOT_PRINT_3b7fcb8d"
OTHER_SECRET = "TEST_EIS_SECRET_DIFFERENT_91a7c0"


class P605L3MigrateEisSecretTests(unittest.TestCase):
    def _layout(self, source_texts: list[str], *, source_mode: int = 0o600):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        arvectum = root / "arvectum-os"
        local = root / "local-secrets"
        arvectum.mkdir(mode=0o700)
        local.mkdir(mode=0o700)
        os.chmod(arvectum, 0o700)
        os.chmod(local, 0o700)

        sources: list[tuple[Path, Path]] = []
        for index, source_text in enumerate(source_texts):
            product = root / f"AI-Corporation-{index}"
            product.mkdir(mode=0o700)
            os.chmod(product, 0o700)
            source = product / ".env.local"
            source.write_text(source_text, encoding="utf-8")
            os.chmod(source, source_mode)
            sources.append((source, product))

        destination = local / "eis-soap-token"
        return temp, arvectum, sources, destination

    def test_migrates_seven_matching_legacy_copies_without_secret_output(self) -> None:
        source_texts = [
            "AI_CORP_DEBUG=false\n"
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
            "ZAKUPKI_GOV_RU_SOAP_ENABLED=1\n"
            for _ in range(7)
        ]
        temp, arvectum, sources, destination = self._layout(source_texts)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(
            sources,
            destination,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_secret_migration_status=PASS", output)
        self.assertIn("source_count=7", output)
        self.assertIn("sources_with_secret_before=7", output)
        self.assertIn("sources_scrubbed=7", output)
        self.assertIn("all_source_secrets_consistent=true", output)
        self.assertNotIn(SECRET, output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertEqual(os.stat(destination).st_mode & 0o777, 0o600)
        for source, _ in sources:
            remaining = source.read_text(encoding="utf-8")
            self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", remaining)
            self.assertIn("AI_CORP_DEBUG=false", remaining)

    def test_differing_legacy_secrets_fail_before_any_write_or_scrub(self) -> None:
        texts = [
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={OTHER_SECRET}\n",
        ]
        temp, arvectum, sources, destination = self._layout(texts)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SOURCE_SECRETS_DIFFER", output)
        self.assertNotIn(SECRET, output)
        self.assertNotIn(OTHER_SECRET, output)
        self.assertFalse(destination.exists())
        for source, _ in sources:
            self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", source.read_text(encoding="utf-8"))

    def test_existing_matching_destination_is_reused_and_sources_scrubbed(self) -> None:
        texts = [
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
        ]
        temp, arvectum, sources, destination = self._layout(texts)
        self.addCleanup(temp.cleanup)
        destination.write_text(f"{SECRET}\n", encoding="utf-8")
        os.chmod(destination, 0o600)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("destination_created=false", output)
        self.assertIn("destination_reused=true", output)
        self.assertIn("sources_scrubbed=2", output)
        self.assertNotIn(SECRET, output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)

    def test_existing_mismatching_destination_is_never_overwritten(self) -> None:
        texts = [f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"]
        temp, arvectum, sources, destination = self._layout(texts)
        self.addCleanup(temp.cleanup)
        destination.write_text(f"{OTHER_SECRET}\n", encoding="utf-8")
        os.chmod(destination, 0o600)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SOURCE_SECRETS_DIFFER", output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), OTHER_SECRET)
        self.assertIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", sources[0][0].read_text(encoding="utf-8"))
        self.assertNotIn(SECRET, output)
        self.assertNotIn(OTHER_SECRET, output)

    def test_idempotent_retry_passes_after_all_sources_are_scrubbed(self) -> None:
        texts = [
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
        ]
        temp, arvectum, sources, destination = self._layout(texts)
        self.addCleanup(temp.cleanup)

        first_rc, _ = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        second_rc, second_lines = MODULE.migrate_secret_set(
            sources,
            destination,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(second_lines)

        self.assertEqual(first_rc, 0)
        self.assertEqual(second_rc, 0)
        self.assertIn("sources_with_secret_before=0", output)
        self.assertIn("sources_already_scrubbed_before=2", output)
        self.assertIn("sources_scrubbed=0", output)
        self.assertIn("destination_reused=true", output)
        self.assertNotIn(SECRET, output)

    def test_partial_retry_scrubs_only_remaining_matching_sources(self) -> None:
        texts = [
            "AI_CORP_DEBUG=false\n",
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
        ]
        temp, arvectum, sources, destination = self._layout(texts)
        self.addCleanup(temp.cleanup)
        destination.write_text(f"{SECRET}\n", encoding="utf-8")
        os.chmod(destination, 0o600)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("sources_already_scrubbed_before=1", output)
        self.assertIn("sources_scrubbed=2", output)
        for source, _ in sources:
            self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", source.read_text(encoding="utf-8"))

    def test_single_source_api_still_migrates_quoted_secret(self) -> None:
        temp, arvectum, sources, destination = self._layout(
            [f'ZAKUPKI_GOV_RU_SOAP_TOKEN="{SECRET}"\n']
        )
        self.addCleanup(temp.cleanup)
        source, product = sources[0]

        rc, lines = MODULE.migrate_secret(
            source,
            product,
            destination,
            arvectum_repo_root=arvectum,
        )

        self.assertEqual(rc, 0)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertNotIn(SECRET, "\n".join(lines))

    def test_export_form_is_supported(self) -> None:
        temp, arvectum, sources, destination = self._layout(
            [f"export ZAKUPKI_GOV_RU_SOAP_TOKEN='{SECRET}'\n"]
        )
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)

        self.assertEqual(rc, 0)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertNotIn(SECRET, "\n".join(lines))

    def test_no_secret_and_no_destination_fails_closed(self) -> None:
        temp, arvectum, sources, destination = self._layout(["AI_CORP_DEBUG=false\n"])
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_SOURCE_NOT_FOUND", "\n".join(lines))
        self.assertFalse(destination.exists())

    def test_duplicate_secret_key_fails_closed_without_value_output(self) -> None:
        text = (
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}-duplicate\n"
        )
        temp, arvectum, sources, destination = self._layout([text])
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_KEY_AMBIGUOUS", output)
        self.assertNotIn(SECRET, output)
        self.assertFalse(destination.exists())

    def test_placeholder_secret_fails_closed(self) -> None:
        temp, arvectum, sources, destination = self._layout(
            ["ZAKUPKI_GOV_RU_SOAP_TOKEN=replace_me_do_not_commit_real_token\n"]
        )
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_NOT_CONFIGURED", "\n".join(lines))
        self.assertFalse(destination.exists())

    def test_broad_source_permissions_fail_before_reading_secret(self) -> None:
        temp, arvectum, sources, destination = self._layout(
            [f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"],
            source_mode=0o644,
        )
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SOURCE_ENV_PERMISSIONS_TOO_BROAD", output)
        self.assertNotIn(SECRET, output)
        self.assertFalse(destination.exists())

    def test_destination_inside_any_product_checkout_is_rejected(self) -> None:
        temp, arvectum, sources, _ = self._layout(
            [
                f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
                f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n",
            ]
        )
        self.addCleanup(temp.cleanup)
        destination = sources[1][1] / "eis-soap-token"

        rc, lines = MODULE.migrate_secret_set(sources, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DESTINATION_INSIDE_SOURCE_CHECKOUT", output)
        self.assertNotIn(SECRET, output)
        self.assertFalse(destination.exists())

    def test_duplicate_source_env_is_rejected(self) -> None:
        temp, arvectum, sources, destination = self._layout(
            [f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"]
        )
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret_set(
            [sources[0], sources[0]],
            destination,
            arvectum_repo_root=arvectum,
        )

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SOURCE_ENV_DUPLICATED", "\n".join(lines))
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
