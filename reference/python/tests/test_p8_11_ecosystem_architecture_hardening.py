from __future__ import annotations

import ast
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = TEST_ROOT.parent
SOURCE_ROOT = PYTHON_ROOT / "arvectum_os_ref"
REPO_ROOT = TEST_ROOT.parents[2]
DOCS_ROOT = REPO_ROOT / "docs"

CAPABILITY_IDS = ("CAP-001", "CAP-002", "CAP-003", "CAP-004")


class P811EcosystemArchitectureHardeningTests(unittest.TestCase):
    """Guards the bounded historical P8.11 ADR/refactoring/lifecycle disposition."""

    @staticmethod
    def _section(text: str, start: str, end: str) -> str:
        return text.split(start, 1)[1].split(end, 1)[0]

    def test_capability_catalog_remains_incubating_provisional(self) -> None:
        catalog = (
            DOCS_ROOT / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md"
        ).read_text(encoding="utf-8")
        summary = self._section(
            catalog,
            "## 2. Current capability summary",
            "## 3. Retained boundaries",
        )
        rows = {
            capability_id: next(
                line
                for line in summary.splitlines()
                if line.startswith(f"| `{capability_id}` |")
            )
            for capability_id in CAPABILITY_IDS
        }
        self.assertEqual(set(rows), set(CAPABILITY_IDS))
        for capability_id, row in rows.items():
            with self.subTest(capability=capability_id):
                self.assertIn("| `Incubating` | `Provisional` |", row)
                self.assertNotIn("| `Active` |", row)

    def test_external_onboarding_remains_bounded_reference_not_platform_registry(self) -> None:
        path = SOURCE_ROOT / "external_consumer_onboarding.py"
        source = path.read_text(encoding="utf-8")
        module_docstring = ast.get_docstring(ast.parse(source, filename=str(path))) or ""
        lowered = " ".join(module_docstring.lower().split())
        self.assertIn("internal reference slice", lowered)
        self.assertIn("does not define a public sdk/api", lowered)
        self.assertIn("package/registry protocol", lowered)
        self.assertIn("capability lifecycle transition", lowered)
        self.assertIn("product-owned source declaration", lowered)

    def test_portability_and_multi_org_non_claims_remain_explicit(self) -> None:
        p807 = (
            DOCS_ROOT
            / "reviews"
            / "P8-07-portability-export-migration-customer-handover-interoperability-proof.md"
        ).read_text(encoding="utf-8")
        p808 = (
            DOCS_ROOT
            / "reviews"
            / "P8-08-multi-organization-isolation-cross-organization-security-validation.md"
        ).read_text(encoding="utf-8")

        self.assertIn("external customer transfer NOT ACTIVATED", p807)
        self.assertIn("Actual customer/cross-Organization transfer is `NOT ACTIVATED`", p807)
        self.assertIn("realistic two-Organization isolation remains unproven", p808)
        self.assertIn("Complete / NOT ACTIVATED", p808)

    def test_p8_11_adr_disposition_remains_historical_and_bounded(self) -> None:
        review = (
            DOCS_ROOT
            / "reviews"
            / "P8-11-ecosystem-architecture-hardening-adr-refactoring-lifecycle-disposition.md"
        ).read_text(encoding="utf-8")
        self.assertIn("**ADR decision: no new ADR is justified at P8.11.**", review)
        self.assertIn("CAP-004", review)
        self.assertIn("Retain Incubating / Provisional — stronger external reuse evidence", review)
        self.assertIn("No material runtime refactor is justified", review)

    def test_root_readme_defers_current_action_to_canonical_roadmap(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/roadmap/ROADMAP.md", readme)
        self.assertIn("only canonical source for current action", readme)
        self.assertNotIn("The current canonical action is **P6.03", readme)
        self.assertNotIn("The current canonical action is **P8.11", readme)
        self.assertNotIn("The current canonical action is **R28", readme)
        self.assertNotIn("The current canonical action is **P8.12", readme)

    def test_p8_11_review_preserves_next_hardening_gate_and_non_promotions(self) -> None:
        review = (
            DOCS_ROOT
            / "reviews"
            / "P8-11-ecosystem-architecture-hardening-adr-refactoring-lifecycle-disposition.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Status: `Complete / PASS", review)
        self.assertIn("No capability is promoted to `Active`", review)
        self.assertIn("P8.08 realistic two-Organization isolation remains explicitly unproven", review)
        self.assertIn("`R28 — M8 Ecosystem Hardening + Milestone Code Health Gate`", review)
        self.assertIn("P8.12 remains after R28", review)

    def test_phase_and_master_roadmaps_preserve_p8_11_hardening_sequence(self) -> None:
        phase8 = (
            DOCS_ROOT / "roadmap" / "PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md"
        ).read_text(encoding="utf-8")
        master = (DOCS_ROOT / "roadmap" / "ROADMAP.md").read_text(encoding="utf-8")

        p811_row = "| `P8.11` | Ecosystem architecture hardening + ADR/refactoring/lifecycle disposition |"
        r28_row = "| `R28` | M8 Ecosystem Hardening + Milestone Code Health Gate |"
        p812_row = "| `P8.12` | Phase 8 / M8 closure review |"

        self.assertIn(p811_row, phase8)
        self.assertIn(r28_row, phase8)
        self.assertIn(p812_row, phase8)
        self.assertLess(phase8.index(p811_row), phase8.index(r28_row))
        self.assertLess(phase8.index(r28_row), phase8.index(p812_row))
        p811_line = next(
            line for line in phase8.splitlines() if line.startswith(p811_row)
        )
        self.assertIn("🟩 Complete / PASS", p811_line)

        phase8_rows = [
            line
            for line in master.splitlines()
            if line.startswith("| `Phase 8` | Ecosystem and External Integration |")
        ]
        self.assertEqual(len(phase8_rows), 1)
        self.assertIn("🟩 Complete / PASS", phase8_rows[0])
        self.assertIn("M8", phase8_rows[0])
        self.assertIn("exact activated one-Organization scope", phase8_rows[0])


if __name__ == "__main__":
    unittest.main()
