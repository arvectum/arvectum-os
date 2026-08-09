from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.product_contract_resolution as resolution_module
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_contract_resolution import (
    AmbiguousDependencyResolutionError,
    DependencyCompatibilityDecision,
    DependencySupportDisposition,
    DeprecatedDependencyResolutionError,
    GovernedDependencyVersionEvidence,
    IncompatibleDependencyVersionError,
    ProductContractResolutionContinuityError,
    RetiredDependencyResolutionError,
    UnsupportedDependencyResolutionError,
    evaluate_product_contract_dependencies,
    resolve_product_contract_dependencies,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from bounded_product_ref.contract import build_p4_08_product_contract


UTC = timezone.utc


class P503GovernedDependencyVersionResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        principal = Principal(Identity("principal", "p5-03-developer", "platform"))
        actor = ActorContext(principal, organization)
        self.contract = build_p4_08_product_contract(
            actor=actor,
            created_at=datetime(2026, 8, 9, 12, 30, tzinfo=UTC),
        )

    def _supported_versions(self):
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "test-governed-provider-evidence:"
                    f"{dependency.dependency_id.namespace}:{dependency.dependency_id.value}:"
                    f"{dependency.contract_version}"
                ),
            )
            for dependency in self.contract.dependencies
        )

    def _resolve(self, governed_versions=None, effective_product_contract=None):
        return resolve_product_contract_dependencies(
            contract=self.contract,
            effective_product_contract=(
                self.contract.version_pin
                if effective_product_contract is None
                else effective_product_contract
            ),
            governed_versions=(
                self._supported_versions() if governed_versions is None else governed_versions
            ),
        )

    def test_exact_declared_versions_resolve_with_explicit_compatible_decisions(self) -> None:
        report = self._resolve()

        self.assertTrue(report.is_compatible)
        self.assertEqual(report.product_contract, self.contract.version_pin)
        self.assertEqual(report.product_id, self.contract.product_id)
        self.assertEqual(report.product_version, self.contract.product_version)
        self.assertEqual(len(report.evaluations), len(self.contract.dependencies))
        self.assertTrue(
            all(
                item.decision is DependencyCompatibilityDecision.COMPATIBLE
                for item in report.evaluations
            )
        )

    def test_resolution_preserves_r13_dependency_and_operation_failure_semantics(self) -> None:
        report = self._resolve()
        source_dependencies = {item.dependency_id: item for item in self.contract.dependencies}

        for evaluation in report.evaluations:
            source = source_dependencies[evaluation.dependency_id]
            self.assertEqual(evaluation.declared_contract_version, source.contract_version)
            self.assertEqual(evaluation.allowed_operations, source.allowed_operations)
            self.assertEqual(evaluation.provider_responsibility, source.provider_responsibility)
            self.assertEqual(evaluation.consumer_responsibility, source.consumer_responsibility)
            self.assertEqual(evaluation.dependency_failure_behavior, source.failure_behavior)
            expected_operation_failures = tuple(
                (operation.operation_name, operation.failure_behavior)
                for operation in self.contract.operations
                if operation.dependency_id == source.dependency_id
            )
            self.assertEqual(
                evaluation.operation_failure_behaviors,
                expected_operation_failures,
            )

    def test_effective_product_contract_version_must_match_exact_semantic_owner(self) -> None:
        stale_pin = replace(
            self.contract.version_pin,
            version_id=Identity(
                "product-contract-version",
                "p4-08-bounded-review-product-v0.0.9",
                self.contract.version_pin.version_id.scope,
            ),
        )
        with self.assertRaises(ProductContractResolutionContinuityError):
            self._resolve(effective_product_contract=stale_pin)

    def test_nearby_semantic_version_is_not_inferred_compatible(self) -> None:
        versions = list(self._supported_versions())
        versions[0] = replace(versions[0], contract_version="1.0.1")

        report = evaluate_product_contract_dependencies(
            contract=self.contract,
            effective_product_contract=self.contract.version_pin,
            governed_versions=tuple(versions),
        )
        evaluation = report.evaluations[0]
        self.assertEqual(
            evaluation.decision,
            DependencyCompatibilityDecision.VERSION_MISMATCH,
        )
        self.assertIn("1.0.1", evaluation.observed_contract_versions)
        self.assertIsNotNone(evaluation.migration_obligation)

        with self.assertRaises(IncompatibleDependencyVersionError):
            self._resolve(governed_versions=tuple(versions))

    def test_missing_governed_dependency_evidence_is_unsupported(self) -> None:
        versions = self._supported_versions()[1:]
        report = evaluate_product_contract_dependencies(
            contract=self.contract,
            effective_product_contract=self.contract.version_pin,
            governed_versions=versions,
        )
        self.assertEqual(
            report.evaluations[0].decision,
            DependencyCompatibilityDecision.UNSUPPORTED,
        )
        with self.assertRaises(UnsupportedDependencyResolutionError):
            self._resolve(governed_versions=versions)

    def test_explicit_unsupported_exact_version_fails_closed(self) -> None:
        versions = list(self._supported_versions())
        versions[0] = replace(
            versions[0],
            disposition=DependencySupportDisposition.UNSUPPORTED,
        )
        with self.assertRaises(UnsupportedDependencyResolutionError):
            self._resolve(governed_versions=tuple(versions))

    def test_deprecated_exact_version_records_migration_and_rejects_reliance(self) -> None:
        versions = list(self._supported_versions())
        versions[0] = replace(
            versions[0],
            disposition=DependencySupportDisposition.DEPRECATED,
            migration_obligation=(
                "Create a new immutable Product Contract version after reviewing the provider replacement."
            ),
        )
        report = evaluate_product_contract_dependencies(
            contract=self.contract,
            effective_product_contract=self.contract.version_pin,
            governed_versions=tuple(versions),
        )
        evaluation = report.evaluations[0]
        self.assertEqual(evaluation.decision, DependencyCompatibilityDecision.DEPRECATED)
        self.assertIn("new immutable Product Contract", evaluation.migration_obligation)
        with self.assertRaises(DeprecatedDependencyResolutionError):
            self._resolve(governed_versions=tuple(versions))

    def test_retired_exact_version_records_migration_and_rejects_reliance(self) -> None:
        versions = list(self._supported_versions())
        versions[0] = replace(
            versions[0],
            disposition=DependencySupportDisposition.RETIRED,
            migration_obligation="Retire the product reliance or revise the Product Contract boundary.",
        )
        with self.assertRaises(RetiredDependencyResolutionError):
            self._resolve(governed_versions=tuple(versions))

    def test_deprecated_or_retired_evidence_requires_migration_obligation(self) -> None:
        dependency = self.contract.dependencies[0]
        for disposition in (
            DependencySupportDisposition.DEPRECATED,
            DependencySupportDisposition.RETIRED,
        ):
            with self.subTest(disposition=disposition.value):
                with self.assertRaises(ValueError):
                    GovernedDependencyVersionEvidence(
                        dependency_id=dependency.dependency_id,
                        contract_version=dependency.contract_version,
                        disposition=disposition,
                        governance_reference="test:provider-governance",
                    )

    def test_duplicate_exact_governed_assertions_are_ambiguous(self) -> None:
        versions = self._supported_versions()
        duplicate = replace(
            versions[0],
            governance_reference="test:conflicting-governed-provider-evidence",
        )
        with self.assertRaises(AmbiguousDependencyResolutionError):
            self._resolve(governed_versions=versions + (duplicate,))

    def test_compatibility_report_is_not_permission_authority_or_capability_lifecycle(self) -> None:
        report = self._resolve()
        field_sets = (
            {item.name for item in fields(report)},
            {item.name for item in fields(report.evaluations[0])},
            {item.name for item in fields(self._supported_versions()[0])},
        )
        for field_set in field_sets:
            for forbidden in (
                "authentication",
                "authorization",
                "permission",
                "organizational_authority",
                "approval",
                "capability_lifecycle",
                "active",
            ):
                self.assertNotIn(forbidden, field_set)

    def test_resolver_remains_static_internal_and_does_not_select_negotiation_stack(self) -> None:
        source = inspect.getsource(resolution_module).lower()
        self.assertIn("single executable semantic owner", source)
        self.assertIn("internal", source)
        self.assertIn("provisional", source)
        self.assertIn("no fallback version is selected automatically", source)

        for forbidden in (
            "import packaging",
            "specifierset",
            "import semver",
            "import yaml",
            "import json",
            "protobuf",
            "openapi",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
