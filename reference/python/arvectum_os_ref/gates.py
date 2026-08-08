"""P1.05 — separate Authorization and Organizational Authority gates.

This module models already-governed gate decision evidence for the bounded
reference slice. It does not define how a real organization issues permissions,
delegations or decision authority, and it does not adopt the Proposed Decision
Authority Policy as normative. Missing or denied required gates fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .canonical import AuthorityMode, CanonicalRecord
from .execution import ExecutionContext, ExecutionLifecycle, GovernedVersionPin
from .identity import Identity
from .security import ActorContext


class GateKind(str, Enum):
    AUTHORIZATION = "Authorization"
    ORGANIZATIONAL_AUTHORITY = "OrganizationalAuthority"


class GateOutcome(str, Enum):
    ALLOW = "Allow"
    DENY = "Deny"


_GATE_SEMANTIC_TYPES = {
    GateKind.AUTHORIZATION: "platform.authorization-decision",
    GateKind.ORGANIZATIONAL_AUTHORITY: "platform.organizational-authority-decision",
}

_GATE_AUTHORITY_SCOPES = {
    GateKind.AUTHORIZATION: "platform.authorization/decision",
    GateKind.ORGANIZATIONAL_AUTHORITY: "platform.organizational-authority/decision",
}


@dataclass(frozen=True, slots=True)
class GateDecision:
    """One immutable governed decision for exactly one required execution gate."""

    record: CanonicalRecord
    kind: GateKind
    outcome: GateOutcome
    basis_ref: Identity
    subject_principal_id: Identity
    execution_subject_id: Identity
    evaluated_execution_version_id: Identity
    workflow_version_id: Identity
    operation_name: str
    target_subject_id: Identity
    target_version_id: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("GateDecision must use a CanonicalRecord envelope")
        if not isinstance(self.kind, GateKind):
            raise ValueError("gate kind must be explicit")
        if not isinstance(self.outcome, GateOutcome):
            raise ValueError("gate outcome must be explicit")
        if not isinstance(self.basis_ref, Identity):
            raise ValueError("gate decision must reference an explicit governed basis")
        if self.record.semantic_type != _GATE_SEMANTIC_TYPES[self.kind]:
            raise ValueError("gate Canonical Record semantic_type must match gate kind")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("P1.05 gate decision evidence uses Native authority")
        if self.record.authority_scope != _GATE_AUTHORITY_SCOPES[self.kind]:
            raise ValueError("gate authority_scope must match gate kind")
        if self.record.lifecycle_status != self.outcome.value:
            raise ValueError("gate record lifecycle_status must match decision outcome")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("gate operation_name must be explicit")

        organization_scope = self.record.organization.organization_id.value
        identities = (
            self.record.subject_id,
            self.record.version_id,
            self.basis_ref,
            self.subject_principal_id,
            self.execution_subject_id,
            self.evaluated_execution_version_id,
            self.workflow_version_id,
            self.target_subject_id,
            self.target_version_id,
        )
        if any(not isinstance(identity, Identity) for identity in identities):
            raise ValueError("gate decision references must be Identity values")
        organization_scoped = (
            self.record.subject_id,
            self.record.version_id,
            self.basis_ref,
            self.execution_subject_id,
            self.evaluated_execution_version_id,
            self.workflow_version_id,
            self.target_subject_id,
            self.target_version_id,
        )
        if any(identity.scope != organization_scope for identity in organization_scoped):
            raise ValueError("governed gate references must remain within Organization scope")
        if self.record.subject_id == self.record.version_id:
            raise ValueError("gate decision Subject and Version Identity must remain distinct")
        if self.basis_ref not in self.record.provenance_refs:
            raise ValueError("gate decision provenance must preserve the governed basis reference")

    @property
    def version_pin(self) -> GovernedVersionPin:
        return GovernedVersionPin.from_record(self.record)


@dataclass(frozen=True, slots=True)
class GateEvaluation:
    """Fail-closed evaluation of the two independently required P1.05 gates."""

    authorization: GateDecision | None
    organizational_authority: GateDecision | None

    @property
    def authorization_allowed(self) -> bool:
        return self.authorization is not None and self.authorization.outcome is GateOutcome.ALLOW

    @property
    def organizational_authority_allowed(self) -> bool:
        return (
            self.organizational_authority is not None
            and self.organizational_authority.outcome is GateOutcome.ALLOW
        )

    @property
    def can_proceed(self) -> bool:
        return self.authorization_allowed and self.organizational_authority_allowed

    @property
    def unresolved_gates(self) -> tuple[GateKind, ...]:
        unresolved: list[GateKind] = []
        if self.authorization is None:
            unresolved.append(GateKind.AUTHORIZATION)
        if self.organizational_authority is None:
            unresolved.append(GateKind.ORGANIZATIONAL_AUTHORITY)
        return tuple(unresolved)


def _validate_decision_for_execution(
    *,
    execution: ExecutionContext,
    decision: GateDecision,
    expected_kind: GateKind,
) -> None:
    if decision.kind is not expected_kind:
        raise ValueError(f"expected {expected_kind.value} decision")
    if decision.record.organization != execution.organization:
        raise ValueError("gate decision and execution must share Organization scope")
    if decision.subject_principal_id != execution.initiating_actor.actual_principal.principal_id:
        raise ValueError("gate decision must apply to the initiating Principal")
    if decision.execution_subject_id != execution.execution_subject_id:
        raise ValueError("gate decision must reference the exact Execution Subject Identity")
    if decision.evaluated_execution_version_id != execution.execution_version_id:
        raise ValueError("gate decision must reference the exact Execution Context version evaluated")
    if decision.workflow_version_id != execution.workflow.version_id:
        raise ValueError("gate decision must reference the exact pinned Workflow Version Identity")
    if decision.operation_name != execution.operation_name:
        raise ValueError("gate decision operation must match the Execution Context operation")
    if len(execution.material_inputs) != 1:
        raise ValueError("P1.05 bounded slice requires exactly one material input")
    material = execution.material_inputs[0]
    if decision.target_subject_id != material.subject_id or decision.target_version_id != material.version_id:
        raise ValueError("gate decision must reference the exact pinned target Subject and Version Identity")


def evaluate_p1_05_gates(
    *,
    execution: ExecutionContext,
    authorization: GateDecision | None = None,
    organizational_authority: GateDecision | None = None,
) -> GateEvaluation:
    """Evaluate the two required gates independently and deny by default."""

    if execution.record.lifecycle_status != ExecutionLifecycle.AWAITING_GATE.value:
        raise ValueError("P1.05 gates can only evaluate an AwaitingGate Execution Context version")
    if authorization is not None:
        _validate_decision_for_execution(
            execution=execution,
            decision=authorization,
            expected_kind=GateKind.AUTHORIZATION,
        )
    if organizational_authority is not None:
        _validate_decision_for_execution(
            execution=execution,
            decision=organizational_authority,
            expected_kind=GateKind.ORGANIZATIONAL_AUTHORITY,
        )
    return GateEvaluation(
        authorization=authorization,
        organizational_authority=organizational_authority,
    )


def build_p1_05_gate_decision(
    *,
    execution: ExecutionContext,
    kind: GateKind,
    outcome: GateOutcome,
    decision_actor: ActorContext,
    basis_ref: Identity,
) -> GateDecision:
    """Build deterministic governed fixture evidence for one P1.05 gate.

    Construction records a decision and its governed basis supplied by the
    caller; it does not itself determine whether the actor is entitled to issue
    that decision in a real deployment. Policy administration, delegation and
    real organizational authority issuance remain outside this bounded slice.
    """

    if execution.record.lifecycle_status != ExecutionLifecycle.AWAITING_GATE.value:
        raise ValueError("gate decision fixture must evaluate the AwaitingGate execution version")
    if decision_actor.organization != execution.organization:
        raise ValueError("gate decision actor must share Organization scope")
    if not isinstance(kind, GateKind):
        raise ValueError("gate kind must be explicit")
    if not isinstance(outcome, GateOutcome):
        raise ValueError("gate outcome must be explicit")
    if not isinstance(basis_ref, Identity):
        raise ValueError("gate decision basis_ref must be explicit")
    if basis_ref.scope != execution.organization.organization_id.value:
        raise ValueError("gate decision basis_ref must share Organization scope")
    if len(execution.material_inputs) != 1:
        raise ValueError("P1.05 bounded slice requires exactly one material input")

    material = execution.material_inputs[0]
    suffix = "authorization" if kind is GateKind.AUTHORIZATION else "organizational-authority"
    outcome_suffix = outcome.value.lower()
    record = CanonicalRecord(
        subject_id=Identity(
            f"{suffix}-decision-subject",
            f"reference-subject-maintenance-execution-1-{suffix}-{outcome_suffix}",
            execution.organization.organization_id.value,
        ),
        version_id=Identity(
            f"{suffix}-decision-version",
            f"reference-subject-maintenance-execution-1-{suffix}-{outcome_suffix}-v1",
            execution.organization.organization_id.value,
        ),
        semantic_type=_GATE_SEMANTIC_TYPES[kind],
        schema_version="1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=_GATE_AUTHORITY_SCOPES[kind],
        accountable_owner_id=decision_actor.actual_principal.principal_id,
        creation_actor=decision_actor,
        created_at=datetime.fromisoformat("2026-08-08T04:00:00+00:00"),
        provenance_refs=(
            decision_actor.actual_principal.principal_id,
            basis_ref,
            execution.execution_subject_id,
            execution.execution_version_id,
            execution.workflow.version_id,
            material.subject_id,
            material.version_id,
        ),
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(("operation", execution.operation_name),),
        lifecycle_status=outcome.value,
        predecessor_version_id=None,
    )
    return GateDecision(
        record=record,
        kind=kind,
        outcome=outcome,
        basis_ref=basis_ref,
        subject_principal_id=execution.initiating_actor.actual_principal.principal_id,
        execution_subject_id=execution.execution_subject_id,
        evaluated_execution_version_id=execution.execution_version_id,
        workflow_version_id=execution.workflow.version_id,
        operation_name=execution.operation_name,
        target_subject_id=material.subject_id,
        target_version_id=material.version_id,
    )


def admit_p1_05_ready_execution(
    *,
    execution: ExecutionContext,
    authorization: GateDecision | None = None,
    organizational_authority: GateDecision | None = None,
) -> ExecutionContext:
    """Create the immutable Ready execution version only after both explicit allows."""

    evaluation = evaluate_p1_05_gates(
        execution=execution,
        authorization=authorization,
        organizational_authority=organizational_authority,
    )
    if not evaluation.can_proceed:
        raise PermissionError("required Authorization and Organizational Authority gates must both explicitly allow")

    assert authorization is not None
    assert organizational_authority is not None
    gate_pins = (
        authorization.version_pin,
        organizational_authority.version_pin,
    )
    record = CanonicalRecord(
        subject_id=execution.execution_subject_id,
        version_id=Identity(
            "execution-version",
            "reference-subject-maintenance-execution-1-v2",
            execution.organization.organization_id.value,
        ),
        semantic_type=execution.record.semantic_type,
        schema_version=execution.record.schema_version,
        organization=execution.organization,
        authority_mode=execution.record.authority_mode,
        authority_scope=execution.record.authority_scope,
        accountable_owner_id=execution.record.accountable_owner_id,
        creation_actor=execution.initiating_actor,
        created_at=datetime.fromisoformat("2026-08-08T04:05:00+00:00"),
        provenance_refs=(
            *execution.record.provenance_refs,
            authorization.record.subject_id,
            authorization.record.version_id,
            authorization.basis_ref,
            organizational_authority.record.subject_id,
            organizational_authority.record.version_id,
            organizational_authority.basis_ref,
        ),
        integrity_metadata=execution.record.integrity_metadata,
        payload=execution.record.payload,
        lifecycle_status=ExecutionLifecycle.READY.value,
        predecessor_version_id=execution.execution_version_id,
    )
    return ExecutionContext(
        record=record,
        workflow=execution.workflow,
        operation_name=execution.operation_name,
        material_inputs=execution.material_inputs,
        gate_decisions=gate_pins,
    )
