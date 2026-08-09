from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.product_contract_declaration as declaration_module
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAPABILITY_CONTRACT_VERSION,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessMode,
    HiddenProductPlatformCouplingError,
    ProductBoundaryMechanism,
    ProductContractCanonicalAccessError,
    ProductContractDependencyError,
    ProductContractLifecycle,
    ProductContractLifecycleError,
    ProductContractSecurityBoundaryError,
)
from arvectum_os_ref.product_contract_declaration import (
    ProductContractDeclarationValidation,
    validate_product_contract_declaration,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from bounded_product_ref.contract import (
    GOVERNED_RUNTIME_DEPENDENCY,
    GOVERNED_RUNTIME_CONTRACT_VERSION,
    OP_RECORD_TASK_DECISION,
    build_p4_08_product_contract,
)


UTC = timezone.utc


class P502ProductContractDeclarationValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "developer-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 8, 0, tzinfo=UTC),
        )

    def _validate(self, contract=None, **kwargs) -> ProductContractDeclarationValidation:
        return validate_product_contract_declaration(
            contract=self.contract if contract is None else contract,
            **kwargs,
        )

    def test_p4_08_exact_declaration_validates_as_provisional(self) -> None:
        result = self._validate()

        self.assertEqual(result.product_contract.subject_id, self.contract.record.subject_id)
        self.assertEqual(result.product_contract.version_id, self.contract.record.version_id)
        self.assertEqual(result.product_id, self.contract.product_id)
        self.assertEqual(result.product_version, "0.1.0")
        self.assertEqual(result.organization, self.organization)
        self.assertEqual(result.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(len(result.dependencies), 3)
        self.assertEqual(len(result.operations), 3)
        self.assertEqual(len(result.canonical_accesses), 3)
        with self.assertRaises(FrozenInstanceError):
            result.product_version = "changed"  # type: ignore[misc]

    def test_dependency_identity_versions_and_operations_are_inspectable(self) -> None:
        result = self._validate()
        dependencies = {item.dependency_id: item for item in result.dependencies}

        self.assertEqual(
            dependencies[CAP_001_DOCUMENT_ARTIFACT].contract_version,
            CAPABILITY_CONTRACT_VERSION,
        )
        self.assertEqual(
            dependencies[CAP_002_MEMORY_KNOWLEDGE].contract_version,
            CAPABILITY_CONTRACT_VERSION,
        )
        self.assertEqual(
            dependencies[GOVERNED_RUNTIME_DEPENDENCY].contract_version,
            GOVERNED_RUNTIME_CONTRACT_VERSION,
        )
        self.assertTrue(all(item.provisional for item in result.dependencies))
        operation_names = {item.operation_name for item in result.operations}
        self.assertIn(OP_RECORD_TASK_DECISION, operation_names)

    def test_validation_result_is_not_permission_authority_or_capability_activation(self) -> None:
        result = self._validate()
        result_fields = {item.name for item in fields(result)}
        dependency_fields = {item.name for item in fields(result.dependencies[0])}

        for forbidden in (
            "authentication",
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "capability_lifecycle",
            "active",
        ):
            self.assertNotIn(forbidden, result_fields)
            self.assertNotIn(forbidden, dependency_fields)

        self.assertEqual(result.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertTrue(all(item.provisional for item in result.dependencies))

    def test_non_provisional_contract_lifecycle_fails_closed(self) -> None:
        for lifecycle in (
            ProductContractLifecycle.DRAFT,
            ProductContractLifecycle.STABLE,
            ProductContractLifecycle.DEPRECATED,
            ProductContractLifecycle.RETIRED,
        ):
            with self.subTest(lifecycle=lifecycle.value):
                record = replace(self.contract.record, lifecycle_status=lifecycle.value)
                contract = replace(self.contract, record=record)
                with self.assertRaises(ProductContractLifecycleError):
                    self._validate(contract)

    def test_dependency_reliance_must_remain_explicitly_provisional(self) -> None:
        changed = replace(self.contract.dependencies[0], provisional=False)
        contract = replace(
            self.contract,
            dependencies=(changed,) + self.contract.dependencies[1:],
        )
        with self.assertRaises(ProductContractDependencyError):
            self._validate(contract)

    def test_dependency_allowed_operation_requires_exact_operation_declaration(self) -> None:
        changed = replace(
            self.contract.dependencies[0],
            allowed_operations=self.contract.dependencies[0].allowed_operations
            + ("p5.02.undeclared-operation",),
        )
        contract = replace(
            self.contract,
            dependencies=(changed,) + self.contract.dependencies[1:],
        )
        with self.assertRaises(ProductContractDependencyError):
            self._validate(contract)

    def test_read_operation_requires_authorization_and_data_governance(self) -> None:
        read_operation = self.contract.operations[0]
        changed = replace(
            read_operation,
            required_gates=(GovernedGateKind.DATA_GOVERNANCE,),
        )
        contract = replace(
            self.contract,
            operations=(changed,) + self.contract.operations[1:],
        )
        with self.assertRaises(ProductContractSecurityBoundaryError):
            self._validate(contract)

    def test_canonical_mutation_requires_organizational_authority_declaration(self) -> None:
        mutation = self.contract.operations[2]
        changed = replace(
            mutation,
            required_gates=(
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            ),
        )
        contract = replace(
            self.contract,
            operations=self.contract.operations[:2] + (changed,),
        )
        with self.assertRaises(ProductContractSecurityBoundaryError):
            self._validate(contract)

    def test_read_operation_without_canonical_read_declaration_fails_closed(self) -> None:
        changed = replace(self.contract.operations[0], canonical_accesses=())
        contract = replace(
            self.contract,
            operations=(changed,) + self.contract.operations[1:],
        )
        with self.assertRaises(ProductContractCanonicalAccessError):
            self._validate(contract)

    def test_canonical_mutation_without_write_declaration_fails_closed(self) -> None:
        mutation = self.contract.operations[2]
        access = replace(
            mutation.canonical_accesses[0],
            access_modes=(CanonicalAccessMode.READ,),
        )
        changed = replace(mutation, canonical_accesses=(access,))
        contract = replace(
            self.contract,
            operations=self.contract.operations[:2] + (changed,),
        )
        with self.assertRaises(ProductContractCanonicalAccessError):
            self._validate(contract)

    def test_authority_source_and_failure_declarations_are_preserved(self) -> None:
        result = self._validate()

        for access in result.canonical_accesses:
            self.assertTrue(access.authoritative_source.strip())
            self.assertTrue(access.failure_behavior.strip())
            self.assertTrue(access.authority_scope.strip())
            self.assertTrue(access.access_modes)

        with self.assertRaises(ValueError):
            replace(
                self.contract.operations[0].canonical_accesses[0],
                authoritative_source="",
            )

    def test_portability_retention_review_and_exit_are_required(self) -> None:
        required_fields = (
            "portability_responsibility",
            "retention_deletion_responsibility",
            "review_condition",
            "exit_path",
        )
        for field_name in required_fields:
            with self.subTest(field=field_name):
                with self.assertRaises(ValueError):
                    replace(self.contract, **{field_name: ""})

    def test_organization_scope_drift_fails_during_declaration_construction(self) -> None:
        with self.assertRaises(ValueError):
            replace(
                self.contract,
                product_id=Identity("product", "bounded-review-product", "other-org"),
            )

    def test_hidden_boundary_mechanisms_are_rejected_statically(self) -> None:
        hidden = (
            ProductBoundaryMechanism.INTERNAL_TABLE,
            ProductBoundaryMechanism.INTERNAL_IMPORT,
            ProductBoundaryMechanism.UNDOCUMENTED_ENDPOINT,
            ProductBoundaryMechanism.PRIVATE_EVENT_STREAM,
            ProductBoundaryMechanism.IMPLICIT_SHARED_STATE,
        )
        for mechanism in hidden:
            with self.subTest(mechanism=mechanism.value):
                with self.assertRaises(HiddenProductPlatformCouplingError):
                    self._validate(boundary_mechanisms=(mechanism,))

    def test_empty_or_mixed_boundary_mechanism_declaration_fails_closed(self) -> None:
        with self.assertRaises(HiddenProductPlatformCouplingError):
            self._validate(boundary_mechanisms=())
        with self.assertRaises(HiddenProductPlatformCouplingError):
            self._validate(
                boundary_mechanisms=(
                    ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,
                    ProductBoundaryMechanism.INTERNAL_IMPORT,
                )
            )

    def test_validation_model_remains_internal_reversible_and_domain_neutral(self) -> None:
        source = inspect.getsource(declaration_module).lower()
        for forbidden_domain in ("tender", "supplier", "procurement", "rfq"):
            self.assertNotIn(forbidden_domain, source)
        for forbidden_import in ("import yaml", "import json", "protobuf", "openapi"):
            self.assertNotIn(forbidden_import, source)
        self.assertIn("internal", source)
        self.assertIn("provisional", source)
        self.assertIn("not a standardized product contract schema", source)


if __name__ == "__main__":
    unittest.main()
