from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

import p6_05_l3_secure_local_config as MODULE


VALID_TOKEN = "TEST_SECRET_VALUE_DO_NOT_PRINT_4f71977f"
VALID_CONFIG = """\
ZAKUPKI_GOV_RU_SOAP_ENABLED=1
ZAKUPKI_GOV_RU_SOAP_TOKEN_OWNER=individual
ZAKUPKI_GOV_RU_SOAP_DISABLE_PROXY_FOR_EIS=1
ZAKUPKI_GOV_RU_SOAP_REQUIRE_DIRECT_RU_ROUTE=1
ZAKUPKI_GOV_RU_SOAP_TRUST_ENV_PROXY=0
ZAKUPKI_GOV_RU_SOAP_DEBUG=0
"""


class P605L3SecureLocalConfigTests(unittest.TestCase):
    def _external_files(
        self,
        *,
        config_text: str = VALID_CONFIG,
        secret_text: str = VALID_TOKEN,
        config_mode: int = 0o600,
        secret_mode: int = 0o600,
    ):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        repo = root / "source-checkout"
        repo.mkdir(mode=0o700)
        config_dir = root / "local-config"
        secret_dir = root / "local-secrets"
        config_dir.mkdir(mode=0o700)
        secret_dir.mkdir(mode=0o700)
        os.chmod(config_dir, 0o700)
        os.chmod(secret_dir, 0o700)
        config = config_dir / "p6-05-l3.env"
        secret = secret_dir / "eis-soap-token"
        config.write_text(config_text, encoding="utf-8")
        secret.write_text(secret_text, encoding="utf-8")
        os.chmod(config, config_mode)
        os.chmod(secret, secret_mode)
        return temp, repo, config, secret

    def test_separate_owner_only_config_and_secret_pass_without_secret_output(self) -> None:
        temp, repo, config, secret = self._external_files()
        self.addCleanup(temp.cleanup)
        rc, lines = MODULE.run_preflight(config, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 0)
        self.assertIn("p6_05_l3_status=PASS", output)
        self.assertIn("secret.ZAKUPKI_GOV_RU_SOAP_TOKEN=configured", output)
        self.assertNotIn(VALID_TOKEN, output)

    def test_secret_value_in_nonsecret_config_fails_closed(self) -> None:
        text = VALID_CONFIG + f"ZAKUPKI_GOV_RU_SOAP_TOKEN={VALID_TOKEN}\n"
        temp, repo, config, secret = self._external_files(config_text=text)
        self.addCleanup(temp.cleanup)
        rc, lines = MODULE.run_preflight(config, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_VALUE_IN_NONSECRET_CONFIG", output)
        self.assertNotIn(VALID_TOKEN, output)

    def test_placeholder_secret_fails_closed_without_printing_value(self) -> None:
        placeholder = "replace_me_do_not_commit_real_token"
        temp, repo, config, secret = self._external_files(secret_text=placeholder)
        self.addCleanup(temp.cleanup)
        rc, lines = MODULE.run_preflight(config, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_NOT_CONFIGURED", output)
        self.assertNotIn(placeholder, output)

    def test_broad_secret_file_permissions_fail_closed(self) -> None:
        temp, repo, config, secret = self._external_files(secret_mode=0o644)
        self.addCleanup(temp.cleanup)
        rc, lines = MODULE.run_preflight(config, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_FILE_PERMISSIONS_TOO_BROAD", output)
        self.assertNotIn(VALID_TOKEN, output)

    def test_config_inside_source_control_is_rejected_before_read(self) -> None:
        temp, repo, config, secret = self._external_files()
        self.addCleanup(temp.cleanup)
        inside = repo / "local.env"
        inside.write_text(VALID_CONFIG, encoding="utf-8")
        os.chmod(inside, 0o600)
        rc, lines = MODULE.run_preflight(inside, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONFIG_INSIDE_SOURCE_CONTROL", output)
        self.assertNotIn(VALID_TOKEN, output)

    def test_wrong_security_control_fails_without_echoing_actual_value(self) -> None:
        unsafe = "unsafe-debug-value"
        text = VALID_CONFIG.replace("ZAKUPKI_GOV_RU_SOAP_DEBUG=0", f"ZAKUPKI_GOV_RU_SOAP_DEBUG={unsafe}")
        temp, repo, config, secret = self._external_files(config_text=text)
        self.addCleanup(temp.cleanup)
        rc, lines = MODULE.run_preflight(config, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_subject=ZAKUPKI_GOV_RU_SOAP_DEBUG", output)
        self.assertNotIn(unsafe, output)
        self.assertNotIn(VALID_TOKEN, output)

    def test_undeclared_key_is_rejected_from_nonsecret_config(self) -> None:
        text = VALID_CONFIG + "UNDECLARED_LOCAL_VALUE=should-not-be-here\n"
        temp, repo, config, secret = self._external_files(config_text=text)
        self.addCleanup(temp.cleanup)
        rc, lines = MODULE.run_preflight(config, secret, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=UNDECLARED_CONFIG_KEY", output)
        self.assertNotIn("should-not-be-here", output)
        self.assertNotIn(VALID_TOKEN, output)

    def test_secret_symlink_is_rejected(self) -> None:
        temp, repo, config, secret = self._external_files()
        self.addCleanup(temp.cleanup)
        link = secret.parent / "eis-token-link"
        link.symlink_to(secret)
        rc, lines = MODULE.run_preflight(config, link, repo_root=repo)
        output = "\n".join(lines)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=SECRET_SYMLINK_NOT_ALLOWED", output)
        self.assertNotIn(VALID_TOKEN, output)


if __name__ == "__main__":
    unittest.main()
