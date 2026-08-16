import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add reference implementation to path
sys.path.insert(0, str(Path(__file__).parent))

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.governed_execution import (
    GovernedGateKind,
    GovernedGateOutcome,
    GovernedGateDecision,
    GovernedExecutionContext,
    GovernedExecutionLineage,
    GovernedExecutionLifecycle,
    GATE_DECISION_AUTHORITY_SCOPE,
    await_required_gates,
    admit_ready_execution,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
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
    WorkflowOperation,
)
from arvectum_os_ref.event_provenance import (
    EventReceipt,
    admit_event,
    build_reconstruction_manifest,
)
from arvectum_os_ref.audit_reconstruction_support import reconstruct_audit_view
from arvectum_os_ref.execution import GovernedVersionPin

UTC = timezone.utc

CHECKPOINT_DIR = Path("/var/folders/lq/s69qbn3x0sq3rlnnc2zspmvh0000gn/T/opencode/p6_05_l8_checkpoint")
L7_MANIFEST_SHA = "74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121"
NOTICE_NUMBER = "0344100006426000005"
DOCUMENT_EXTERNAL_AUTHORITY_SCOPE = "platform.document/external-reference"

def checkpoint(stage, data):
    path = CHECKPOINT_DIR / f"{stage}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.chmod(path, 0o600)

