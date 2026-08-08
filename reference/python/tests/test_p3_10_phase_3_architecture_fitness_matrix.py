from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = TEST_ROOT.parent
SOURCE_ROOT = PYTHON_ROOT / "arvectum_os_ref"
REPO_ROOT = TEST_ROOT.parents[2]
DOCS_ROOT = REPO_ROOT / "docs"


@dataclass(frozen=True)
class FitnessEvidence:
    test_file: str
    test_name: str


@dataclass(frozen=True)
class FitnessRow:
    matrix_id: str
    dimension: str
    authority: tuple[str, ...]
    roadmap_coverage: tuple[str, ...]
    evidence: tuple[FitnessEvidence, ...]


FITNESS_MATRIX = (
    FitnessRow(
        "FIT-01",
        "Bounded domain-neutral capability boundaries",
        ("RFC-0001 §§10–15", "RFC-0004 §§6, 14", "P3.02 Provisional capability contracts"),
        ("capability boundaries",),
        (
            FitnessEvidence(
                "test_p3_10_phase_3_architecture_fitness_matrix.py",
                "test_phase_3_capability_modules_are_product_domain_neutral",
            ),
            FitnessEvidence(
                "test_p3_09_shared_capability_reuse.py",
                "test_discovery_led_consumer_reuses_same_capabilities_over_document_source",
            ),
        ),
    ),
    FitnessRow(
        "FIT-02",
        "Incubating lifecycle, Provisional contracts and accountable ownership",
        ("RFC-0001 §§11.2–11.4", "P3.02 Provisional capability contracts", "Capability catalog"),
        ("lifecycle and ownership", "commercial and conformance restraint"),
        (
            FitnessEvidence(
                "test_p3_10_phase_3_architecture_fitness_matrix.py",
                "test_capability_lifecycle_and_owner_remain_incubating_provisional",
            ),
        ),
    ),
    FitnessRow(
        "FIT-03",
        "Document and Artifact immutable identity, admission and exact reliance",
        ("RFC-0002 §§8, 14", "RFC-0008 §§6–7, 17"),
        ("authority and provenance",),
        (
            FitnessEvidence(
                "test_p3_03_document_artifact_governance.py",
                "test_document_subject_identity_is_stable_across_immutable_versions",
            ),
            FitnessEvidence(
                "test_p3_03_document_artifact_governance.py",
                "test_transient_artifact_is_not_governed_merely_by_existing",
            ),
            FitnessEvidence(
                "test_p3_03_document_artifact_governance.py",
                "test_exact_reliance_pins_document_version_and_artifact_without_head_inference",
            ),
        ),
    ),
    FitnessRow(
        "FIT-04",
        "Memory and Knowledge epistemic separation, promotion gates and exact reliance",
        ("RFC-0007 §§6–8, 27",),
        ("authority and provenance",),
        (
            FitnessEvidence(
                "test_p3_04_memory_knowledge_governance.py",
                "test_memory_preserves_epistemic_role_without_silent_validation",
            ),
            FitnessEvidence(
                "test_p3_04_memory_knowledge_governance.py",
                "test_validation_and_approval_are_distinct_promotion_gates",
            ),
            FitnessEvidence(
                "test_p3_04_memory_knowledge_governance.py",
                "test_exact_reliance_pins_old_version_without_head_inference",
            ),
        ),
    ),
    FitnessRow(
        "FIT-05",
        "Search projection non-authority, current-policy enforcement and exact source resolution",
        ("RFC-0002 §8.7", "RFC-0007 §§15, 27", "RFC-0008 §21"),
        ("non-authoritative projections", "security rights and Organization scope"),
        (
            FitnessEvidence(
                "test_p3_05_search_index_projection.py",
                "test_projection_is_derived_and_has_no_canonical_authority_fields",
            ),
            FitnessEvidence(
                "test_p3_05_search_index_projection.py",
                "test_query_rechecks_current_constraints_without_rebuild",
            ),
            FitnessEvidence(
                "test_p3_05_search_index_projection.py",
                "test_hit_resolution_requires_separate_source_access_and_exact_current_version",
            ),
        ),
    ),
    FitnessRow(
        "FIT-06",
        "Audit reconstruction is derived, evidence-honest and read-only",
        ("RFC-0005 §26", "RFC-0006 §§6, 22"),
        ("authority and provenance", "non-authoritative projections"),
        (
            FitnessEvidence(
                "test_p3_06_audit_reconstruction_support.py",
                "test_complete_view_is_derived_and_preserves_exact_references",
            ),
            FitnessEvidence(
                "test_p3_06_audit_reconstruction_support.py",
                "test_deleted_unavailable_and_missing_evidence_are_not_invented",
            ),
            FitnessEvidence(
                "test_p3_06_audit_reconstruction_support.py",
                "test_reconstruction_is_read_only_and_never_replays_execution",
            ),
        ),
    ),
    FitnessRow(
        "FIT-07",
        "Cross-capability Organization, purpose, right and classification enforcement",
        ("RFC-0003 §§14–17, 28–29", "RFC-0001 §§17, 19"),
        ("security rights and Organization scope",),
        (
            FitnessEvidence(
                "test_p3_07_cross_capability_enforcement.py",
                "test_cap001_denies_cross_organization_and_rights_mismatch",
            ),
            FitnessEvidence(
                "test_p3_07_cross_capability_enforcement.py",
                "test_cap003_discovery_and_source_access_use_same_context",
            ),
            FitnessEvidence(
                "test_p3_07_cross_capability_enforcement.py",
                "test_cap004_redacts_disallowed_evidence_and_denies_foreign_organization",
            ),
        ),
    ),
    FitnessRow(
        "FIT-08",
        "Authorization, data governance, validation and Organizational Authority remain distinct",
        ("RFC-0003 §6", "RFC-0005 §12", "RFC-0007 §8.4"),
        ("security rights and Organization scope", "lifecycle and ownership"),
        (
            FitnessEvidence(
                "test_p3_07_cross_capability_enforcement.py",
                "test_access_context_grants_no_organizational_authority",
            ),
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_authorization_and_data_governance_boundaries_cannot_be_dropped",
            ),
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_contract_admission_creates_no_approval_or_authority",
            ),
        ),
    ),
    FitnessRow(
        "FIT-09",
        "Exact Product Contract dependency/version boundary and hidden-coupling rejection",
        ("RFC-0004 §§7–12, 18–19",),
        ("Product Contract isolation",),
        (
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_exact_contract_and_capability_versions_are_preserved",
            ),
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_undeclared_or_wrong_version_dependency_fails_closed",
            ),
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_hidden_platform_coupling_is_rejected",
            ),
        ),
    ),
    FitnessRow(
        "FIT-10",
        "Product Contract canonical-read declarations and Organization isolation",
        ("RFC-0003 §§7, 15", "RFC-0004 §§10, 20"),
        ("Product Contract isolation", "security rights and Organization scope"),
        (
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_cross_organization_contract_reliance_is_rejected",
            ),
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_canonical_source_read_must_be_declared",
            ),
            FitnessEvidence(
                "test_p3_08_product_contract_consumption.py",
                "test_search_visibility_still_does_not_grant_source_access",
            ),
        ),
    ),
    FitnessRow(
        "FIT-11",
        "Materially distinct multi-consumer reuse without shared-contract broadening",
        ("RFC-0001 §§11–12, 22", "RFC-0004 §14", "P3.02 capability contracts"),
        ("materially distinct reuse", "capability boundaries"),
        (
            FitnessEvidence(
                "test_p3_09_shared_capability_reuse.py",
                "test_two_materially_distinct_consumers_reuse_all_four_capabilities",
            ),
            FitnessEvidence(
                "test_p3_09_shared_capability_reuse.py",
                "test_identical_composition_order_is_not_materially_distinct_evidence",
            ),
            FitnessEvidence(
                "test_p3_09_shared_capability_reuse.py",
                "test_capability_contract_version_cannot_be_broadened_for_second_consumer",
            ),
        ),
    ),
    FitnessRow(
        "FIT-12",
        "Consumer composition and Product Contract isolation remain product-owned",
        ("RFC-0004 §§6, 11, 14",),
        ("Product Contract isolation", "materially distinct reuse", "capability boundaries"),
        (
            FitnessEvidence(
                "test_p3_09_shared_capability_reuse.py",
                "test_second_consumer_cannot_borrow_first_consumer_contract",
            ),
            FitnessEvidence(
                "test_p3_09_shared_capability_reuse.py",
                "test_consumer_specific_source_read_does_not_bleed_into_other_contract",
            ),
        ),
    ),
    FitnessRow(
        "FIT-13",
        "Portable and rebuildable derived state preserves exact governed references",
        ("RFC-0001 §18", "RFC-0003 §§20–21", "RFC-0007 §21", "RFC-0008 §§23–24"),
        ("portability", "non-authoritative projections"),
        (
            FitnessEvidence(
                "test_p3_03_document_artifact_governance.py",
                "test_hash_and_storage_locator_do_not_define_document_identity",
            ),
            FitnessEvidence(
                "test_p3_05_search_index_projection.py",
                "test_rebuild_replaces_disposable_stale_state_without_authority_migration",
            ),
            FitnessEvidence(
                "test_p3_06_audit_reconstruction_support.py",
                "test_export_preserves_reference_status_without_hidden_content",
            ),
        ),
    ),
    FitnessRow(
        "FIT-14",
        "Technology and durable-infrastructure independence",
        ("RFC-0001 §23", "RFC-0002 §16", "RFC-0003 §26", "P3.02 ADR gate"),
        ("portability", "ADR triggers"),
        (
            FitnessEvidence(
                "test_p3_10_phase_3_architecture_fitness_matrix.py",
                "test_phase_3_capability_modules_do_not_select_durable_infrastructure",
            ),
        ),
    ),
    FitnessRow(
        "FIT-15",
        "ADR-trigger boundaries stay explicit during bounded incubation",
        ("RFC-0001 §23", "P3.02 §9 ADR gate assessment"),
        ("ADR triggers",),
        (
            FitnessEvidence(
                "test_p3_10_phase_3_architecture_fitness_matrix.py",
                "test_phase_3_contract_keeps_adr_trigger_boundaries_explicit",
            ),
        ),
    ),
    FitnessRow(
        "FIT-16",
        "Commercial, conformance and capability-promotion restraint",
        ("RFC-0001 §§11, 14, 24–25", "RFC-0004 §22", "Capability catalog"),
        ("commercial and conformance restraint", "lifecycle and ownership"),
        (
            FitnessEvidence(
                "test_p3_10_phase_3_architecture_fitness_matrix.py",
                "test_phase_3_status_does_not_implicitly_promote_or_overclaim",
            ),
        ),
    ),
)


