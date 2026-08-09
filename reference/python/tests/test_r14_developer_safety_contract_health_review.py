from __future__ import annotations

import ast
from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_composition as facade_module
import bounded_product_ref.integration_journeys as product_journeys
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_composition import (
    IntegrationCompositionConstructionError,
    IntegrationCompositionEvidenceRequiredError,
    IntegrationCompositionFacade,
    compose_integration_facade,
)
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    DeprecatedDependencyResolutionError,
    GovernedDependencyVersionEvidence,
    UnsupportedDependencyResolutionError,
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
from bounded_product_ref.integration_journeys import (
    enter_facade_read_journey,
    start_facade_action_journey,
)


UTC = timezone.utc


class R14DeveloperSafetyContractHealthReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "r14-developer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = product_id_for(self.actor)
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=self._time(0),
        )
        self.access = AccessRequest(
            actor=self.actor,
            purpose="bounded-product-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.document_request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=self.access,
        )

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 9, 15, minute, tzinfo=UTC)

    def _supported_versions(self) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "r14-current-provider-evidence:"
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
            integrity_metadata=(("representation", "r14-contract-health-test"),),
            payload=(),
            lifecycle_status=lifecycle_status,
        )

    def _runtime_interaction(self) -> ProductRuntimeInteraction:
        task_subject = Identity("product-task", "r14-task", "org-a")
        task_record = self._record(
            subject_id=task_subject,
            version_id=Identity("product-task-version", "r14-task-v1", "org-a"),
            semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
            authority_scope=PRODUCT_TASK_AUTHORITY_SCOPE,
            lifecycle_status="Open",
            provenance_refs=(self.principal.principal_id, self.product_id),
        )
        workflow_record = self._record(
            subject_id=Identity("workflow-subject", "r14-task-decision", "org-a"),
            version_id=Identity("workflow-version", "r14-task-decision-v1", "org-a"),
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

    def _changed_support(
        self,
        *,
        dependency_id: Identity,
        disposition: DependencySupportDisposition,
    ) -> tuple[GovernedDependencyVersionEvidence, ...]:
        changed = []
        for item in self._supported_versions():
            if item.dependency_id != dependency_id:
                changed.append(item)
                continue
            migration = None
            if disposition in (
                DependencySupportDisposition.DEPRECATED,
                DependencySupportDisposition.RETIRED,
            ):
                migration = "Review and revise the immutable Product Contract reliance."
            changed.append(
                replace(
                    item,
                    disposition=disposition,
                    governance_reference=(
                        "r14-updated-provider-evidence:"
                        f"{dependency_id.namespace}:{dependency_id.value}:"
                        f"{item.contract_version}:{disposition.value}"
                    ),
                    migration_obligation=migration,
                )
            )
        return tuple(changed)

    def test_r14_f1_direct_facade_construction_fails_closed(self) -> None:
        composed = self._facade()
        with self.assertRaises(IntegrationCompositionConstructionError):
            IntegrationCompositionFacade(
                contract=self.contract,
                actor=self.actor,
                declaration=composed.declaration_evidence,
                compatibility=composed.compatibility_evidence,
            )

    def test_r14_f2_j1_requires_explicit_current_dependency_evidence(self) -> None:
        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            self._facade().admit_capability(self.document_request)

    def test_r14_f2_j2_requires_explicit_current_dependency_evidence(self) -> None:
        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            self._facade().start_governed_execution(
                interaction=self._runtime_interaction(),
                execution_id=Identity("execution-subject", "r14-missing-current", "org-a"),
                version_id=Identity("execution-version", "r14-missing-current-v1", "org-a"),
                created_at=self._time(2),
            )

    def test_composition_time_supported_dependency_cannot_hide_current_deprecation_for_j1(self) -> None:
        facade = self._facade()
        current = self._changed_support(
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            disposition=DependencySupportDisposition.DEPRECATED,
        )
        with self.assertRaises(DeprecatedDependencyResolutionError):
            facade.admit_capability(
                self.document_request,
                governed_versions=current,
            )

    def test_composition_time_supported_dependency_cannot_hide_current_unsupported_j2(self) -> None:
        facade = self._facade()
        current = self._changed_support(
            dependency_id=GOVERNED_RUNTIME_DEPENDENCY,
            disposition=DependencySupportDisposition.UNSUPPORTED,
        )
        with self.assertRaises(UnsupportedDependencyResolutionError):
            facade.start_governed_execution(
                interaction=self._runtime_interaction(),
                execution_id=Identity("execution-subject", "r14-unsupported", "org-a"),
                version_id=Identity("execution-version", "r14-unsupported-v1", "org-a"),
                created_at=self._time(3),
                governed_versions=current,
            )

    def test_current_supported_evidence_allows_j1_without_creating_authority(self) -> None:
        admission = self._facade().admit_capability(
            self.document_request,
            governed_versions=self._supported_versions(),
        )
        self.assertEqual(admission.product_contract_version_id, self.contract.record.version_id)
        names = {field.name for field in fields(admission)}
        for forbidden in (
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "data_right",
            "active",
        ):
            self.assertNotIn(forbidden, names)

    def test_current_supported_evidence_allows_j2_with_gates_still_unresolved(self) -> None:
        execution = self._facade().start_governed_execution(
            interaction=self._runtime_interaction(),
            execution_id=Identity("execution-subject", "r14-supported", "org-a"),
            version_id=Identity("execution-version", "r14-supported-v1", "org-a"),
            created_at=self._time(4),
            governed_versions=self._supported_versions(),
        )
        self.assertEqual(execution.product_contract, self.contract.version_pin)
        self.assertFalse(execution.gate_decisions)
        self.assertFalse(execution.gates_satisfied)

    def test_product_journeys_pass_current_evidence_without_new_platform_imports(self) -> None:
        facade = self._facade()
        entry = enter_facade_read_journey(
            facade=facade,
            capability_requests=(self.document_request,),
            governed_versions=self._supported_versions(),
        )
        self.assertEqual(len(entry.capability_admissions), 1)

        execution = start_facade_action_journey(
            facade=facade,
            interaction=self._runtime_interaction(),
            execution_id=Identity("execution-subject", "r14-product-journey", "org-a"),
            version_id=Identity("execution-version", "r14-product-journey-v1", "org-a"),
            created_at=self._time(5),
            governed_versions=self._supported_versions(),
        )
        self.assertFalse(execution.gate_decisions)

        tree = ast.parse(inspect.getsource(product_journeys))
        platform_imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("arvectum_os_ref")
        )
        self.assertEqual(platform_imports, ("arvectum_os_ref.integration_composition",))

    def test_composition_snapshot_is_inspection_evidence_not_current_authority(self) -> None:
        facade = self._facade()
        self.assertTrue(facade.compatibility_evidence.is_compatible)
        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            facade.admit_capability(self.document_request)

    def test_r14_remediation_stays_internal_provisional_and_does_not_select_registry_or_public_stack(self) -> None:
        source = inspect.getsource(facade_module).lower()
        self.assertIn("internal", source)
        self.assertIn("provisional", source)
        self.assertIn("current governed", source)
        self.assertIn("resolve_product_contract_dependencies", source)
        self.assertIn("_internal_composition_token", source)

        for forbidden in (
            "import fastapi",
            "import requests",
            "import grpc",
            "import socket",
            "import yaml",
            "import json",
            "protobuf",
            "openapi",
            "semver",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
