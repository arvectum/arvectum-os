from dataclasses import FrozenInstanceError
import unittest

from arvectum_os_ref.audit_reconstruction_support import (
    AuditReconstructionError,
    EvidenceAvailability,
    EvidenceDisposition,
    export_reconstruction_package,
    reconstruct_audit_view,
)
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import OrganizationScope


class P306AuditReconstructionSupportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.execution_id = self._id("execution-subject", "execution-a")
        self.actor_id = self._id("principal", "initiator")
        self.workflow = self._pin("workflow", "workflow-a", "workflow-a-v1", "platform.workflow")
        self.input = self._pin("input", "input-a", "input-a-v1", "example.input")
        self.contract = self._pin("contract", "contract-a", "contract-a-v1", "platform.product-contract")
        self.gate = self._pin("gate", "gate-a", "gate-a-v1", "platform.execution-gate-decision")
        self.execution_v1 = self._pin("execution", "execution-a", "execution-a-v1", "platform.execution-context")
        self.execution_v2 = self._pin("execution", "execution-a", "execution-a-v2", "platform.execution-context")
        self.result = self._pin("result", "result-a", "result-a-v1", "example.result")
        self.event = self._pin("event", "event-a", "event-a-v1", "platform.event")
        self.correlation = (self.execution_id,)
        self.causation = (self.execution_v2.version_id,)
        self.manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.execution_id,
            initiating_actor_id=self.actor_id,
            operation_name="bounded-operation",
            workflow=self.workflow,
            material_inputs=(self.input,),
            gate_decisions=(self.gate,),
            execution_versions=(self.execution_v1, self.execution_v2),
            results=(self.result,),
            events=(self.event,),
            event_types=(("platform.operation.succeeded", "1"),),
            correlation_refs=self.correlation,
            causation_refs=self.causation,
            provenance_refs=tuple(dict.fromkeys((
                self.actor_id,
                self.execution_id,
                self.workflow.subject_id,
                self.workflow.version_id,
                self.input.subject_id,
                self.input.version_id,
                self.contract.subject_id,
                self.contract.version_id,
                self.gate.subject_id,
                self.gate.version_id,
                self.execution_v1.subject_id,
                self.execution_v1.version_id,
                self.execution_v2.version_id,
                self.result.subject_id,
                self.result.version_id,
                self.event.subject_id,
                self.event.version_id,
            ))),
            product_contract=self.contract,
        )

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _pin(self, namespace: str, subject: str, version: str, semantic_type: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            subject_id=self._id(f"{namespace}-subject", subject),
            version_id=self._id(f"{namespace}-version", version),
            semantic_type=semantic_type,
            authority_scope=f"{semantic_type}/state",
            lifecycle_status="Retained",
        )

    def test_complete_view_is_derived_and_preserves_exact_references(self) -> None:
        view = reconstruct_audit_view(manifest=self.manifest, organization=self.organization)
        self.assertTrue(view.complete)
        self.assertEqual(view.execution_subject_id, self.execution_id)
        self.assertEqual(view.initiating_actor_id, self.actor_id)
        self.assertEqual(view.operation_name, "bounded-operation")
        self.assertEqual(
            {item.version_id for item in view.evidence},
            {
                self.workflow.version_id,
                self.input.version_id,
                self.contract.version_id,
                self.gate.version_id,
                self.execution_v1.version_id,
                self.execution_v2.version_id,
                self.result.version_id,
                self.event.version_id,
            },
        )
        self.assertFalse(hasattr(view, "authority_mode"))
        with self.assertRaises(FrozenInstanceError):
            view.complete = False

    def test_redacted_evidence_is_explicit_and_does_not_leak_source_pin(self) -> None:
        view = reconstruct_audit_view(
            manifest=self.manifest,
            organization=self.organization,
            dispositions=(
                EvidenceDisposition(
                    self.input.version_id,
                    EvidenceAvailability.REDACTED,
                    "reviewer is not permitted to view this classified input",
                ),
            ),
        )
        item = next(item for item in view.evidence if item.version_id == self.input.version_id)
        self.assertEqual(item.availability, EvidenceAvailability.REDACTED)
        self.assertIsNone(item.source)
        self.assertFalse(view.complete)

    def test_deleted_unavailable_and_missing_evidence_are_not_invented(self) -> None:
        view = reconstruct_audit_view(
            manifest=self.manifest,
            organization=self.organization,
            dispositions=(
                EvidenceDisposition(self.gate.version_id, EvidenceAvailability.DELETED, "lawful retention deletion"),
                EvidenceDisposition(self.result.version_id, EvidenceAvailability.UNAVAILABLE, "authoritative source unavailable"),
                EvidenceDisposition(self.event.version_id, EvidenceAvailability.MISSING, "required evidence reference cannot currently be resolved"),
            ),
        )
        states = {item.version_id: item.availability for item in view.evidence}
        self.assertEqual(states[self.gate.version_id], EvidenceAvailability.DELETED)
        self.assertEqual(states[self.result.version_id], EvidenceAvailability.UNAVAILABLE)
        self.assertEqual(states[self.event.version_id], EvidenceAvailability.MISSING)
        self.assertFalse(view.complete)
        for item in view.evidence:
            if item.availability is not EvidenceAvailability.AVAILABLE:
                self.assertIsNone(item.source)

    def test_wrong_organization_fails_closed(self) -> None:
        other = OrganizationScope(Identity("organization", "org-b", "platform"))
        with self.assertRaises(AuditReconstructionError):
            reconstruct_audit_view(manifest=self.manifest, organization=other)

    def test_unknown_or_duplicate_disposition_fails_closed(self) -> None:
        unknown = EvidenceDisposition(
            self._id("unknown-version", "unknown-v1"),
            EvidenceAvailability.MISSING,
            "not part of governed reconstruction",
        )
        with self.assertRaises(AuditReconstructionError):
            reconstruct_audit_view(
                manifest=self.manifest,
                organization=self.organization,
                dispositions=(unknown,),
            )
        disposition = EvidenceDisposition(
            self.event.version_id,
            EvidenceAvailability.MISSING,
            "missing",
        )
        with self.assertRaises(AuditReconstructionError):
            reconstruct_audit_view(
                manifest=self.manifest,
                organization=self.organization,
                dispositions=(disposition, disposition),
            )

    def test_non_available_disposition_requires_reason(self) -> None:
        with self.assertRaises(AuditReconstructionError):
            EvidenceDisposition(self.event.version_id, EvidenceAvailability.REDACTED)

    def test_export_preserves_reference_status_without_hidden_content(self) -> None:
        view = reconstruct_audit_view(
            manifest=self.manifest,
            organization=self.organization,
            dispositions=(
                EvidenceDisposition(
                    self.result.version_id,
                    EvidenceAvailability.REDACTED,
                    "bounded export redaction",
                ),
            ),
        )
        package = export_reconstruction_package(view)
        self.assertEqual(package.organization, self.organization)
        self.assertEqual(package.execution_subject_id, self.execution_id)
        self.assertEqual(package.correlation_refs, self.correlation)
        self.assertEqual(package.causation_refs, self.causation)
        self.assertFalse(package.complete)
        redacted = next(row for row in package.evidence if row[1] == self.result.version_id)
        self.assertEqual(redacted[2], EvidenceAvailability.REDACTED)
        self.assertEqual(redacted[3], "bounded export redaction")

    def test_reconstruction_is_read_only_and_never_replays_execution(self) -> None:
        before = self.manifest
        view = reconstruct_audit_view(manifest=self.manifest, organization=self.organization)
        export_reconstruction_package(view)
        self.assertIs(self.manifest, before)
        self.assertFalse(hasattr(view, "transition"))
        self.assertFalse(hasattr(view, "approve"))
        self.assertFalse(hasattr(view, "replay"))

    def test_exact_version_can_fill_multiple_reconstruction_roles(self) -> None:
        # P6.05 use case: same pin as material-input and result
        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.execution_id,
            initiating_actor_id=self.actor_id,
            operation_name="identity-preserving-admission",
            workflow=self.workflow,
            material_inputs=(self.result,), # REUSED PIN
            gate_decisions=(self.gate,),
            execution_versions=(self.execution_v1, self.execution_v2),
            results=(self.result,), # REUSED PIN
            events=(self.event,),
            event_types=(("platform.operation.succeeded", "1"),),
            correlation_refs=self.correlation,
            causation_refs=self.causation,
            provenance_refs=self.manifest.provenance_refs,
        )
        view = reconstruct_audit_view(manifest=manifest, organization=self.organization)
        self.assertTrue(view.complete)

        # Verify two role entries for one version ID
        matches = [item for item in view.evidence if item.version_id == self.result.version_id]
        self.assertEqual(len(matches), 2)
        roles = {item.role for item in matches}
        self.assertEqual(roles, {"material-input", "result"})
        for item in matches:
            self.assertEqual(item.source, self.result)
            self.assertEqual(item.availability, EvidenceAvailability.AVAILABLE)

    def test_shared_version_disposition_applies_to_every_role(self) -> None:
        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.execution_id,
            initiating_actor_id=self.actor_id,
            operation_name="identity-preserving-admission",
            workflow=self.workflow,
            material_inputs=(self.result,),
            gate_decisions=(self.gate,),
            execution_versions=(self.execution_v1, self.execution_v2),
            results=(self.result,),
            events=(self.event,),
            event_types=(("platform.operation.succeeded", "1"),),
            correlation_refs=self.correlation,
            causation_refs=self.causation,
            provenance_refs=self.manifest.provenance_refs,
        )
        # One disposition for the shared version ID
        dispositions = (
            EvidenceDisposition(self.result.version_id, EvidenceAvailability.REDACTED, "shared redaction"),
        )
        view = reconstruct_audit_view(manifest=manifest, organization=self.organization, dispositions=dispositions)
        self.assertFalse(view.complete)

        matches = [item for item in view.evidence if item.version_id == self.result.version_id]
        self.assertEqual(len(matches), 2)
        for item in matches:
            self.assertEqual(item.availability, EvidenceAvailability.REDACTED)
            self.assertIsNone(item.source)
            self.assertEqual(item.reason, "shared redaction")

    def test_cross_role_same_version_with_conflicting_pin_fails_closed(self) -> None:
        # Conflicting pin (different semantic_type)
        conflicting_result = self._pin("result", "result-a", "result-a-v1", "different.type")
        self.assertEqual(conflicting_result.version_id, self.result.version_id)
        self.assertNotEqual(conflicting_result, self.result)

        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.execution_id,
            initiating_actor_id=self.actor_id,
            operation_name="ambiguous-admission",
            workflow=self.workflow,
            material_inputs=(self.result,),
            gate_decisions=(self.gate,),
            execution_versions=(self.execution_v1, self.execution_v2),
            results=(conflicting_result,), # CONFLICT
            events=(self.event,),
            event_types=(("platform.operation.succeeded", "1"),),
            correlation_refs=self.correlation,
            causation_refs=self.causation,
            provenance_refs=self.manifest.provenance_refs,
        )
        with self.assertRaisesRegex(AuditReconstructionError, "ambiguous reused Version Identity"):
            reconstruct_audit_view(manifest=manifest, organization=self.organization)

    def test_export_preserves_role_multiplicity(self) -> None:
        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.execution_id,
            initiating_actor_id=self.actor_id,
            operation_name="identity-preserving-admission",
            workflow=self.workflow,
            material_inputs=(self.result,),
            gate_decisions=(self.gate,),
            execution_versions=(self.execution_v1, self.execution_v2),
            results=(self.result,),
            events=(self.event,),
            event_types=(("platform.operation.succeeded", "1"),),
            correlation_refs=self.correlation,
            causation_refs=self.causation,
            provenance_refs=self.manifest.provenance_refs,
        )
        view = reconstruct_audit_view(manifest=manifest, organization=self.organization)
        package = export_reconstruction_package(view)

        # Verify two rows in evidence export
        matches = [row for row in package.evidence if row[1] == self.result.version_id]
        self.assertEqual(len(matches), 2)
        roles = {row[0] for row in matches}
        self.assertEqual(roles, {"material-input", "result"})


if __name__ == "__main__":
    unittest.main()
