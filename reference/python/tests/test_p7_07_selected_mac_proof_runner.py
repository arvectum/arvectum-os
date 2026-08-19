import unittest
from pathlib import Path
from types import SimpleNamespace

import p7_07_selected_mac_proof_runner as proof


class P707SelectedMacProofRunnerTests(unittest.TestCase):
    def test_same_reliance_requires_exact_item_subject_version_artifact_integrity_authority_and_contract(self):
        base = dict(
            storage_item_id="a" * 64,
            subject_identity="document-subject/s@o",
            version_identity="document-version/v@o",
            artifact_identity="artifact/a@o",
            integrity_ref="sha256:" + "b" * 64,
            authoritative_source="ЕИС / zakupki.gov.ru",
            product_contract_version="0.1.0",
        )
        first = SimpleNamespace(**base)
        second = SimpleNamespace(**base)
        self.assertTrue(proof._same_reliance(first, second))
        changed = SimpleNamespace(**{**base, "version_identity": "document-version/v2@o"})
        self.assertFalse(proof._same_reliance(first, changed))

    def test_product_origin_allowlist_contains_only_canonical_repository_forms(self):
        self.assertTrue(proof.CANONICAL_PRODUCT_ORIGINS)
        for value in proof.CANONICAL_PRODUCT_ORIGINS:
            self.assertIn("arvectum/tender-agent", value)
            self.assertNotIn("arutyunoveth", value)

    def test_proof_source_uses_existing_p702_restart_and_no_network_fetch(self):
        source = Path(proof.__file__).read_text(encoding="utf-8")
        self.assertIn('"p7_02_macos_service.sh"', source)
        self.assertIn('"restart"', source)
        self.assertIn('after_health["generation"] <= before_health["generation"]', source)
        self.assertIn('after_health.get("previous_instance_id") != before_health["instance_id"]', source)
        self.assertIn("_state_digest(runtime_root)", source)
        self.assertNotIn("git fetch", source)
        self.assertNotIn("requests", source)
        self.assertNotIn("urllib.request", source)
        self.assertNotIn("getDocsIP(", source)


if __name__ == "__main__":
    unittest.main()
