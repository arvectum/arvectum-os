from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode
from arvectum_os_ref.document_artifact_governance import (
    ArtifactState,
    DocumentVersionCandidate,
)
from arvectum_os_ref.governed_execution import (
    ConsequentialOperationNotAdmittedError,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_composition import IntegrationCompositionContinuityError
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
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


if __name__ == "__main__":
    unittest.main()
