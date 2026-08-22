from __future__ import annotations

import unittest
from unittest.mock import patch

from workspace_app.config import ConfigurationError, WorkspaceSettings


class WorkspaceSettingsTests(unittest.TestCase):
    def test_http_profile_is_loopback_only(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "ARVECTUM_WORKSPACE_ORIGIN": "http://0.0.0.0:8769",
                "ARVECTUM_WORKSPACE_BIND_HOST": "0.0.0.0",
                "ARVECTUM_WORKSPACE_ALLOW_LOOPBACK_HTTP": "true",
            },
            clear=True,
        ):
            with self.assertRaises(ConfigurationError):
                WorkspaceSettings.from_env()

    def test_origin_host_must_be_allowlisted(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "ARVECTUM_WORKSPACE_ORIGIN": "http://127.0.0.1:8769",
                "ARVECTUM_WORKSPACE_BIND_HOST": "127.0.0.1",
                "ARVECTUM_WORKSPACE_ALLOWED_HOSTS": "localhost:8769",
            },
            clear=True,
        ):
            with self.assertRaises(ConfigurationError):
                WorkspaceSettings.from_env()

    def test_copilot_model_endpoint_is_opt_in_and_loopback_only(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            settings = WorkspaceSettings.from_env()
            self.assertIsNone(settings.copilot_model_url)

        with patch.dict(
            "os.environ",
            {"ARVECTUM_WORKSPACE_COPILOT_MODEL_URL": "http://127.0.0.1:8080/v1/chat/completions"},
            clear=True,
        ):
            settings = WorkspaceSettings.from_env()
            self.assertEqual(settings.copilot_model_url, "http://127.0.0.1:8080/v1/chat/completions")

        with patch.dict(
            "os.environ",
            {"ARVECTUM_WORKSPACE_COPILOT_MODEL_URL": "https://external-model.example/v1/chat/completions"},
            clear=True,
        ):
            with self.assertRaises(ConfigurationError):
                WorkspaceSettings.from_env()

    def test_copilot_model_endpoint_cannot_embed_credentials(self) -> None:
        with patch.dict(
            "os.environ",
            {"ARVECTUM_WORKSPACE_COPILOT_MODEL_URL": "http://user:secret@127.0.0.1:8080/v1/chat/completions"},
            clear=True,
        ):
            with self.assertRaises(ConfigurationError):
                WorkspaceSettings.from_env()


if __name__ == "__main__":
    unittest.main()