EXPECTED_ROADMAP_COVERAGE = {
    "capability boundaries",
    "lifecycle and ownership",
    "authority and provenance",
    "security rights and Organization scope",
    "Product Contract isolation",
    "non-authoritative projections",
    "materially distinct reuse",
    "portability",
    "ADR triggers",
    "commercial and conformance restraint",
}

REQUIRED_SEMANTIC_OWNER_TEST_FILES = {
    "test_p3_03_document_artifact_governance.py",
    "test_p3_04_memory_knowledge_governance.py",
    "test_p3_05_search_index_projection.py",
    "test_p3_06_audit_reconstruction_support.py",
    "test_p3_07_cross_capability_enforcement.py",
    "test_p3_08_product_contract_consumption.py",
    "test_p3_09_shared_capability_reuse.py",
}

PHASE_3_CAPABILITY_MODULES = (
    "document_artifact_governance.py",
    "memory_knowledge_governance.py",
    "search_index_projection.py",
    "audit_reconstruction_support.py",
    "cross_capability_enforcement.py",
    "product_capability_consumption.py",
    "shared_capability_reuse.py",
)

FORBIDDEN_PRODUCT_DOMAIN_MARKERS = (
    "tender",
    "procurement",
    "supplier",
    "request_for_quotation",
    "purchase_order",
    "bid_submission",
)

