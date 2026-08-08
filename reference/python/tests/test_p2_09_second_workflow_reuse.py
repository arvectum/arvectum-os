from __future__ import annotations

import ast
from dataclasses import replace
from datetime import datetime, timezone
import inspect
import sys
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.event_provenance import EventReceipt
from arvectum_os_ref.governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractLifecycle,
    ProductOperationDeclaration,
    ProductRuntimeInteraction,
    start_product_governed_execution,
)
from arvectum_os_ref.relationships import (
    EndpointReferenceRole,
    RelationshipEndpoint,
    RelationshipTypeReference,
    TraversalDirection,
    create_typed_relationship,
    traverse_relationships,
)
from arvectum_os_ref.runtime_consistency import (
    ConsequentialOutcome,
    RetrySemantics,
    RuntimeConsistencyState,
    commit_canonical_mutation,
    record_external_consequence_attempt,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)


UTC = timezone.utc


class P209SecondBoundedWorkflowReuseProofTests(unittest.TestCase):
    """Prove two materially distinct workflows reuse the same bounded Core Runtime.

    This file is intentionally an evidence fixture rather than a new platform
    abstraction.  The post-P2.09 R3 gate is the designated point to refactor any
    abstraction pressure revealed by the two workflows.
    """

    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "initiator", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_actor = ActorContext(
            Principal(Identity("principal", "decision-actor", "platform")),
            self.organization,
        )
        self.producer = Identity("principal", "runtime-event-producer", "platform")
        self.dependency_id = Identity("platform-contract", "governed-runtime", "platform")

        # Workflow A: a direct canonical mutation against one exact current version.
        self.canonical_v1 = self._record(
            subject="canonical-subject",
            version="canonical-subject-v1",
            semantic_type="example.subject",
            authority_scope="example.subject/state",
            payload=(("state", "initial"),),
        )
        self.canonical_workflow = self._workflow(
            subject="canonical-workflow",
            version="canonical-workflow-v1",
            operation="update-subject",
            target=self.canonical_v1,
            side_effects=(OperationSideEffectClass.CANONICAL_MUTATION,),
        )
        self.canonical_gates = (
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.VALIDATION,
        )
        self.canonical_contract = self._contract(
            name="canonical-contract",
            product_name="bounded-consumer-a",
            workflow=self.canonical_workflow,
            required_gates=self.canonical_gates,
            canonical_accesses=(
                self._access(
                    semantic_type=self.canonical_v1.semantic_type,
                    authority_scope=self.canonical_v1.authority_scope,
                    modes=(CanonicalAccessMode.READ, CanonicalAccessMode.WRITE),
                ),
            ),
        )
        self.canonical_interaction = self._interaction(
            product_id=self.canonical_contract.product_id,
            workflow=self.canonical_workflow,
            operation="update-subject",
            material_inputs=(self.canonical_v1,),
            required_gates=self.canonical_gates,
        )
        self.canonical_running = self._run_interaction(
            contract=self.canonical_contract,
            interaction=self.canonical_interaction,
            execution_name="canonical-execution",
        )

        # Workflow B: resolve an earlier effective version while a future-effective
        # Canonical Head already exists, follow a version-pinned relationship, then
        # perform external-mutation/commitment effects under a different gate set.
        switch = self._time(60)
        self.external_v1 = self._record(
            subject="external-subject",
            version="external-subject-v1",
            semantic_type="example.subject",
            authority_scope="example.subject/state",
            payload=(("state", "currently-effective"),),
            effective_from=self._time(-60),
            effective_until=switch,
        )
        self.external_v2 = replace(
            self.external_v1,
            version_id=self._id("canonical-version", "external-subject-v2"),
            created_at=self._time(10),
            predecessor_version_id=self.external_v1.version_id,
            payload=(("state", "future-effective-head"),),
            effective_from=switch,
            effective_until=None,
        )
        self.external_lineage = CanonicalLineage((self.external_v2, self.external_v1))
        self.effective_external = self.external_lineage.resolve_effective(at=self._time(20))

        self.context_record = self._record(
            subject="context-subject",
            version="context-subject-v1",
            semantic_type="example.context",
            authority_scope="example.context/state",
            payload=(("context", "bounded"),),
        )
        self.relationship = create_typed_relationship(
            relationship_id=self._id("relationship", "external-to-context"),
            version_id=self._id("relationship-version", "external-to-context-v1"),
            relationship_type=RelationshipTypeReference(
                type_id=Identity("relationship-type", "uses-context", "platform"),
                version_id=Identity("relationship-type-version", "uses-context-v1", "platform"),
                semantic_name="uses_context",
                schema_version="1",
            ),
            source=RelationshipEndpoint(
                EndpointReferenceRole.VERSION_IDENTITY,
                self.effective_external.version_id,
            ),
            target=RelationshipEndpoint(
                EndpointReferenceRole.SUBJECT_IDENTITY,
                self.context_record.subject_id,
            ),
            organization=self.organization,
            actor=self.actor,
            authority_scope="platform.relationship/assertion",
            created_at=self._time(21),
            lifecycle_status="Active",
        )
        self.external_workflow = self._workflow(
            subject="external-workflow",
            version="external-workflow-v1",
            operation="apply-external-change",
            target=self.effective_external,
            side_effects=(
                OperationSideEffectClass.EXTERNAL_MUTATION,
                OperationSideEffectClass.COMMITMENT,
            ),
        )
        self.external_gates = (
            GovernedGateKind.ACTOR_ASSURANCE,
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
        self.external_contract = self._contract(
            name="external-contract",
            product_name="bounded-consumer-b",
            workflow=self.external_workflow,
            required_gates=self.external_gates,
            canonical_accesses=(
                self._access(
                    semantic_type=self.effective_external.semantic_type,
                    authority_scope=self.effective_external.authority_scope,
                    modes=(CanonicalAccessMode.READ,),
                ),
                self._access(
                    semantic_type=self.context_record.semantic_type,
                    authority_scope=self.context_record.authority_scope,
                    modes=(CanonicalAccessMode.READ,),
                ),
                self._access(
                    semantic_type=self.relationship.record.semantic_type,
                    authority_scope=self.relationship.record.authority_scope,
                    modes=(CanonicalAccessMode.READ,),
                ),
            ),
        )
        self.external_interaction = self._interaction(
            product_id=self.external_contract.product_id,
            workflow=self.external_workflow,
            operation="apply-external-change",
            material_inputs=(
                self.effective_external,
                self.context_record,
                self.relationship.record,
            ),
            required_gates=self.external_gates,
        )
        self.external_running = self._run_interaction(
            contract=self.external_contract,
            interaction=self.external_interaction,
            execution_name="external-execution",
        )

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 8, 10, 0, tzinfo=UTC) + __import__("datetime").timedelta(minutes=minute)

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(
        self,
        *,
        subject: str,
        version: str,
        semantic_type: str,
        authority_scope: str,
        payload: tuple[tuple[str, str], ...],
        effective_from: datetime | None = None,
        effective_until: datetime | None = None,
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("canonical-subject", subject),
            version_id=self._id("canonical-version", version),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "p2.09-test"),),
            payload=payload,
            lifecycle_status="Active",
            effective_from=effective_from,
            effective_until=effective_until,
        )

    def _workflow(
        self,
        *,
        subject: str,
        version: str,
        operation: str,
        target: CanonicalRecord,
        side_effects: tuple[OperationSideEffectClass, ...],
    ) -> WorkflowDefinition:
        record = CanonicalRecord(
            subject_id=self._id("workflow-subject", subject),
            version_id=self._id("workflow-version", version),
            semantic_type="platform.workflow",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id, target.subject_id, target.version_id),
            integrity_metadata=(("representation", "p2.09-test"),),
            payload=(("operation", operation),),
            lifecycle_status="Approved",
        )
        return WorkflowDefinition(
            record=record,
            operations=(
                WorkflowOperation(
                    semantic_name=operation,
                    target_subject_id=target.subject_id,
                    target_semantic_type=target.semantic_type,
                    side_effect_classes=side_effects,
                ),
            ),
        )

    def _access(
        self,
        *,
        semantic_type: str,
        authority_scope: str,
        modes: tuple[CanonicalAccessMode, ...],
    ) -> CanonicalAccessDeclaration:
        return CanonicalAccessDeclaration(
            semantic_type=semantic_type,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            access_modes=modes,
            authoritative_source="Arvectum OS within the declared Native authority scope",
            failure_behavior="fail closed on undeclared canonical reliance",
        )

    def _contract(
        self,
        *,
        name: str,
        product_name: str,
        workflow: WorkflowDefinition,
        required_gates: tuple[GovernedGateKind, ...],
        canonical_accesses: tuple[CanonicalAccessDeclaration, ...],
    ) -> ProductContract:
        product_id = self._id("product", product_name)
        operation = workflow.operations[0]
        record = CanonicalRecord(
            subject_id=self._id("product-contract-subject", name),
            version_id=self._id("product-contract-version", f"{name}-v1"),
            semantic_type="platform.product-contract",
            schema_version="p2.09-internal-1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.product-contract/boundary",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id, product_id),
            integrity_metadata=(("representation", "p2.09-test"),),
            payload=(("scope", "bounded second-workflow reuse proof"),),
            lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
        )
        return ProductContract(
            record=record,
            product_id=product_id,
            product_version="0.1",
            bounded_scope="one domain-neutral P2.09 reuse-proof interaction",
            compatibility_assumptions=(
                "bounded P2 Core Runtime internal/provisional semantics",
            ),
            dependencies=(
                PlatformDependencyDeclaration(
                    dependency_id=self.dependency_id,
                    contract_version="p2-core-runtime-internal-1",
                    allowed_operations=(operation.semantic_name,),
                    provider_responsibility="execute bounded governed runtime semantics",
                    consumer_responsibility="supply exact governed inputs and required gate evidence",
                    failure_behavior="fail closed before governed reliance",
                    provisional=True,
                ),
            ),
            operations=(
                ProductOperationDeclaration(
                    operation_name=operation.semantic_name,
                    dependency_id=self.dependency_id,
                    side_effect_classes=operation.side_effect_classes,
                    required_gates=required_gates,
                    canonical_accesses=canonical_accesses,
                    failure_behavior="fail closed without claiming a consequential result",
                ),
            ),
            portability_responsibility="preserve governed identities and exact version references",
            retention_deletion_responsibility="inherit applicable Organization retention/deletion rules",
            review_condition="mandatory R3 reuse refactoring review after P2.09",
            exit_path="refactor, contain or retire bounded evidence after R3",
        )

    def _interaction(
        self,
        *,
        product_id: Identity,
        workflow: WorkflowDefinition,
        operation: str,
        material_inputs: tuple[CanonicalRecord, ...],
        required_gates: tuple[GovernedGateKind, ...],
    ) -> ProductRuntimeInteraction:
        return ProductRuntimeInteraction(
            organization=self.organization,
            product_id=product_id,
            product_version="0.1",
            dependency_id=self.dependency_id,
            dependency_contract_version="p2-core-runtime-internal-1",
            workflow=workflow,
            operation_name=operation,
            material_inputs=material_inputs,
            required_gates=required_gates,
        )

    def _run_interaction(
        self,
        *,
        contract: ProductContract,
        interaction: ProductRuntimeInteraction,
        execution_name: str,
    ) -> GovernedExecutionContext:
        """One shared runtime path for both workflow configurations."""

        created = start_product_governed_execution(
            contract=contract,
            interaction=interaction,
            actor=self.actor,
            execution_id=self._id("execution-subject", execution_name),
            version_id=self._id("execution-version", f"{execution_name}-v1"),
            created_at=self._time(30),
        )
        awaiting = await_required_gates(
            created,
            version_id=self._id("execution-version", f"{execution_name}-v2"),
            actor=self.actor,
            created_at=self._time(31),
        )
        decisions = tuple(
            build_governed_gate_decision(
                execution=awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=self.decision_actor,
                basis_ref=self._id("governed-basis", f"{execution_name}-{kind.value}"),
                decision_id=self._id("gate-decision-subject", f"{execution_name}-{kind.value}"),
                version_id=self._id("gate-decision-version", f"{execution_name}-{kind.value}-v1"),
                created_at=self._time(32),
            )
            for kind in interaction.required_gates
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=self._id("execution-version", f"{execution_name}-v3"),
            actor=self.actor,
            created_at=self._time(33),
        )
        return transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", f"{execution_name}-v4"),
            actor=self.actor,
            created_at=self._time(34),
        )

    def _event_receipt(
        self,
        *,
        execution: GovernedExecutionContext,
        result: CanonicalRecord,
    ) -> EventReceipt:
        return EventReceipt(
            event_id=self._id("event-subject", "canonical-update-succeeded"),
            version_id=self._id("event-version", "canonical-update-succeeded-v1"),
            event_type="platform.canonical-mutation.succeeded",
            event_schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            authoritative_source="Arvectum OS",
            occurred_at=self._time(40),
            recorded_at=self._time(41),
            producer_id=self.producer,
            initiating_actor_id=self.principal.principal_id,
            execution_subject_id=execution.execution_subject_id,
            execution_version_id=execution.execution_version_id,
            related_subject_ids=(result.subject_id,),
            related_version_ids=(result.version_id,),
            correlation_refs=(execution.execution_subject_id,),
            causation_refs=(execution.execution_version_id,),
            classification="internal",
            access_scope="organization",
            provenance_refs=(
                self.producer,
                self.principal.principal_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                result.subject_id,
                result.version_id,
            ),
            integrity_metadata=(("representation", "p2.09-test-receipt"),),
            payload=(("operation", execution.operation_name), ("outcome", "Succeeded")),
        )

    def test_two_materially_distinct_workflows_reuse_same_governed_execution_type(self) -> None:
        self.assertIsInstance(self.canonical_running, GovernedExecutionContext)
        self.assertIsInstance(self.external_running, GovernedExecutionContext)
        self.assertEqual(self.canonical_running.lifecycle, GovernedExecutionLifecycle.RUNNING)
        self.assertEqual(self.external_running.lifecycle, GovernedExecutionLifecycle.RUNNING)
        self.assertNotEqual(
            self.canonical_running.operation_side_effects,
            self.external_running.operation_side_effects,
        )
        self.assertNotEqual(self.canonical_running.required_gates, self.external_running.required_gates)

    def test_both_workflows_pin_exact_product_contract_workflow_and_material_versions(self) -> None:
        pairs = (
            (
                self.canonical_running,
                self.canonical_contract,
                self.canonical_workflow,
                (self.canonical_v1.version_id,),
            ),
            (
                self.external_running,
                self.external_contract,
                self.external_workflow,
                (
                    self.effective_external.version_id,
                    self.context_record.version_id,
                    self.relationship.record.version_id,
                ),
            ),
        )
        for execution, contract, workflow, versions in pairs:
            with self.subTest(operation=execution.operation_name):
                self.assertEqual(execution.product_contract.version_id, contract.record.version_id)
                self.assertEqual(execution.workflow.version_id, workflow.workflow_version_id)
                self.assertEqual(tuple(pin.version_id for pin in execution.material_inputs), versions)
                self.assertTrue(execution.gates_satisfied)

    def test_second_workflow_relies_on_effective_version_not_future_canonical_head(self) -> None:
        self.assertIs(self.external_lineage.head, self.external_v2)
        self.assertIs(self.effective_external, self.external_v1)
        self.assertNotEqual(self.external_lineage.head.version_id, self.effective_external.version_id)
        self.assertEqual(
            self.external_running.material_inputs[0].version_id,
            self.effective_external.version_id,
        )
        self.assertNotEqual(
            self.external_running.material_inputs[0].version_id,
            self.external_lineage.head.version_id,
        )

    def test_second_workflow_reuses_version_pinned_relationship_without_authority_grant(self) -> None:
        matches = traverse_relationships(
            (self.relationship,),
            endpoint=RelationshipEndpoint(
                EndpointReferenceRole.VERSION_IDENTITY,
                self.effective_external.version_id,
            ),
            direction=TraversalDirection.OUTBOUND,
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].opposite_endpoint.identity, self.context_record.subject_id)
        self.assertIn(
            self.relationship.record.version_id,
            tuple(pin.version_id for pin in self.external_running.material_inputs),
        )
        self.assertFalse(self.relationship.intrinsically_grants_authorization)
        self.assertFalse(self.relationship.intrinsically_grants_organizational_authority)
        self.assertIn(GovernedGateKind.AUTHORIZATION, self.external_running.required_gates)
        self.assertIn(GovernedGateKind.CONSEQUENTIAL_APPROVAL, self.external_running.required_gates)

    def test_canonical_workflow_commits_exact_successor_and_event_once(self) -> None:
        candidate = replace(
            self.canonical_v1,
            version_id=self._id("canonical-version", "canonical-subject-v2"),
            created_at=self._time(40),
            predecessor_version_id=self.canonical_v1.version_id,
            provenance_refs=(
                self.principal.principal_id,
                self.canonical_running.execution_subject_id,
                self.canonical_running.execution_version_id,
                self.canonical_v1.subject_id,
                self.canonical_v1.version_id,
            ),
            payload=(("state", "updated"),),
        )
        receipt = self._event_receipt(execution=self.canonical_running, result=candidate)
        initial_state = RuntimeConsistencyState(canonical_records=(self.canonical_v1,))
        first = commit_canonical_mutation(
            state=initial_state,
            execution=self.canonical_running,
            expected_head_version_id=self.canonical_v1.version_id,
            candidate=candidate,
            event_receipt=receipt,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="canonical-subject-v2",
        )
        retry = commit_canonical_mutation(
            state=first.state,
            execution=self.canonical_running,
            expected_head_version_id=self.canonical_v1.version_id,
            candidate=candidate,
            event_receipt=receipt,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="canonical-subject-v2",
        )
        self.assertEqual(first.state.head.version_id, candidate.version_id)
        self.assertEqual(first.event.related_version_ids, (candidate.version_id,))
        self.assertFalse(first.duplicate)
        self.assertTrue(retry.duplicate)
        self.assertIs(retry.state, first.state)
        self.assertEqual(len(retry.state.canonical_records), 2)
        self.assertEqual(len(retry.state.admitted_events), 1)
        self.assertEqual(len(retry.state.attempts), 1)

    def test_second_workflow_records_external_effect_without_canonical_or_event_publication(self) -> None:
        initial_state = RuntimeConsistencyState(
            canonical_records=(self.external_v2, self.external_v1),
        )
        mutation = record_external_consequence_attempt(
            state=initial_state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-system-a"), ("command", "apply")),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="external-system-a-apply",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        commitment = record_external_consequence_attempt(
            state=mutation.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.COMMITMENT,
            effect_descriptor=(("commitment", "bounded-domain-neutral"),),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="bounded-domain-neutral-commitment",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(mutation.succeeded)
        self.assertTrue(commitment.succeeded)
        self.assertEqual(commitment.state.canonical_records, initial_state.canonical_records)
        self.assertFalse(commitment.state.admitted_events)
        self.assertEqual(len(commitment.state.attempts), 2)

    def test_second_workflow_keyed_external_retry_is_duplicate_not_second_effect(self) -> None:
        initial_state = RuntimeConsistencyState(
            canonical_records=(self.external_v2, self.external_v1),
        )
        first = record_external_consequence_attempt(
            state=initial_state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-system-a"), ("command", "apply")),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="external-system-a-apply",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        retry = record_external_consequence_attempt(
            state=first.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-system-a"), ("command", "apply")),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="external-system-a-apply",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(retry.duplicate)
        self.assertIs(retry.state, first.state)
        self.assertEqual(len(retry.state.attempts), 1)

    def test_shared_fixture_contains_one_governed_orchestration_path_not_two_harnesses(self) -> None:
        source = inspect.getsource(sys.modules[__name__])
        tree = ast.parse(source)
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        self.assertNotIn("arvectum_os_ref.reference_scenario", imported_modules)
        self.assertNotIn("arvectum_os_ref.reference_runtime_adapters", imported_modules)
        self.assertNotIn("arvectum_os_ref.runtime", imported_modules)

        helper_source = inspect.getsource(self._run_interaction)
        self.assertEqual(helper_source.count("start_product_governed_execution("), 1)
        self.assertEqual(helper_source.count("await_required_gates("), 1)
        self.assertEqual(helper_source.count("admit_ready_execution("), 1)
        self.assertEqual(helper_source.count("transition_governed_execution("), 1)


if __name__ == "__main__":
    unittest.main()
