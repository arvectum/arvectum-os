from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

import p6_05_l3_migrate_eis_secret as MODULE


SECRET = "TEST_EIS_SECRET_DO_NOT_PRINT_3b7fcb8d"


class P605L3MigrateEisSecretTests(unittest.TestCase):
    def _layout(self, source_text: str, *, source_mode: int = 0o600):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        arvectum = root / "arvectum-os"
        product = root / "AI-Corporation"
        local = root / "local-secrets"
        arvectum.mkdir(mode=0o700)
        product.mkdir(mode=0o700)
        local.mkdir(mode=0o700)
        os.chmod(arvectum, 0o700)
        os.chmod(product, 0o700)
        os.chmod(local, 0o700)
        source = product / ".env.local"
        source.write_text(source_text, encoding="utf-8")
        os.chmod(source, source_mode)
        destination = local / "eis-soap-token"
        return temp, arvectum, product, source, destination

    def test_migrates_once_without_printing_or_hashing_secret(self) -> None:
        source_text = (
            "AI_CORP_DEBUG=false\n"
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
            "ZAKUPKI_GOV_RU_SOAP_ENABLED=1\n"
        )
        temp, arvectum, product, source, destination = self._layout(source_text)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(
            source,
            product,
            destination,
            arvectum_repo_root=arvectum,
        )
        output = "\n".join(lines)

        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_secret_migration_status=PASS", output)
        self.assertIn("source_secret_removed=true", output)
        self.assertNotIn(SECRET, output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertEqual(os.stat(destination).st_mode & 0o777, 0o600)
        remaining = source.read_text(encoding="utf-8")
        self.assertNotIn("ZAKUPKI_GOV_RU_SOAP_TOKEN", remaining)
        self.assertIn("AI_CORP_DEBUG=false", remaining)
        self.assertIn("ZAKUPKI_GOV_RU_SOAP_ENABLED=1", remaining)

    def test_quoted_secret_is_migrated_without_quotes(self) -> None:
        source_text = f'ZAKUPKI_GOV_RU_SOAP_TOKEN="{SECRET}"\n'
        temp, arvectum, product, source, destination = self._layout(source_text)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)

        self.assertEqual(rc, 0)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertNotIn(SECRET, "\n".join(lines))

    def test_export_form_is_supported_for_legacy_shell_sourced_env(self) -> None:
        source_text = f"export ZAKUPKI_GOV_RU_SOAP_TOKEN='{SECRET}'\n"
        temp, arvectum, product, source, destination = self._layout(source_text)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)

        self.assertEqual(rc, 0)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), SECRET)
        self.assertNotIn(SECRET, "\n".join(lines))

    def test_missing_secret_key_fails_closed(self) -> None:
        temp, arvectum, product, source, destination = self._layout("AI_CORP_DEBUG=false\n")
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_KEY_NOT_FOUND", output)
        self.assertFalse(destination.exists())

    def test_duplicate_secret_key_fails_closed_without_value_output(self) -> None:
        source_text = (
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
            f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}-duplicate\n"
        )
        temp, arvectum, product, source, destination = self._layout(source_text)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_KEY_AMBIGUOUS", output)
        self.assertNotIn(SECRET, output)
        self.assertFalse(destination.exists())

    def test_placeholder_secret_fails_closed(self) -> None:
        source_text = "ZAKUPKI_GOV_RU_SOAP_TOKEN=replace_me_do_not_commit_real_token\n"
        temp, arvectum, product, source, destination = self._layout(source_text)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_NOT_CONFIGURED", "\n".join(lines))
        self.assertFalse(destination.exists())

    def test_broad_source_permissions_fail_before_reading_secret(self) -> None:
        source_text = f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
        temp, arvectum, product, source, destination = self._layout(source_text, source_mode=0o644)
        self.addCleanup(temp.cleanup)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SOURCE_ENV_PERMISSIONS_TOO_BROAD", output)
        self.assertNotIn(SECRET, output)
        self.assertFalse(destination.exists())

    def test_destination_inside_product_checkout_is_rejected(self) -> None:
        source_text = f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
        temp, arvectum, product, source, _ = self._layout(source_text)
        self.addCleanup(temp.cleanup)
        destination = product / "eis-soap-token"

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DESTINATION_INSIDE_SOURCE_CHECKOUT", output)
        self.assertNotIn(SECRET, output)
        self.assertFalse(destination.exists())

    def test_existing_destination_is_never_overwritten(self) -> None:
        source_text = f"ZAKUPKI_GOV_RU_SOAP_TOKEN={SECRET}\n"
        temp, arvectum, product, source, destination = self._layout(source_text)
        self.addCleanup(temp.cleanup)
        destination.write_text("EXISTING_SAFE_SENTINEL\n", encoding="utf-8")
        os.chmod(destination, 0o600)

        rc, lines = MODULE.migrate_secret(source, product, destination, arvectum_repo_root=arvectum)
        output = "\n".join(lines)

        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DESTINATION_ALREADY_EXISTS", output)
        self.assertEqual(destination.read_text(encoding="utf-8").strip(), "EXISTING_SAFE_SENTINEL")
        self.assertNotIn(SECRET, output)


if __name__ == "__main__":
    unittest.main()
