"""P1.04 — Execution Context and exact version pinning for the reference slice.

The representation is intentionally in-memory and domain-neutral. It starts one
RFC-0002/RFC-0005 Execution Context and preserves exact immutable versions that
materially govern the bounded attempt. Authorization, Organizational Authority,
approval evaluation and canonical mutation remain outside P1.04.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .canonical import AuthorityMode, CanonicalRecord
from .identity import Identity
from .security import ActorContext, OrganizationScope
from .workflow import OperationSideEffectClass, WorkflowDefinition


class ExecutionLifecycle(str, Enum):
    """Initial RFC-0005 execution condition exercised by P1.04."""

    AWAITING_GATE = "AwaitingGate"


@dataclass(frozen=True, slots=True)
class GovernedVersionPin:
    """Exact immutable governed version relied upon by one execution."""

    subject_id: Identity
    version_id: Identity
    semantic_type: str
    authority_scope: str

    def __post_init__(self) -> None:
        if not isinstance(self.subject_id, Identity):
            raise ValueError("pin subject_id must be an Identity")
        if not isinstance(self.version_id, Identity):
            raise ValueError("pin version_id must be an Identity")
        if self.subject_id == self.version_id:
            raise ValueError("pin Subject Identity and Version Identity must remain distinct")
        if self.subject_id.scope != self.version_id.scope:
            raise ValueError("pinned Subject/Version Identity scope must match")
        if not isinstance(self.semantic_type, str) or not self.semantic_type.strip():
            raise ValueError("pin semantic_type must be a non-empty string")
        if not isinstance(self.authority_scope, str) or not self.authority_scope.strip():
            raise ValueError("pin authority_scope must be explicit")

    @classmethod
    def from_record(cls, record: CanonicalRecord) -> "GovernedVersionPin":
        if not isinstance(record, CanonicalRecord):
            raise ValueError("only CanonicalRecord versions can be pinned by P1.04")
        return cls(
            subject_id=record.subject_id,
            version_id=record.version_id,
            semantic_type=record.semantic_type,
            authority_scope=record.authority_scope,
        )


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Initial immutable Execution Context version for one governed attempt."""

    record: CanonicalRecord
    workflow: GovernedVersionPin
    operation_name: str
    material_inputs: tuple[GovernedVersionPin, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("Execution Context must use a CanonicalRecord envelope")
        if self.record.semantic_type != "platform.execution-context":
            raise ValueError("Execution Context Canonical Record semantic_type must be platform.execution-context")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("Arvectum OS Execution Context must use Native authority")
        if self.record.lifecycle_status != ExecutionLifecycle.AWAITING_GATE.value:
            raise ValueError("P1.04 initial Execution Context must await unresolved governance gates")
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ValueError("effective Workflow version pin must be explicit")
        if self.workflow.semantic_type != "platform.workflow":
            raise ValueError("workflow pin must reference a platform.workflow version")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("operation_name must be explicit")
        if not isinstance(self.material_inputs, tuple) or not self.material_inputs:
            raise ValueError("at least one material input version must be pinned")
        if any(not isinstance(item, GovernedVersionPin) for item in self.material_inputs):
            raise ValueError("material_inputs must contain GovernedVersionPin values")
        organization_scope = self.record.organization.organization_id.value
        identities = (
            self.record.subject_id,
            self.record.version_id,
            self.workflow.subject_id,
            self.workflow.version_id,
            *(identity for pin in self.material_inputs for identity in (pin.subject_id, pin.version_id)),
        )
        if any(identity.scope != organization_scope for identity in identities):
            raise ValueError("Execution Context and all pinned governed versions must share Organization scope")
        if self.record.subject_id == self.workflow.subject_id:
            raise ValueError("Workflow and Execution Context must have distinct Subject Identities")
        version_ids = tuple(pin.version_id for pin in self.material_inputs)
        if len(set(version_ids)) != len(version_ids):
            raise ValueError("material input Version Identities must not be duplicated")

    @property
    def execution_subject_id(self) -> Identity:
        return self.record.subject_id

    @property
    def execution_version_id(self) -> Identity:
        return self.record.version_id

    @property
    def organization(self) -> OrganizationScope:
        return self.record.organization

    @property
    def initiating_actor(self) -> ActorContext:
        return self.record.creation_actor


def start_p1_04_execution(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    workflow: WorkflowDefinition,
    material_input: CanonicalRecord,
) -> ExecutionContext:
    """Start the deterministic P1.04 attempt and pin exact governed versions."""

    if actor.organization != organization:
        raise ValueError("Execution actor must share Organization scope")
    if workflow.organization != organization:
        raise ValueError("Execution Workflow must share Organization scope")
    if material_input.organization != organization:
        raise ValueError("material input must share Organization scope")
    if workflow.record.lifecycle_status != "Approved":
        raise ValueError("P1.04 requires the explicitly supplied effective Workflow version to be Approved")

    matching_operations = tuple(
        operation
        for operation in workflow.operations
        if operation.target_subject_id == material_input.subject_id
        and operation.target_semantic_type == material_input.semantic_type
        and OperationSideEffectClass.CANONICAL_MUTATION in operation.side_effect_classes
    )
    if len(matching_operations) != 1:
        raise ValueError("Workflow must declare exactly one scoped CanonicalMutation operation for the material input")
    operation = matching_operations[0]

    workflow_pin = GovernedVersionPin.from_record(workflow.record)
    input_pin = GovernedVersionPin.from_record(material_input)
    record = CanonicalRecord(
        subject_id=Identity(
            "execution-subject",
            "reference-subject-maintenance-execution-1",
            organization.organization_id.value,
        ),
        version_id=Identity(
            "execution-version",
            "reference-subject-maintenance-execution-1-v1",
            organization.organization_id.value,
        ),
        semantic_type="platform.execution-context",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.governed-execution/context",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=datetime.fromisoformat("2026-08-08T03:00:00+00:00"),
        provenance_refs=(
            actor.actual_principal.principal_id,
            workflow_pin.subject_id,
            workflow_pin.version_id,
            input_pin.subject_id,
            input_pin.version_id,
        ),
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(),
        lifecycle_status=ExecutionLifecycle.AWAITING_GATE.value,
        predecessor_version_id=None,
    )
    return ExecutionContext(
        record=record,
        workflow=workflow_pin,
        operation_name=operation.semantic_name,
        material_inputs=(input_pin,),
    )
