"""P8.04 governed evidence admission for the EIS temporal-revalidation run.

Reads the owner-local fresh observation and comparison manifests produced by the
Tender Operator P8.04 harness, verifies each manifest's canonical-body SHA-256
integrity, then admits the minimum governed canonical evidence under the P8.03
contract (Provisional 0.1.0) and reconstructs the read-only audit view without
replaying any external retrieval.

Remediation notes (final cross-review, iteration 7):
- Organization and Actor resolve from the established owner-local P6.05-L4
  context (M7 persistent owner-operated scope). No P8-specific Organization or
  operator is minted.
- Authorization is the **actual** P7.04 least-privilege access decision, not a
  label: the harness verifies the canonical A8 owner decision, provisions one
  exact temporary P7.04 grant for the exact P8.04 operation/resource/local path,
  calls ``p7_04_persistent_access.authorize_from_credential_file``, and fails
  closed unless ``allowed is True`` and ``reason == EXPLICIT_LEAST_PRIVILEGE_GRANT``.
  The Authorization gate basis binds the actual returned P7.04 ``grant_id``
  (``authorization-basis:p7-04-persistent-access-grant:<grant_id>``), never a
  bare ``p7-04-persistent-access:owner-operated`` label. The temporary grant is
  revoked in ``finally`` and proven revoked after the run. Only non-secret
  provenance (grant id, operation, resource, access path, Organization,
  Principal, decision reason) is preserved.
- A8 (``DECISION-2026-08-20-PHASE-8-ACTIVATION``) remains Organizational
  Authority / approved bounded-program basis. P7.04 is the technical
  Authorization basis. They are kept distinct; P7.04 access never satisfies
  Organizational Authority or Consequential Approval.
- Product attribution uses the real Tender Operator product identity
  (``arvectum-tender-operator``). Arvectum OS is the platform producer, not the
  product. Product Contract resolution never substitutes for P7.04 authorization.
- The externally observed documents stay ``External Reference``; the locally
  derived comparison result is ``Native`` governed authority with provenance to
  both External Reference observations (fresh observation and pinned baseline).
- Live-run provenance: the source SHA-256s identify the exact uncommitted
  Tender Operator implementation used around the original live observation; the
  Tender Agent merge SHA ``449cf980...`` is the reviewed canonical publication
  after the live observation. They are not the same immutable version and the
  merge SHA is never recorded as the live executor.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

sys.path.insert(0, str(Path(__file__).parent))

import p7_04_persistent_access as p704
from arvectum_os_ref.canonical import (
    AuthorityMode,
    CanonicalRecord,
    ExternalAuthorityContract,
)
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.event_provenance import (
    EventReceipt,
    admit_event,
    build_reconstruction_manifest,
)
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_execution import (
    GATE_DECISION_AUTHORITY_SCOPE,
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedGateDecision,
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAPABILITY_CONTRACT_VERSION,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)
from p6_03_tender_operator_ref.contract import (
    PRODUCT_COMPATIBILITY_LINE,
    product_id_for,
)
from p7_04_persistent_access import load_p6_owner_context

NOTICE_NUMBER = "0344100006426000005"
BASELINE_MANIFEST_SHA256 = "74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121"
P803_CONTRACT_SUBJECT = "integration-contract/p8-03-eis-authority-revalidation"
P803_CONTRACT_VERSION = "integration-contract-version/p8-03-eis-authority-revalidation-v0.1.0"
DOCUMENT_EXTERNAL_AUTHORITY_SCOPE = "platform.document/external-reference"
DERIVED_REVALIDATION_AUTHORITY_SCOPE = "platform.external-revalidation"
OWNER_CONTEXT_LABEL = "ООО «Арвектум»"

# Exact bounded P7.04 access scope for the P8.04 governed-admission operation.
# No wildcard, ambient or admin access; the temporary grant is exact on
# operation, resource and the local access path.
AUTHORIZATION_OPERATION: Final = "p8.04.eis-revalidation.admit"
AUTHORIZATION_RESOURCE: Final = "p8-04:eis-revalidation:0344100006426000005"
AUTHORIZATION_ACCESS_PATH: Final = "local"
AUTHORIZATION_BASIS_NAMESPACE: Final = "authorization-basis"
AUTHORIZATION_GRANT_PREFIX: Final = "p7-04-persistent-access-grant:"

# Canonical A8 owner decision: Organizational Authority / approved
# bounded-program basis. P7.04 is the technical Authorization basis; A8 is not.
A8_DECISION_RELATIVE_PATH: Final = (
    "docs/governance/decisions/DECISION-2026-08-20-PHASE-8-ACTIVATION.md"
)
A8_DECISION_REQUIRED_MARKERS: Final = (
    "Status: `Approved`",
    "Decision subject: `P8.00-A8 — Owner activation decision`",
    NOTICE_NUMBER,
)

# Live-run provenance binding. The source SHA-256s identify the exact
# uncommitted Tender Operator implementation used around the original live
# observation; the Tender Agent merge SHA is the reviewed canonical publication
# AFTER the live observation. They are not the same immutable version.
LIVE_SOURCE_SHA256: Final = {
    "p8_04_eis_temporal_revalidation.py": (
        "29fc5471f4d6f797bb8eb5b8274aef77832445aa19d15750cb2bec9a75efb96e"
    ),
    "p8_04_run_eis_temporal_revalidation.py": (
        "ef41fb1a75fcf2d992edae05b238292a20aca67015dea7c924d2bf5c4aeb569e"
    ),
}
POST_LIVE_CANONICAL_TENDER_AGENT_SHA: Final = "449cf980e46f561d6819349a3c5c258a069c0594"

# Gate bases reference pre-existing governed evidence, mirroring the canonical
# P7.07 contour. No P8-specific authority is minted here. Authorization is
# dynamic (bound to the actual returned P7.04 grant id); the remaining gates use
# their static pre-existing bases below.
GATE_BASIS: dict[GovernedGateKind, tuple[str, str]] = {
    GovernedGateKind.ORGANIZATIONAL_AUTHORITY: (
        "organizational-authority-basis",
        "decision-2026-08-20-phase-8-activation",
    ),
    GovernedGateKind.DATA_GOVERNANCE: (
        "data-governance-basis",
        "p6-02-v0.1.0+p6-05-l7-exact-eis-manifest",
    ),
    GovernedGateKind.CONSEQUENTIAL_APPROVAL: (
        "consequential-approval-basis",
        "decision-2026-08-20-phase-8-activation",
    ),
}

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json_bytes(payload: dict) -> bytes:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _verify_manifest_integrity(manifest: dict, *, label: str) -> None:
    """Domain-neutral canonical-body SHA-256 verification before governed admission.

    Recomputed independently of any cross-field comparison; a mismatch fails
    closed and never admits governed PASS evidence from the tampered manifest.
    """
    if not isinstance(manifest, dict):
        raise SystemExit(f"BLOCKED: {label} is not a JSON object")
    body = {
        key: value
        for key, value in manifest.items()
        if key not in ("manifest_sha256", "manifest_integrity_ref")
    }
    actual = hashlib.sha256(_canonical_json_bytes(body)).hexdigest()
    expected = manifest.get("manifest_sha256")
    if not isinstance(expected, str) or expected != actual:
        raise SystemExit(f"BLOCKED: {label} canonical-body SHA-256 integrity mismatch")


def _load_owner_context(path: str) -> tuple[Identity, Identity]:
    """Resolve the real M7 Organization/Actor identities from the owner context."""
    return load_p6_owner_context(Path(path).expanduser())


def authorization_basis_value(grant_id: str) -> str:
    """Bind the Authorization gate basis to the actual returned P7.04 grant id."""
    if not isinstance(grant_id, str) or not grant_id or ":" in grant_id:
        raise SystemExit("BLOCKED: P7.04 grant reference invalid for authorization basis")
    return f"{AUTHORIZATION_GRANT_PREFIX}{grant_id}"


def _verify_a8_owner_decision(repo_root: Path) -> None:
    """Verify the canonical A8 owner decision exists and is Approved.

    A8 is Organizational Authority / approved bounded-program basis. It is not
    technical Authorization and never substitutes for the P7.04 decision.
    """
    root = Path(repo_root).expanduser().resolve()
    path = (root / A8_DECISION_RELATIVE_PATH).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise SystemExit("BLOCKED: A8 owner decision escaped exact release source") from exc
    if not path.is_file() or path.is_symlink():
        raise SystemExit("BLOCKED: approved A8 owner decision missing from exact release")
    text = path.read_text(encoding="utf-8")
    if any(marker not in text for marker in A8_DECISION_REQUIRED_MARKERS):
        raise SystemExit("BLOCKED: A8 owner decision does not preserve required bounded approval")


def evaluate_authorization(
    *,
    access_root: Path,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
    operation: str = AUTHORIZATION_OPERATION,
    resource: str = AUTHORIZATION_RESOURCE,
    access_path: str = AUTHORIZATION_ACCESS_PATH,
) -> p704.AccessDecision:
    """Evaluate the exact P7.04 least-privilege access decision (no mutation).

    The returned decision preserves only non-secret provenance: grant id,
    operation, resource, access path, Organization, Principal, decision reason.
    No credential secret is exposed.
    """
    return p704.authorize_from_credential_file(
        access_root.expanduser(),
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
        operation=operation,
        resource=resource,
        access_path=access_path,
    )


def _require_explicit_grant(decision: p704.AccessDecision) -> str:
    """Fail closed unless the decision is an explicit least-privilege grant."""
    if not decision.allowed:
        raise SystemExit(f"BLOCKED: P7.04 authorization denied before gates: {decision.reason}")
    if decision.reason != "EXPLICIT_LEAST_PRIVILEGE_GRANT":
        raise SystemExit(
            f"BLOCKED: P7.04 authorization requires EXPLICIT_LEAST_PRIVILEGE_GRANT, got {decision.reason!r}"
        )
    if decision.principal_kind != "human":
        raise SystemExit("BLOCKED: P7.04 bounded admission requires the attributable human operator")
    if decision.organizational_authority_satisfied or decision.consequential_approval_satisfied:
        raise SystemExit("BLOCKED: P7.04 access must not satisfy Organizational Authority or Consequential Approval")
    if not isinstance(decision.grant_id, str) or not decision.grant_id:
        raise SystemExit("BLOCKED: P7.04 explicit grant reference missing")
    return decision.grant_id


def provision_and_authorize(
    *,
    access_root: Path,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
) -> tuple[p704.AccessDecision, str]:
    """Provision the single exact temporary P7.04 grant, then authorize.

    Returns ``(decision, temporary_grant_id)``. The caller must revoke the
    temporary grant in ``finally`` and prove it is revoked after the run. No
    wildcard, admin, second-Organization, ambient-role or permanent P8 grant is
    ever created.
    """
    access_root = Path(access_root).expanduser()
    temporary_grant_id = p704.grant_access(
        access_root,
        principal,
        operation=AUTHORIZATION_OPERATION,
        resource=AUTHORIZATION_RESOURCE,
        access_paths=(AUTHORIZATION_ACCESS_PATH,),
    )
    decision = evaluate_authorization(
        access_root=access_root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    return decision, temporary_grant_id


def _revoke_temporary_grant(access_root: Path, grant_id: str) -> None:
    """Revoke the temporary P8.04 grant and prove it is revoked."""
    access_root = Path(access_root).expanduser()
    p704.revoke_grant(access_root, grant_id)
    state = p704.load_access_store(access_root)
    record = state["grants"].get(grant_id)
    if record is None or record.get("status") != "revoked":
        raise SystemExit("FAIL-CLOSED: temporary P8.04 grant is not revoked after the run")


def _build_gate_decisions(
    *,
    gates: tuple[GovernedGateKind, ...],
    organization: OrganizationScope,
    actor: ActorContext,
    created_at: datetime,
    scope: str,
    execution_subject: Identity,
    evaluated_execution_version_id: Identity,
    workflow_version_id: Identity,
    observation_version_id: Identity,
    product_contract_version_id: Identity,
    authorization_grant_id: str,
) -> tuple[GovernedGateDecision, ...]:
    """Build the four gate decisions; Authorization binds the actual P7.04 grant id."""
    decisions: list[GovernedGateDecision] = []
    for i, gate in enumerate(gates):
        if gate == GovernedGateKind.AUTHORIZATION:
            basis_ref = Identity(
                AUTHORIZATION_BASIS_NAMESPACE,
                authorization_basis_value(authorization_grant_id),
                scope,
            )
        else:
            basis_namespace, basis_value = GATE_BASIS[gate]
            basis_ref = Identity(basis_namespace, basis_value, scope)
        decisions.append(
            GovernedGateDecision(
                record=CanonicalRecord(
                    Identity("gate-decision", f"p8-04-gate-{i}", scope),
                    Identity("gate-decision-version", f"p8-04-gate-{i}-1", scope),
                    "platform.execution-gate-decision",
                    "1",
                    organization,
                    AuthorityMode.NATIVE,
                    GATE_DECISION_AUTHORITY_SCOPE,
                    actor.actual_principal.principal_id,
                    actor,
                    created_at,
                    (
                        actor.actual_principal.principal_id,
                        basis_ref,
                        execution_subject,
                        evaluated_execution_version_id,
                        workflow_version_id,
                        observation_version_id,
                        product_contract_version_id,
                    ),
                    (("gate", gate.value),),
                    (),
                    "Allow",
                ),
                kind=gate,
                outcome=GovernedGateOutcome.ALLOW,
                basis_ref=basis_ref,
                execution_subject_id=execution_subject,
                evaluated_execution_version_id=evaluated_execution_version_id,
                workflow_version_id=workflow_version_id,
                operation_name="OP_ADMIT_DOCUMENT_VERSION",
                material_input_version_ids=(observation_version_id,),
                product_contract_version_id=product_contract_version_id,
            )
        )
    return tuple(decisions)


def _contract_pin(scope: str) -> GovernedVersionPin:
    subject = Identity("integration-contract", P803_CONTRACT_SUBJECT, scope)
    version = Identity("integration-contract-version", P803_CONTRACT_VERSION, scope)
    return GovernedVersionPin(
        subject,
        version,
        "platform.integration-contract",
        "platform.integration-contract/definition",
        "Provisional",
    )


def main() -> int:
    runs_root = os.environ.get("AI_CORP_TENDER_OPERATOR_DEMO_RUNS_DIR", "").strip()
    run_id = os.environ.get("P8_04_RUN_ID", "").strip()
    owner_context_path = os.environ.get("P8_04_P6_OWNER_CONTEXT", "").strip()
    access_root_raw = os.environ.get("P8_04_ACCESS_ROOT", "").strip()
    credential_id = os.environ.get("P8_04_CREDENTIAL_ID", "").strip()
    credential_file_raw = os.environ.get("P8_04_CREDENTIAL_FILE", "").strip()
    if not runs_root or not run_id:
        raise SystemExit("P8_04 requires AI_CORP_TENDER_OPERATOR_DEMO_RUNS_DIR and P8_04_RUN_ID")
    if not owner_context_path:
        raise SystemExit("P8_04 requires P8_04_P6_OWNER_CONTEXT (owner-local P6.05-L4 context)")
    if not access_root_raw or not credential_id or not credential_file_raw:
        raise SystemExit(
            "P8_04 requires P8_04_ACCESS_ROOT, P8_04_CREDENTIAL_ID and P8_04_CREDENTIAL_FILE "
            "(owner-operated P7.04 persistent access)"
        )
    access_root = Path(access_root_raw).expanduser()
    credential_file = Path(credential_file_raw).expanduser()
    procurement_dir = Path(runs_root) / run_id / "procurement"
    fresh = _load_json(procurement_dir / "p8-04-fresh-observation.json")
    comparison = _load_json(procurement_dir / "p8-04-comparison.json")

    _verify_manifest_integrity(fresh, label="fresh observation manifest")
    _verify_manifest_integrity(comparison, label="comparison manifest")

    if comparison.get("aggregate_result") not in ("NO_CHANGE", "CHANGE_DETECTED"):
        raise SystemExit(f"BLOCKED: unexpected aggregate_result {comparison.get('aggregate_result')!r}")
    if comparison.get("baseline_manifest_sha256") != BASELINE_MANIFEST_SHA256:
        raise SystemExit("BLOCKED: comparison does not pin the immutable P6 baseline SHA-256")
    if comparison.get("fresh_manifest_sha256") != fresh.get("manifest_sha256"):
        raise SystemExit("BLOCKED: comparison fresh hash does not match fresh observation manifest")
    if comparison.get("evidence_completeness") != "complete":
        raise SystemExit("BLOCKED: comparison evidence completeness is not 'complete'")

    try:
        org_id, operator_id = _load_owner_context(owner_context_path)
    except Exception as exc:
        raise SystemExit(f"BLOCKED: P6.05-L4 owner context cannot be resolved: {exc}") from exc
    scope = org_id.value
    organization = OrganizationScope(org_id)
    actor = ActorContext(Principal(operator_id), organization)
    created_at = datetime(2026, 8, 20, 8, 40, tzinfo=UTC)
    product_contract_pin = _contract_pin(scope)
    product_id = product_id_for(actor)
    baseline_identity = Identity(
        "baseline", f"p6-05-exact-attachment-evidence-{BASELINE_MANIFEST_SHA256[:16]}", scope
    )

    # Material governed input: the fresh observation evidence manifest
    authority = ExternalAuthorityContract(
        authoritative_system="zakupki.gov.ru",
        external_object_ref=f"44fz:notice:{NOTICE_NUMBER}",
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        retrieval_or_sync="SOAP getDocsByReestrNumber + exact attachment download (P8.04 fresh observation)",
        freshness_expectation="fresh P8.04 observation compared against immutable P6 baseline",
        source_version_semantics="complete tender attachment set with exact byte digests",
        conflict_rule="fail-closed; mismatch is CHANGE_DETECTED, missing evidence blocks PASS",
        failure_behavior="missing/incomplete evidence blocks governed PASS",
        permitted_transformations=("integrity hashing", "manifest generation", "deterministic comparison"),
        retention_deletion="owner-only evidence rules; P6 baseline preserved immutable",
        portability="governed reconstruction manifest without source credentials",
    )

    observation_subject = Identity("observation", f"eis-observation-{NOTICE_NUMBER}-fresh-v1", scope)
    observation_version = Identity(
        "observation-version", f"eis-observation-{NOTICE_NUMBER}-fresh-v1", scope
    )
    observation_record = CanonicalRecord(
        subject_id=observation_subject,
        version_id=observation_version,
        semantic_type="platform.document",
        schema_version="p8.04-eis-fresh-observation-v1",
        organization=organization,
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id,),
        integrity_metadata=(
            ("manifest_sha256", fresh.get("manifest_sha256", "")),
            ("observed_at", fresh.get("retrieved_at", "")),
            ("external_source_version", fresh.get("external_source_version", "")),
        ),
        payload=(
            ("notice_number", NOTICE_NUMBER),
            ("external_source_authority", fresh.get("external_source_authority", "")),
        ),
        lifecycle_status="AdmissionCandidate",
        external_authority=authority,
    )

    # Locally derived deterministic comparison: Native governed authority with
    # provenance to both External Reference observations (fresh + pinned baseline).
    comparison_record = CanonicalRecord(
        subject_id=Identity("comparison", f"eis-revalidation-{NOTICE_NUMBER}", scope),
        version_id=Identity("comparison-version", f"eis-revalidation-{NOTICE_NUMBER}-v1", scope),
        semantic_type="platform.external-revalidation",
        schema_version="p8.04-eis-temporal-revalidation-v1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=DERIVED_REVALIDATION_AUTHORITY_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(
            actor.actual_principal.principal_id,
            observation_version,
            baseline_identity,
        ),
        integrity_metadata=(
            ("baseline_manifest_sha256", BASELINE_MANIFEST_SHA256),
            ("fresh_manifest_sha256", comparison.get("fresh_manifest_sha256", "")),
            ("aggregate_result", comparison.get("aggregate_result", "")),
            ("comparison_manifest_sha256", comparison.get("manifest_sha256", "")),
        ),
        payload=(
            ("notice_number", NOTICE_NUMBER),
            ("external_source_authority", comparison.get("external_source_authority", "")),
        ),
        lifecycle_status="AdmissionCandidate",
    )

    artifact = ArtifactContent(
        artifact_id=Identity("artifact", f"p8-04-fresh-manifest-{NOTICE_NUMBER}-v1", scope),
        organization=organization,
        content_ref=f"owner-local://runs/{run_id}/procurement/p8-04-fresh-observation.json",
        media_type="application/json",
        integrity_ref=f"sha256:{fresh.get('manifest_sha256', '')}",
        rendition_role="evidence-manifest",
        handling=HandlingConstraints(
            "restricted-pilot",
            "external-authority-revalidation",
            ("read",),
            "owner-retention",
        ),
    )
    candidate = DocumentVersionCandidate(observation_record, (artifact,), "evidence-manifest")

    workflow_subject = Identity("workflow", "p8-04-revalidate-eis", scope)
    workflow_version = Identity("workflow-version", "p8-04-revalidate-eis-v1", scope)
    workflow_pin = GovernedVersionPin(
        workflow_subject, workflow_version, "platform.workflow", "platform.workflow/definition", "Approved"
    )
    workflow = WorkflowDefinition(
        record=CanonicalRecord(
            workflow_subject,
            workflow_version,
            "platform.workflow",
            "1",
            organization,
            AuthorityMode.NATIVE,
            "platform.workflow/definition",
            actor.actual_principal.principal_id,
            actor,
            created_at,
            (actor.actual_principal.principal_id,),
            (("type", "external-revalidation"),),
            (),
            "Approved",
        ),
        operations=(
            WorkflowOperation(
                semantic_name="OP_ADMIT_DOCUMENT_VERSION",
                target_subject_id=observation_subject,
                target_semantic_type="platform.document",
                side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
            ),
        ),
    )

    interaction = ProductRuntimeInteraction(
        organization=organization,
        product_id=product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        workflow=workflow,
        operation_name="OP_ADMIT_DOCUMENT_VERSION",
        material_inputs=(observation_record,),
        required_gates=(
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        ),
    )

    execution_subject = Identity("execution", "p8-04-revalidation", scope)
    v0_record = CanonicalRecord(
        subject_id=execution_subject,
        version_id=Identity("execution-version", "created", scope),
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
        lifecycle_status="Created",
    )
    material_input_pin = GovernedVersionPin(
        observation_subject,
        observation_version,
        "platform.document",
        DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        None,
    )
    v0 = GovernedExecutionContext(
        record=v0_record,
        workflow=workflow_pin,
        operation_name="OP_ADMIT_DOCUMENT_VERSION",
        operation_side_effects=(OperationSideEffectClass.CANONICAL_MUTATION,),
        material_inputs=(material_input_pin,),
        required_gates=interaction.required_gates,
        gate_decisions=(),
        product_contract=product_contract_pin,
    )

    v1 = await_required_gates(
        v0,
        version_id=Identity("execution-version", "awaiting-gate", scope),
        actor=actor,
        created_at=created_at,
    )

    _verify_a8_owner_decision(REPO_ROOT)
    decision = None
    temporary_grant_id = None
    try:
        decision, temporary_grant_id = provision_and_authorize(
            access_root=access_root,
            organization=org_id,
            principal=operator_id,
            credential_id=credential_id,
            credential_file=credential_file,
        )
        authorization_grant_id = _require_explicit_grant(decision)
        if authorization_grant_id != temporary_grant_id:
            raise SystemExit("BLOCKED: P7.04 grant reference mismatch")

        decisions = _build_gate_decisions(
            gates=interaction.required_gates,
            organization=organization,
            actor=actor,
            created_at=created_at,
            scope=scope,
            execution_subject=execution_subject,
            evaluated_execution_version_id=v1.execution_version_id,
            workflow_version_id=workflow_version,
            observation_version_id=observation_version,
            product_contract_version_id=product_contract_pin.version_id,
            authorization_grant_id=authorization_grant_id,
        )
        v2 = admit_ready_execution(
            v1,
            decisions=tuple(decisions),
            version_id=Identity("execution-version", "ready", scope),
            actor=actor,
            created_at=created_at,
        )
        v3 = transition_governed_execution(
            v2,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=Identity("execution-version", "running", scope),
            actor=actor,
            created_at=created_at,
        )

        admitted = admit_document_version(candidate)
        admitted_record = admitted.canonical_record
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
            external_authority=admitted_record.external_authority,
        )

        v4 = transition_governed_execution(
            v3,
            lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
            version_id=Identity("execution-version", "succeeded", scope),
            actor=actor,
            created_at=created_at,
            additional_provenance_refs=(
                final_admitted_record.version_id,
                comparison_record.version_id,
            ),
        )

        final_comparison_record = CanonicalRecord(
            subject_id=comparison_record.subject_id,
            version_id=comparison_record.version_id,
            semantic_type=comparison_record.semantic_type,
            schema_version=comparison_record.schema_version,
            organization=comparison_record.organization,
            authority_mode=comparison_record.authority_mode,
            authority_scope=comparison_record.authority_scope,
            accountable_owner_id=comparison_record.accountable_owner_id,
            creation_actor=comparison_record.creation_actor,
            created_at=comparison_record.created_at,
            provenance_refs=(
                *comparison_record.provenance_refs,
                execution_subject,
                v3.execution_version_id,
            ),
            integrity_metadata=comparison_record.integrity_metadata,
            payload=comparison_record.payload,
            lifecycle_status="Admitted",
        )

        platform_producer = Identity("producer", "platform.core", scope)
        event_id = Identity("event", f"p8-04-revalidation-event-{NOTICE_NUMBER}", scope)
        event_version_id = Identity("event-version", f"p8-04-revalidation-event-{NOTICE_NUMBER}-1", scope)
        provenance_refs = tuple(
            sorted(
                {
                    actor.actual_principal.principal_id,
                    product_id,
                    platform_producer,
                    execution_subject,
                    v4.execution_version_id,
                    final_admitted_record.subject_id,
                    final_admitted_record.version_id,
                    final_comparison_record.subject_id,
                    final_comparison_record.version_id,
                },
                key=lambda x: str(x),
            )
        )
        receipt = EventReceipt(
            event_id=event_id,
            version_id=event_version_id,
            event_type="platform.external-revalidation.completed",
            event_schema_version="1",
            organization=organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/admission",
            authoritative_source="platform.core",
            occurred_at=created_at,
            recorded_at=created_at,
            producer_id=platform_producer,
            initiating_actor_id=actor.actual_principal.principal_id,
            execution_subject_id=v4.execution_subject_id,
            execution_version_id=v4.execution_version_id,
            related_subject_ids=(final_admitted_record.subject_id, final_comparison_record.subject_id),
            related_version_ids=(final_admitted_record.version_id, final_comparison_record.version_id),
            correlation_refs=(execution_subject,),
            causation_refs=(v4.execution_version_id,),
            classification="internal",
            access_scope="organization",
            provenance_refs=provenance_refs,
        integrity_metadata=(
            ("aggregate_result", comparison.get("aggregate_result", "")),
            (
                "live_source_p8_04_temporal_sha256",
                LIVE_SOURCE_SHA256["p8_04_eis_temporal_revalidation.py"],
            ),
            (
                "live_source_p8_04_run_sha256",
                LIVE_SOURCE_SHA256["p8_04_run_eis_temporal_revalidation.py"],
            ),
            (
                "canonical_tender_agent_sha",
                POST_LIVE_CANONICAL_TENDER_AGENT_SHA,
            ),
        ),
        payload=(
            ("notice_number", NOTICE_NUMBER),
            ("baseline_manifest_sha256", BASELINE_MANIFEST_SHA256),
        ),
        )
        event_result = admit_event(
            receipt=receipt,
            execution=v4,
            related_records=(final_admitted_record, final_comparison_record),
        )

        patched_versions = []
        manifest_material_input_pin = GovernedVersionPin(
            observation_subject,
            observation_version,
            "platform.document",
            DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            "Admitted",
        )
        for ev in (v0, v1, v2, v3, v4):
            patched_versions.append(
                GovernedExecutionContext(
                    record=ev.record,
                    workflow=ev.workflow,
                    operation_name=ev.operation_name,
                    operation_side_effects=ev.operation_side_effects,
                    material_inputs=(manifest_material_input_pin,),
                    required_gates=ev.required_gates,
                    gate_decisions=ev.gate_decisions,
                    product_contract=ev.product_contract,
                )
            )
        manifest = build_reconstruction_manifest(
            execution_versions=tuple(patched_versions),
            result_records=(final_admitted_record, final_comparison_record),
            events=(event_result.event,),
        )

        from arvectum_os_ref.audit_reconstruction_support import reconstruct_audit_view

        view = reconstruct_audit_view(manifest=manifest, organization=organization)
        package = export_package(view, organization, execution_subject)
        _revoke_temporary_grant(access_root, temporary_grant_id)
        temporary_grant_id = None
        _print_evidence(decision, view, event_result, package, comparison)
        return 0
    finally:
        if temporary_grant_id is not None:
            try:
                _revoke_temporary_grant(access_root, temporary_grant_id)
            except Exception:  # noqa: BLE001, S110 - best-effort cleanup; primary error preserved
                pass


def _print_evidence(decision, view, event_result, package, comparison) -> None:
    """Print sanitized governed evidence. No credential/secret material is ever printed."""
    org_value = decision.organization.get("value", "") if isinstance(decision.organization, dict) else ""
    principal_value = decision.principal.get("value", "") if isinstance(decision.principal, dict) else ""
    print("RESULT: PASS")
    print(f"aggregate_result: {comparison.get('aggregate_result')}")
    print(f"baseline_manifest_sha256: {BASELINE_MANIFEST_SHA256}")
    print(f"fresh_manifest_sha256: {comparison.get('fresh_manifest_sha256')}")
    print(f"comparison_manifest_sha256: {comparison.get('manifest_sha256')}")
    print(f"reconstruction_complete: {view.complete}")
    print(f"event_version: {event_result.event.version_id}")
    print(f"evidence_roles: {len(package.evidence)}")
    print("product_id: arvectum-tender-operator")
    print(f"organization: {org_value}")
    print(f"organization_label: {OWNER_CONTEXT_LABEL}")
    print(f"principal: {principal_value}")
    print(f"principal_kind: {decision.principal_kind}")
    print(f"authorization_allowed: {decision.allowed}")
    print(f"authorization_reason: {decision.reason}")
    print(f"authorization_grant_id: {decision.grant_id}")
    print(f"authorization_grant_basis: {authorization_basis_value(decision.grant_id)}")
    print(f"authorization_operation: {decision.operation}")
    print(f"authorization_resource: {decision.resource}")
    print(f"authorization_access_path: {decision.access_path}")
    print(f"gate_authorization: {GovernedGateKind.AUTHORIZATION.value}")
    print(f"gate_organizational_authority: {GovernedGateKind.ORGANIZATIONAL_AUTHORITY.value}")
    print(f"gate_data_governance: {GovernedGateKind.DATA_GOVERNANCE.value}")
    print(f"gate_consequential_approval: {GovernedGateKind.CONSEQUENTIAL_APPROVAL.value}")
    print("organizational_authority_basis: decision-2026-08-20-phase-8-activation (A8 Approved)")
    print("data_governance_basis: p6-02-v0.1.0+p6-05-l7-exact-eis-manifest")
    print("consequential_approval_basis: decision-2026-08-20-phase-8-activation")
    print("temporary_grant_revoked: True")
    print(f"live_source_{'p8_04_eis_temporal_revalidation_py'}: {LIVE_SOURCE_SHA256['p8_04_eis_temporal_revalidation.py']}")
    print(f"live_source_{'p8_04_run_eis_temporal_revalidation_py'}: {LIVE_SOURCE_SHA256['p8_04_run_eis_temporal_revalidation.py']}")
    print(f"canonical_tender_agent_sha: {POST_LIVE_CANONICAL_TENDER_AGENT_SHA} (post-live reviewed publication)")
    print("additional_live_eis_calls: 0")


def export_package(view, organization, execution_subject):
    from arvectum_os_ref.audit_reconstruction_support import (
        export_reconstruction_package,
    )

    return export_reconstruction_package(view)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print("RESULT: FAIL-CLOSED")
        print(f"ERROR: {exc}")
        sys.exit(1)
