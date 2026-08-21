from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
MASTER_ROADMAP = REPO_ROOT / "docs" / "roadmap" / "ROADMAP.md"
PHASE8_ROADMAP = REPO_ROOT / "docs" / "roadmap" / "PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md"
CLOSURE_REVIEW = REPO_ROOT / "docs" / "reviews" / "P8-12-phase-8-m8-closure-review.md"
LEGACY_CAPABILITY_CATALOG = REPO_ROOT / "docs" / "architecture" / "CAPABILITY-CATALOG.md"
ACTIVE_CAPABILITY_CATALOG = REPO_ROOT / "docs" / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md"
P803_CONTRACT = REPO_ROOT / "docs" / "contracts" / "P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md"
P806_CONTRACT = REPO_ROOT / "docs" / "contracts" / "P8-06-CREATIVE-TEST-AGENT-PROVISIONAL-PRODUCT-CONTRACT.md"
ADR_DIR = REPO_ROOT / "docs" / "adrs"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalized(path: Path) -> str:
    return " ".join(_text(path).split())


def _row(text: str, prefix: str) -> str:
    return next(line for line in text.splitlines() if line.startswith(prefix))


class P812Phase8M8ClosureTests(unittest.TestCase):
    """Stable historical guards for scoped Phase 8 / M8 closure.

    The tests deliberately protect the closure meaning and its non-claims. They
    do not pin a future master-roadmap current action, so a later separately
    governed phase can be admitted without rewriting P8.12 history.
    """

    def test_closure_review_records_scoped_m8_pass_and_conditional_multi_org_limit(self) -> None:
        review = _normalized(CLOSURE_REVIEW)
        self.assertIn("`P8.12 = Complete / PASS`", review)
        self.assertIn("`M8 = Achieved / PASS — exact activated scope only`", review)
        self.assertIn("exact activated one-Organization", review)
        self.assertIn("NOT ACTIVATED / NOT PROVEN", review)
        self.assertIn("NOT ACTIVATED / NOT APPLICABLE TO DECLARED SCOPE", review)
        self.assertIn("P8.12 closes Phase 8", review)
        self.assertIn("invent or admit Phase 9", review)

    def test_master_and_phase_roadmaps_preserve_historical_phase8_closure(self) -> None:
        master = _text(MASTER_ROADMAP)
        phase = _text(PHASE8_ROADMAP)

        phase8_row = _row(master, "| `Phase 8` | Ecosystem and External Integration |")
        self.assertIn("🟩 Complete / PASS", phase8_row)
        self.assertIn("M8", phase8_row)
        self.assertIn("achieved for exact activated scope", phase8_row)

        p812_master = _row(master, "| `P8.12` | Phase 8 / M8 closure review |")
        p812_phase = _row(phase, "| `P8.12` | Phase 8 / M8 closure review |")
        self.assertIn("🟩 Complete / PASS", p812_master)
        self.assertIn("🟩 Complete / PASS", p812_phase)
        self.assertIn("Status: `Complete / PASS`", phase)

    def test_unactivated_relationship_classes_are_not_upgraded_by_milestone_closure(self) -> None:
        review = _normalized(CLOSURE_REVIEW)
        phase = _normalized(PHASE8_ROADMAP)
        for text in (review, phase):
            self.assertIn("P8.08", text)
            self.assertIn("NOT ACTIVATED / NOT PROVEN", text)
            self.assertIn("P8.07", text)
            self.assertIn("external customer/cross-Organization transfer", text)
            self.assertIn("NOT ACTIVATED", text)
        self.assertIn("no synthetic multi-Organization proof", phase)

    def test_active_capability_catalog_remains_lifecycle_authority_and_legacy_view_is_retired(self) -> None:
        active_text = _text(ACTIVE_CAPABILITY_CATALOG)
        legacy = _normalized(LEGACY_CAPABILITY_CATALOG)

        self.assertIn("Status: `Active`", active_text)
        for cap in ("CAP-001", "CAP-002", "CAP-003", "CAP-004"):
            with self.subTest(capability=cap):
                row = _row(active_text, f"| `{cap}` |")
                self.assertIn("| `Incubating` | `Provisional` |", row)

        self.assertIn("Status: `Deprecated / Informative`", legacy)
        self.assertIn("PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md", legacy)
        self.assertIn("current lifecycle inventory", legacy)
        self.assertIn("**not**", legacy)
        self.assertIn("performs **no lifecycle transition**", legacy)
        self.assertNotIn("No capability is currently recorded as `Active` or `Incubating`", legacy)

    def test_phase8_product_contracts_remain_provisional_not_stable(self) -> None:
        for contract_path in (P803_CONTRACT, P806_CONTRACT):
            with self.subTest(contract=contract_path.name):
                contract = _normalized(contract_path)
                self.assertIn("Provisional", contract)
                self.assertIn("0.1.0", contract)
                self.assertNotIn("Lifecycle: `Stable`", contract)
                self.assertNotIn("Status: `Stable`", contract)

    def test_closure_introduces_no_accepted_adr_or_public_stable_commitment(self) -> None:
        adr_files = sorted(path.name for path in ADR_DIR.glob("*.md") if path.name != "README.md")
        self.assertEqual(adr_files, [])

        review = _normalized(CLOSURE_REVIEW).lower()
        for marker in (
            "no public/stable api, sdk, manifest, registry, connector protocol or export format is admitted",
            "no external/customer production",
            "no platform capability becomes `active`",
            "no product contract becomes `stable`",
        ):
            self.assertIn(marker, review)

    def test_post_m8_work_is_not_implicitly_admitted_by_p8_12(self) -> None:
        review = _normalized(CLOSURE_REVIEW)
        self.assertIn("No post-M8 numbered implementation phase is currently defined", review)
        self.assertIn("separate governed roadmap/activation decision", review)
        self.assertIn("P8.12 closes Phase 8", review)
        self.assertIn("invent or admit Phase 9", review)


if __name__ == "__main__":
    unittest.main()
