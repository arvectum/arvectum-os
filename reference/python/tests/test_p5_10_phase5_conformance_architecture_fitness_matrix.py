from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import unittest


@dataclass(frozen=True)
class EvidenceRef:
    filename: str
    class_name: str
    method_name: str


@dataclass(frozen=True)
class FitnessMatrixRow:
    row_id: str
    dimension: str
    positive: tuple[EvidenceRef, ...]
    negative: tuple[EvidenceRef, ...]


def ref(filename: str, class_name: str, method_name: str) -> EvidenceRef:
    return EvidenceRef(filename, class_name, method_name)


P502 = "P502ProductContractDeclarationValidationTests"
P503 = "P503GovernedDependencyVersionResolutionTests"
P506 = "P506SecurityAuthorityRightsIntegrationGuardsTests"
P507 = "P507EventProvenancePortabilityIntegrationSupportTests"
P508 = "P508WorkspaceCapabilityIntegrationAdaptersTests"
P509 = "P509SecondMateriallyDistinctIntegrationReuseTests"
R14 = "R14DeveloperSafetyContractHealthReviewTests"
R15 = "R15ReuseDeveloperExperienceRefactoringReviewTests"


MATRIX = (
    FitnessMatrixRow(
        "CF-01",
        "Product Contract declaration/version identity",
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_p4_08_exact_declaration_validates_as_provisional"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_second_contract_reuses_p5_02_declaration_validation_without_fake_canonical_read"),
        ),
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_effective_product_contract_version_must_match_exact_semantic_owner"),
        ),
    ),
    FitnessMatrixRow(
        "CF-02",
        "Dependency/version continuity",
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_exact_declared_versions_resolve_with_explicit_compatible_decisions"),
            ref("test_p5_08_workspace_capability_integration_adapters.py", P508, "test_adapter_composition_preserves_exact_facade_contract_context"),
        ),
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_nearby_semantic_version_is_not_inferred_compatible"),
        ),
    ),
    FitnessMatrixRow(
        "CF-03",
        "Dependency provider/consumer/failure responsibility continuity",
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_resolution_preserves_r13_dependency_and_operation_failure_semantics"),
        ),
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_dependency_allowed_operation_requires_exact_operation_declaration"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_second_integration_cannot_smuggle_an_undeclared_dependency"),
        ),
    ),
    FitnessMatrixRow(
        "CF-04",
        "Current dependency-support evidence / stale-evidence fail-closed behavior",
        (
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_current_supported_evidence_allows_j1_without_creating_authority"),
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_current_supported_evidence_allows_j2_with_gates_still_unresolved"),
        ),
        (
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_r14_f2_j1_requires_explicit_current_dependency_evidence"),
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_composition_snapshot_is_inspection_evidence_not_current_authority"),
        ),
    ),
    FitnessMatrixRow(
        "CF-05",
        "Hidden-coupling prohibition",
        (
            ref("test_p5_08_workspace_capability_integration_adapters.py", P508, "test_product_adapter_journey_has_one_integration_facing_platform_import"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_both_consumers_use_the_same_integration_adapter_module"),
        ),
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_hidden_boundary_mechanisms_are_rejected_statically"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_second_consumer_has_no_workspace_event_store_or_capability_private_import"),
        ),
    ),
    FitnessMatrixRow(
        "CF-06",
        "Organization isolation",
        (
            ref("test_p5_08_workspace_capability_integration_adapters.py", P508, "test_adapter_composition_preserves_exact_facade_contract_context"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_reconstruction_executes_through_same_adapters_and_preserves_exact_contract_context"),
        ),
        (
            ref("test_p5_06_security_authority_rights_integration_guards.py", P506, "test_wrong_organization_actor_cannot_compose_facade"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_cross_organization_reconstruction_fails_closed"),
        ),
    ),
    FitnessMatrixRow(
        "CF-07",
        "Authorization vs Organizational Authority separation",
        (
            ref("test_p5_06_security_authority_rights_integration_guards.py", P506, "test_all_independent_required_gates_must_allow_before_ready"),
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_current_supported_evidence_allows_j2_with_gates_still_unresolved"),
        ),
        (
            ref("test_p5_06_security_authority_rights_integration_guards.py", P506, "test_missing_authorization_and_authority_gates_fail_closed"),
            ref("test_p5_06_security_authority_rights_integration_guards.py", P506, "test_denied_authorization_fails_closed_even_when_other_gates_allow"),
        ),
    ),
    FitnessMatrixRow(
        "CF-08",
        "Governed canonical mutation path",
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_canonical_mutation_requires_organizational_authority_declaration"),
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_current_supported_evidence_allows_j2_with_gates_still_unresolved"),
        ),
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_canonical_mutation_without_write_declaration_fails_closed"),
            ref("test_p5_06_security_authority_rights_integration_guards.py", P506, "test_missing_authorization_and_authority_gates_fail_closed"),
        ),
    ),
    FitnessMatrixRow(
        "CF-09",
        "Event/provenance attribution",
        (
            ref("test_p5_07_event_provenance_portability_integration_support.py", P507, "test_event_preserves_exact_actor_execution_product_contract_and_version_context"),
            ref("test_p5_07_event_provenance_portability_integration_support.py", P507, "test_represented_actor_context_is_preserved_without_erasing_actual_actor"),
        ),
        (
            ref("test_p5_07_event_provenance_portability_integration_support.py", P507, "test_product_contract_continuity_cannot_be_dropped_before_event_support"),
            ref("test_p5_07_event_provenance_portability_integration_support.py", P507, "test_wrong_organization_event_identity_fails_closed"),
        ),
    ),
    FitnessMatrixRow(
        "CF-10",
        "Rights/minimization/data-governance continuity",
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_read_operation_requires_authorization_and_data_governance"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_evidence_rights_remain_owned_by_capability_and_redact_without_private_fallback"),
        ),
        (
            ref("test_p5_06_security_authority_rights_integration_guards.py", P506, "test_capability_admission_does_not_bypass_purpose_or_right_semantic_owner"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_cross_organization_reconstruction_fails_closed"),
        ),
    ),
    FitnessMatrixRow(
        "CF-11",
        "Portability",
        (
            ref("test_p5_07_event_provenance_portability_integration_support.py", P507, "test_portable_fixture_preserves_semantic_identities_and_relationships"),
            ref("test_p5_07_event_provenance_portability_integration_support.py", P507, "test_module_remains_internal_provisional_and_vendor_serialization_neutral"),
        ),
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_portability_retention_review_and_exit_are_required"),
        ),
    ),
    FitnessMatrixRow(
        "CF-12",
        "Capability/Product Contract lifecycle separation",
        (
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_reuse_does_not_promote_capability_or_contract_lifecycle"),
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_validation_result_is_not_permission_authority_or_capability_activation"),
        ),
        (
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_non_provisional_contract_lifecycle_fails_closed"),
        ),
    ),
    FitnessMatrixRow(
        "CF-13",
        "Unsupported/deprecated dependency behavior",
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_exact_declared_versions_resolve_with_explicit_compatible_decisions"),
        ),
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_explicit_unsupported_exact_version_fails_closed"),
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_deprecated_exact_version_records_migration_and_rejects_reliance"),
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_retired_exact_version_records_migration_and_rejects_reliance"),
            ref("test_r14_developer_safety_contract_health_review.py", R14, "test_composition_time_supported_dependency_cannot_hide_current_deprecation_for_j1"),
        ),
    ),
    FitnessMatrixRow(
        "CF-14",
        "Second-integration reuse",
        (
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_second_contract_is_materially_distinct_from_first_product_contract"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_both_consumers_use_the_same_integration_adapter_module"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_reconstruction_executes_through_same_adapters_and_preserves_exact_contract_context"),
        ),
        (
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_current_provider_evidence_is_still_required_for_second_integration"),
            ref("test_p5_09_second_materially_distinct_integration_reuse.py", P509, "test_second_integration_cannot_smuggle_an_undeclared_dependency"),
        ),
    ),
    FitnessMatrixRow(
        "CF-15",
        "No accidental public/stable compatibility promise",
        (
            ref("test_r15_reuse_developer_experience_refactoring_review.py", R15, "test_refactoring_remains_internal_provisional_without_public_boundary_inflation"),
            ref("test_p5_08_workspace_capability_integration_adapters.py", P508, "test_adapter_module_remains_internal_provisional_and_stack_neutral"),
        ),
        (
            ref("test_p5_03_product_contract_dependency_resolution.py", P503, "test_resolver_remains_static_internal_and_does_not_select_negotiation_stack"),
            ref("test_p5_02_product_contract_declaration_validation.py", P502, "test_non_provisional_contract_lifecycle_fails_closed"),
        ),
    ),
)


class P510Phase5ConformanceArchitectureFitnessMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tests_dir = Path(__file__).resolve().parent
        self.repo_root = Path(__file__).resolve().parents[3]

    @staticmethod
    def _test_methods(path: Path) -> dict[str, set[str]]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        return {
            node.name: {
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                and child.name.startswith("test_")
            }
            for node in tree.body
            if isinstance(node, ast.ClassDef)
        }

    def test_matrix_contains_exact_phase5_minimum_dimensions(self) -> None:
        expected = (
            ("CF-01", "Product Contract declaration/version identity"),
            ("CF-02", "Dependency/version continuity"),
            ("CF-03", "Dependency provider/consumer/failure responsibility continuity"),
            ("CF-04", "Current dependency-support evidence / stale-evidence fail-closed behavior"),
            ("CF-05", "Hidden-coupling prohibition"),
            ("CF-06", "Organization isolation"),
            ("CF-07", "Authorization vs Organizational Authority separation"),
            ("CF-08", "Governed canonical mutation path"),
            ("CF-09", "Event/provenance attribution"),
            ("CF-10", "Rights/minimization/data-governance continuity"),
            ("CF-11", "Portability"),
            ("CF-12", "Capability/Product Contract lifecycle separation"),
            ("CF-13", "Unsupported/deprecated dependency behavior"),
            ("CF-14", "Second-integration reuse"),
            ("CF-15", "No accidental public/stable compatibility promise"),
        )
        self.assertEqual(tuple((row.row_id, row.dimension) for row in MATRIX), expected)

    def test_every_matrix_row_has_positive_and_negative_executable_evidence(self) -> None:
        for row in MATRIX:
            with self.subTest(row=row.row_id):
                self.assertTrue(row.positive)
                self.assertTrue(row.negative)

    def test_all_evidence_references_resolve_to_current_test_cases(self) -> None:
        cache: dict[str, dict[str, set[str]]] = {}
        for row in MATRIX:
            for evidence in row.positive + row.negative:
                path = self.tests_dir / evidence.filename
                with self.subTest(row=row.row_id, evidence=evidence):
                    self.assertTrue(path.is_file(), evidence.filename)
                    methods = cache.setdefault(evidence.filename, self._test_methods(path))
                    self.assertIn(evidence.class_name, methods)
                    self.assertIn(evidence.method_name, methods[evidence.class_name])

    def test_matrix_is_cross_phase_evidence_not_single_test_self_certification(self) -> None:
        referenced_files = {
            evidence.filename
            for row in MATRIX
            for evidence in row.positive + row.negative
        }
        required_sources = {
            "test_p5_02_product_contract_declaration_validation.py",
            "test_p5_03_product_contract_dependency_resolution.py",
            "test_p5_06_security_authority_rights_integration_guards.py",
            "test_p5_07_event_provenance_portability_integration_support.py",
            "test_p5_08_workspace_capability_integration_adapters.py",
            "test_p5_09_second_materially_distinct_integration_reuse.py",
            "test_r14_developer_safety_contract_health_review.py",
            "test_r15_reuse_developer_experience_refactoring_review.py",
        }
        self.assertTrue(required_sources.issubset(referenced_files))
        self.assertNotIn(Path(__file__).name, referenced_files)

    def test_high_risk_rows_retain_their_required_fail_closed_sources(self) -> None:
        rows = {row.row_id: row for row in MATRIX}
        self.assertTrue(any(ref_.filename.startswith("test_r14_") for ref_ in rows["CF-04"].negative))
        self.assertTrue(any(ref_.filename.startswith("test_p5_06_") for ref_ in rows["CF-07"].negative))
        self.assertTrue(any(ref_.filename.startswith("test_p5_07_") for ref_ in rows["CF-09"].negative))
        self.assertTrue(any(ref_.filename.startswith("test_p5_09_") for ref_ in rows["CF-14"].positive))
        self.assertTrue(any(ref_.filename.startswith("test_r15_") for ref_ in rows["CF-15"].positive))

    def test_canonical_review_declares_matrix_as_evidence_index_not_semantic_owner(self) -> None:
        review_path = self.repo_root / "docs" / "reviews" / "P5-10-phase-5-conformance-architecture-fitness-matrix.md"
        self.assertTrue(review_path.is_file())
        review = review_path.read_text(encoding="utf-8")
        for row in MATRIX:
            self.assertIn(f"`{row.row_id}`", review)
        self.assertIn("evidence index", review.lower())
        self.assertIn("not a semantic owner", review.lower())
        self.assertIn("R16 — M5 Integration Hardening", review)


if __name__ == "__main__":
    unittest.main()
