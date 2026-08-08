"""Executable P4.08 Provisional Product Contract for the bounded product reference.

This is product-owned reference evidence. It reuses the RFC-0004 Product Contract
validator and the Phase 3 Provisional capability-contract tokens without turning
them into a public/stable interface or changing any capability lifecycle state.
"""

from __future__ import annotations

from datetime import datetime
from typing import Final

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    OP_RETRIEVE_KNOWLEDGE,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractLifecycle,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext
from arvectum_os_ref.workflow import OperationSideEffectClass


PRODUCT_VERSION: Final = "0.1.0"
PRODUCT_ID_VALUE: Final = "bounded-review-product"
PRODUCT_CONTRACT_SCHEMA_VERSION: Final = "p4.08-internal-1"

GOVERNED_RUNTIME_DEPENDENCY: Final = Identity(
    "platform-contract", "governed-runtime", "platform"
)
GOVERNED_RUNTIME_CONTRACT_VERSION: Final = "p2-core-runtime-internal-1"
OP_RECORD_TASK_DECISION: Final = "p4.08.record-task-decision"

PRODUCT_TASK_SEMANTIC_TYPE: Final = "product.bounded-review-task"
PRODUCT_TASK_AUTHORITY_SCOPE: Final = f"{PRODUCT_TASK_SEMANTIC_TYPE}/state"


def product_id_for(actor: ActorContext) -> Identity:
    """Return the product identity scoped to the Actor's current Organization."""

    if not isinstance(actor, ActorContext):
        raise ValueError("Product Contract construction requires an attributable ActorContext")
    return Identity(
        "product",
        PRODUCT_ID_VALUE,
        actor.organization.organization_id.value,
    )


def _dependency(
    dependency_id: Identity,
    contract_version: str,
    operations: tuple[str, ...],
    *,
    provider: str,
    consumer: str,
) -> PlatformDependencyDeclaration:
    return PlatformDependencyDeclaration(
        dependency_id=dependency_id,
        contract_version=contract_version,
        allowed_operations=operations,
        provider_responsibility=provider,
        consumer_responsibility=consumer,
        failure_behavior=(
            "Fail closed without falling back to platform internals, ambient authority, "
            "stale presentation state or undeclared shared state."
        ),
        provisional=True,
    )


def _read_access(semantic_type: str) -> CanonicalAccessDeclaration:
    return CanonicalAccessDeclaration(
        semantic_type=semantic_type,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=f"{semantic_type}/state",
        access_modes=(CanonicalAccessMode.READ,),
        authoritative_source=(
            "Arvectum OS only within the bounded Native authority scope declared by the source"
        ),
        failure_behavior="Reject undeclared or mismatched exact canonical read.",
    )


def _read_operation(
    operation_name: str,
    dependency_id: Identity,
    semantic_type: str,
) -> ProductOperationDeclaration:
    return ProductOperationDeclaration(
        operation_name=operation_name,
        dependency_id=dependency_id,
        side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
        required_gates=(
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.DATA_GOVERNANCE,
        ),
        canonical_accesses=(_read_access(semantic_type),),
        failure_behavior=(
            "Fail closed without source disclosure, authority widening or hidden coupling."
        ),
    )


def _task_mutation_access() -> CanonicalAccessDeclaration:
    return CanonicalAccessDeclaration(
        semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=PRODUCT_TASK_AUTHORITY_SCOPE,
        access_modes=(CanonicalAccessMode.READ, CanonicalAccessMode.WRITE),
        authoritative_source=(
            "The bounded product owns its own task state; Arvectum OS provides governed execution semantics."
        ),
        failure_behavior="Reject undeclared task-state read/write or authority-scope mismatch.",
    )


