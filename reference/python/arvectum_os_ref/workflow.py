"""P1.03 — versioned Workflow baseline for the bounded reference slice.

The representation is intentionally in-memory and domain-neutral. It proves
RFC-0005 Workflow identity/version and operation-declaration semantics without
introducing an Execution Context, authorization decision, Organizational
Authority grant, workflow engine, scheduler or mutation runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .canonical import AuthorityMode, CanonicalRecord
from .identity import Identity
from .security import ActorContext, OrganizationScope


class WorkflowLifecycle(str, Enum):
    """Bounded RFC-0005 lifecycle labels used by the reference Workflow."""

    DRAFT = "Draft"
    APPROVED = "Approved"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"


class OperationSideEffectClass(str, Enum):
    """RFC-0005 operation side-effect classes."""

    READ_ONLY = "ReadOnly"
    TRANSIENT = "Transient"
    CANONICAL_MUTATION = "CanonicalMutation"
    EXTERNAL_MUTATION = "ExternalMutation"
    COMMITMENT = "Commitment"


@dataclass(frozen=True, slots=True)
class WorkflowOperation:
    """One immutable semantic operation declaration inside a Workflow version."""

    semantic_name: str
    target_subject_id: Identity
    target_semantic_type: str
    side_effect_classes: tuple[OperationSideEffectClass, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.semantic_name, str) or not self.semantic_name.strip():
            raise ValueError("operation semantic_name must be a non-empty string")
        if not isinstance(self.target_subject_id, Identity):
            raise ValueError("target_subject_id must be an Identity")
        if not isinstance(self.target_semantic_type, str) or not self.target_semantic_type.strip():
            raise ValueError("target_semantic_type must be a non-empty string")
        if not isinstance(self.side_effect_classes, tuple) or not self.side_effect_classes:
            raise ValueError("side_effect_classes must be explicit")
        if any(not isinstance(item, OperationSideEffectClass) for item in self.side_effect_classes):
            raise ValueError("side_effect_classes must contain OperationSideEffectClass values")
        if len(set(self.side_effect_classes)) != len(self.side_effect_classes):
            raise ValueError("side_effect_classes must not contain duplicates")


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    """Immutable type-specific Workflow definition bound to one Canonical Record version.

    The Canonical Record supplies the governed envelope and exact Subject/Version
    identities. The operations tuple is the bounded type-specific definition.
    Declaring a mutation-capable operation does not grant authorization,
    Organizational Authority or consequential approval.
    """

    record: CanonicalRecord
    operations: tuple[WorkflowOperation, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("Workflow must be represented by a CanonicalRecord envelope")
        if self.record.semantic_type != "platform.workflow":
            raise ValueError("Workflow Canonical Record semantic_type must be platform.workflow")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("P1.03 Workflow baseline uses Native authority only")
        try:
            WorkflowLifecycle(self.record.lifecycle_status)
        except (TypeError, ValueError) as exc:
            raise ValueError("Workflow lifecycle_status must be an RFC-0005 lifecycle value") from exc
        if not isinstance(self.operations, tuple) or not self.operations:
            raise ValueError("Workflow must declare at least one operation")
        if any(not isinstance(operation, WorkflowOperation) for operation in self.operations):
            raise ValueError("operations must contain WorkflowOperation values")
        organization_scope = self.record.organization.organization_id.value
        if self.record.subject_id.scope != organization_scope or self.record.version_id.scope != organization_scope:
            raise ValueError("Workflow Subject/Version Identity scope must match Organization scope")
        if any(operation.target_subject_id.scope != organization_scope for operation in self.operations):
            raise ValueError("Workflow operation targets must remain within Organization scope in P1.03")
        names = tuple(operation.semantic_name for operation in self.operations)
        if len(set(names)) != len(names):
            raise ValueError("operation semantic names must be unique within one Workflow version")

    @property
    def workflow_subject_id(self) -> Identity:
        return self.record.subject_id

    @property
    def workflow_version_id(self) -> Identity:
        return self.record.version_id

    @property
    def organization(self) -> OrganizationScope:
        return self.record.organization

    def declares_canonical_mutation_for(self, record: CanonicalRecord) -> bool:
        """Return whether this version declares a CanonicalMutation for a record.

        This is definition inspection only. It is deliberately not an
        authorization, authority, approval or execution decision.
        """

        return any(
            operation.target_subject_id == record.subject_id
            and operation.target_semantic_type == record.semantic_type
            and OperationSideEffectClass.CANONICAL_MUTATION in operation.side_effect_classes
            for operation in self.operations
        )


def build_p1_03_workflow(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    target_record: CanonicalRecord,
) -> WorkflowDefinition:
    """Build the first immutable Workflow version used by the Phase 1 fixture."""

    if target_record.organization != organization:
        raise ValueError("Workflow and target Canonical Record must share Organization scope in P1.03")
    if actor.organization != organization:
        raise ValueError("Workflow creation actor must share Organization scope")

    record = CanonicalRecord(
        subject_id=Identity(
            "workflow-subject",
            "reference-subject-maintenance",
            organization.organization_id.value,
        ),
        version_id=Identity(
            "workflow-version",
            "reference-subject-maintenance-v1",
            organization.organization_id.value,
        ),
        semantic_type="platform.workflow",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.workflow/definition",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=datetime.fromisoformat("2026-08-07T19:10:00+00:00"),
        provenance_refs=(actor.actual_principal.principal_id, target_record.subject_id),
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(),
        lifecycle_status=WorkflowLifecycle.APPROVED.value,
        predecessor_version_id=None,
    )

    operation = WorkflowOperation(
        semantic_name="update-reference-subject",
        target_subject_id=target_record.subject_id,
        target_semantic_type=target_record.semantic_type,
        side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
    )
    return WorkflowDefinition(record=record, operations=(operation,))
