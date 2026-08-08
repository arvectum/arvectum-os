from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import unittest


class P406DocumentArtifactWorkspaceDemoTests(unittest.TestCase):
    def test_static_demo_renders_document_artifact_semantics_without_server(self) -> None:
        reference_root = Path(__file__).parents[1]
        demo = reference_root / "examples" / "p4_06_document_artifact_workspace_demo.py"
        env = os.environ.copy()
        env["PYTHONPATH"] = str(reference_root)
        completed = subprocess.run(
            [sys.executable, str(demo)],
            cwd=reference_root,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        html = completed.stdout
        self.assertIn("Arvectum OS P4.06 Document / Artifact workspace", html)
        self.assertIn("data-document-workspace=\"open\"", html)
        self.assertIn("operating-standard", html)
        self.assertIn("operating-standard-v1", html)
        self.assertIn("operating-standard-v2", html)
        self.assertIn("standard-v1-source", html)
        self.assertIn("standard-v1-pdf", html)
        self.assertIn("render-to-pdf", html)
        self.assertIn("working-candidate-v3", html)
        self.assertIn("Non-canonical candidate", html)
        self.assertIn("no admission/promotion control", html)
        self.assertIn("present, value hidden", html)
        self.assertNotIn("internal-demo://", html)
        self.assertNotIn("content:standard", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)


if __name__ == "__main__":
    unittest.main()
