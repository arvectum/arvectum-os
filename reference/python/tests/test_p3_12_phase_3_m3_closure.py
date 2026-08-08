from __future__ import annotations

from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TEST_ROOT.parents[2]
DOCS_ROOT = REPO_ROOT / "docs"
CAPABILITY_IDS = ("CAP-001", "CAP-002", "CAP-003", "CAP-004")


class P312Phase3M3ClosureTests(unittest.TestCase):
    """Guards the bounded Phase 3 / M3 closure state without freezing later phases."""

    def test_canonical_closure_review_records_bounded_m3_pass(self) -> None:
        review = (
            DOCS_ROOT / "reviews" / "P3-12-phase-3-m3-closure-review.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Status: `Complete`", review)
        self.assertIn("Milestone: `M3 — Validated shared capability baseline` — `Achieved`", review)
        self.assertIn(
            "PASS — M3 achieved for the declared bounded shared-capability reference scope.",
            review,
        )
        self.assertIn("CAP-001 through CAP-004 remain `Incubating / Provisional`", review)
        self.assertIn("Phase 4 is **not automatically activated**", review)

    def test_phase_3_roadmap_is_closed_without_capability_promotion(self) -> None:
        roadmap = (
            DOCS_ROOT / "roadmap" / "PHASE-3-SHARED-PLATFORM-CAPABILITIES.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Status: `Complete`", roadmap)
        self.assertIn("Milestone: `M3 — Validated shared capability baseline` — `Achieved`", roadmap)
        self.assertIn(
            "| `P3.12` | Phase 3 / M3 closure review | 🟩 Complete / PASS | `██████████ 100%` |",
            roadmap,
        )
        for capability_id in CAPABILITY_IDS:
            self.assertNotIn(f"{capability_id} | `Active`", roadmap)

    def test_canonical_roadmap_preserves_m3_scope_as_later_phases_progress(self) -> None:
        roadmap = (DOCS_ROOT / "roadmap" / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn(
            "| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |",
            roadmap,
        )
        self.assertIn("| `Phase 4` | Workspace / Operator Experience |", roadmap)
        self.assertIn(
            "Phase status, capability lifecycle, operational environment and conformance maturity remain distinct.",
            roadmap,
        )
        self.assertIn(
            "M3 does not imply lifecycle `Active`, operational readiness, Stable Product Contracts, public API compatibility, production deployment or customer-facing SLA/support commitments.",
            roadmap,
        )

    def test_capability_catalog_preserves_exact_incubating_provisional_set(self) -> None:
        catalog = (
            DOCS_ROOT / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md"
        ).read_text(encoding="utf-8")

        for capability_id in CAPABILITY_IDS:
            rows = [
                line
                for line in catalog.splitlines()
                if line.startswith(f"| `{capability_id}` |")
            ]
            self.assertEqual(len(rows), 1, capability_id)
            self.assertIn("| `Incubating` | `Provisional` |", rows[0])
            self.assertIn("M3 achieved", rows[0])
            self.assertNotIn("| `Active` |", rows[0])

    def test_root_readme_preserves_m3_scope_as_phase_4_progresses(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("`Phase 3 — Shared Platform Capabilities` is complete", readme)
        self.assertIn("`M3 — Validated shared capability baseline` is achieved", readme)
        self.assertIn("`Phase 4 — Workspace / Operator Experience`", readme)
        self.assertIn(
            "M3 closure does not promote any capability to `Active`",
            readme,
        )
        self.assertIn(
            "Phase status, capability lifecycle, operational environment and conformance maturity remain distinct.",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