def build_p4_08_product_contract(
    *,
    actor: ActorContext,
    created_at: datetime,
) -> ProductContract:
    """Build the exact immutable Provisional Product Contract used by P4.08.

    The contract declares two shared capability reads plus one bounded Governed
    Execution operation for product-owned task-state mutation. Possession of this
    object is never authorization, Organizational Authority or approval.
    """

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    product_id = product_id_for(actor)
    owner = actor.actual_principal.principal_id

    record = CanonicalRecord(
        subject_id=Identity("product-contract-subject", "p4-08-bounded-review-product", scope),
        version_id=Identity(
            "product-contract-version",
            "p4-08-bounded-review-product-v0.1.0",
            scope,
        ),
        semantic_type="platform.product-contract",
        schema_version=PRODUCT_CONTRACT_SCHEMA_VERSION,
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.product-contract/boundary",
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(owner, product_id),
        integrity_metadata=(("representation", "bounded-p4.08-reference-contract"),),
        payload=(("scope", "bounded cross-capability product task/context composition"),),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    dependencies = (
        _dependency(
            CAP_001_DOCUMENT_ARTIFACT,
            CAPABILITY_CONTRACT_VERSION,
            (OP_RESOLVE_DOCUMENT,),
            provider="Preserve CAP-001 / RFC-0008 governed Document and Artifact semantics.",
            consumer=(
                "Use only the declared Product Contract, current Organization/Actor access context "
                "and exact source/version semantics."
            ),
        ),
        _dependency(
            CAP_002_MEMORY_KNOWLEDGE,
            CAPABILITY_CONTRACT_VERSION,
            (OP_RETRIEVE_KNOWLEDGE,),
            provider="Preserve CAP-002 / RFC-0007 governed Memory and Knowledge semantics.",
            consumer=(
                "Treat retrieval as bounded context, preserve freshness/provenance/exact Version, "
                "and never treat retrieval as authority."
            ),
        ),
        _dependency(
            GOVERNED_RUNTIME_DEPENDENCY,
            GOVERNED_RUNTIME_CONTRACT_VERSION,
            (OP_RECORD_TASK_DECISION,),
            provider=(
                "Provide the existing bounded RFC-0005 Governed Execution/runtime semantics only."
            ),
            consumer=(
                "Keep task/business meaning product-owned, pin this Product Contract version, "
                "supply all required gates, and use the R10 operator-safety guard for operator action."
            ),
        ),
    )

    operations = (
        _read_operation(
            OP_RESOLVE_DOCUMENT,
            CAP_001_DOCUMENT_ARTIFACT,
            "platform.document",
        ),
        _read_operation(
            OP_RETRIEVE_KNOWLEDGE,
            CAP_002_MEMORY_KNOWLEDGE,
            "platform.knowledge",
        ),
        ProductOperationDeclaration(
            operation_name=OP_RECORD_TASK_DECISION,
            dependency_id=GOVERNED_RUNTIME_DEPENDENCY,
            side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
            required_gates=(
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            ),
            canonical_accesses=(_task_mutation_access(),),
            failure_behavior=(
                "Fail closed without product task mutation. Product Contract possession never "
                "satisfies Authorization, Organizational Authority, Data Governance or approval."
            ),
        ),
    )

    return ProductContract(
        record=record,
        product_id=product_id,
        product_version=PRODUCT_VERSION,
        bounded_scope=(
            "One synthetic product-owned task enters the shared workspace, composes CAP-001 and "
            "CAP-002 context, returns domain decisions to the product boundary, and may request "
            "one product task-state mutation only through Product Contract-backed Governed Execution "
            "plus the R10 operator-safety guard."
        ),
        compatibility_assumptions=(
            "CAP-001 and CAP-002 remain Incubating / Provisional at contract baseline 1.0.0.",
            "Governed Runtime dependency remains the bounded internal P2 reference contract.",
            "All operation tokens and Python types are internal evidence, not public compatibility promises.",
        ),
        dependencies=dependencies,
        operations=operations,
        portability_responsibility=(
            "Preserve product task identity and governed exact references; shared presentation state remains rebuildable."
        ),
        retention_deletion_responsibility=(
            "Apply current source handling/retention/deletion constraints and avoid copying protected payload into product context."
        ),
        review_condition=(
            "Review at R11 or earlier on material Product Contract, capability, security, authority or composition change."
        ),
        exit_path=(
            "Revise with a new immutable Provisional version, contain or retire the bounded product; "
            "Stable status requires a separate RFC-0004 lifecycle decision."
        ),
    )
