"""Deterministic Phase 1 fixture retained through the historical P2.01 seam.

R3 classifies ``RuntimeComposition`` and ``reference_runtime_operations()`` as
reference-compatibility infrastructure for the original P1/P2.01 evidence, not
as the reusable Phase 2 Core Runtime entry.  The materially distinct P2.09
workflow reuses later domain-neutral runtime owners directly and does not depend
on this fixture path.
"""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import CanonicalRecord, build_p1_02_native_record
from .identity import Identity
from .portability import PortableSemanticFixture, export_p1_10_semantic_fixture
from .reference_runtime_adapters import reference_runtime_operations
from .runtime import RuntimeComposition, RuntimeExecutionRequest, RuntimeExecutionResult
from .security import ActorContext, OrganizationScope, Principal
from .workflow import WorkflowDefinition, build_p1_03_workflow


@dataclass(frozen=True, slots=True)
class Phase1ReferenceScenario:
    """One complete deterministic P1 fixture around historical execution evidence."""

    organization: OrganizationScope
    principal: Principal
    actor: ActorContext
    decision_principal: Principal
    decision_actor: ActorContext
    input_record: CanonicalRecord
    workflow: WorkflowDefinition
    request: RuntimeExecutionRequest
    runtime_result: RuntimeExecutionResult

    def export_portable_fixture(self) -> PortableSemanticFixture:
        """Reuse the existing P1.10 evidence exporter over the reference result.

        Portability remains evidence/fixture behavior for the historical P1 path;
        it is not made a Core Runtime contract by this compatibility scenario.
        """

        result = self.runtime_result
        return export_p1_10_semantic_fixture(
            input_record=self.input_record,
            workflow=self.workflow,
            awaiting_execution=result.awaiting_execution,
            authorization=result.authorization,
            organizational_authority=result.organizational_authority,
            ready_execution=result.ready_execution,
            mutation=result.mutation,
            event=result.event,
            evidence=result.reconstruction,
            observation=result.observation,
        )


def build_p1_reference_scenario(
    *,
    runtime: RuntimeComposition | None = None,
) -> Phase1ReferenceScenario:
    """Build deterministic P1 fixtures and execute the compatibility composition."""

    organization = OrganizationScope(Identity("organization", "org-a", "platform"))
    principal = Principal(Identity("principal", "principal-1", "platform"))
    actor = ActorContext(principal, organization)
    decision_principal = Principal(Identity("principal", "principal-2", "platform"))
    decision_actor = ActorContext(decision_principal, organization)

    input_record = build_p1_02_native_record(
        organization=organization,
        actor=actor,
    )
    workflow = build_p1_03_workflow(
        organization=organization,
        actor=actor,
        target_record=input_record,
    )
    request = RuntimeExecutionRequest(
        organization=organization,
        actor=actor,
        decision_actor=decision_actor,
        workflow=workflow,
        material_input=input_record,
        authorization_basis_ref=Identity(
            "governed-basis",
            "authorization-fixture-v1",
            organization.organization_id.value,
        ),
        organizational_authority_basis_ref=Identity(
            "governed-basis",
            "authority-fixture-v1",
            organization.organization_id.value,
        ),
        new_version_id=Identity(
            "canonical-version",
            "subject-1-v2",
            organization.organization_id.value,
        ),
        new_payload=(("label", "domain-neutral reference subject updated"),),
    )
    composition = runtime
    if composition is None:
        composition = RuntimeComposition(operations=reference_runtime_operations())
    result = composition.execute(request)
    return Phase1ReferenceScenario(
        organization=organization,
        principal=principal,
        actor=actor,
        decision_principal=decision_principal,
        decision_actor=decision_actor,
        input_record=input_record,
        workflow=workflow,
        request=request,
        runtime_result=result,
    )
