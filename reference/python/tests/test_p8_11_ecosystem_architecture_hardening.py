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
    """Guards the bounded P8.11 ADR/refactoring/lifecycle disposition."""

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
        lowered = module_docstring.lower()
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

    def test_no_adr_file_exists_without_revisiting_p8_11_disposition(self) -> None:
        adr_files = tuple(
            path.name
            for path in (DOCS_ROOT / "adrs").glob("ADR-*.md")
            if path.is_file()
        )
        self.assertEqual(adr_files, ())

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
        self.assertNotIn("The current canonical action is **P8.12", readme)

    def test_p8_11_review_preserves_next_closure_gate_and_non_promotions(self) -> None:
        review = (
            DOCS_ROOT
            / "reviews"
            / "P8-11-ecosystem-architecture-hardening-adr-refactoring-lifecycle-disposition.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Status: `Complete / PASS", review)
        self.assertIn("No capability is promoted to `Active`", review)
        self.assertIn("P8.08 realistic two-Organization isolation remains explicitly unproven", review)
        self.assertIn("`P8.12 — Phase 8 / M8 closure review`", review)


if __name__ == "__main__":
    unittest.main()
