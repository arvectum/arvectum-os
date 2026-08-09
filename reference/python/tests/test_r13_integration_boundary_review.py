from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.product_contract_declaration as declaration_module
from arvectum_os_ref.product_contract import ProductContractLifecycle
from arvectum_os_ref.product_contract_declaration import validate_product_contract_declaration
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.identity import Identity
from bounded_product_ref.contract import build_p4_08_product_contract


UTC = timezone.utc


class R13IntegrationBoundaryReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        principal = Principal(Identity("principal", "r13-developer", "platform"))
        self.actor = ActorContext(principal, organization)
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 9, 30, tzinfo=UTC),
        )
        self.validation = validate_product_contract_declaration(contract=self.contract)

    def test_derived_dependency_evidence_preserves_rfc0004_boundary_responsibilities(self) -> None:
        source = {item.dependency_id: item for item in self.contract.dependencies}
        derived = {item.dependency_id: item for item in self.validation.dependencies}

        self.assertEqual(set(derived), set(source))
        for dependency_id, declaration in source.items():
            evidence = derived[dependency_id]
            self.assertEqual(evidence.contract_version, declaration.contract_version)
            self.assertEqual(evidence.allowed_operations, declaration.allowed_operations)
            self.assertEqual(evidence.provider_responsibility, declaration.provider_responsibility)
            self.assertEqual(evidence.consumer_responsibility, declaration.consumer_responsibility)
            self.assertEqual(evidence.failure_behavior, declaration.failure_behavior)
            self.assertEqual(evidence.provisional, declaration.provisional)

    def test_derived_operation_evidence_preserves_failure_semantics(self) -> None:
        source = {item.operation_name: item for item in self.contract.operations}
        derived = {item.operation_name: item for item in self.validation.operations}

        self.assertEqual(set(derived), set(source))
        for operation_name, declaration in source.items():
            evidence = derived[operation_name]
            self.assertEqual(evidence.dependency_id, declaration.dependency_id)
            self.assertEqual(evidence.side_effect_classes, declaration.side_effect_classes)
            self.assertEqual(evidence.required_gates, declaration.required_gates)
            self.assertEqual(evidence.failure_behavior, declaration.failure_behavior)

    def test_derived_evidence_fails_closed_when_boundary_responsibility_is_erased(self) -> None:
        dependency = self.validation.dependencies[0]
        for field_name in (
            "provider_responsibility",
            "consumer_responsibility",
            "failure_behavior",
        ):
            with self.subTest(field=field_name):
                with self.assertRaises(ValueError):
                    replace(dependency, **{field_name: ""})

        with self.assertRaises(ValueError):
            replace(self.validation.operations[0], failure_behavior="")

    def test_validation_evidence_is_not_a_permission_or_capability_lifecycle_source(self) -> None:
        self.assertEqual(self.validation.lifecycle, ProductContractLifecycle.PROVISIONAL)

        field_sets = [
            {item.name for item in fields(self.validation)},
            {item.name for item in fields(self.validation.dependencies[0])},
            {item.name for item in fields(self.validation.operations[0])},
        ]
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

    def test_validator_remains_an_internal_derived_view_not_a_parallel_manifest(self) -> None:
        source = inspect.getsource(declaration_module).lower()

        self.assertIn("single executable declaration model", source)
        self.assertIn("not a standardized product contract schema", source)
        self.assertIn("internal", source)
        self.assertIn("provisional", source)
        for forbidden in (
            "import yaml",
            "import json",
            "protobuf",
            "openapi",
            "package registry",
            "extension registry",
        ):
            self.assertNotIn(forbidden, source)

        with self.assertRaises(TypeError):
            validate_product_contract_declaration(contract={})  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
