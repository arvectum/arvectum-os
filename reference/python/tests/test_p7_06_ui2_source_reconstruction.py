from __future__ import annotations

import inspect
import unittest
from datetime import datetime, timezone

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_interaction_reconstruction import (
    SourceReconstructionState,
    build_source_reconstruction_view,
    render_source_reconstruction_html,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal

import p7_06_ui2_governed_interaction as ui2


UTC = timezone.utc


class P706UI2SourceReconstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-ui2-recon", "platform"))
        self.principal = Principal(Identity("principal", "owner-ui2-recon", "org-ui2-recon"))
        self.actor = ActorContext(self.principal, self.organization)
        self.historical_execution_subject = self._id("execution-subject", "historical-execution")
        self.historical_execution_v1 = self._id("execution-version", "historical-execution-v1")
        self.historical_execution_v2 = self._id("execution-version", "historical-execution-v2")
        self.source = CanonicalRecord(
            subject_id=self._id("canonical-subject", "source"),
            version_id=self._id("canonical-version", "source-v2"),
            semantic_type="example.source",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="example.source/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 18, 14, 0, tzinfo=UTC),
            provenance_refs=(
                self.principal.principal_id,
                self.historical_execution_subject,
                self.historical_execution_v2,
            ),
            integrity_metadata=(("representation", "ui2-reconstruction-test"),),
            payload=(("state", "governed-result"),),
            lifecycle_status="Established",
            predecessor_version_id=None,
        )
        self.manifest = self._manifest(self.source)

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.organization.organization_id.value)

    def _pin(
        self,
        namespace: str,
        subject: str,
        version_namespace: str,
        version: str,
        semantic_type: str,
        authority_scope: str,
        lifecycle: str | None = None,
    ) -> GovernedVersionPin:
        return GovernedVersionPin(
            subject_id=self._id(namespace, subject),
            version_id=self._id(version_namespace, version),
            semantic_type=semantic_type,
            authority_scope=authority_scope,
            lifecycle_status=lifecycle,
        )

    def _manifest(self, source: CanonicalRecord) -> ReconstructionManifest:
        workflow = self._pin(
            "workflow-subject",
            "historical-workflow",
            "workflow-version",
            "historical-workflow-v1",
            "platform.workflow",
            "platform.workflow/definition",
            "Approved",
        )
        material = self._pin(
            "canonical-subject",
            "source-v1-subject",
            "canonical-version",
            "source-v1",
            "example.source",
            "example.source/state",
            "Established",
        )
        execution_v1 = GovernedVersionPin(
            subject_id=self.historical_execution_subject,
            version_id=self.historical_execution_v1,
            semantic_type="platform.execution-context",
            authority_scope="platform.governed-execution/context",
            lifecycle_status="Created",
        )
        execution_v2 = GovernedVersionPin(
            subject_id=self.historical_execution_subject,
            version_id=self.historical_execution_v2,
            semantic_type="platform.execution-context",
            authority_scope="platform.governed-execution/context",
            lifecycle_status="Succeeded",
        )
        result = GovernedVersionPin.from_record(source)
        event_subject = self._id("event-subject", "historical-event")
        event_version = self._id("event-version", "historical-event-v1")
        event = GovernedVersionPin(
            subject_id=event_subject,
            version_id=event_version,
            semantic_type="platform.event",
            authority_scope="platform.event/governed-outcome",
            lifecycle_status="Admitted",
        )
        return ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.historical_execution_subject,
            initiating_actor_id=self.principal.principal_id,
            operation_name="produce-governed-source",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution_v1, execution_v2),
            results=(result,),
            events=(event,),
            event_types=(("platform.canonical-mutation.succeeded", "1"),),
            correlation_refs=(self.historical_execution_subject,),
            causation_refs=(self.historical_execution_v2,),
            provenance_refs=(
                self.principal.principal_id,
                self.historical_execution_subject,
                workflow.subject_id,
                workflow.version_id,
                source.subject_id,
                source.version_id,
                event_subject,
                event_version,
            ),
        )

    def test_exact_rfc0006_manifest_is_bound_to_source_and_rendered_without_replay_claim(self) -> None:
        view = build_source_reconstruction_view(
            organization=self.organization,
            source_record=self.source,
            manifest=self.manifest,
        )
        self.assertEqual(view.state, SourceReconstructionState.AVAILABLE)
        self.assertEqual(view.source_subject_id, self.source.subject_id)
        self.assertEqual(view.source_version_id, self.source.version_id)
        self.assertEqual(view.execution_subject_id, self.historical_execution_subject)
        self.assertEqual(view.execution_version_id, self.historical_execution_v2)
        html = render_source_reconstruction_html(view)
        self.assertIn('data-source-reconstruction="available"', html)
        self.assertIn(self.source.version_id.value, html)
        self.assertIn(self.historical_execution_v2.value, html)
        self.assertIn("platform.canonical-mutation.succeeded", html)
        self.assertIn("never repeats an external or consequential effect", html)

    def test_absent_manifest_is_truthfully_unavailable_and_does_not_infer_current_action(self) -> None:
        view = build_source_reconstruction_view(
            organization=self.organization,
            source_record=self.source,
            manifest=None,
        )
        self.assertEqual(view.state, SourceReconstructionState.UNAVAILABLE)
        html = render_source_reconstruction_html(view)
        self.assertIn('data-source-reconstruction="unavailable"', html)
        self.assertIn("does not infer one from the current action", html)
        self.assertNotIn(self.historical_execution_v2.value, html)

    def test_manifest_for_different_exact_result_version_is_rejected(self) -> None:
        other = CanonicalRecord(
            subject_id=self.source.subject_id,
            version_id=self._id("canonical-version", "source-v3"),
            semantic_type=self.source.semantic_type,
            schema_version=self.source.schema_version,
            organization=self.organization,
            authority_mode=self.source.authority_mode,
            authority_scope=self.source.authority_scope,
            accountable_owner_id=self.source.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self.source.created_at,
            provenance_refs=self.source.provenance_refs,
            integrity_metadata=self.source.integrity_metadata,
            payload=self.source.payload,
            lifecycle_status=self.source.lifecycle_status,
            predecessor_version_id=self.source.version_id,
        )
        wrong_manifest = self._manifest(other)
        with self.assertRaisesRegex(ValueError, "exact inspected source Version"):
            build_source_reconstruction_view(
                organization=self.organization,
                source_record=self.source,
                manifest=wrong_manifest,
            )

    def test_manifest_without_source_provenance_to_reconstructed_execution_is_rejected(self) -> None:
        unlinked_source = CanonicalRecord(
            subject_id=self.source.subject_id,
            version_id=self.source.version_id,
            semantic_type=self.source.semantic_type,
            schema_version=self.source.schema_version,
            organization=self.organization,
            authority_mode=self.source.authority_mode,
            authority_scope=self.source.authority_scope,
            accountable_owner_id=self.source.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self.source.created_at,
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=self.source.integrity_metadata,
            payload=self.source.payload,
            lifecycle_status=self.source.lifecycle_status,
            predecessor_version_id=self.source.predecessor_version_id,
        )
        with self.assertRaisesRegex(ValueError, "provenance"):
            build_source_reconstruction_view(
                organization=self.organization,
                source_record=unlinked_source,
                manifest=self.manifest,
            )

    def test_http_adapter_has_separate_trusted_reconstruction_provider_not_browser_field(self) -> None:
        signature = inspect.signature(ui2.make_server)
        self.assertIn("reconstruction_provider", signature.parameters)
        source = inspect.getsource(ui2)
        self.assertIn("build_source_reconstruction_view", source)
        self.assertIn("render_source_reconstruction_html", source)
        self.assertNotIn('"reconstruction"}', source)
        self.assertIn(
            'set(values) != {"interaction_id", "csrf"}',
            source,
        )


if __name__ == "__main__":
    unittest.main()
