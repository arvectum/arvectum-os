from __future__ import annotations

import unittest
from pathlib import Path

import p7_06_ui2_governed_interaction as ui2
import p7_06_ui3_private_operator as ui3


class _FakeServer:
    server_address = ("127.0.0.1", 8766)


class _FakeHandler:
    def __init__(self, *, origin: str | None = "http://127.0.0.1:8766") -> None:
        self.server = _FakeServer()
        self.headers: dict[str, str] = {"Host": "127.0.0.1:8766"}
        if origin is not None:
            self.headers["Origin"] = origin
        self.sent_headers: list[tuple[str, str]] = []

    def send_header(self, name: str, value: str) -> None:
        self.sent_headers.append((name, value))


class P706UI3BrowserUnlockCompatibilityTests(unittest.TestCase):
    def test_private_ui_uses_same_origin_referrer_policy_for_strict_form_origin(self) -> None:
        handler = _FakeHandler()
        ui2._security_headers(handler)
        headers = dict(handler.sent_headers)

        # A no-referrer policy can cause ordinary browser form POSTs to carry
        # Origin: null in some user agents.  The private UI keeps the stricter
        # exact-Origin server check and instead limits referrer disclosure to
        # the same loopback origin only.
        self.assertEqual(headers["Referrer-Policy"], "same-origin")
        self.assertEqual(headers["X-Frame-Options"], "DENY")
        self.assertIn("form-action 'self'", headers["Content-Security-Policy"])

    def test_same_origin_server_boundary_remains_exact_and_fail_closed(self) -> None:
        ui2._require_same_origin(_FakeHandler())

        for origin in (None, "null", "http://evil.invalid", "http://127.0.0.1:8765"):
            with self.subTest(origin=origin), self.assertRaises(ui2.UI2BoundaryError):
                ui2._require_same_origin(_FakeHandler(origin=origin))

        wrong_host = _FakeHandler()
        wrong_host.headers["Host"] = "localhost:8766"
        with self.assertRaises(ui2.UI2BoundaryError):
            ui2._require_same_origin(wrong_host)

    def test_ui3_unlock_still_inherits_shared_security_headers(self) -> None:
        source = Path(ui3.__file__).read_text(encoding="utf-8")
        self.assertIn("ui2._security_headers(self)", source)
        self.assertIn('form method="post" action="{UNLOCK}"', source)
        self.assertIn('type="hidden" name="csrf"', source)


if __name__ == "__main__":
    unittest.main()
