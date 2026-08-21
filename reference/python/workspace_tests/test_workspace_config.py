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


if __name__ == "__main__":
    unittest.main()
