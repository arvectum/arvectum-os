from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.product_contract as product_contract_module
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.governed_execution import (
    GovernedExecutionLifecycle,
    GovernedGateKind,
    GovernedGateOutcome,
    RequiredGateUnresolvedError,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    HiddenProductPlatformCouplingError,
    PlatformDependencyDeclaration,
    ProductBoundaryMechanism,
    ProductContract,
    ProductContractCanonicalAccessError,
    ProductContractDependencyError,
    ProductContractLifecycle,
    ProductContractLifecycleError,
    ProductContractOperationError,
    ProductContractScopeError,
    ProductContractSecurityBoundaryError,
    ProductOperationDeclaration,
    ProductRuntimeInteraction,
    start_product_governed_execution,
    validate_product_contract_interaction,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)


UTC = timezone.utc


class P207ProductContractRuntimeBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_actor = ActorContext(
            Principal(Identity("principal", "decision-principal", "platform")),
            self.organization,
        )
        self.product_id = self._id("product", "synthetic-product")
        self.dependency_id = Identity("platform-contract", "governed-runtime", "platform")
        self.subject = self._record("subject-a", "subject-a-v1", "example.subject")
        self.required_gates = (
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
        )
        self.workflow = self._workflow()
        self.contract = self._contract()
        self.interaction = self._interaction()

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 8, 9, minute, tzinfo=UTC)

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(self, subject: str, version: str, semantic_type: str) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("canonical-subject", subject),
            version_id=self._id("canonical-version", version),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="example.subject/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "test"),),
            payload=(("value", version),),
            lifecycle_status="Active",
        )

    def _workflow(self) -> WorkflowDefinition:
        record = CanonicalRecord(
            subject_id=self._id("workflow-subject", "synthetic-workflow"),
            version_id=self._id("workflow-version", "synthetic-workflow-v1"),
            semantic_type="platform.workflow",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id, self.subject.subject_id),
            integrity_metadata=(("representation", "test"),),
            lifecycle_status="Approved",
        )
        return WorkflowDefinition(
            record=record,
            operations=(
                WorkflowOperation(
                    semantic_name="update-subject",
                    target_subject_id=self.subject.subject_id,
                    target_semantic_type=self.subject.semantic_type,
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )

    def _dependency(self) -> PlatformDependencyDeclaration:
        return PlatformDependencyDeclaration(
            dependency_id=self.dependency_id,
            contract_version="p2-core-runtime-internal-1",
            allowed_operations=("update-subject",),
            provider_responsibility="execute bounded governed runtime semantics",
            consumer_responsibility="supply exact governed inputs and gate evidence",
            failure_behavior="fail closed before governed reliance",
            provisional=True,
        )

    def _access(
        self,
        modes: tuple[CanonicalAccessMode, ...] = (
            CanonicalAccessMode.READ,
            CanonicalAccessMode.WRITE,
        ),
        *,
        authority_scope: str = "example.subject/state",
    ) -> CanonicalAccessDeclaration:
        return CanonicalAccessDeclaration(
            semantic_type=self.subject.semantic_type,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            access_modes=modes,
            authoritative_source="Arvectum OS within the declared Native authority scope",
            failure_behavior="reject undeclared or mismatched canonical access",
        )

    def _operation(
        self,
        *,
        side_effects: tuple[OperationSideEffectClass, ...] = (
            OperationSideEffectClass.CANONICAL_MUTATION,
        ),
        required_gates: tuple[GovernedGateKind, ...] | None = None,
        accesses: tuple[CanonicalAccessDeclaration, ...] | None = None,
    ) -> ProductOperationDeclaration:
        return ProductOperationDeclaration(
            operation_name="update-subject",
            dependency_id=self.dependency_id,
            side_effect_classes=side_effects,
            required_gates=self.required_gates if required_gates is None else required_gates,
            canonical_accesses=(self._access(),) if accesses is None else accesses,
            failure_behavior="fail closed without mutation",
        )

    def _contract(
        self,
        *,
        lifecycle: ProductContractLifecycle = ProductContractLifecycle.PROVISIONAL,
        dependency: PlatformDependencyDeclaration | None = None,
        operation: ProductOperationDeclaration | None = None,
    ) -> ProductContract:
        record = CanonicalRecord(
            subject_id=self._id("product-contract-subject", "synthetic-product-boundary"),
            version_id=self._id("product-contract-version", "synthetic-product-boundary-v1"),
            semantic_type="platform.product-contract",
            schema_version="p2.07-internal-1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.product-contract/boundary",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id, self.product_id),
            integrity_metadata=(("representation", "frozen-in-memory-reference"),),
            payload=(("scope", "bounded synthetic product/runtime interaction"),),
            lifecycle_status=lifecycle.value,
        )
        return ProductContract(
            record=record,
            product_id=self.product_id,
            product_version="0.1",
            bounded_scope="one synthetic product-like canonical mutation",
            compatibility_assumptions=(
                "Accepted RFC-0004/RFC-0005 semantics in the bounded Core Runtime",
            ),
            dependencies=(self._dependency() if dependency is None else dependency,),
            operations=(self._operation() if operation is None else operation,),
            portability_responsibility="preserve governed identities and exact version references",
            retention_deletion_responsibility="inherit applicable Organization retention/deletion rules",
            review_condition="review at P2.09 reuse proof or earlier material boundary change",
            exit_path="revise, stabilize through separate governance, contain or retire",
        )

    def _interaction(
        self,
        *,
        product_id: Identity | None = None,
        product_version: str = "0.1",
        dependency_id: Identity | None = None,
        dependency_contract_version: str = "p2-core-runtime-internal-1",
        required_gates: tuple[GovernedGateKind, ...] | None = None,
        mechanism: ProductBoundaryMechanism = ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,
    ) -> ProductRuntimeInteraction:
        return ProductRuntimeInteraction(
            organization=self.organization,
            product_id=self.product_id if product_id is None else product_id,
            product_version=product_version,
            dependency_id=self.dependency_id if dependency_id is None else dependency_id,
            dependency_contract_version=dependency_contract_version,
            workflow=self.workflow,
            operation_name="update-subject",
            material_inputs=(self.subject,),
            required_gates=self.required_gates if required_gates is None else required_gates,
            mechanism=mechanism,
        )

    def _start(self):
        return start_product_governed_execution(
            contract=self.contract,
            interaction=self.interaction,
            actor=self.actor,
            execution_id=self._id("execution-subject", "product-execution"),
            version_id=self._id("execution-version", "product-execution-v1"),
            created_at=self._time(1),
        )

    def test_contract_is_immutable_exact_governed_version(self) -> None:
        self.assertEqual(self.contract.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(self.contract.version_pin.version_id, self.contract.record.version_id)
        self.assertIn(self.product_id, self.contract.record.provenance_refs)
        with self.assertRaises(FrozenInstanceError):
            self.contract.product_version = "changed"  # type: ignore[misc]

    def test_valid_contract_admits_and_runtime_pins_exact_contract_version(self) -> None:
        admission = validate_product_contract_interaction(
            contract=self.contract, interaction=self.interaction
        )
        self.assertEqual(admission.product_contract.version_id, self.contract.record.version_id)
        created = self._start()
        self.assertEqual(created.lifecycle, GovernedExecutionLifecycle.CREATED)
        self.assertEqual(created.product_contract.version_id, self.contract.record.version_id)
        self.assertIn(self.contract.record.version_id, created.record.provenance_refs)

    def test_contract_validation_does_not_satisfy_runtime_gates(self) -> None:
        awaiting = await_required_gates(
            self._start(),
            version_id=self._id("execution-version", "product-execution-v2"),
            actor=self.actor,
            created_at=self._time(2),
        )
        self.assertFalse(awaiting.gate_decisions)
        with self.assertRaises(RequiredGateUnresolvedError):
            admit_ready_execution(
                awaiting,
                decisions=(),
                version_id=self._id("execution-version", "product-execution-v3"),
                actor=self.actor,
                created_at=self._time(3),
            )

    def test_gate_decision_keeps_exact_contract_attribution(self) -> None:
        awaiting = await_required_gates(
            self._start(),
            version_id=self._id("execution-version", "product-execution-v2"),
            actor=self.actor,
            created_at=self._time(2),
        )
        decision = build_governed_gate_decision(
            execution=awaiting,
            kind=GovernedGateKind.AUTHORIZATION,
            outcome=GovernedGateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=self._id("governed-basis", "authorization-basis"),
            decision_id=self._id("gate-decision-subject", "authorization-decision"),
            version_id=self._id("gate-decision-version", "authorization-decision-v1"),
            created_at=self._time(3),
        )
        self.assertEqual(decision.product_contract_version_id, self.contract.record.version_id)

    def test_product_identity_version_and_lifecycle_fail_closed(self) -> None:
        with self.assertRaises(ProductContractScopeError):
            validate_product_contract_interaction(
                contract=self.contract,
                interaction=self._interaction(product_id=self._id("product", "other")),
            )
        with self.assertRaises(ProductContractScopeError):
            validate_product_contract_interaction(
                contract=self.contract,
                interaction=self._interaction(product_version="0.2"),
            )
        for lifecycle in (
            ProductContractLifecycle.DRAFT,
            ProductContractLifecycle.STABLE,
            ProductContractLifecycle.DEPRECATED,
            ProductContractLifecycle.RETIRED,
        ):
            with self.subTest(lifecycle=lifecycle.value):
                with self.assertRaises(ProductContractLifecycleError):
                    validate_product_contract_interaction(
                        contract=self._contract(lifecycle=lifecycle),
                        interaction=self.interaction,
                    )

    def test_dependency_identity_version_and_operation_must_be_declared(self) -> None:
        with self.assertRaises(ProductContractDependencyError):
            validate_product_contract_interaction(
                contract=self.contract,
                interaction=self._interaction(
                    dependency_id=Identity("platform-contract", "other", "platform")
                ),
            )
        with self.assertRaises(ProductContractDependencyError):
            validate_product_contract_interaction(
                contract=self.contract,
                interaction=self._interaction(
                    dependency_contract_version="p2-core-runtime-internal-2"
                ),
            )
        dependency = replace(self._dependency(), allowed_operations=("other-operation",))
        with self.assertRaises(ProductContractDependencyError):
            validate_product_contract_interaction(
                contract=self._contract(dependency=dependency), interaction=self.interaction
            )

    def test_hidden_internal_coupling_is_rejected(self) -> None:
        for mechanism in (
            ProductBoundaryMechanism.INTERNAL_TABLE,
            ProductBoundaryMechanism.INTERNAL_IMPORT,
            ProductBoundaryMechanism.UNDOCUMENTED_ENDPOINT,
            ProductBoundaryMechanism.PRIVATE_EVENT_STREAM,
            ProductBoundaryMechanism.IMPLICIT_SHARED_STATE,
        ):
            with self.subTest(mechanism=mechanism.value):
                with self.assertRaises(HiddenProductPlatformCouplingError):
                    validate_product_contract_interaction(
                        contract=self.contract,
                        interaction=self._interaction(mechanism=mechanism),
                    )

    def test_canonical_read_write_and_authority_scope_are_enforced(self) -> None:
        for accesses in (
            (self._access((CanonicalAccessMode.WRITE,)),),
            (self._access((CanonicalAccessMode.READ,)),),
            (self._access(authority_scope="different.authority/scope"),),
        ):
            with self.subTest(accesses=accesses):
                with self.assertRaises(ProductContractCanonicalAccessError):
                    validate_product_contract_interaction(
                        contract=self._contract(operation=self._operation(accesses=accesses)),
                        interaction=self.interaction,
                    )

    def test_contract_required_authority_gate_cannot_be_dropped(self) -> None:
        reduced = (GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE)
        with self.assertRaises(ProductContractSecurityBoundaryError):
            validate_product_contract_interaction(
                contract=self.contract,
                interaction=self._interaction(required_gates=reduced),
            )

    def test_workflow_side_effects_and_operation_must_match_contract(self) -> None:
        with self.assertRaises(ProductContractOperationError):
            validate_product_contract_interaction(
                contract=self._contract(
                    operation=self._operation(side_effects=(OperationSideEffectClass.READ_ONLY,))
                ),
                interaction=self.interaction,
            )
        with self.assertRaises(ProductContractOperationError):
            validate_product_contract_interaction(
                contract=self._contract(
                    operation=replace(self._operation(), operation_name="different-operation")
                ),
                interaction=self.interaction,
            )

    def test_cross_organization_actor_cannot_enter_runtime(self) -> None:
        other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        other_actor = ActorContext(self.principal, other_org)
        with self.assertRaises(ProductContractScopeError):
            start_product_governed_execution(
                contract=self.contract,
                interaction=self.interaction,
                actor=other_actor,
                execution_id=self._id("execution-subject", "cross-org"),
                version_id=self._id("execution-version", "cross-org-v1"),
                created_at=self._time(1),
            )

    def test_provisional_contract_requires_boundary_responsibilities(self) -> None:
        for changes in (
            {"compatibility_assumptions": ()},
            {"review_condition": ""},
            {"exit_path": ""},
            {"portability_responsibility": ""},
            {"retention_deletion_responsibility": ""},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    replace(self.contract, **changes)

    def test_provisional_dependency_does_not_claim_capability_lifecycle(self) -> None:
        dependency = self.contract.dependencies[0]
        self.assertTrue(dependency.provisional)
        self.assertFalse(hasattr(dependency, "capability_lifecycle"))
        self.assertFalse(hasattr(dependency, "active"))

    def test_runtime_boundary_remains_internal_domain_neutral(self) -> None:
        source = inspect.getsource(product_contract_module).lower()
        for forbidden in ("tender", "supplier", "procurement", "rfq"):
            self.assertNotIn(forbidden, source)
        self.assertIn("internal", source)
        self.assertIn("provisional", source)
        self.assertIn("not a standardized manifest", source)


if __name__ == "__main__":
    unittest.main()
