import ast
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from arvectum_os_ref.audit_reconstruction_support import EvidenceAvailability, EvidenceDisposition
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.event_provenance import CanonicalEvent, ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.provenance_inspection import (
    ProvenanceInspection,
    ProvenanceInspectionBlockedState,
    ProvenanceInspectionBlockCode,
    ProvenanceReferenceBasis,
    ReconstructionPresentationAuthority,
    ReplayPresentationMode,
    inspect_version_event_provenance,
    render_provenance_inspection_html,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


UTC = timezone.utc


class P404VersionEventProvenanceReconstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.execution_id = self._id("execution-subject", "execution-a")
        self.execution_v1 = self._execution_pin("execution-a-v1")
        self.execution_v2 = self._execution_pin("execution-a-v2")
        self.workflow = self._pin("workflow", "workflow-a", "workflow-a-v1", "platform.workflow")
        self.material = self._pin("subject", "input-a", "input-a-v1", "example.subject")
        self.gate = self._pin(
            "gate-decision", "authorization-a", "authorization-a-v1", "platform.authorization-decision"
        )
        self.result = self._pin("result", "result-a", "result-a-v1", "example.result")
        self.event_pin = self._pin("event", "event-a", "event-a-v1", "platform.event")
        self.manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=self.execution_id,
            initiating_actor_id=self.principal.principal_id,
            operation_name="update-subject",
            workflow=self.workflow,
            material_inputs=(self.material,),
            gate_decisions=(self.gate,),
            execution_versions=(self.execution_v1, self.execution_v2),
            results=(self.result,),
            events=(self.event_pin,),
            event_types=(("platform.canonical-mutation.succeeded", "1"),),
            correlation_refs=(self.execution_id,),
            causation_refs=(self.execution_v2.version_id,),
            provenance_refs=(
                self.principal.principal_id,
                self.execution_id,
                self.workflow.subject_id,
                self.workflow.version_id,
                self.material.subject_id,
                self.material.version_id,
                self.gate.subject_id,
                self.gate.version_id,
                self.execution_v1.version_id,
                self.execution_v2.version_id,
                self.result.subject_id,
                self.result.version_id,
                self.event_pin.subject_id,
                self.event_pin.version_id,
            ),
        )
        self.event = self._event()
        self.request = AccessRequest(
            actor=self.actor,
            purpose="audit-review",
            required_right="inspect-evidence",
            allowed_classifications=("internal",),
        )
        self.constraints = tuple(
            (version_id, "audit-review", ("inspect-evidence",), "internal")
            for version_id in self._evidence_version_ids()
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, "org-a")

    def _pin(
        self,
        namespace: str,
        subject_value: str,
        version_value: str,
        semantic_type: str,
    ) -> GovernedVersionPin:
        return GovernedVersionPin(
            subject_id=self._id(namespace, subject_value),
            version_id=self._id(f"{namespace}-version", version_value),
            semantic_type=semantic_type,
            authority_scope=f"{semantic_type}/state",
            lifecycle_status="Established",
        )

    def _execution_pin(self, version_value: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            subject_id=self.execution_id,
            version_id=self._id("execution-version", version_value),
            semantic_type="platform.execution-context",
            authority_scope="platform.execution-context/state",
            lifecycle_status="Succeeded",
        )

    def _evidence_version_ids(self) -> tuple[Identity, ...]:
        return (
            self.workflow.version_id,
            self.material.version_id,
            self.gate.version_id,
            self.execution_v1.version_id,
            self.execution_v2.version_id,
            self.result.version_id,
            self.event_pin.version_id,
        )

    def _event(self) -> CanonicalEvent:
        occurred_at = datetime(2026, 8, 8, 9, 5, tzinfo=UTC)
        recorded_at = datetime(2026, 8, 8, 9, 6, tzinfo=UTC)
        producer = Identity("principal", "event-producer", "platform")
        related_subjects = (self.result.subject_id,)
        related_versions = (self.result.version_id,)
        record = CanonicalRecord(
            subject_id=self.event_pin.subject_id,
            version_id=self.event_pin.version_id,
            semantic_type="platform.event",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=recorded_at,
            provenance_refs=(
                producer,
                self.principal.principal_id,
                self.execution_id,
                self.execution_v2.version_id,
                *related_subjects,
                *related_versions,
            ),
            integrity_metadata=(("representation", "p4.04-test"),),
            payload=(),
            lifecycle_status="Admitted",
            predecessor_version_id=None,
        )
        return CanonicalEvent(
            record=record,
            event_type="platform.canonical-mutation.succeeded",
            event_schema_version="1",
            authoritative_source="Arvectum OS",
            occurred_at=occurred_at,
            recorded_at=recorded_at,
            producer_id=producer,
            initiating_actor_id=self.principal.principal_id,
            execution_subject_id=self.execution_id,
            execution_version_id=self.execution_v2.version_id,
            related_subject_ids=related_subjects,
            related_version_ids=related_versions,
            correlation_refs=(self.execution_id,),
            causation_refs=(self.execution_v2.version_id,),
            classification="internal",
            access_scope="audit-review",
        )

    def _state(self, *, exact_version: Identity | None = None) -> WorkspaceShellState:
        opened = open_workspace_shell(self.actor)
        self.assertIsInstance(opened, WorkspaceShellState)
        reference = (
            SubjectNavigationReference(self.organization, self.execution_id)
            if exact_version is None
            else ExactVersionNavigationReference(self.organization, self.execution_id, exact_version)
        )
        return navigate_workspace(
            opened,
            destination=WorkspaceDestination.EVIDENCE,
            reference=reference,
        )

    def _authorization(
        self,
        *,
        actor: ActorContext | None = None,
        allowed: bool = True,
        decision_value: str = "allow-execution-a",
    ) -> CurrentSourceAuthorization:
        actual_actor = actor or self.actor
        return CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=actual_actor.actual_principal.principal_id,
            represented_principal_id=(
                None
                if actual_actor.represented_principal is None
                else actual_actor.represented_principal.principal_id
            ),
            resource_subject_id=self.execution_id,
            decision_version_id=self._id("authorization-decision-version", decision_value),
            allowed=allowed,
        )

    def _inspect(
        self,
        *,
        state: WorkspaceShellState | None = None,
        manifest: ReconstructionManifest | None = None,
        canonical_events: tuple[CanonicalEvent, ...] | None = None,
        constraints: tuple[tuple[Identity, str, tuple[str, ...], str], ...] | None = None,
        authorizations: tuple[CurrentSourceAuthorization, ...] | None = None,
        source_dispositions: tuple[EvidenceDisposition, ...] = (),
        request: AccessRequest | None = None,
    ):
        return inspect_version_event_provenance(
            state or self._state(),
            manifest=manifest or self.manifest,
            canonical_events=(self.event,) if canonical_events is None else canonical_events,
            access_request=request or self.request,
            evidence_constraints=self.constraints if constraints is None else constraints,
            authorizations=(self._authorization(),) if authorizations is None else authorizations,
            source_dispositions=source_dispositions,
        )

    def test_subject_reconstruction_exposes_exact_versions_and_canonical_event_history(self) -> None:
        result = self._inspect()
        self.assertIsInstance(result, ProvenanceInspection)
        self.assertEqual(result.reference_basis, ProvenanceReferenceBasis.EXECUTION_SUBJECT)
        self.assertIsNone(result.selected_execution_version_id)
        self.assertTrue(result.audit_view.complete)
        self.assertFalse(result.telemetry_included)
        self.assertEqual(result.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        self.assertEqual(
            result.reconstruction_authority,
            ReconstructionPresentationAuthority.DERIVED_NON_AUTHORITATIVE,
        )
        self.assertEqual(result.replay_mode, ReplayPresentationMode.PROJECTION_ONLY)
        self.assertEqual(tuple(item.version_id for item in result.events), (self.event_pin.version_id,))
        event = result.events[0]
        self.assertEqual(event.occurred_at_text, "2026-08-08T09:05:00+00:00")
        self.assertEqual(event.recorded_at_text, "2026-08-08T09:06:00+00:00")
        self.assertEqual(event.correlation_refs, (self.execution_id,))
        self.assertEqual(event.causation_refs, (self.execution_v2.version_id,))
        self.assertEqual(event.authoritative_source, "Arvectum OS")

    def test_exact_execution_version_selection_is_preserved(self) -> None:
        result = self._inspect(state=self._state(exact_version=self.execution_v1.version_id))
        self.assertIsInstance(result, ProvenanceInspection)
        self.assertEqual(result.reference_basis, ProvenanceReferenceBasis.EXACT_EXECUTION_VERSION)
        self.assertEqual(result.selected_execution_version_id, self.execution_v1.version_id)
        versions = {item.version_id for item in result.audit_view.evidence}
        self.assertIn(self.execution_v1.version_id, versions)
        self.assertIn(self.execution_v2.version_id, versions)

    def test_unknown_exact_version_fails_without_fallback_after_evidence_access(self) -> None:
        unknown = self._id("execution-version", "unknown")
        result = self._inspect(state=self._state(exact_version=unknown))
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.VERSION_UNAVAILABLE)
        self.assertNotIn(self.execution_v2.version_id.value, result.status_text)

    def test_source_authorization_precedes_exact_version_existence_disclosure(self) -> None:
        unknown = self._id("execution-version", "protected-question")
        result = self._inspect(state=self._state(exact_version=unknown), authorizations=())
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.ACCESS_DENIED)
        self.assertNotEqual(result.code, ProvenanceInspectionBlockCode.VERSION_UNAVAILABLE)
        self.assertNotIn(unknown.value, result.status_text)

    def test_p3_07_evidence_enforcement_precedes_exact_version_existence_disclosure(self) -> None:
        unknown = self._id("execution-version", "protected-after-source-auth")
        result = self._inspect(
            state=self._state(exact_version=unknown),
            constraints=self.constraints[:-1],
        )
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT)
        self.assertNotEqual(result.code, ProvenanceInspectionBlockCode.VERSION_UNAVAILABLE)
        self.assertNotIn(unknown.value, result.status_text)

    def test_access_request_actor_mismatch_precedes_exact_version_existence_disclosure(self) -> None:
        unknown = self._id("execution-version", "protected-actor-context")
        other_actor = ActorContext(
            Principal(Identity("principal", "operator-2", "platform")),
            self.organization,
        )
        wrong_request = AccessRequest(
            actor=other_actor,
            purpose=self.request.purpose,
            required_right=self.request.required_right,
            allowed_classifications=self.request.allowed_classifications,
        )
        result = self._inspect(
            state=self._state(exact_version=unknown),
            request=wrong_request,
        )
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.ACCESS_DENIED)
        self.assertNotIn(unknown.value, result.status_text)

    def test_authorization_is_actor_bound_and_duplicate_decisions_fail_closed(self) -> None:
        other_actor = ActorContext(
            Principal(Identity("principal", "operator-2", "platform")),
            self.organization,
        )
        wrong_actor = self._inspect(authorizations=(self._authorization(actor=other_actor),))
        duplicate = self._inspect(
            authorizations=(
                self._authorization(decision_value="allow-a"),
                self._authorization(decision_value="allow-b"),
            )
        )
        denied = self._inspect(authorizations=(self._authorization(allowed=False),))
        for result in (wrong_actor, duplicate, denied):
            with self.subTest(result=result):
                self.assertIsInstance(result, ProvenanceInspectionBlockedState)
                self.assertEqual(result.code, ProvenanceInspectionBlockCode.ACCESS_DENIED)
                self.assertFalse(result.governed_content_visible)

    def test_every_exact_evidence_version_requires_current_constraints(self) -> None:
        result = self._inspect(constraints=self.constraints[:-1])
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT)
        self.assertFalse(result.governed_content_visible)

    def test_classification_denial_redacts_event_metadata_and_marks_reconstruction_incomplete(self) -> None:
        constraints = tuple(
            (
                version_id,
                purpose,
                rights,
                "restricted" if version_id == self.event_pin.version_id else classification,
            )
            for version_id, purpose, rights, classification in self.constraints
        )
        result = self._inspect(constraints=constraints, canonical_events=())
        self.assertIsInstance(result, ProvenanceInspection)
        self.assertFalse(result.audit_view.complete)
        self.assertEqual(result.events, ())
        event_evidence = tuple(item for item in result.audit_view.evidence if item.role == "event")
        self.assertEqual(event_evidence[0].availability, EvidenceAvailability.REDACTED)

    def test_lawful_deletion_gap_is_shown_without_fabricating_event_history(self) -> None:
        deletion = EvidenceDisposition(
            version_id=self.event_pin.version_id,
            availability=EvidenceAvailability.DELETED,
            reason="payload removed under applicable retention/deletion policy",
        )
        result = self._inspect(source_dispositions=(deletion,), canonical_events=())
        self.assertIsInstance(result, ProvenanceInspection)
        self.assertFalse(result.audit_view.complete)
        self.assertEqual(result.events, ())
        html = render_provenance_inspection_html(result)
        self.assertIn("Deleted", html)
        self.assertIn("retention/deletion policy", html)
        self.assertIn("does not infer or fabricate missing history", html)

    def test_missing_non_event_evidence_reduces_claim_but_keeps_visible_event(self) -> None:
        missing = EvidenceDisposition(
            version_id=self.result.version_id,
            availability=EvidenceAvailability.MISSING,
            reason="historical result evidence is not available",
        )
        result = self._inspect(source_dispositions=(missing,))
        self.assertIsInstance(result, ProvenanceInspection)
        self.assertFalse(result.audit_view.complete)
        self.assertEqual(len(result.events), 1)
        html = render_provenance_inspection_html(result)
        self.assertIn("Incomplete", html)
        self.assertIn("historical result evidence is not available", html)

    def test_unavailable_evidence_can_express_uncertainty_without_inventing_history(self) -> None:
        unavailable = EvidenceDisposition(
            version_id=self.result.version_id,
            availability=EvidenceAvailability.UNAVAILABLE,
            reason="external outcome remains uncertain pending reconciliation evidence",
        )
        result = self._inspect(source_dispositions=(unavailable,))
        self.assertIsInstance(result, ProvenanceInspection)
        self.assertFalse(result.audit_view.complete)
        html = render_provenance_inspection_html(result)
        self.assertIn("uncertain pending reconciliation evidence", html)
        self.assertIn("uncertainty", html)

    def test_access_redaction_dominates_more_specific_source_disposition(self) -> None:
        constraints = tuple(
            (
                version_id,
                purpose,
                rights,
                "restricted" if version_id == self.event_pin.version_id else classification,
            )
            for version_id, purpose, rights, classification in self.constraints
        )
        deletion = EvidenceDisposition(
            version_id=self.event_pin.version_id,
            availability=EvidenceAvailability.DELETED,
            reason="sensitive deletion detail that must not cross denied access",
        )
        result = self._inspect(
            constraints=constraints,
            source_dispositions=(deletion,),
            canonical_events=(),
        )
        self.assertIsInstance(result, ProvenanceInspection)
        event_item = tuple(item for item in result.audit_view.evidence if item.role == "event")[0]
        self.assertEqual(event_item.availability, EvidenceAvailability.REDACTED)
        self.assertNotIn("sensitive deletion detail", event_item.reason or "")
        self.assertNotIn("sensitive deletion detail", render_provenance_inspection_html(result))

    def test_unknown_source_disposition_fails_closed(self) -> None:
        unknown = EvidenceDisposition(
            version_id=self._id("evidence-version", "unknown"),
            availability=EvidenceAvailability.UNAVAILABLE,
            reason="not part of reconstruction",
        )
        result = self._inspect(source_dispositions=(unknown,))
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT)

    def test_event_source_must_match_exact_visible_manifest_versions(self) -> None:
        missing_event = self._inspect(canonical_events=())
        extra_event = replace(
            self.event,
            record=replace(
                self.event.record,
                subject_id=self._id("event", "event-extra"),
                version_id=self._id("event-version", "event-extra-v1"),
            ),
        )
        extra = self._inspect(canonical_events=(self.event, extra_event))
        for result in (missing_event, extra):
            with self.subTest(result=result):
                self.assertIsInstance(result, ProvenanceInspectionBlockedState)
                self.assertEqual(result.code, ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT)

    def test_event_type_schema_drift_is_not_silently_reinterpreted(self) -> None:
        changed = replace(self.event, event_type="platform.changed-meaning")
        result = self._inspect(canonical_events=(changed,))
        self.assertIsInstance(result, ProvenanceInspectionBlockedState)
        self.assertEqual(result.code, ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT)

    def test_renderer_labels_event_telemetry_correlation_causation_and_replay_boundaries(self) -> None:
        result = self._inspect()
        self.assertIsInstance(result, ProvenanceInspection)
        html = render_provenance_inspection_html(result)
        self.assertIn("Canonical Event history", html)
        self.assertIn("raw logs, metrics, traces", html)
        self.assertIn("Occurrence time and recording/admission time are distinct", html)
        self.assertIn("Correlation is not causation", html)
        self.assertIn("Derived, read-only, non-authoritative reconstruction", html)
        self.assertIn("No replay is executed by this view", html)
        self.assertIn("new Governed Execution", html)
        self.assertIn("never becomes a source of truth", html)
        self.assertIn("Producer", html)
        self.assertIn("Authority", html)
        self.assertIn("Related exact Version references", html)

    def test_renderer_escapes_governed_text(self) -> None:
        manifest = replace(self.manifest, operation_name="<script>alert('x')</script>")
        result = self._inspect(manifest=manifest)
        self.assertIsInstance(result, ProvenanceInspection)
        html = render_provenance_inspection_html(result)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_presentation_has_no_mutation_replay_or_telemetry_authority_surface(self) -> None:
        result = self._inspect()
        self.assertIsInstance(result, ProvenanceInspection)
        for name in (
            "mutate",
            "approve",
            "authorize",
            "admit_event",
            "execute_replay",
            "logs",
            "metrics",
            "traces",
        ):
            self.assertFalse(hasattr(result, name), name)

    def test_module_stays_internal_and_does_not_select_delivery_or_frontend_infrastructure(self) -> None:
        module_path = Path(__file__).parents[1] / "arvectum_os_ref" / "provenance_inspection.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imported = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            (node.module or "").split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.level == 0
        )
        forbidden = {
            "fastapi",
            "flask",
            "django",
            "sqlalchemy",
            "requests",
            "kafka",
            "opentelemetry",
            "sqlite3",
            "subprocess",
        }
        self.assertTrue(imported.isdisjoint(forbidden), imported & forbidden)
        source = module_path.read_text(encoding="utf-8")
        self.assertNotIn("def admit_event", source)
        self.assertNotIn("def transition_governed_execution", source)
        self.assertNotIn("def rebuild_non_authoritative_projection", source)


if __name__ == "__main__":
    unittest.main()
