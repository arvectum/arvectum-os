from __future__ import annotations

import ast
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
REFERENCE_ROOT = REPO_ROOT / "reference" / "python"
PHASE8_ROADMAP = REPO_ROOT / "docs" / "roadmap" / "PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md"
MASTER_ROADMAP = REPO_ROOT / "docs" / "roadmap" / "ROADMAP.md"
P811_REVIEW = REPO_ROOT / "docs" / "reviews" / "P8-11-ecosystem-architecture-hardening-adr-refactoring-lifecycle-disposition.md"
P808_REVIEW = REPO_ROOT / "docs" / "reviews" / "P8-08-multi-organization-isolation-cross-organization-security-validation.md"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "reference-python-ci.yml"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalized(path: Path) -> str:
    return " ".join(_text(path).split())


def _import_roots(path: Path) -> set[str]:
    tree = ast.parse(_text(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


class R28M8EcosystemCodeHealthGateTests(unittest.TestCase):
    """High-value non-regression checks for the M8 pre-closure code-health gate.

    These checks deliberately protect governed boundaries rather than arbitrary
    line-count, complexity or coverage thresholds. They do not turn the current
    reference harnesses into public/stable APIs and do not substitute for the
    full Reference Python regression suite.
    """

    def test_bounded_phase8_harnesses_do_not_gain_external_transport_side_effects(self) -> None:
        paths = (
            REFERENCE_ROOT / "p8_05_external_boundary_evidence.py",
            REFERENCE_ROOT / "p8_07_handover_interoperability.py",
            REFERENCE_ROOT / "arvectum_os_ref" / "external_consumer_onboarding.py",
        )
        forbidden = {"requests", "httpx", "urllib", "socket"}
        for path in paths:
            with self.subTest(path=path.name):
                self.assertFalse(
                    _import_roots(path) & forbidden,
                    f"{path.name} must remain bounded evidence rather than a live external transport client",
                )

    def test_external_consumer_onboarding_remains_internal_product_owned_and_non_authoritative(self) -> None:
        normalized = _normalized(
            REFERENCE_ROOT / "arvectum_os_ref" / "external_consumer_onboarding.py"
        ).lower()
        for marker in (
            "internal reference slice",
            "does not define a public sdk/api",
            "not a platform manifest",
            "grants no authentication, authorization, permission, organizational authority",
            "not a governed lifecycle model",
        ):
            self.assertIn(marker, normalized)

    def test_handover_proof_remains_non_public_and_external_transfer_fail_closed(self) -> None:
        normalized = _normalized(REFERENCE_ROOT / "p8_07_handover_interoperability.py").lower()
        for marker in (
            "not a public export api",
            "does not authorize a customer handover",
            "external transfer activation is outside the current p8.07 proof",
            '"external_effect_replay_authorized": false',
            '"cross_organization_transfer": false',
        ):
            self.assertIn(marker, normalized)

    def test_realistic_multi_organization_claim_remains_explicitly_unproven(self) -> None:
        review = _normalized(P808_REVIEW).upper()
        roadmap = _normalized(PHASE8_ROADMAP).upper()
        self.assertIn("NOT ACTIVATED", review)
        self.assertIn("NOT PROVEN", review)
        self.assertIn("P8.08", roadmap)
        self.assertIn("NOT PROVEN", roadmap)

    def test_no_accepted_adr_or_public_surface_is_accidentally_introduced(self) -> None:
        adr_files = sorted(
            path.name
            for path in (REPO_ROOT / "docs" / "adrs").glob("*.md")
            if path.name != "README.md"
        )
        self.assertEqual(adr_files, [])
        review = _normalized(P811_REVIEW).lower()
        for marker in (
            "no new adr is justified",
            "public sdk/api",
            "defer / not admitted",
            "retain incubating / provisional",
        ):
            self.assertIn(marker, review)

    def test_repository_generated_artifact_guard_remains_enabled(self) -> None:
        workflow = _text(CI_WORKFLOW)
        self.assertIn("Reject tracked Python generated artifacts", workflow)
        self.assertIn("__pycache__", workflow)
        self.assertIn("\\.py[co]$", workflow)
        self.assertIn("\\.pytest_cache/", workflow)

    def test_r28_completion_remains_ordered_before_p8_12_without_transient_status_coupling(self) -> None:
        phase8 = _normalized(PHASE8_ROADMAP)
        master = _normalized(MASTER_ROADMAP)
        r28_heading = "### R28 — M8 Ecosystem Hardening + Milestone Code Health Gate"
        p812_heading = "### P8.12 — Phase 8 / M8 closure review"
        r28_row = "| `R28` | M8 Ecosystem Hardening + Milestone Code Health Gate |"
        p812_row = "| `P8.12` | Phase 8 / M8 closure review |"

        r28 = phase8.index(r28_heading)
        p812 = phase8.index(p812_heading)
        self.assertLess(r28, p812)
        r28_section = phase8[r28:p812]
        self.assertIn("Status: Complete / PASS", r28_section)
        self.assertIn("Milestone gate:", r28_section)
        self.assertIn("M8 Milestone Code Health Gate", r28_section)
        self.assertIn("does not itself close M8", r28_section)

        for roadmap_name, roadmap in (("phase8", phase8), ("master", master)):
            with self.subTest(roadmap=roadmap_name):
                self.assertIn(r28_row, roadmap)
                self.assertIn(p812_row, roadmap)
                self.assertLess(roadmap.index(r28_row), roadmap.index(p812_row))
                self.assertIn(
                    "| `R28` | M8 Ecosystem Hardening + Milestone Code Health Gate | 🟩 Complete / PASS |",
                    roadmap,
                )
                self.assertIn(
                    "| `P8.12` | Phase 8 / M8 closure review | 🟨 Current |",
                    roadmap,
                )
                self.assertIn(
                    "> **P8.12 — Phase 8 / M8 closure review.**",
                    roadmap,
                )


if __name__ == "__main__":
    unittest.main()
