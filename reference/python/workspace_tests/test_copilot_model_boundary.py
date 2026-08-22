from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from workspace_app.copilot import CopilotEvidence, LoopbackChatModel


class _ModelResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self, limit: int) -> bytes:
        return json.dumps(
            {"choices": [{"message": {"content": "Grounded synthesis with explicit uncertainty."}}]}
        ).encode("utf-8")


class LoopbackModelBoundaryTests(unittest.TestCase):
    def test_model_packet_withholds_opaque_workspace_identity_and_keeps_grounding_metadata(self) -> None:
        evidence = (
            CopilotEvidence(
                source_id="object:opaque-secret-workspace-id",
                label="Inspectable notice",
                summary="Current Workspace evidence points to an External Reference.",
                authority="External Reference · authoritative source",
                freshness="fresh",
                open_href="/objects/opaque-secret-workspace-id",
                semantic_role="Document",
                knowledge_role=None,
            ),
        )
        captured: dict[str, object] = {}

        def fake_urlopen(request, timeout: int):
            captured["timeout"] = timeout
            captured["payload"] = json.loads(request.data.decode("utf-8"))
            return _ModelResponse()

        model = LoopbackChatModel("http://127.0.0.1:8080/v1/chat/completions", "bounded-local", 12)
        with patch("workspace_app.copilot.urlopen", side_effect=fake_urlopen):
            result = model.synthesize("What is the current status?", evidence)

        self.assertEqual(result, "Grounded synthesis with explicit uncertainty.")
        self.assertEqual(captured["timeout"], 12)
        payload = captured["payload"]
        self.assertIsInstance(payload, dict)
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("opaque-secret-workspace-id", serialized)
        self.assertNotIn("/objects/", serialized)
        self.assertIn("Inspectable notice", serialized)
        self.assertIn("External Reference", serialized)
        self.assertIn("fresh", serialized)
        self.assertIn("untrusted data", serialized)


if __name__ == "__main__":
    unittest.main()
