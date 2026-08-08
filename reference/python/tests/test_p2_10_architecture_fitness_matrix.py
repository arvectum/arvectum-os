from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = TEST_ROOT.parent / "arvectum_os_ref"


@dataclass(frozen=True)
class FitnessEvidence:
    test_file: str
    test_name: str


@dataclass(frozen=True)
class FitnessRow:
    matrix_id: str
    dimension: str
    authority: tuple[str, ...]
    evidence: tuple[FitnessEvidence, ...]


FITNESS_MATRIX = (
    FitnessRow(
        "FIT-01",
        "identity and Organization scope isolation",
        ("RFC-0002", "RFC-0003", "RFC-0005"),
        (
            FitnessEvidence(
                "test_p2_03_typed_relationships.py",
                "test_bounded_runtime_rejects_cross_organization_endpoint",
            ),
            FitnessEvidence(
                "test_p2_04_governed_execution.py",
                "test_start_fails_closed_for_scope_or_operation_mismatch",
            ),
            FitnessEvidence(
                "test_p2_07_product_contract.py",
                "test_cross_organization_actor_cannot_enter_runtime",
            ),
        ),
    ),
    FitnessRow(
        "FIT-02",
        "immutable Canonical Record and Relationship histories",
        ("RFC-0002",),
        (
            FitnessEvidence(
                "test_p2_02_canonical_lineage.py",
                "test_subject_identity_is_stable_across_immutable_versions",
            ),
            FitnessEvidence(
                "test_p2_03_typed_relationships.py",
                "test_relationship_version_is_immutable",
            ),
            FitnessEvidence(
                "test_p2_03_typed_relationships.py",
                "test_termination_is_new_version_and_prior_active_history_is_preserved",
            ),
        ),
    ),
    FitnessRow(
        "FIT-03",
        "Head versus Effective Version resolution",
        ("RFC-0002",),
        (
            FitnessEvidence(
                "test_p2_02_canonical_lineage.py",
                "test_future_effective_head_can_differ_from_effective_version",
            ),
            FitnessEvidence(
                "test_p2_03_typed_relationships.py",
                "test_effective_relationship_resolution_reuses_canonical_half_open_semantics",
            ),
        ),
    ),
    FitnessRow(
        "FIT-04",
        "exact consequential version pinning",
        ("RFC-0002", "RFC-0005"),
        (
            FitnessEvidence(
                "test_p2_02_canonical_lineage.py",
                "test_exact_version_identity_remains_resolvable_for_consequential_pinning",
            ),
            FitnessEvidence(
                "test_p2_04_governed_execution.py",
                "test_created_pins_exact_workflow_input_and_product_contract",
            ),
            FitnessEvidence(
                "test_p2_09_second_workflow_reuse.py",
                "test_both_workflows_pin_exact_product_contract_workflow_and_material_versions",
            ),
        ),
    ),
    FitnessRow(
        "FIT-05",
        "separate authority and gate semantics",
        ("RFC-0003", "RFC-0005"),
        (
            FitnessEvidence(
                "test_p2_04_governed_execution.py",
                "test_six_gate_concepts_remain_distinct",
            ),
            FitnessEvidence(
                "test_p2_04_governed_execution.py",
                "test_missing_and_denied_required_gates_fail_closed",
            ),
            FitnessEvidence(
                "test_p2_07_product_contract.py",
                "test_contract_validation_does_not_satisfy_runtime_gates",
            ),
        ),
    ),
    FitnessRow(
        "FIT-06",
        "direct consequential mutation rejection",
        ("RFC-0001", "RFC-0005"),
        (
            FitnessEvidence(
                "test_p2_04_governed_execution.py",
                "test_direct_or_pregate_consequential_effect_is_rejected_and_only_declared_effect_is_admitted",
            ),
        ),
    ),
    FitnessRow(
        "FIT-07",
        "idempotency retry and conflict behavior",
        ("RFC-0005", "RFC-0006"),
        (
            FitnessEvidence(
                "test_p2_06_runtime_consistency.py",
                "test_exact_keyed_retry_returns_committed_result_without_repeating_effects",
            ),
            FitnessEvidence(
                "test_p2_06_runtime_consistency.py",
                "test_retry_token_cannot_be_rebound_to_different_immutable_invocation",
            ),
            FitnessEvidence(
                "test_p2_06_runtime_consistency.py",
                "test_stale_expected_head_is_rejected_instead_of_overwriting_newer_state",
            ),
        ),
    ),
    FitnessRow(
        "FIT-08",
        "Event duplicate and conflict admission",
        ("RFC-0002", "RFC-0006"),
        (
            FitnessEvidence(
                "test_p2_05_event_provenance.py",
                "test_duplicate_delivery_of_same_occurrence_is_idempotent",
            ),
            FitnessEvidence(
                "test_p2_05_event_provenance.py",
                "test_conflicting_content_for_same_event_identity_is_rejected",
            ),
            FitnessEvidence(
                "test_p2_05_event_provenance.py",
                "test_event_version_identity_cannot_be_reused_by_another_event",
            ),
        ),
    ),
    FitnessRow(
        "FIT-09",
        "reconstruction completeness",
        ("RFC-0001", "RFC-0005", "RFC-0006"),
        (
            FitnessEvidence(
                "test_p2_05_event_provenance.py",
                "test_reconstruction_identifies_exact_governed_versions",
            ),
        ),
    ),
    FitnessRow(
        "FIT-10",
        "Product Contract enforcement",
        ("RFC-0003", "RFC-0004", "RFC-0005"),
        (
            FitnessEvidence(
                "test_p2_07_product_contract.py",
                "test_valid_contract_admits_and_runtime_pins_exact_contract_version",
            ),
            FitnessEvidence(
                "test_p2_07_product_contract.py",
                "test_hidden_internal_coupling_is_rejected",
            ),
            FitnessEvidence(
                "test_p2_07_product_contract.py",
                "test_canonical_read_write_and_authority_scope_are_enforced",
            ),
        ),
    ),
    FitnessRow(
        "FIT-11",
        "projection non-authority and replay safety",
        ("RFC-0002", "RFC-0005", "RFC-0006"),
        (
            FitnessEvidence(
                "test_p2_08_portability_replay_projection.py",
                "test_two_distinct_scenarios_rebuild_zero_effect_non_authoritative_projections",
            ),
            FitnessEvidence(
                "test_p2_08_portability_replay_projection.py",
                "test_projection_cannot_mint_governed_pin_without_exact_canonical_source",
            ),
        ),
    ),
    FitnessRow(
        "FIT-12",
        "portability semantic round-trip",
        ("RFC-0002", "RFC-0003", "RFC-0006"),
        (
            FitnessEvidence(
                "test_p2_08_portability_replay_projection.py",
                "test_relationship_scenario_round_trips_semantic_meaning",
            ),
            FitnessEvidence(
                "test_p2_08_portability_replay_projection.py",
                "test_event_scenario_round_trips_exact_event_semantics",
            ),
        ),
    ),
    FitnessRow(
        "FIT-13",
        "product-domain leakage checks",
        ("RFC-0001", "RFC-0004"),
        (
            FitnessEvidence(
                "test_p2_10_architecture_fitness_matrix.py",
                "test_shared_runtime_modules_are_product_domain_neutral",
            ),
            FitnessEvidence(
                "test_r3_reuse_refactoring.py",
                "test_product_contract_entry_uses_governed_execution_not_historical_composition",
            ),
        ),
    ),
    FitnessRow(
        "FIT-14",
        "migration and reversibility constraints",
        ("RFC-0001", "RFC-0002", "RFC-0003"),
        (
            FitnessEvidence(
                "test_p2_10_architecture_fitness_matrix.py",
                "test_shared_runtime_does_not_select_durable_infrastructure",
            ),
            FitnessEvidence(
                "test_r2_runtime_health.py",
                "test_accumulated_runtime_does_not_select_durable_infrastructure",
            ),
            FitnessEvidence(
                "test_r3_reuse_refactoring.py",
                "test_historical_request_is_not_generalized_to_fit_second_workflow",
            ),
        ),
    ),
)


