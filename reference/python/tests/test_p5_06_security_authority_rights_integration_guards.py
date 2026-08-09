from __future__ import annotations

from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_composition as facade_module
import arvectum_os_ref.integration_scaffolding as scaffolding_module
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
)
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.governed_execution import (
    GovernedExecutionLifecycle,
    GovernedGateKind,
    GovernedGateOutcome,
    RequiredGateDeniedError,
    RequiredGateUnresolvedError,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    resume_governed_execution,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_composition import compose_integration_facade
from arvectum_os_ref.integration_scaffolding import run_local_integration_harness
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
    consume_document,
)
from arvectum_os_ref.product_contract import (
    ProductContractScopeError,
    ProductRuntimeInteraction,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
    ProductContractResolutionContinuityError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
)
from arvectum_os_ref.workspace_shell import PresentationAuthority
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


class P506SecurityAuthorityRightsIntegrationGuardsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.principal = Principal(Identity("principal", "p5-06-developer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.other_actor = ActorContext(
            Principal(Identity("principal", "p5-06-other", "platform")),
            self.other_org,
        )
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

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 9, 14, minute, tzinfo=UTC)

    def _supported_versions(self) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "p5.06-governed-provider-evidence:"
                    f"{dependency.dependency_id.namespace}:"
                    f"{dependency.dependency_id.value}:"
                    f"{dependency.contract_version}"
                ),
            )
            for dependency in self.contract.dependencies
        )

    def _facade(self, *, actor=None, effective_product_contract=None):
        return compose_integration_facade(
            contract=self.contract,
            actor=self.actor if actor is None else actor,
            effective_product_contract=(
                self.contract.version_pin
                if effective_product_contract is None
                else effective_product_contract
            ),
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
            integrity_metadata=(("representation", "p5.06-integration-guard-test"),),
            payload=(),
            lifecycle_status=lifecycle_status,
        )

    def _capability_request(self, *, access: AccessRequest | None = None) -> CapabilityConsumptionRequest:
        return CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=self.access if access is None else access,
        )

    def _runtime_interaction(self) -> ProductRuntimeInteraction:
        task_subject = Identity("product-task", "p5-06-task", "org-a")
        task_record = self._record(
            subject_id=task_subject,
            version_id=Identity("product-task-version", "p5-06-task-v1", "org-a"),
            semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
            authority_scope=PRODUCT_TASK_AUTHORITY_SCOPE,
            lifecycle_status="Open",
            provenance_refs=(self.principal.principal_id, self.product_id),
        )
        workflow_record = self._record(
            subject_id=Identity("workflow-subject", "p5-06-task-decision", "org-a"),
            version_id=Identity("workflow-version", "p5-06-task-decision-v1", "org-a"),
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

    def _created_execution(self):
        return self._facade().start_governed_execution(
            interaction=self._runtime_interaction(),
            execution_id=Identity("execution-subject", "p5-06-task-execution", "org-a"),
            version_id=Identity("execution-version", "p5-06-task-execution-v1", "org-a"),
            created_at=self._time(2),
        )

    def _awaiting_execution(self):
        return await_required_gates(
            self._created_execution(),
            version_id=Identity("execution-version", "p5-06-task-execution-v2", "org-a"),
            actor=self.actor,
            created_at=self._time(3),
        )

    def _gate_decision(
        self,
        execution,
        kind: GovernedGateKind,
        *,
        outcome: GovernedGateOutcome = GovernedGateOutcome.ALLOW,
        suffix: str | None = None,
    ):
        token = suffix or kind.value.lower()
        return build_governed_gate_decision(
            execution=execution,
            kind=kind,
            outcome=outcome,
            decision_actor=self.actor,
            basis_ref=Identity("governed-basis", f"p5-06-{token}-basis", "org-a"),
            decision_id=Identity("gate-decision-subject", f"p5-06-{token}", "org-a"),
            version_id=Identity("gate-decision-version", f"p5-06-{token}-v1", "org-a"),
            created_at=self._time(4),
        )

    def _all_gate_decisions(self, execution, *, denied_kind: GovernedGateKind | None = None):
        return tuple(
            self._gate_decision(
                execution,
                kind,
                outcome=(
                    GovernedGateOutcome.DENY
                    if kind is denied_kind
                    else GovernedGateOutcome.ALLOW
                ),
            )
            for kind in execution.required_gates
        )

    def _document(self):
        record = self._record(
            subject_id=Identity("document-subject", "p5-06-doc", "org-a"),
            version_id=Identity("document-version", "p5-06-doc-v1", "org-a"),
            semantic_type="platform.document",
            authority_scope="platform.document/state",
            lifecycle_status="Retained",
            provenance_refs=(self.principal.principal_id,),
        )
        artifact = ArtifactContent(
            Identity("artifact", "p5-06-doc-source", "org-a"),
            self.org,
            "content-ref:p5-06",
            "text/plain",
            "sha256:p5-06",
            "source",
            HandlingConstraints(
                "internal",
                "bounded-product-review",
                ("read",),
                "retain",
            ),
        )
        return admit_document_version(
            candidate=DocumentVersionCandidate(record, (artifact,), "source")
        ), artifact

    def test_wrong_organization_actor_cannot_compose_facade(self) -> None:
        with self.assertRaises(ProductContractScopeError):
            self._facade(actor=self.other_actor)

    def test_wrong_organization_capability_request_cannot_cross_composed_boundary(self) -> None:
        other_access = AccessRequest(
            actor=self.other_actor,
            purpose="bounded-product-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        other_request = CapabilityConsumptionRequest(
            organization=self.other_org,
            product_id=Identity("product", "bounded-review-product", "org-b"),
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=other_access,
        )
        with self.assertRaises(ProductContractScopeError):
            self._facade().admit_capability(other_request)

    def test_contract_and_capability_admission_do_not_create_authority(self) -> None:
        admission = self._facade().admit_capability(self._capability_request())
        names = {field.name for field in fields(admission)}
        for forbidden in (
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "data_right",
            "allowed",
        ):
            self.assertNotIn(forbidden, names)

    def test_capability_admission_does_not_bypass_purpose_or_right_semantic_owner(self) -> None:
        admitted, artifact = self._document()
        denied_access = AccessRequest(
            actor=self.actor,
            purpose="bounded-product-review",
            required_right="export",
            allowed_classifications=("internal",),
        )
        request = self._capability_request(access=denied_access)

        self._facade().admit_capability(request)
        with self.assertRaises(CrossCapabilityEnforcementError):
            consume_document(
                contract=self.contract,
                request=request,
                admitted=admitted,
                artifact_id=artifact.artifact_id,
            )

    def test_missing_authorization_and_authority_gates_fail_closed(self) -> None:
        awaiting = self._awaiting_execution()
        with self.assertRaises(RequiredGateUnresolvedError):
            admit_ready_execution(
                awaiting,
                decisions=(),
                version_id=Identity("execution-version", "p5-06-task-execution-v3", "org-a"),
                actor=self.actor,
                created_at=self._time(5),
            )

        without_authority = tuple(
            self._gate_decision(awaiting, kind)
            for kind in awaiting.required_gates
            if kind is not GovernedGateKind.ORGANIZATIONAL_AUTHORITY
        )
        with self.assertRaises(RequiredGateUnresolvedError):
            admit_ready_execution(
                awaiting,
                decisions=without_authority,
                version_id=Identity("execution-version", "p5-06-task-execution-v4", "org-a"),
                actor=self.actor,
                created_at=self._time(6),
            )

    def test_denied_authorization_fails_closed_even_when_other_gates_allow(self) -> None:
        awaiting = self._awaiting_execution()
        decisions = self._all_gate_decisions(
            awaiting,
            denied_kind=GovernedGateKind.AUTHORIZATION,
        )
        with self.assertRaises(RequiredGateDeniedError):
            admit_ready_execution(
                awaiting,
                decisions=decisions,
                version_id=Identity("execution-version", "p5-06-task-execution-v5", "org-a"),
                actor=self.actor,
                created_at=self._time(7),
            )

    def test_all_independent_required_gates_must_allow_before_ready(self) -> None:
        awaiting = self._awaiting_execution()
        ready = admit_ready_execution(
            awaiting,
            decisions=self._all_gate_decisions(awaiting),
            version_id=Identity("execution-version", "p5-06-task-execution-ready", "org-a"),
            actor=self.actor,
            created_at=self._time(8),
        )
        self.assertEqual(ready.lifecycle, GovernedExecutionLifecycle.READY)
        self.assertTrue(ready.gates_satisfied)
        self.assertEqual(ready.product_contract, self.contract.version_pin)

    def test_stale_gate_decisions_cannot_self_advance_after_re_evaluation_boundary(self) -> None:
        awaiting = self._awaiting_execution()
        old_decisions = self._all_gate_decisions(awaiting)
        ready = admit_ready_execution(
            awaiting,
            decisions=old_decisions,
            version_id=Identity("execution-version", "p5-06-stale-ready", "org-a"),
            actor=self.actor,
            created_at=self._time(9),
        )
        waiting = transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.WAITING,
            version_id=Identity("execution-version", "p5-06-stale-waiting", "org-a"),
            actor=self.actor,
            created_at=self._time(10),
        )
        reevaluate = resume_governed_execution(
            waiting,
            gates_still_valid=False,
            version_id=Identity("execution-version", "p5-06-stale-reevaluate", "org-a"),
            actor=self.actor,
            created_at=self._time(11),
        )
        self.assertEqual(reevaluate.lifecycle, GovernedExecutionLifecycle.AWAITING_GATE)
        self.assertFalse(reevaluate.gate_decisions)

        with self.assertRaises(ValueError):
            admit_ready_execution(
                reevaluate,
                decisions=old_decisions,
                version_id=Identity("execution-version", "p5-06-stale-illegal-ready", "org-a"),
                actor=self.actor,
                created_at=self._time(12),
            )

    def test_stale_product_contract_version_cannot_self_advance_composition(self) -> None:
        stale_pin = replace(
            self.contract.version_pin,
            version_id=Identity(
                "product-contract-version",
                "p4-08-bounded-review-product-v0.0.9",
                self.contract.version_pin.version_id.scope,
            ),
        )
        with self.assertRaises(ProductContractResolutionContinuityError):
            self._facade(effective_product_contract=stale_pin)

    def test_local_harness_remains_non_authoritative_and_contains_no_authority_decision(self) -> None:
        result = run_local_integration_harness(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )
        self.assertEqual(
            result.workspace.presentation_authority,
            PresentationAuthority.NON_AUTHORITATIVE,
        )
        names = {field.name for field in fields(result)}
        for forbidden in (
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "data_right",
        ):
            self.assertNotIn(forbidden, names)

    def test_convenience_modules_delegate_instead_of_owning_security_policy(self) -> None:
        facade_source = inspect.getsource(facade_module)
        scaffold_source = inspect.getsource(scaffolding_module)

        self.assertIn("validate_capability_consumption", facade_source)
        self.assertIn("start_product_governed_execution", facade_source)
        self.assertIn("compose_integration_facade", scaffold_source)
        self.assertNotIn("class AuthorizationPolicy", facade_source)
        self.assertNotIn("class AuthorizationPolicy", scaffold_source)
        self.assertNotIn("class OrganizationalAuthority", facade_source)
        self.assertNotIn("class OrganizationalAuthority", scaffold_source)


if __name__ == "__main__":
    unittest.main()
