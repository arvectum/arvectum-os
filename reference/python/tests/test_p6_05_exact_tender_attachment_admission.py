from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.document_artifact_governance import (
    ArtifactState,
    DocumentVersionCandidate,
)
from arvectum_os_ref.governed_execution import (
    ConsequentialOperationNotAdmittedError,
    GovernedGateOutcome,
    GovernedExecutionLifecycle,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_composition import IntegrationCompositionContinuityError
from arvectum_os_ref.product_capability_consumption import (
    AccessRequest,
    CapabilityConsumptionRequest,
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
)
from arvectum_os_ref.event_provenance import (
    EventReceipt,
    admit_event,
    build_reconstruction_manifest,
    CanonicalEvent,
)
from p6_05_tender_attachment_ref.contract import (
    OP_ADMIT_DOCUMENT_VERSION,
    P6_02_CANONICAL_BLOB_SHA,
)
from p6_05_tender_attachment_ref.scenario import (
    SYNTHETIC_MANIFEST_SHA256,
    build_p6_05_synthetic_admission_scenario,
)


UTC = timezone.utc


class P605ExactTenderAttachmentAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = build_p6_05_synthetic_admission_scenario()
        self.base_time = datetime(2026, 8, 9, 18, 40, tzinfo=UTC)

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.scenario.organization.organization_id.value)

    def _created_execution(self):
        return self.scenario.adapters.facade.start_governed_execution(
            interaction=self.scenario.interaction,
            execution_id=self._id("execution-subject", "p6-05-admission"),
            version_id=self._id("execution-version", "p6-05-admission-v1"),
            created_at=self.base_time,
            governed_versions=self.scenario.governed_versions,
        )

    def _ready_execution(self):
        awaiting = await_required_gates(
            self._created_execution(),
            version_id=self._id("execution-version", "p6-05-admission-v2"),
            actor=self.scenario.actor,
            created_at=self.base_time + timedelta(minutes=1),
        )
        decisions = []
        for index, kind in enumerate(awaiting.required_gates, start=1):
            decisions.append(
                build_governed_gate_decision(
                    execution=awaiting,
                    kind=kind,
                    outcome=GovernedGateOutcome.ALLOW,
                    decision_actor=self.scenario.actor,
                    basis_ref=self._id("governed-basis", f"{kind.value.lower()}-basis"),
                    decision_id=self._id("gate-decision-subject", f"p6-05-{index}"),
                    version_id=self._id("gate-decision-version", f"p6-05-{index}-v1"),
                    created_at=self.base_time + timedelta(minutes=1 + index),
                )
            )
        return admit_ready_execution(
            awaiting,
            decisions=tuple(decisions),
            version_id=self._id("execution-version", "p6-05-admission-v3"),
            actor=self.scenario.actor,
            created_at=self.base_time + timedelta(minutes=10),
        )

    def test_projection_preserves_exact_p6_02_version_and_does_not_add_cap002_or_cap003(self) -> None:
        contract = self.scenario.contract
        self.assertEqual(
            contract.version_pin.version_id.value,
            "p6-02-arvectum-tender-operator-v0.1.0",
        )
        self.assertNotEqual(contract.record.version_id, contract.version_pin.version_id)
        self.assertNotEqual(contract.record.subject_id, contract.version_pin.subject_id)
        self.assertEqual(contract.canonical_source_blob_sha, P6_02_CANONICAL_BLOB_SHA)

        dependency_ids = {item.dependency_id for item in contract.dependencies}
        self.assertIn(CAP_001_DOCUMENT_ARTIFACT, dependency_ids)
        self.assertNotIn(CAP_002_MEMORY_KNOWLEDGE, dependency_ids)
        self.assertNotIn(CAP_003_SEARCH_PROJECTION, dependency_ids)
        admission = next(
            item for item in contract.operations if item.operation_name == OP_ADMIT_DOCUMENT_VERSION
        )
        self.assertEqual(admission.dependency_id, CAP_001_DOCUMENT_ARTIFACT)

    def test_exact_manifest_is_admitted_only_after_governed_execution_gates(self) -> None:
        admitted = self.scenario.adapters.capabilities.admit_document_version(
            execution=self._ready_execution(),
            candidate=self.scenario.candidate,
        )
        self.assertEqual(
            admitted.version_id,
            self.scenario.candidate.canonical_record.version_id,
        )
        self.assertIs(admitted.canonical_record.authority_mode, AuthorityMode.EXTERNAL_REFERENCE)
        self.assertEqual(len(admitted.artifacts), 1)
        self.assertIs(admitted.artifacts[0].state, ArtifactState.GOVERNED)
        self.assertEqual(
            admitted.artifacts[0].integrity_ref,
            f"sha256:{SYNTHETIC_MANIFEST_SHA256}",
        )
        self.assertEqual(
            dict(admitted.canonical_record.integrity_metadata)["member_count"],
            "7",
        )

    def test_created_execution_cannot_admit_document_candidate(self) -> None:
        with self.assertRaises(ConsequentialOperationNotAdmittedError):
            self.scenario.adapters.capabilities.admit_document_version(
                execution=self._created_execution(),
                candidate=self.scenario.candidate,
            )

    def test_candidate_must_be_exact_execution_material_input(self) -> None:
        wrong_record = replace(
            self.scenario.candidate.canonical_record,
            version_id=self._id("document-version", "different-version"),
        )
        wrong_candidate = DocumentVersionCandidate(
            wrong_record,
            self.scenario.candidate.artifacts,
            self.scenario.candidate.designated_rendition_role,
        )
        with self.assertRaises(IntegrationCompositionContinuityError):
            self.scenario.adapters.capabilities.admit_document_version(
                execution=self._ready_execution(),
                candidate=wrong_candidate,
            )

    def test_end_to_end_identity_preserving_reconstruction(self) -> None:
        # Sequence: Create -> Gates -> Ready
        v1 = self._created_execution()

        # FIX: result must reference execution for reconstruction to pass
        execution_subject = v1.execution_subject_id
        orig_record = self.scenario.candidate.canonical_record
        fixed_record = replace(
            orig_record,
            provenance_refs=tuple(dict.fromkeys(orig_record.provenance_refs + (execution_subject,)))
        )
        fixed_candidate = DocumentVersionCandidate(
            fixed_record, self.scenario.candidate.artifacts, self.scenario.candidate.designated_rendition_role
        )

        # We must re-create execution with the fixed record as material input
        interaction = replace(self.scenario.interaction, material_inputs=(fixed_record,))
        v1 = self.scenario.adapters.facade.start_governed_execution(
            interaction=interaction,
            execution_id=execution_subject,
            version_id=self._id("execution-version", "p6-05-v1"),
            created_at=self.base_time,
            governed_versions=self.scenario.governed_versions,
        )

        v2 = await_required_gates(
            v1, version_id=self._id("execution-version", "p6-05-v2"),
            actor=self.scenario.actor, created_at=self.base_time + timedelta(minutes=1)
        )
        decisions = []
        for index, kind in enumerate(v2.required_gates, start=1):
            decisions.append(build_governed_gate_decision(
                execution=v2, kind=kind, outcome=GovernedGateOutcome.ALLOW, decision_actor=self.scenario.actor,
                basis_ref=self._id("basis", f"gate-{index}"),
                decision_id=self._id("gate-decision", f"gate-{index}"),
                version_id=self._id("gate-version", f"gate-{index}-v1"),
                created_at=self.base_time + timedelta(minutes=1 + index)
            ))
        ready = admit_ready_execution(
            v2, decisions=tuple(decisions),
            version_id=self._id("execution-version", "p6-05-v3"),
            actor=self.scenario.actor, created_at=self.base_time + timedelta(minutes=10)
        )

        # 1. Admit Document Version (ID preserved)
        admitted = self.scenario.adapters.capabilities.admit_document_version(
            execution=ready, candidate=fixed_candidate
        )
        self.assertEqual(admitted.version_id, fixed_candidate.canonical_record.version_id)

        # 2. Transition to terminal Succeeded
        running = transition_governed_execution(
            ready, lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", "p6-05-v4"),
            actor=self.scenario.actor, created_at=self.base_time + timedelta(minutes=11)
        )
        terminal = transition_governed_execution(
            running, lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
            version_id=self._id("execution-version", "p6-05-v5"),
            actor=self.scenario.actor, created_at=self.base_time + timedelta(minutes=12),
            additional_provenance_refs=(admitted.document_id, admitted.version_id)
        )

        # 3. Event admission
        receipt = EventReceipt(
            event_id=self._id("event-subject", "admission"),
            version_id=self._id("event-version", "admission-v1"),
            event_type="p6.05.document-admitted", event_schema_version="1",
            organization=self.scenario.organization, authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.document/admission", authoritative_source="platform.core",
            occurred_at=self.base_time + timedelta(minutes=11),
            recorded_at=self.base_time + timedelta(minutes=13),
            producer_id=self._id("producer", "platform.core"),
            initiating_actor_id=self.scenario.actor.actual_principal.principal_id,
            execution_subject_id=terminal.execution_subject_id,
            execution_version_id=terminal.execution_version_id,
            related_subject_ids=(admitted.document_id,),
            related_version_ids=(admitted.version_id,),
            correlation_refs=(terminal.execution_subject_id,),
            causation_refs=(terminal.execution_version_id,),
            classification="internal", access_scope="organization",
            provenance_refs=(
                self._id("producer", "platform.core"),
                self.scenario.actor.actual_principal.principal_id,
                terminal.execution_subject_id, terminal.execution_version_id,
                admitted.document_id, admitted.version_id
            ),
            integrity_metadata=(("rep", "mock"),), payload=()
        )
        ev_result = admit_event(receipt=receipt, execution=terminal, related_records=(admitted.canonical_record,))

        # 4. Reconstruct
        manifest = build_reconstruction_manifest(
            execution_versions=(v1, v2, ready, running, terminal),
            result_records=(admitted.canonical_record,),
            events=(ev_result.event,)
        )

        # Verify overlap (identity-preserving)
        self.assertEqual(manifest.material_inputs[0].version_id, manifest.results[0].version_id)

        # 5. Access
        access_request = AccessRequest(
            actor=self.scenario.actor, purpose="review", required_right="read", allowed_classifications=("internal",)
        )
        pins = [manifest.workflow] + list(manifest.material_inputs) + list(manifest.gate_decisions) + list(manifest.execution_versions) + list(manifest.results) + list(manifest.events)
        if manifest.product_contract:
            pins.append(manifest.product_contract)
        v_ids = {pin.version_id for pin in pins}
        constraints = tuple((vid, "review", ("read",), "internal") for vid in v_ids)

        reconstruction = self.scenario.adapters.capabilities.reconstruct_execution(
            request=CapabilityConsumptionRequest(
                organization=self.scenario.organization, product_id=self.scenario.contract.product_id,
                product_version=self.scenario.contract.product_version,
                dependency_id=CAP_004_AUDIT_RECONSTRUCTION, dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
                operation_name=OP_RECONSTRUCT_EXECUTION, access=access_request
            ),
            governed_versions=self.scenario.governed_versions,
            manifest=manifest, evidence_constraints=constraints
        )
        self.assertTrue(reconstruction.complete)
        # Verify two roles for the shared version
        matches = [item for item in reconstruction.evidence if item.version_id == admitted.version_id]
        self.assertEqual(len(matches), 2)
        roles = {item.role for item in matches}
        self.assertEqual(roles, {"material-input", "result"})


if __name__ == "__main__":
    unittest.main()
