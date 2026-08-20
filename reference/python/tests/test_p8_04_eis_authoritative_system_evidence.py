"""Offline P8.04 governed-evidence coverage.

Uses synthetic redacted manifests only (no real tender bytes). Proves the
bounded governed admission + read-only reconstruction boundary required by the
P8.03 contract: immutable baseline reference, distinct fresh observation,
deterministic comparison, Event/provenance, and reconstruction without any
network replay. The Organization/Actor come from a synthetic but structurally
exact P6.05-L4 owner context, so identity resolution is exercised through the
same fail-closed path used for the real owner-local context.

Authorization is exercised against a real P7.04 owner-operated registry created
in the test sandbox: the exact temporary least-privilege grant is provisioned,
authorize_from_credential_file is called with the exact bounded scope, ALLOW is
possible only for EXPLICIT_LEAST_PRIVILEGE_GRANT, and the Authorization gate
basis binds the actual returned grant id. No credential secret is exposed.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import p7_04_persistent_access as p704
from arvectum_os_ref.audit_reconstruction_support import reconstruct_audit_view
from arvectum_os_ref.canonical import (
    AuthorityMode,
    CanonicalRecord,
    ExternalAuthorityContract,
)
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from arvectum_os_ref.event_provenance import (
    EventReceipt,
    admit_event,
    build_reconstruction_manifest,
)
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
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
from p8_04_eis_authoritative_system_evidence import (
    AUTHORIZATION_ACCESS_PATH,
    AUTHORIZATION_BASIS_NAMESPACE,
    AUTHORIZATION_OPERATION,
    AUTHORIZATION_RESOURCE,
    BASELINE_MANIFEST_SHA256,
    DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
    GATE_BASIS,
    LIVE_SOURCE_SHA256,
    NOTICE_NUMBER,
    POST_LIVE_CANONICAL_TENDER_AGENT_SHA,
    REPO_ROOT,
    _build_gate_decisions,
    _require_explicit_grant,
    _verify_a8_owner_decision,
    authorization_basis_value,
    evaluate_authorization,
)

SCOPE = "synthetic-org-scope-0001"
OPERATOR = "synthetic-operator-0001"


def _canonical_sha(payload: dict) -> str:
    body = {k: v for k, v in payload.items() if k not in ("manifest_sha256", "manifest_integrity_ref")}
    return hashlib.sha256(
        json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _blocked_network():
    import socket

    def fail(*_args, **_kwargs):
        raise RuntimeError("network replay attempted during reconstruction")

    socket.socket = fail
    socket.create_connection = fail


def _identity(namespace: str, value: str) -> Identity:
    return Identity(namespace, value, SCOPE)


def _write_owner_context(path: Path, *, context_label: str = "ООО «Арвектум»") -> Path:
    payload = {
        "schema_version": "p6.05-l4-local-context-1",
        "organization": {
            "identity": {"namespace": "organization", "value": SCOPE, "scope": "platform"},
            "context_label": context_label,
        },
        "operator": {
            "identity": {"namespace": "principal", "value": OPERATOR, "scope": SCOPE},
            "principal_category": "human",
            "operating_mode": "owner-operated",
        },
        "authority": {
            "authorization_grants": [],
            "delegations": [],
            "organizational_authority_claimed": False,
        },
        "authentication": {"evidence_refs": []},
        "bootstrap": {"scope": "P6.05-L4", "owner_authorization_asserted": True},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(path, 0o600)
    return path


def _org_and_actor():
    organization = OrganizationScope(Identity("organization", SCOPE, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", OPERATOR, SCOPE)),
        organization,
    )
    return organization, actor


def _fresh_manifest_payload() -> dict:
    payload = {
        "schema_version": "p6.05-exact-attachment-evidence-v1",
        "purpose": "exact-tender-attachment-evidence",
        "status": "PASS_EXACT_ATTACHMENT_EVIDENCE",
        "notice_number": NOTICE_NUMBER,
        "expected_document_count": 7,
        "exact_document_count": 7,
        "missing_names": [],
        "duplicate_names": [],
        "external_actions": False,
        "external_source_authority": "ЕИС / zakupki.gov.ru",
        "external_source_reference": f"44fz-notice:{NOTICE_NUMBER}",
        "external_source_version": "synthetic-ref",
        "retrieved_at": "2026-08-20T08:40:00+00:00",
        "documents": [],
    }
    payload["manifest_sha256"] = _canonical_sha(payload)
    return payload


def _comparison_payload(fresh_manifest_sha256: str, status: str = "NO_CHANGE") -> dict:
    payload = {
        "schema_version": "p8.04-eis-temporal-revalidation-v1",
        "purpose": "p8.04-eis-temporal-revalidation",
        "status": status,
        "notice_number": NOTICE_NUMBER,
        "external_source_authority": "ЕИС / zakupki.gov.ru",
        "external_source_reference": f"44fz-notice:{NOTICE_NUMBER}",
        "baseline_manifest_sha256": BASELINE_MANIFEST_SHA256,
        "fresh_manifest_sha256": fresh_manifest_sha256,
        "fresh_observed_at": "2026-08-20T08:40:00+00:00",
        "external_actions": False,
        "comparison_entries": [],
        "aggregate_result": status,
        "evidence_completeness": "complete",
    }
    payload["manifest_sha256"] = _canonical_sha(payload)
    return payload


FRESH_SHA = _fresh_manifest_payload()["manifest_sha256"]


class P804GovernedEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization, self.actor = _org_and_actor()
        self.created_at = datetime(2026, 8, 20, 8, 40, tzinfo=UTC)
        self.product_contract_pin = GovernedVersionPin(
            Identity("integration-contract", "p8-03-eis-authority-revalidation", SCOPE),
            Identity("integration-contract-version", "p8-03-eis-authority-revalidation-v0.1.0", SCOPE),
            "platform.integration-contract",
            "platform.integration-contract/definition",
            "Provisional",
        )
        self.tmp = Path(tempfile.mkdtemp(prefix="p8-04-test-")).resolve()
        self.owner_context = _write_owner_context(self.tmp / "local-context" / "organization-operator.json")
        self.human = Identity("principal", OPERATOR, SCOPE)
        self.access_root = self.tmp / "access"
        p704.bootstrap_from_p6_owner_context(self.access_root, self.owner_context)
        self.issued = p704.issue_credential(self.access_root, self.human)
        self.credential_id = self.issued["credential_id"]
        self.credential_file = Path(self.issued["secret_path"])

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _authority(self) -> ExternalAuthorityContract:
        return ExternalAuthorityContract(
            authoritative_system="zakupki.gov.ru",
            external_object_ref=f"44fz:notice:{NOTICE_NUMBER}",
            authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            retrieval_or_sync="SOAP getDocsByReestrNumber (read-only, P8.04)",
            freshness_expectation="fresh P8.04 observation vs immutable P6 baseline",
            source_version_semantics="complete tender attachment set with exact byte digests",
            conflict_rule="fail-closed",
            failure_behavior="missing evidence blocks PASS",
            permitted_transformations=("integrity hashing", "manifest generation", "comparison"),
            retention_deletion="owner-only rules",
            portability="governed reconstruction manifest",
        )

    def _observation_candidate(self):
        observation_subject = _identity("observation", f"eis-observation-{NOTICE_NUMBER}-fresh-v1")
        observation_version = _identity("observation-version", f"eis-observation-{NOTICE_NUMBER}-fresh-v1")
        record = CanonicalRecord(
            subject_id=observation_subject,
            version_id=observation_version,
            semantic_type="platform.document",
            schema_version="p8.04-eis-fresh-observation-v1",
            organization=self.organization,
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            accountable_owner_id=self.actor.actual_principal.principal_id,
            creation_actor=self.actor,
            created_at=self.created_at,
            provenance_refs=(self.actor.actual_principal.principal_id,),
            integrity_metadata=(("manifest_sha256", FRESH_SHA), ("observed_at", "2026-08-20T08:40:00+00:00")),
            payload=(("notice_number", NOTICE_NUMBER),),
            lifecycle_status="AdmissionCandidate",
            external_authority=self._authority(),
        )
        artifact = ArtifactContent(
            artifact_id=_identity("artifact", f"p8-04-fresh-manifest-{NOTICE_NUMBER}-v1"),
            organization=self.organization,
            content_ref="owner-local://runs/synthetic/p8-04-fresh-observation.json",
            media_type="application/json",
            integrity_ref=f"sha256:{FRESH_SHA}",
            rendition_role="evidence-manifest",
            handling=HandlingConstraints("restricted-pilot", "external-authority-revalidation", ("read",), "owner-retention"),
        )
        return DocumentVersionCandidate(record, (artifact,), "evidence-manifest")

    def _comparison_record(self):
        baseline_identity = _identity("baseline", f"p6-05-exact-attachment-evidence-{BASELINE_MANIFEST_SHA256[:16]}")
        return CanonicalRecord(
            subject_id=_identity("comparison", f"eis-revalidation-{NOTICE_NUMBER}"),
            version_id=_identity("comparison-version", f"eis-revalidation-{NOTICE_NUMBER}-v1"),
            semantic_type="platform.external-revalidation",
            schema_version="p8.04-eis-temporal-revalidation-v1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.external-revalidation",
            accountable_owner_id=self.actor.actual_principal.principal_id,
            creation_actor=self.actor,
            created_at=self.created_at,
            provenance_refs=(
                self.actor.actual_principal.principal_id,
                _identity("observation-version", f"eis-observation-{NOTICE_NUMBER}-fresh-v1"),
                baseline_identity,
            ),
            integrity_metadata=(
                ("baseline_manifest_sha256", BASELINE_MANIFEST_SHA256),
                ("fresh_manifest_sha256", FRESH_SHA),
                ("aggregate_result", "NO_CHANGE"),
            ),
            payload=(("notice_number", NOTICE_NUMBER),),
            lifecycle_status="AdmissionCandidate",
        )

    def _interaction(self, observation_record):
        workflow_subject = _identity("workflow", "p8-04-revalidate-eis")
        workflow_version = _identity("workflow-version", "p8-04-revalidate-eis-v1")
        workflow = WorkflowDefinition(
            record=CanonicalRecord(
                workflow_subject,
                workflow_version,
                "platform.workflow",
                "1",
                self.organization,
                AuthorityMode.NATIVE,
                "platform.workflow/definition",
                self.actor.actual_principal.principal_id,
                self.actor,
                self.created_at,
                (self.actor.actual_principal.principal_id,),
                (("type", "external-revalidation"),),
                (),
                "Approved",
            ),
            operations=(
                WorkflowOperation(
                    semantic_name="OP_ADMIT_DOCUMENT_VERSION",
                    target_subject_id=observation_record.subject_id,
                    target_semantic_type="platform.document",
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )
        return ProductRuntimeInteraction(
            organization=self.organization,
            product_id=Identity("product", "arvectum-tender-operator", SCOPE),
            product_version="restricted-paid-pilot/44fz-prebid-v1",
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

    # ---- manifest / structural tests ----

    def test_synthetic_manifests_are_internally_consistent(self) -> None:
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        self.assertEqual(comparison["baseline_manifest_sha256"], BASELINE_MANIFEST_SHA256)
        self.assertEqual(comparison["fresh_manifest_sha256"], fresh["manifest_sha256"])
        self.assertEqual(comparison["aggregate_result"], "NO_CHANGE")
        self.assertEqual(comparison["evidence_completeness"], "complete")

    def test_gate_bases_reference_existing_governed_evidence(self) -> None:
        self.assertNotIn(GovernedGateKind.AUTHORIZATION, GATE_BASIS)
        self.assertEqual(
            GATE_BASIS[GovernedGateKind.ORGANIZATIONAL_AUTHORITY],
            ("organizational-authority-basis", "decision-2026-08-20-phase-8-activation"),
        )
        self.assertEqual(
            GATE_BASIS[GovernedGateKind.DATA_GOVERNANCE],
            ("data-governance-basis", "p6-02-v0.1.0+p6-05-l7-exact-eis-manifest"),
        )
        self.assertEqual(
            GATE_BASIS[GovernedGateKind.CONSEQUENTIAL_APPROVAL],
            ("consequential-approval-basis", "decision-2026-08-20-phase-8-activation"),
        )
        for basis in GATE_BASIS.values():
            self.assertNotIn("owner-auth", basis)
            self.assertNotEqual(basis[0], "authority")

    def test_authorization_basis_is_dynamic_and_binds_grant_id(self) -> None:
        basis = authorization_basis_value("abc123")
        self.assertEqual(basis, "p7-04-persistent-access-grant:abc123")
        self.assertTrue(basis.startswith("p7-04-persistent-access-grant:"))
        for ns, value in GATE_BASIS.values():
            self.assertNotEqual(basis, value)
            self.assertTrue(ns.endswith("-basis"))
            self.assertNotEqual(ns, AUTHORIZATION_BASIS_NAMESPACE)
        with self.assertRaises(SystemExit):
            authorization_basis_value("bad:grant")

    def test_observation_is_external_reference_and_comparison_is_native(self) -> None:
        observation = self._observation_candidate().canonical_record
        self.assertEqual(observation.authority_mode, AuthorityMode.EXTERNAL_REFERENCE)
        self.assertIsNotNone(observation.external_authority)
        comparison = self._comparison_record()
        self.assertEqual(comparison.authority_mode, AuthorityMode.NATIVE)
        self.assertIsNone(comparison.external_authority)
        provenance_namespaces = {ref.namespace for ref in comparison.provenance_refs}
        self.assertIn("observation-version", provenance_namespaces)
        self.assertIn("baseline", provenance_namespaces)

    def test_product_attribution_is_tender_operator_not_platform(self) -> None:
        interaction = self._interaction(self._observation_candidate().canonical_record)
        self.assertEqual(interaction.product_id.value, "arvectum-tender-operator")
        self.assertNotEqual(interaction.product_id.value, "arvectum-os")
        self.assertEqual(interaction.product_version, "restricted-paid-pilot/44fz-prebid-v1")

    def test_live_provenance_constants_are_preserved_and_distinct(self) -> None:
        self.assertEqual(
            LIVE_SOURCE_SHA256["p8_04_eis_temporal_revalidation.py"],
            "29fc5471f4d6f797bb8eb5b8274aef77832445aa19d15750cb2bec9a75efb96e",
        )
        self.assertEqual(
            LIVE_SOURCE_SHA256["p8_04_run_eis_temporal_revalidation.py"],
            "ef41fb1a75fcf2d992edae05b238292a20aca67015dea7c924d2bf5c4aeb569e",
        )
        self.assertEqual(POST_LIVE_CANONICAL_TENDER_AGENT_SHA, "449cf980e46f561d6819349a3c5c258a069c0594")
        for live_sha in LIVE_SOURCE_SHA256.values():
            self.assertNotEqual(live_sha, POST_LIVE_CANONICAL_TENDER_AGENT_SHA)

    def test_a8_owner_decision_is_approved_in_exact_release(self) -> None:
        _verify_a8_owner_decision(REPO_ROOT)
        with self.assertRaises(SystemExit) as caught:
            _verify_a8_owner_decision(self.tmp / "missing")
        self.assertIn("BLOCKED", str(caught.exception))

    def test_reconstruction_complete_without_network_replay(self) -> None:
        _blocked_network()
        observation_candidate = self._observation_candidate()
        observation_record = observation_candidate.canonical_record
        comparison_record = self._comparison_record()
        interaction = self._interaction(observation_record)

        execution_subject = _identity("execution", "p8-04-revalidation")
        workflow_pin = GovernedVersionPin(
            interaction.workflow.record.subject_id,
            interaction.workflow.record.version_id,
            "platform.workflow",
            "platform.workflow/definition",
            "Approved",
        )
        material_input_pin = GovernedVersionPin(
            observation_record.subject_id,
            observation_record.version_id,
            "platform.document",
            DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            "Admitted",
        )
        v0 = GovernedExecutionContext(
            record=CanonicalRecord(
                subject_id=execution_subject,
                version_id=_identity("execution-version", "created"),
                semantic_type="platform.execution-context",
                schema_version="1",
                organization=self.organization,
                authority_mode=AuthorityMode.NATIVE,
                authority_scope="platform.execution",
                accountable_owner_id=self.actor.actual_principal.principal_id,
                creation_actor=self.actor,
                created_at=self.created_at,
                provenance_refs=(self.actor.actual_principal.principal_id, self.product_contract_pin.version_id),
                integrity_metadata=(("state", "Created"),),
                payload=(),
                lifecycle_status="Created",
            ),
            workflow=workflow_pin,
            operation_name="OP_ADMIT_DOCUMENT_VERSION",
            operation_side_effects=(OperationSideEffectClass.CANONICAL_MUTATION,),
            material_inputs=(material_input_pin,),
            required_gates=interaction.required_gates,
            gate_decisions=(),
            product_contract=self.product_contract_pin,
        )
        v1 = await_required_gates(
            v0,
            version_id=_identity("execution-version", "awaiting-gate"),
            actor=self.actor,
            created_at=self.created_at,
        )
        decisions = _build_gate_decisions(
            gates=interaction.required_gates,
            organization=self.organization,
            actor=self.actor,
            created_at=self.created_at,
            scope=SCOPE,
            execution_subject=execution_subject,
            evaluated_execution_version_id=v1.execution_version_id,
            workflow_version_id=interaction.workflow.record.version_id,
            observation_version_id=observation_record.version_id,
            product_contract_version_id=self.product_contract_pin.version_id,
            authorization_grant_id="test-grant-id",
        )
        v2 = admit_ready_execution(
            v1,
            decisions=decisions,
            version_id=_identity("execution-version", "ready"),
            actor=self.actor,
            created_at=self.created_at,
        )
        v3 = transition_governed_execution(
            v2,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=_identity("execution-version", "running"),
            actor=self.actor,
            created_at=self.created_at,
        )

        admitted_observation = CanonicalRecord(
            subject_id=observation_record.subject_id,
            version_id=observation_record.version_id,
            semantic_type=observation_record.semantic_type,
            schema_version=observation_record.schema_version,
            organization=observation_record.organization,
            authority_mode=observation_record.authority_mode,
            authority_scope=observation_record.authority_scope,
            accountable_owner_id=observation_record.accountable_owner_id,
            creation_actor=observation_record.creation_actor,
            created_at=observation_record.created_at,
            provenance_refs=(*observation_record.provenance_refs, execution_subject, v3.execution_version_id),
            integrity_metadata=observation_record.integrity_metadata,
            payload=observation_record.payload,
            lifecycle_status="Admitted",
            external_authority=observation_record.external_authority,
        )
        final_comparison = CanonicalRecord(
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
            provenance_refs=(*comparison_record.provenance_refs, execution_subject, v3.execution_version_id),
            integrity_metadata=comparison_record.integrity_metadata,
            payload=comparison_record.payload,
            lifecycle_status="Admitted",
        )
        v4 = transition_governed_execution(
            v3,
            lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
            version_id=_identity("execution-version", "succeeded"),
            actor=self.actor,
            created_at=self.created_at,
            additional_provenance_refs=(admitted_observation.version_id, final_comparison.version_id),
        )

        event_id = _identity("event", f"p8-04-revalidation-event-{NOTICE_NUMBER}")
        event_version = _identity("event-version", f"p8-04-revalidation-event-{NOTICE_NUMBER}-1")
        provenance = tuple(
            sorted(
                {
                    self.actor.actual_principal.principal_id,
                    interaction.product_id,
                    _identity("producer", "platform.core"),
                    execution_subject,
                    v4.execution_version_id,
                    admitted_observation.subject_id,
                    admitted_observation.version_id,
                    final_comparison.subject_id,
                    final_comparison.version_id,
                },
                key=lambda x: str(x),
            )
        )
        receipt = EventReceipt(
            event_id=event_id,
            version_id=event_version,
            event_type="platform.external-revalidation.completed",
            event_schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/admission",
            authoritative_source="platform.core",
            occurred_at=self.created_at,
            recorded_at=self.created_at,
            producer_id=_identity("producer", "platform.core"),
            initiating_actor_id=self.actor.actual_principal.principal_id,
            execution_subject_id=execution_subject,
            execution_version_id=v4.execution_version_id,
            related_subject_ids=(admitted_observation.subject_id, final_comparison.subject_id),
            related_version_ids=(admitted_observation.version_id, final_comparison.version_id),
            correlation_refs=(execution_subject,),
            causation_refs=(v4.execution_version_id,),
            classification="internal",
            access_scope="organization",
            provenance_refs=provenance,
            integrity_metadata=(("aggregate_result", "NO_CHANGE"),),
            payload=(("notice_number", NOTICE_NUMBER), ("baseline_manifest_sha256", BASELINE_MANIFEST_SHA256)),
        )
        event_result = admit_event(
            receipt=receipt,
            execution=v4,
            related_records=(admitted_observation, final_comparison),
        )

        patched = tuple(
            GovernedExecutionContext(
                record=ev.record,
                workflow=ev.workflow,
                operation_name=ev.operation_name,
                operation_side_effects=ev.operation_side_effects,
                material_inputs=(material_input_pin,),
                required_gates=ev.required_gates,
                gate_decisions=ev.gate_decisions,
                product_contract=ev.product_contract,
            )
            for ev in (v0, v1, v2, v3, v4)
        )
        manifest = build_reconstruction_manifest(
            execution_versions=patched,
            result_records=(admitted_observation, final_comparison),
            events=(event_result.event,),
        )
        view = reconstruct_audit_view(manifest=manifest, organization=self.organization)
        self.assertTrue(view.complete)
        result_roles = {item.role for item in view.evidence}
        self.assertIn("material-input", result_roles)
        self.assertIn("result", result_roles)
        self.assertIn("event", result_roles)

    # ---- P7.04 authorization decision tests ----

    def _evaluate(self, **overrides):
        kwargs = {
            "access_root": self.access_root,
            "organization": Identity("organization", SCOPE, "platform"),
            "principal": self.human,
            "credential_id": self.credential_id,
            "credential_file": self.credential_file,
        }
        kwargs.update(overrides)
        return evaluate_authorization(**kwargs)

    def _grant(self, *, operation=AUTHORIZATION_OPERATION, resource=AUTHORIZATION_RESOURCE, access_paths=("local",)):
        return p704.grant_access(self.access_root, self.human, operation=operation, resource=resource, access_paths=access_paths)

    def test_authorization_exact_grant_and_valid_credential_allows(self) -> None:
        self._grant()
        decision = self._evaluate()
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "EXPLICIT_LEAST_PRIVILEGE_GRANT")
        self.assertIsNotNone(decision.grant_id)
        self.assertEqual(decision.operation, AUTHORIZATION_OPERATION)
        self.assertEqual(decision.resource, AUTHORIZATION_RESOURCE)
        self.assertEqual(decision.access_path, AUTHORIZATION_ACCESS_PATH)
        self.assertEqual(decision.principal_kind, "human")
        self.assertFalse(decision.organizational_authority_satisfied)
        self.assertFalse(decision.consequential_approval_satisfied)

    def test_authorization_no_grant_blocked(self) -> None:
        decision = self._evaluate()
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "NO_EXPLICIT_GRANT")
        with self.assertRaises(SystemExit) as caught:
            _require_explicit_grant(decision)
        self.assertIn("BLOCKED", str(caught.exception))

    def test_authorization_wrong_operation_blocked(self) -> None:
        self._grant(operation="p8.04.eis-revalidation.other")
        decision = self._evaluate()
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "NO_EXPLICIT_GRANT")
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_wrong_resource_blocked(self) -> None:
        self._grant(resource="p8-04:eis-revalidation:another-notice")
        decision = self._evaluate()
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "NO_EXPLICIT_GRANT")
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_wrong_organization_blocked(self) -> None:
        self._grant()
        decision = self._evaluate(organization=Identity("organization", "foreign-org", "platform"))
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "ORGANIZATION_SCOPE_MISMATCH")
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_wrong_principal_blocked(self) -> None:
        self._grant()
        other = Identity("principal", "unregistered-principal", SCOPE)
        decision = self._evaluate(principal=other)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "PRINCIPAL_NOT_REGISTERED")
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_revoked_credential_blocked(self) -> None:
        self._grant()
        p704.revoke_credential(self.access_root, self.credential_id)
        decision = self._evaluate()
        self.assertFalse(decision.allowed)
        self.assertIn(decision.reason, {"CREDENTIAL_REVOKED", "CREDENTIAL_SECRET_UNAVAILABLE"})
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_invalid_credential_blocked(self) -> None:
        self._grant()
        bogus = self.tmp / "bogus.secret"
        bogus.write_text("not-the-real-secret\n", encoding="utf-8")
        os.chmod(bogus, 0o600)
        decision = self._evaluate(credential_file=bogus)
        self.assertFalse(decision.allowed)
        self.assertIn(decision.reason, {"AUTHENTICATION_FAILED", "CREDENTIAL_SECRET_UNAVAILABLE"})
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_revoked_grant_blocked(self) -> None:
        grant_id = self._grant()
        p704.revoke_grant(self.access_root, grant_id)
        decision = self._evaluate()
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "NO_EXPLICIT_GRANT")
        with self.assertRaises(SystemExit):
            _require_explicit_grant(decision)

    def test_authorization_gate_basis_binds_actual_returned_grant_id(self) -> None:
        self._grant()
        decision = self._evaluate()
        grant_id = _require_explicit_grant(decision)
        observation_record = self._observation_candidate().canonical_record
        interaction = self._interaction(observation_record)
        execution_subject = _identity("execution", "p8-04-revalidation")
        v0 = GovernedExecutionContext(
            record=CanonicalRecord(
                subject_id=execution_subject,
                version_id=_identity("execution-version", "created"),
                semantic_type="platform.execution-context",
                schema_version="1",
                organization=self.organization,
                authority_mode=AuthorityMode.NATIVE,
                authority_scope="platform.execution",
                accountable_owner_id=self.actor.actual_principal.principal_id,
                creation_actor=self.actor,
                created_at=self.created_at,
                provenance_refs=(self.actor.actual_principal.principal_id, self.product_contract_pin.version_id),
                integrity_metadata=(("state", "Created"),),
                payload=(),
                lifecycle_status="Created",
            ),
            workflow=GovernedVersionPin(
                interaction.workflow.record.subject_id,
                interaction.workflow.record.version_id,
                "platform.workflow",
                "platform.workflow/definition",
                "Approved",
            ),
            operation_name="OP_ADMIT_DOCUMENT_VERSION",
            operation_side_effects=(OperationSideEffectClass.CANONICAL_MUTATION,),
            material_inputs=(
                GovernedVersionPin(
                    observation_record.subject_id,
                    observation_record.version_id,
                    "platform.document",
                    DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
                    None,
                ),
            ),
            required_gates=interaction.required_gates,
            gate_decisions=(),
            product_contract=self.product_contract_pin,
        )
        v1 = await_required_gates(
            v0,
            version_id=_identity("execution-version", "awaiting-gate"),
            actor=self.actor,
            created_at=self.created_at,
        )
        decisions = _build_gate_decisions(
            gates=interaction.required_gates,
            organization=self.organization,
            actor=self.actor,
            created_at=self.created_at,
            scope=SCOPE,
            execution_subject=execution_subject,
            evaluated_execution_version_id=v1.execution_version_id,
            workflow_version_id=interaction.workflow.record.version_id,
            observation_version_id=_identity("observation-version", f"eis-observation-{NOTICE_NUMBER}-fresh-v1"),
            product_contract_version_id=self.product_contract_pin.version_id,
            authorization_grant_id=grant_id,
        )
        by_kind = {d.kind: d for d in decisions}
        auth = by_kind[GovernedGateKind.AUTHORIZATION]
        self.assertEqual(auth.outcome, GovernedGateOutcome.ALLOW)
        self.assertEqual(auth.basis_ref.namespace, AUTHORIZATION_BASIS_NAMESPACE)
        self.assertEqual(auth.basis_ref.value, authorization_basis_value(grant_id))
        self.assertTrue(auth.basis_ref.value.startswith("p7-04-persistent-access-grant:"))
        self.assertNotEqual(
            auth.basis_ref.value,
            GATE_BASIS[GovernedGateKind.ORGANIZATIONAL_AUTHORITY][1],
        )
        self.assertNotEqual(
            auth.basis_ref.value,
            GATE_BASIS[GovernedGateKind.DATA_GOVERNANCE][1],
        )

    def test_organizational_authority_and_data_governance_remain_separate(self) -> None:
        self._grant()
        decision = self._evaluate()
        self.assertFalse(decision.organizational_authority_satisfied)
        self.assertFalse(decision.consequential_approval_satisfied)
        auth_basis = authorization_basis_value(decision.grant_id)
        self.assertNotEqual(auth_basis, GATE_BASIS[GovernedGateKind.ORGANIZATIONAL_AUTHORITY][1])
        self.assertNotEqual(auth_basis, GATE_BASIS[GovernedGateKind.DATA_GOVERNANCE][1])

    # ---- end-to-end module tests ----

    def _run_main(self, fresh, comparison, owner_context=None, credential_file=None, env_extra=None):
        from p8_04_eis_authoritative_system_evidence import main as p804_main

        env = {
            "AI_CORP_TENDER_OPERATOR_DEMO_RUNS_DIR": "/tmp/synthetic",
            "P8_04_RUN_ID": "synthetic",
            "P8_04_P6_OWNER_CONTEXT": str(owner_context or self.owner_context),
            "P8_04_ACCESS_ROOT": str(self.access_root),
            "P8_04_CREDENTIAL_ID": self.credential_id,
            "P8_04_CREDENTIAL_FILE": str(credential_file or self.credential_file),
        }
        env.update(env_extra or {})
        with patch.dict("os.environ", env, clear=False), patch(
            "p8_04_eis_authoritative_system_evidence._load_json",
            side_effect=[fresh, comparison],
        ):
            return p804_main()

    def test_p804_module_rejects_missing_owner_context(self) -> None:
        from p8_04_eis_authoritative_system_evidence import main as p804_main

        env = {
            "AI_CORP_TENDER_OPERATOR_DEMO_RUNS_DIR": "/tmp/synthetic",
            "P8_04_RUN_ID": "synthetic",
        }
        with patch.dict("os.environ", env, clear=False), self.assertRaises(SystemExit) as caught:
            p804_main()
        self.assertIn("P8_04_P6_OWNER_CONTEXT", str(caught.exception))

    def test_p804_module_rejects_missing_access_inputs(self) -> None:
        from p8_04_eis_authoritative_system_evidence import main as p804_main

        env = {
            "AI_CORP_TENDER_OPERATOR_DEMO_RUNS_DIR": "/tmp/synthetic",
            "P8_04_RUN_ID": "synthetic",
            "P8_04_P6_OWNER_CONTEXT": str(self.owner_context),
        }
        with patch.dict("os.environ", env, clear=False), self.assertRaises(SystemExit) as caught:
            p804_main()
        self.assertIn("P8_04_ACCESS_ROOT", str(caught.exception))

    def test_p804_module_rejects_foreign_owner_context(self) -> None:
        foreign = self.tmp / "foreign" / "organization-operator.json"
        _write_owner_context(foreign, context_label="Другая компания")
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        with self.assertRaises(SystemExit) as caught:
            self._run_main(fresh, comparison, owner_context=foreign)
        self.assertIn("BLOCKED", str(caught.exception))

    def test_p804_module_guards_reject_bad_comparison(self) -> None:
        fresh = _fresh_manifest_payload()
        bad = _comparison_payload(fresh["manifest_sha256"])
        bad["baseline_manifest_sha256"] = "0" * 64
        with self.assertRaises(SystemExit) as caught:
            self._run_main(fresh, bad)
        self.assertIn("BLOCKED", str(caught.exception))

    def test_p804_module_rejects_tampered_fresh_integrity(self) -> None:
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        fresh["manifest_sha256"] = "f" * 64
        with self.assertRaises(SystemExit) as caught:
            self._run_main(fresh, comparison)
        self.assertIn("integrity mismatch", str(caught.exception))

    def test_p804_module_rejects_tampered_comparison_integrity(self) -> None:
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        comparison["manifest_sha256"] = "f" * 64
        with self.assertRaises(SystemExit) as caught:
            self._run_main(fresh, comparison)
        self.assertIn("integrity mismatch", str(caught.exception))

    def test_p804_module_fails_closed_when_credential_revoked(self) -> None:
        p704.revoke_credential(self.access_root, self.credential_id)
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        with self.assertRaises(SystemExit) as caught:
            self._run_main(fresh, comparison)
        self.assertIn("BLOCKED", str(caught.exception))
        state = p704.load_access_store(self.access_root)
        self.assertTrue(all(record["status"] == "revoked" for record in state["grants"].values()))

    def test_product_contract_availability_cannot_bypass_failed_authorization(self) -> None:
        bogus = self.tmp / "bogus.secret"
        bogus.write_text("not-the-real-secret\n", encoding="utf-8")
        os.chmod(bogus, 0o600)
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        with self.assertRaises(SystemExit) as caught:
            self._run_main(fresh, comparison, credential_file=bogus)
        self.assertIn("BLOCKED", str(caught.exception))
        state = p704.load_access_store(self.access_root)
        self.assertTrue(all(record["status"] == "revoked" for record in state["grants"].values()))

    def test_p804_module_full_admission_proves_revoked_grant_and_zero_network(self) -> None:
        _blocked_network()
        fresh = _fresh_manifest_payload()
        comparison = _comparison_payload(fresh["manifest_sha256"])
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            rc = self._run_main(fresh, comparison)
        out = buffer.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("RESULT: PASS", out)
        self.assertIn("aggregate_result: NO_CHANGE", out)
        self.assertIn("reconstruction_complete: True", out)
        self.assertIn("product_id: arvectum-tender-operator", out)
        self.assertIn("authorization_allowed: True", out)
        self.assertIn("authorization_reason: EXPLICIT_LEAST_PRIVILEGE_GRANT", out)
        self.assertIn("authorization_operation: " + AUTHORIZATION_OPERATION, out)
        self.assertIn("authorization_resource: " + AUTHORIZATION_RESOURCE, out)
        self.assertIn("authorization_access_path: local", out)
        self.assertIn("authorization_grant_basis: p7-04-persistent-access-grant:", out)
        self.assertIn("temporary_grant_revoked: True", out)
        self.assertIn("additional_live_eis_calls: 0", out)
        self.assertIn(LIVE_SOURCE_SHA256["p8_04_eis_temporal_revalidation.py"], out)
        self.assertIn(LIVE_SOURCE_SHA256["p8_04_run_eis_temporal_revalidation.py"], out)
        self.assertIn(POST_LIVE_CANONICAL_TENDER_AGENT_SHA, out)

        secret = p704.read_credential_secret(self.credential_file)
        self.assertNotIn(secret, out)
        self.assertNotIn(self.credential_id, out)
        self.assertNotIn("secrets/p7-04", out)

        state = p704.load_access_store(self.access_root)
        remaining = [
            gid for gid, g in state["grants"].items()
            if g["operation"] == AUTHORIZATION_OPERATION
            and g["resource"] == AUTHORIZATION_RESOURCE
            and g["status"] == "active"
        ]
        self.assertEqual(remaining, [])
        revoked = [
            g for g in state["grants"].values()
            if g["operation"] == AUTHORIZATION_OPERATION
            and g["resource"] == AUTHORIZATION_RESOURCE
        ]
        self.assertTrue(revoked)
        self.assertTrue(all(g["status"] == "revoked" and g["revoked_at"] is not None for g in revoked))


if __name__ == "__main__":
    unittest.main()