FORBIDDEN_DURABLE_INFRASTRUCTURE_IMPORTS = {
    "sqlalchemy",
    "psycopg",
    "sqlite3",
    "kafka",
    "celery",
    "redis",
    "neo4j",
    "networkx",
    "elasticsearch",
    "opensearchpy",
    "qdrant_client",
    "pinecone",
    "chromadb",
    "weaviate",
}

CAPABILITY_IDS = ("CAP-001", "CAP-002", "CAP-003", "CAP-004")


class P310Phase3ArchitectureFitnessMatrixTests(unittest.TestCase):
    def _test_names(self, path: Path) -> set[str]:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        return {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        }

    def _import_roots(self, path: Path) -> set[str]:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".", 1)[0])
        return roots

    def test_matrix_ids_are_complete_unique_and_ordered(self) -> None:
        expected = tuple(f"FIT-{index:02d}" for index in range(1, 17))
        actual = tuple(row.matrix_id for row in FITNESS_MATRIX)
        self.assertEqual(actual, expected)
        self.assertEqual(len(set(actual)), len(actual))

    def test_matrix_exactly_covers_required_roadmap_dimensions(self) -> None:
        covered = {
            dimension
            for row in FITNESS_MATRIX
            for dimension in row.roadmap_coverage
        }
        self.assertEqual(covered, EXPECTED_ROADMAP_COVERAGE)

    def test_every_matrix_evidence_anchor_exists(self) -> None:
        names_by_file: dict[str, set[str]] = {}
        for row in FITNESS_MATRIX:
            self.assertTrue(row.authority, row.matrix_id)
            self.assertTrue(row.roadmap_coverage, row.matrix_id)
            self.assertTrue(row.evidence, row.matrix_id)
            for evidence in row.evidence:
                path = TEST_ROOT / evidence.test_file
                self.assertTrue(path.is_file(), f"missing evidence file: {path}")
                names_by_file.setdefault(evidence.test_file, self._test_names(path))
                self.assertIn(
                    evidence.test_name,
                    names_by_file[evidence.test_file],
                    f"stale matrix anchor: {evidence.test_file}::{evidence.test_name}",
                )

    def test_matrix_spans_every_phase_3_semantic_owner_slice(self) -> None:
        evidence_files = {
            evidence.test_file
            for row in FITNESS_MATRIX
            for evidence in row.evidence
        }
        self.assertTrue(REQUIRED_SEMANTIC_OWNER_TEST_FILES.issubset(evidence_files))

    def test_phase_3_capability_modules_are_product_domain_neutral(self) -> None:
        for module_name in PHASE_3_CAPABILITY_MODULES:
            text = (SOURCE_ROOT / module_name).read_text(encoding="utf-8").lower()
            for marker in FORBIDDEN_PRODUCT_DOMAIN_MARKERS:
                self.assertNotIn(marker, text, f"{module_name} leaked product marker {marker!r}")

    def test_phase_3_capability_modules_do_not_select_durable_infrastructure(self) -> None:
        for module_name in PHASE_3_CAPABILITY_MODULES:
            imports = self._import_roots(SOURCE_ROOT / module_name)
            selected = imports.intersection(FORBIDDEN_DURABLE_INFRASTRUCTURE_IMPORTS)
            self.assertEqual(selected, set(), f"{module_name} selected durable infrastructure: {selected}")

    def test_capability_lifecycle_and_owner_remain_incubating_provisional(self) -> None:
        catalog = (DOCS_ROOT / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md").read_text(encoding="utf-8")
        contracts = (DOCS_ROOT / "contracts" / "PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md").read_text(encoding="utf-8")

        for capability_id in CAPABILITY_IDS:
            rows = [line for line in catalog.splitlines() if line.startswith(f"| `{capability_id}` |")]
            self.assertEqual(len(rows), 1, capability_id)
            self.assertIn("| `Incubating` | `Provisional` |", rows[0])

        self.assertEqual(contracts.count("**Lifecycle:** `Incubating`"), 4)
        self.assertEqual(contracts.count("**Contract status:** `Provisional`"), 4)
        self.assertIn(
            "accountable architectural owner: `ООО «Арвектум»` — platform architecture owner",
            contracts,
        )

    def test_phase_3_contract_keeps_adr_trigger_boundaries_explicit(self) -> None:
        contracts = (DOCS_ROOT / "contracts" / "PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md").read_text(encoding="utf-8")
        self.assertIn("## 9. ADR gate assessment", contracts)
        for boundary in (
            "concrete persistence/object-store/search topology",
            "transaction/concurrency mechanism",
            "Event transport/store",
            "IAM/PDP/PEP technology",
            "evidence-integrity mechanism",
            "stable API/serialization",
            "durable projection/replay store",
            "separately deployable service/process topology",
        ):
            self.assertIn(boundary, contracts)

    def test_phase_3_status_does_not_implicitly_promote_or_overclaim(self) -> None:
        catalog = (DOCS_ROOT / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md").read_text(encoding="utf-8")
        contracts = (DOCS_ROOT / "contracts" / "PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md").read_text(encoding="utf-8")
        roadmap = (DOCS_ROOT / "roadmap" / "PHASE-3-SHARED-PLATFORM-CAPABILITIES.md").read_text(encoding="utf-8")

        self.assertIn("`Incubating` is not `Active`", catalog)
        self.assertIn("No capability may become `Active` without separate RFC-0001 admission", catalog)
        self.assertIn("does not amend an Accepted RFC", contracts)
        self.assertIn("promote any capability to `Active`", contracts)
        self.assertIn("P3.10", roadmap)
        self.assertNotIn("CAP-001 | `Active`", roadmap)
        self.assertNotIn("CAP-002 | `Active`", roadmap)
        self.assertNotIn("CAP-003 | `Active`", roadmap)
        self.assertNotIn("CAP-004 | `Active`", roadmap)


if __name__ == "__main__":
    unittest.main()