EXPECTED_DIMENSIONS = (
    "identity and Organization scope isolation",
    "immutable Canonical Record and Relationship histories",
    "Head versus Effective Version resolution",
    "exact consequential version pinning",
    "separate authority and gate semantics",
    "direct consequential mutation rejection",
    "idempotency retry and conflict behavior",
    "Event duplicate and conflict admission",
    "reconstruction completeness",
    "Product Contract enforcement",
    "projection non-authority and replay safety",
    "portability semantic round-trip",
    "product-domain leakage checks",
    "migration and reversibility constraints",
)


CORE_RUNTIME_MODULES = (
    "canonical.py",
    "canonical_lineage.py",
    "relationships.py",
    "governed_execution.py",
    "event_provenance.py",
    "runtime_consistency.py",
    "product_contract.py",
    "portability_runtime.py",
)


class P210CoreRuntimeArchitectureFitnessMatrixTests(unittest.TestCase):
    """Executable index for the final applicable M2 architecture fitness evidence."""

    @staticmethod
    def _test_names(path: Path) -> set[str]:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        return {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        }

    def test_matrix_exactly_covers_the_p210_roadmap_dimensions(self) -> None:
        self.assertEqual(tuple(row.dimension for row in FITNESS_MATRIX), EXPECTED_DIMENSIONS)
        self.assertEqual(
            tuple(row.matrix_id for row in FITNESS_MATRIX),
            tuple(f"FIT-{index:02d}" for index in range(1, 15)),
        )

    def test_every_matrix_evidence_anchor_exists_as_executable_test(self) -> None:
        for row in FITNESS_MATRIX:
            self.assertTrue(row.authority, row.matrix_id)
            self.assertTrue(row.evidence, row.matrix_id)
            for evidence in row.evidence:
                with self.subTest(matrix_id=row.matrix_id, evidence=evidence):
                    path = TEST_ROOT / evidence.test_file
                    self.assertTrue(path.is_file(), path)
                    self.assertIn(evidence.test_name, self._test_names(path))

    def test_matrix_spans_the_final_semantic_owner_evidence_without_p201_composition(self) -> None:
        evidence_files = {
            evidence.test_file for row in FITNESS_MATRIX for evidence in row.evidence
        }
        required_semantic_owner_evidence = {
            "test_p2_02_canonical_lineage.py",
            "test_p2_03_typed_relationships.py",
            "test_p2_04_governed_execution.py",
            "test_p2_05_event_provenance.py",
            "test_p2_06_runtime_consistency.py",
            "test_p2_07_product_contract.py",
            "test_p2_08_portability_replay_projection.py",
            "test_p2_09_second_workflow_reuse.py",
            "test_r2_runtime_health.py",
            "test_r3_reuse_refactoring.py",
        }
        self.assertTrue(required_semantic_owner_evidence.issubset(evidence_files))
        self.assertNotIn("test_p2_01_runtime_composition.py", evidence_files)

    def test_shared_runtime_modules_are_product_domain_neutral(self) -> None:
        product_domain_markers = (
            "tender",
            "procurement",
            "supplier",
            "request_for_quotation",
            "purchase_order",
            "bid_submission",
        )
        combined = "\n".join(
            (PACKAGE_ROOT / module_name).read_text(encoding="utf-8").lower()
            for module_name in CORE_RUNTIME_MODULES
        )
        for marker in product_domain_markers:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)

    def test_shared_runtime_does_not_select_durable_infrastructure(self) -> None:
        forbidden_import_markers = (
            "import sqlalchemy",
            "from sqlalchemy",
            "import psycopg",
            "from psycopg",
            "import sqlite3",
            "import kafka",
            "from kafka",
            "import celery",
            "from celery",
            "import redis",
            "from redis",
            "import neo4j",
            "from neo4j",
            "import networkx",
            "from networkx",
        )
        combined = "\n".join(
            (PACKAGE_ROOT / module_name).read_text(encoding="utf-8").lower()
            for module_name in CORE_RUNTIME_MODULES
        )
        for marker in forbidden_import_markers:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)

    def test_matrix_scope_does_not_claim_unexercised_memory_or_document_architecture(self) -> None:
        dimensions = " ".join(row.dimension for row in FITNESS_MATRIX).lower()
        self.assertNotIn("memory", dimensions)
        self.assertNotIn("knowledge", dimensions)
        self.assertNotIn("document", dimensions)
        self.assertNotIn("artifact", dimensions)


if __name__ == "__main__":
    unittest.main()