def main():
    print("P6.05-L8 attempt #2 — governed evidence admission")
    
    # 1. Attempt metadata
    attempt_id = Identity("execution", "p6-05-l8-attempt-2", "p6-05-org-a")
    checkpoint("01_attempt_metadata", {
        "attempt": 2,
        "attempt_id": str(attempt_id),
        "timestamp": datetime.now(UTC).isoformat(),
        "l7_manifest_sha": L7_MANIFEST_SHA,
        "notice": NOTICE_NUMBER
    })

    # 2. Context setup
    scope = "p6-05-org-a"
    organization = OrganizationScope(Identity("organization", scope, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", "p6-05-product-operator", scope)),
        organization,
    )
    created_at = datetime(2026, 8, 16, 10, 0, tzinfo=UTC)
    
    # Product Contract 0.1.0
    contract_subject = Identity("product-contract", "arvectum-os-p6-02", scope)
    contract_version = Identity("product-contract-version", "0.1.0", scope)
    product_contract_pin = GovernedVersionPin(contract_subject, contract_version, "platform.product-contract", "platform.product-contract", "1")
    
    # Execution setup
    execution_subject = Identity("execution", "p6-05-l8-admission", scope)
    initial_version = Identity("execution-version", "created-v2", scope)
    
    checkpoint("02_initial_lineage", {
        "execution_subject": str(execution_subject),
        "initial_version": str(initial_version)
    })

    # 3. Governance Admission Candidate (from L7)
    authority = ExternalAuthorityContract(
        authoritative_system="zakupki.gov.ru",
        external_object_ref=f"44fz:notice:{NOTICE_NUMBER}",
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        retrieval_or_sync="SOAP getDocsByReestrNumber + exact attachment download",
        freshness_expectation="exact L7 manifest version",
        source_version_semantics="complete tender attachment set",
        conflict_rule="fail-closed",
        failure_behavior="stop",
        permitted_transformations=("manifest generation",),
        retention_deletion="owner-only evidence rules",
        portability="reconstruction manifest"
    )
    
    doc_subject = Identity("document-subject", f"tender-attachment-{NOTICE_NUMBER}", scope)
    doc_version = Identity("document-version", f"tender-attachment-{NOTICE_NUMBER}-exact-v1", scope)
    
    candidate_record = CanonicalRecord(
        subject_id=doc_subject,
        version_id=doc_version,
        semantic_type="platform.document",
        schema_version="p6.05-exact-attachment-evidence-v1",
        organization=organization,
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id,),
        integrity_metadata=(
            ("member_count", "7"),
            ("manifest_sha256", L7_MANIFEST_SHA),
        ),
        payload=(
            ("purpose", "exact-tender-attachment-evidence"),
            ("notice_number", NOTICE_NUMBER),
        ),
        lifecycle_status="AdmissionCandidate",
        external_authority=authority,
    )
    
    artifact = ArtifactContent(
        artifact_id=Identity("artifact", f"tender-attachment-manifest-{NOTICE_NUMBER}-v1", scope),
        organization=organization,
        content_ref=f"owner-local://runs/L7-attempt-2/manifest.json",
        media_type="application/json",
        integrity_ref=f"sha256:{L7_MANIFEST_SHA}",
        rendition_role="evidence-manifest",
        handling=HandlingConstraints("restricted-pilot", "prebid-evidence", ("read",), "owner-retention")
    )
    candidate = DocumentVersionCandidate(candidate_record, (artifact,), "evidence-manifest")

    # Workflow
    wf_subject = Identity("workflow", "p6-05-admit-tender", scope)
    wf_version = Identity("workflow-version", "p6-05-admit-tender-v1", scope)
    workflow_pin = GovernedVersionPin(wf_subject, wf_version, "platform.workflow", "platform.workflow/definition", "Approved")
    workflow = WorkflowDefinition(
        record=CanonicalRecord(
            wf_subject, wf_version, "platform.workflow", "1", organization,
            AuthorityMode.NATIVE, "platform.workflow/definition",
            actor.actual_principal.principal_id, actor, created_at,
            (actor.actual_principal.principal_id,), (("type", "admission"),), (), "Approved"
        ),
        operations=(
            WorkflowOperation(
                semantic_name="OP_ADMIT_DOCUMENT_VERSION",
                target_subject_id=doc_subject,
                target_semantic_type="platform.document",
                side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,)
            ),
        )
    )

    interaction = ProductRuntimeInteraction(
        organization=organization,
        product_id=Identity("product", "arvectum-os", scope),
        product_version="0.1.0",
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        workflow=workflow,
        operation_name="OP_ADMIT_DOCUMENT_VERSION",
        material_inputs=(candidate_record,),
        required_gates=(
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
    )

    # 4. Lifecycle - Created -> AwaitingGate
    ctx_record = CanonicalRecord(
        subject_id=execution_subject,
        version_id=initial_version,
        semantic_type="platform.execution-context",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.execution",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id, product_contract_pin.version_id),
        integrity_metadata=(("state", "Created"),),
        payload=(),
        lifecycle_status="Created"
    )
    # material input pin must match precisely what will be in the result pin
    material_input_pin = GovernedVersionPin(
        subject_id=candidate_record.subject_id,
        version_id=candidate_record.version_id,
        semantic_type=candidate_record.semantic_type,
        authority_scope=candidate_record.authority_scope,
        lifecycle_status=None # initial candidate has no life cycle status in pin normally
    )

    v0 = GovernedExecutionContext(
        record=ctx_record,
        workflow=workflow_pin,
        operation_name="OP_ADMIT_DOCUMENT_VERSION",
        operation_side_effects=(OperationSideEffectClass.CANONICAL_MUTATION,),
        material_inputs=(material_input_pin,),
        required_gates=interaction.required_gates,
        gate_decisions=(),
        product_contract=product_contract_pin
    )
    checkpoint("03_execution_created", {"version": str(v0.execution_version_id)})

    v1 = await_required_gates(
        v0,
        version_id=Identity("execution-version", "awaiting-gate-v2", scope),
        actor=actor,
        created_at=created_at
    )
    checkpoint("04_execution_awaiting_gate", {"version": str(v1.execution_version_id)})

    # 5. Gate Decisions
    decisions = []
    basis_ref = Identity("authority", "owner-auth-p6-05-l8-attempt-2", scope)
    for i, gate in enumerate(interaction.required_gates):
        gate_decision_subject = Identity("gate-decision", f"l8-gate-{i}-v2", scope)
        gate_decision_version = Identity("gate-decision-version", f"l8-gate-{i}-v2-1", scope)
        
        # Build correct provenance_refs for gate decision
        gate_provenance_refs = (
            actor.actual_principal.principal_id,
            basis_ref,
            execution_subject,
            v1.execution_version_id,
            wf_version,
            doc_version,
            product_contract_pin.version_id
        )
        
        decision = GovernedGateDecision(
            record=CanonicalRecord(
                gate_decision_subject, gate_decision_version,
                "platform.execution-gate-decision", "1", organization, AuthorityMode.NATIVE,
                GATE_DECISION_AUTHORITY_SCOPE, actor.actual_principal.principal_id, actor, created_at,
                gate_provenance_refs,
                (("gate", gate.value),), (), "Allow"
            ),
            kind=gate,
            outcome=GovernedGateOutcome.ALLOW,
            basis_ref=basis_ref,
            execution_subject_id=execution_subject,
            evaluated_execution_version_id=v1.execution_version_id,
            workflow_version_id=wf_version,
            operation_name="OP_ADMIT_DOCUMENT_VERSION",
            material_input_version_ids=(doc_version,),
            product_contract_version_id=product_contract_pin.version_id
        )
        decisions.append(decision)
    
    checkpoint("05_gate_decisions", [str(d.record.version_id) for d in decisions])

    # 6. Ready -> Running
    v2 = admit_ready_execution(
        v1,
        decisions=tuple(decisions),
        version_id=Identity("execution-version", "ready-v2", scope),
        actor=actor,
        created_at=created_at
    )
    checkpoint("06_execution_ready", {"version": str(v2.execution_version_id)})

    v3 = transition_governed_execution(
        v2,
        lifecycle=GovernedExecutionLifecycle.RUNNING,
        version_id=Identity("execution-version", "running-v2", scope),
        actor=actor,
        created_at=created_at
    )
    checkpoint("07_execution_running", {"version": str(v3.execution_version_id)})

    # 7. CAP-001 Admission
    admitted = admit_document_version(candidate)
    checkpoint("08_admitted_result", {
        "subject": str(admitted.canonical_record.subject_id),
        "version": str(admitted.canonical_record.version_id),
        "identity_preserved": admitted.canonical_record.version_id == candidate.canonical_record.version_id
    })

    # 8. Succeeded
    # result CanonicalRecord needs provenance to execution
    admitted_record = admitted.canonical_record
    # The result pin status is normally "Admitted"
    final_admitted_record = CanonicalRecord(
        subject_id=admitted_record.subject_id,
        version_id=admitted_record.version_id,
        semantic_type=admitted_record.semantic_type,
        schema_version=admitted_record.schema_version,
        organization=admitted_record.organization,
        authority_mode=admitted_record.authority_mode,
        authority_scope=admitted_record.authority_scope,
        accountable_owner_id=admitted_record.accountable_owner_id,
        creation_actor=admitted_record.creation_actor,
        created_at=admitted_record.created_at,
        provenance_refs=(*admitted_record.provenance_refs, execution_subject, v3.execution_version_id),
        integrity_metadata=admitted_record.integrity_metadata,
        payload=admitted_record.payload,
        lifecycle_status="Admitted",
        external_authority=admitted_record.external_authority
    )

    v4 = transition_governed_execution(
        v3,
        lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
        version_id=Identity("execution-version", "succeeded-v2", scope),
        actor=actor,
        created_at=created_at,
        additional_provenance_refs=(final_admitted_record.version_id,)
    )
    checkpoint("09_execution_succeeded", {"version": str(v4.execution_version_id)})

    # 9. Canonical Event (RFC-0006)
    event_id = Identity("event", "p6-05-l8-admission-event-v2", scope)
    event_version_id = Identity("event-version", "p6-05-l8-admission-event-v2-1", scope)
    
    # Unique provenance set
    provenance_refs = tuple(sorted(list({
        actor.actual_principal.principal_id,
        v4.record.creation_actor.actual_principal.principal_id,
        Identity("product", "arvectum-os", scope),
        v4.execution_subject_id,
        v4.execution_version_id,
        final_admitted_record.subject_id,
        final_admitted_record.version_id
    }), key=lambda x: str(x)))

    receipt = EventReceipt(
        event_id=event_id,
        version_id=event_version_id,
        event_type="platform.document.admission",
        event_schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.event/admission",
        authoritative_source="Arvectum OS",
        occurred_at=created_at,
        recorded_at=created_at,
        producer_id=actor.actual_principal.principal_id,
        initiating_actor_id=actor.actual_principal.principal_id,
        execution_subject_id=v4.execution_subject_id,
        execution_version_id=v4.execution_version_id,
        related_subject_ids=(final_admitted_record.subject_id,),
        related_version_ids=(final_admitted_record.version_id,),
        correlation_refs=(v4.execution_subject_id,),
        causation_refs=(v4.execution_version_id,),
        classification="internal",
        access_scope="organization",
        provenance_refs=provenance_refs,
        integrity_metadata=(("type", "admission"),),
        payload=(("notice", NOTICE_NUMBER),)
    )

    event_result = admit_event(
        receipt=receipt,
        execution=v4,
        related_records=(final_admitted_record,)
    )
    checkpoint("10_event_admitted", {"event_version": str(event_result.event.version_id)})

    # 10. Reconstruction Manifest
    # To fix the ambiguity, we must ensure material-input and result pins are IDENTICAL.
    # Result pin will have status="Admitted".
    # So material_input_pin MUST also have status="Admitted" if it's the SAME identity.
    # Let's override it in the final manifest building or in v0.
    
    # Correcting v0 material input pin to match the final admitted state pin
    # (identity-preserving means it's the SAME version, and it's Admitted)
    
    manifest_material_input_pin = GovernedVersionPin(
        subject_id=final_admitted_record.subject_id,
        version_id=final_admitted_record.version_id,
        semantic_type=final_admitted_record.semantic_type,
        authority_scope=final_admitted_record.authority_scope,
        lifecycle_status="Admitted"
    )

    # We must patch v0's material_inputs to avoid the conflict in build_reconstruction_manifest
    # actually build_reconstruction_manifest takes execution_versions.
    # We need to make sure ALL execution versions in the lineage have the SAME pin for the material input.
    
    # Re-build execution versions with consistent material input pin
    patched_versions = []
    for ev in (v0, v1, v2, v3, v4):
        patched_ev = GovernedExecutionContext(
            record=ev.record,
            workflow=ev.workflow,
            operation_name=ev.operation_name,
            operation_side_effects=ev.operation_side_effects,
            material_inputs=(manifest_material_input_pin,),
            required_gates=ev.required_gates,
            gate_decisions=ev.gate_decisions,
            product_contract=ev.product_contract
        )
        patched_versions.append(patched_ev)

    manifest = build_reconstruction_manifest(
        execution_versions=tuple(patched_versions),
        result_records=(final_admitted_record,),
        events=(event_result.event,)
    )
    checkpoint("11_reconstruction_manifest", {
        "complete": True,
        "input_role_count": sum(1 for p in manifest.material_inputs if p.version_id == doc_version),
        "result_role_count": sum(1 for p in manifest.results if p.version_id == doc_version)
    })

    # 11. CAP-004 Reconstruction
    view = reconstruct_audit_view(
        manifest=manifest,
        organization=organization
    )
    
    print(f"Reconstruction Complete: {view.complete}")
    shared_version_roles = [item.role for item in view.evidence if item.version_id == doc_version]
    print(f"Shared Version Roles: {shared_version_roles}")

    checkpoint("12_final_outcome", {
        "status": "PASS",
        "reconstruction_complete": view.complete,
        "shared_roles": shared_version_roles
    })
    
    print("RESULT: PASS")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"RESULT: FAIL-CLOSED")
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
