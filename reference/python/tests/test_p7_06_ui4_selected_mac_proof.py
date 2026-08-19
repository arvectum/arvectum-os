from __future__ import annotations

import pathlib
import unittest

import p7_06_ui4_selected_mac_proof as proof


class UI4SelectedMacProofSourceTests(unittest.TestCase):
    def test_verifier_self_pins_to_exact_current_release(self):
        text = pathlib.Path(proof.__file__).read_text(encoding="utf-8")
        self.assertIn("release_sha = ui3.verify_exact_release(root)", text)
        self.assertIn('Path(__file__).name', text)
        self.assertIn('Path(__file__).resolve() != pinned.resolve()', text)
        self.assertIn('current.release_sha != release_sha', text)

    def test_verifier_cannot_attest_human_visual_navigation(self):
        text = pathlib.Path(proof.__file__).read_text(encoding="utf-8")
        self.assertIn('"human_visual_navigation_attested": False', text)
        self.assertIn('"operator_friction_review_pending": True', text)
        self.assertNotIn('"human_visual_navigation_attested": True', text)


if __name__ == "__main__":
    unittest.main()
