from __future__ import annotations

from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_evidence as evidence_module
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.event_provenance import EventIdentityConflictError
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_composition import compose_integration_facade
from arvectum_os_ref.integration_evidence import (
    IntegrationEvidenceError,
    PORTABLE_FIXTURE_AUTHORITY_STATUS,
    TELEMETRY_AUTHORITY_STATUS,
    build_integration_event_support,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
)
from bounded_product_ref.contract import (
    GOVERNED_RUNTIME_CONTRACT_VERSION,
    GOVERNED_RUNTIME_DEPENDENCY,
    OP_RECORD_TASK_DECISION,
    PRODUCT_TASK_AUTHORITY_SCOPE,
    PRODUCT_TASK_SEMANTIC_TYPE,
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)


UTC = timezone.utc


class P507EventProvenancePortabilityIntegrationSupportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "p5-07-integration", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = product_id_for(self.actor)
        self.contract = build_p4_08_product_contract(actor=self.actor, created_at=self._time(0))

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 9, 14, minute, tzinfo=UTC)

    def _supported_versions(self) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "test-governed-provider-evidence:"
                    f"{dependency.dependency_id.namespace}:"
                    f"{dependency.dependency_id.value}:"
                    f"{dependency.contract_version}"
                ),
            )
            for dependency in self.contract.dependencies
        )

    def _facade(self):
        return compose_integration_facade(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )

    def _record(
        self,
        *,
        subject_id: Identity,
        version_id: Identity,
        semantic_type: str,
        authority_scope: str,
        lifecycle_status: str,
        provenance_refs: tuple[Identity, ...],
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=subject_id,
            version_id=version_id,
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(1),
            provenance_refs=provenance_refs,
            integrity_metadata=(("representation", "p5.07-test"),),
            payload=(),
            lifecycle_status=lifecycle_status,
        )

    def _interaction(self) -> ProductRuntimeInteraction:
        task_subject = Identity("product-task", "task-p5-07", "org-a")
        task_record = self._record(
            subject_id=task_subject,
            version_id=Identity("product-task-version", "task-p5-07-v1", "org-a"),
            semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
            authority_scope=PRODUCT_TASK_AUTHORITY_SCOPE,
            lifecycle_status="Open",
            provenance_refs=(self.principal.principal_id, self.product_id),
        )
        workflow_record = self._record(
            subject_id=Identity("workflow-subject", "p5-07-task-decision", "org-a"),
            version_id=Identity("workflow-version", "p5-07-task-decision-v1", "org-a"),
            semantic_type="platform.workflow",
            authority_scope="platform.workflow/definition",
            lifecycle_status=WorkflowLifecycle.APPROVED.value,
            provenance_refs=(self.principal.principal_id, task_subject),
        )
        workflow = WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=OP_RECORD_TASK_DECISION,
                    target_subject_id=task_subject,
                    target_semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )
        return ProductRuntimeInteraction(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=GOVERNED_RUNTIME_DEPENDENCY,
            dependency_contract_version=GOVERNED_RUNTIME_CONTRACT_VERSION,
            workflow=workflow,
            operation_name=OP_RECORD_TASK_DECISION,
            material_inputs=(task_record,),
            required_gates=(
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            ),
        )

    def _execution(self, *, actor: ActorContext | None = None):
        facade = self._facade() if actor is None else compose_integration_facade(
            contract=self.contract,
            actor=actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )
        return facade, facade.start_governed_execution(
            interaction=self._interaction(),
            execution_id=Identity("execution-subject", "p5-07-task-1", "org-a"),
            version_id=Identity("execution-version", "p5-07-task-1-v1", "org-a"),
            created_at=self._time(2),
            governed_versions=self._supported_versions(),
        )

    def _support(self, *, facade=None, execution=None, payload=(), admitted_events=()):
        if facade is None or execution is None:
            facade, execution = self._execution()
        interaction = self._interaction()
        return build_integration_event_support(
            facade=facade,
            execution=execution,
            event_id=Identity("event-subject", "p5-07-action-started", "org-a"),
            event_version_id=Identity("event-version", "p5-07-action-started-v1", "org-a"),
            event_type="platform.integration.governed-action.started",
            event_schema_version="1",
            occurred_at=self._time(2),
            recorded_at=self._time(3),
            related_records=interaction.material_inputs,
            admitted_events=admitted_events,
            payload=payload,
        )

    def test_event_preserves_exact_actor_execution_product_contract_and_version_context(self) -> None:
        facade, execution = self._execution()
        result = self._support(facade=facade, execution=execution)
        event = result.admission.event

        self.assertEqual(event.initiating_actor_id, self.principal.principal_id)
        self.assertEqual(event.execution_subject_id, execution.execution_subject_id)
        self.assertEqual(event.execution_version_id, execution.execution_version_id)
        self.assertIn(self.product_id, event.record.provenance_refs)
        self.assertIn(self.contract.record.subject_id, event.record.provenance_refs)
        self.assertIn(self.contract.record.version_id, event.record.provenance_refs)
        self.assertEqual(event.correlation_refs, (execution.execution_subject_id,))
        self.assertEqual(event.causation_refs, (execution.execution_version_id,))

    def test_product_contract_continuity_cannot_be_dropped_before_event_support(self) -> None:
        facade, execution = self._execution()
        drifted = replace(execution, product_contract=None)

        with self.assertRaises(IntegrationEvidenceError):
            self._support(facade=facade, execution=drifted)

    def test_derived_telemetry_is_explicitly_non_authoritative(self) -> None:
        result = self._support()

        self.assertEqual(result.telemetry.authority_status, TELEMETRY_AUTHORITY_STATUS)
        self.assertEqual(result.telemetry.product_contract, self.contract.version_pin)
        self.assertEqual(result.telemetry.event, result.admission.event.version_pin)
        field_names = {field.name for field in fields(result.telemetry)}
        for forbidden in (
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "canonical_record",
        ):
            self.assertNotIn(forbidden, field_names)

    def test_portable_fixture_preserves_semantic_identities_and_relationships(self) -> None:
        result = self._support()
        fixture = result.portable_fixture

        self.assertEqual(fixture.authority_status, PORTABLE_FIXTURE_AUTHORITY_STATUS)
        self.assertEqual(fixture.product_id, self.product_id)
        self.assertEqual(fixture.product_contract, self.contract.version_pin)
        kinds = {link.kind for link in fixture.semantic_links}
        self.assertTrue(
            {
                "event-execution-version",
                "event-execution-correlation",
                "event-product-contract-version",
                "product-contract-product",
                "event-initiating-actor",
                "event-related-version",
            }.issubset(kinds)
        )
        self.assertTrue(all(link.canonical_typed_relationship is False for link in fixture.semantic_links))

    def test_represented_actor_context_is_preserved_without_erasing_actual_actor(self) -> None:
        represented = Principal(Identity("principal", "represented-user", "platform"))
        actor = ActorContext(self.principal, self.org, represented_principal=represented)
        contract = build_p4_08_product_contract(actor=actor, created_at=self._time(0))
        facade = compose_integration_facade(
            contract=contract,
            actor=actor,
            effective_product_contract=contract.version_pin,
            governed_versions=tuple(
                GovernedDependencyVersionEvidence(
                    dependency_id=dependency.dependency_id,
                    contract_version=dependency.contract_version,
                    disposition=DependencySupportDisposition.SUPPORTED,
                    governance_reference="p5.07-represented-actor-test",
                )
                for dependency in contract.dependencies
            ),
        )
        interaction = self._interaction()
        execution = facade.start_governed_execution(
            interaction=interaction,
            execution_id=Identity("execution-subject", "p5-07-represented", "org-a"),
            version_id=Identity("execution-version", "p5-07-represented-v1", "org-a"),
            created_at=self._time(2),
            governed_versions=tuple(
                GovernedDependencyVersionEvidence(
                    dependency_id=dependency.dependency_id,
                    contract_version=dependency.contract_version,
                    disposition=DependencySupportDisposition.SUPPORTED,
                    governance_reference="p5.07-represented-actor-test-current",
                )
                for dependency in contract.dependencies
            ),
        )
        result = build_integration_event_support(
            facade=facade,
            execution=execution,
            event_id=Identity("event-subject", "p5-07-represented-event", "org-a"),
            event_version_id=Identity("event-version", "p5-07-represented-event-v1", "org-a"),
            event_type="platform.integration.governed-action.started",
            event_schema_version="1",
            occurred_at=self._time(2),
            recorded_at=self._time(3),
            related_records=interaction.material_inputs,
        )

        self.assertEqual(result.telemetry.actual_actor_id, self.principal.principal_id)
        self.assertEqual(result.telemetry.represented_actor_id, represented.principal_id)
        self.assertIn(represented.principal_id, result.admission.event.record.provenance_refs)
        self.assertIn("event-represented-actor", {link.kind for link in result.portable_fixture.semantic_links})

    def test_duplicate_delivery_is_idempotently_recognized_by_existing_event_owner(self) -> None:
        first = self._support()
        second = self._support(admitted_events=first.admission.admitted_events)

        self.assertTrue(second.admission.duplicate_delivery)
        self.assertEqual(second.admission.event, first.admission.event)
        self.assertEqual(second.portable_fixture.event, first.portable_fixture.event)

    def test_conflicting_event_identity_remains_owned_by_existing_event_runtime(self) -> None:
        first = self._support(payload=(("attempt", "1"),))
        with self.assertRaises(EventIdentityConflictError):
            self._support(
                payload=(("attempt", "2"),),
                admitted_events=first.admission.admitted_events,
            )

    def test_wrong_organization_event_identity_fails_closed(self) -> None:
        facade, execution = self._execution()
        interaction = self._interaction()
        with self.assertRaises(ValueError):
            build_integration_event_support(
                facade=facade,
                execution=execution,
                event_id=Identity("event-subject", "p5-07-wrong-org", "org-b"),
                event_version_id=Identity("event-version", "p5-07-wrong-org-v1", "org-b"),
                event_type="platform.integration.governed-action.started",
                event_schema_version="1",
                occurred_at=self._time(2),
                recorded_at=self._time(3),
                related_records=interaction.material_inputs,
            )

    def test_module_remains_internal_provisional_and_vendor_serialization_neutral(self) -> None:
        source = inspect.getsource(evidence_module).lower()
        self.assertIn("internal/provisional", source)
        self.assertIn("non-authoritative", source)
        self.assertIn("non-canonical", source)
        self.assertIn("admit_event", source)
        self.assertNotIn("bounded_product_ref", source)

        for forbidden in (
            "import json",
            "import yaml",
            "import requests",
            "import grpc",
            "import socket",
            "protobuf",
            "openapi",
            "kafka",
            "rabbitmq",
            "opentelemetry",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
