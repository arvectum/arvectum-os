from __future__ import annotations

import io
import unittest
from types import SimpleNamespace

import p7_06_ui2_governed_interaction as ui2


class P706UI2AdditionalHTTPBoundaryTests(unittest.TestCase):
    @staticmethod
    def _handler(*, host_header: str, body: bytes = b"", content_type: str = "application/x-www-form-urlencoded"):
        return SimpleNamespace(
            server=SimpleNamespace(server_address=("127.0.0.1", 8766)),
            headers={
                "Host": host_header,
                "Content-Type": content_type,
                "Content-Length": str(len(body)),
            },
            rfile=io.BytesIO(body),
        )

    def test_loopback_host_header_is_exact_and_blocks_dns_rebinding_shape(self) -> None:
        allowed = self._handler(host_header="127.0.0.1:8766")
        ui2._require_loopback_host(allowed)

        for hostile in ("evil.invalid", "evil.invalid:8766", "127.0.0.1.evil.invalid:8766"):
            with self.subTest(hostile=hostile):
                with self.assertRaises(ui2.UI2BoundaryError):
                    ui2._require_loopback_host(self._handler(host_header=hostile))

    def test_malformed_form_encoding_is_a_boundary_denial_not_runtime_failure(self) -> None:
        malformed = b"interaction_id=one&csrf"
        handler = self._handler(host_header="127.0.0.1:8766", body=malformed)
        with self.assertRaises(ui2.UI2BoundaryError):
            ui2._read_form(handler)

    def test_browser_form_shape_cannot_supply_governed_evidence(self) -> None:
        forged = b"interaction_id=one&csrf=token&gate=allow"
        handler = self._handler(host_header="127.0.0.1:8766", body=forged)
        with self.assertRaises(ui2.UI2BoundaryError):
            ui2._read_form(handler)


if __name__ == "__main__":
    unittest.main()
