from __future__ import annotations

import inspect
import unittest
from datetime import datetime, timezone

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.governed_interaction_runtime_outcomes import (
    ObservedConsequentialState,
    inspect_consequential_outcome_evidence,
    render_consequential_outcome_evidence_html,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    RetrySemantics,
    RuntimeConsistencyState,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass

import p7_06_ui2_governed_interaction as ui2


UTC = timezone.utc


class P706UI2RuntimeOutcomeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-ui2-outcome", "platform"))
        self.principal = Principal(Identity("principal", "owner-ui2-outcome", "org-ui2-outcome"))
        self.actor = ActorContext(self.principal, self.organization)
        self.record = CanonicalRecord(
            subject_id=self._id("canonical-subject", "target"),
            version_id=self._id("canonical-version", "target-v1"),
            semantic_type="example.target",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="example.target/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 18, 15, 0, tzinfo=UTC),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "ui2-outcome-test"),),
            payload=(("state", "v1"),),
            lifecycle_status="Established",
            predecessor_version_id=None,
        )
        self.execution_subject = self._id("execution-subject", "execution")
        self.execution_version = self._id("execution-version", "execution-v4")

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.organization.organization_id.value)

    def _attempt(
        self,
        outcome: ConsequentialOutcome,
        *,
        execution_subject_id: Identity | None = None,
        execution_version_id: Identity | None = None,
        token: str = "ui2-outcome-token",
    ) -> ConsequentialAttempt:
        return ConsequentialAttempt(
            execution_subject_id=execution_subject_id or self.execution_subject,
            execution_version_id=execution_version_id or self.execution_version,
            operation_name="update-target",
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token=token,
            fingerprint=("ui2", "outcome", token),
            outcome=outcome,
        )

    def _state(self, outcome: ConsequentialOutcome) -> RuntimeConsistencyState:
        return RuntimeConsistencyState(
            canonical_records=(self.record,),
            attempts=(self._attempt(outcome),),
        )

    def _inspect(self, state: RuntimeConsistencyState):
        return inspect_consequential_outcome_evidence(
            state,
            execution_subject_id=self.execution_subject,
        )

    def test_uncertain_is_rendered_as_observed_uncertain_and_separate_reconciliation_requirement(self) -> None:
        evidence = self._inspect(self._state(ConsequentialOutcome.UNCERTAIN))
        self.assertEqual(evidence.state, ObservedConsequentialState.UNCERTAIN)
        self.assertTrue(evidence.reconciliation_required)
        html = render_consequential_outcome_evidence_html(evidence)
        self.assertIn("Observed governed outcome: <strong>Uncertain</strong>", html)
        self.assertIn("<strong>Reconciliation required.</strong>", html)
        self.assertIn("does not rewrite uncertainty as success/failure", html)
        self.assertIn("does not permit a blind retry", html)

    def test_succeeded_attempt_does_not_infer_reconciliation(self) -> None:
        evidence = self._inspect(self._state(ConsequentialOutcome.SUCCEEDED))
        self.assertEqual(evidence.state, ObservedConsequentialState.SUCCEEDED)
        self.assertFalse(evidence.reconciliation_required)
        html = render_consequential_outcome_evidence_html(evidence)
        self.assertIn("Succeeded", html)
        self.assertNotIn("<strong>Reconciliation required.</strong>", html)

    def test_no_attempt_is_explicit_and_does_not_manufacture_execution_identity(self) -> None:
        evidence = self._inspect(RuntimeConsistencyState(canonical_records=(self.record,)))
        self.assertEqual(evidence.state, ObservedConsequentialState.NONE)
        self.assertIsNone(evidence.execution_subject_id)
        self.assertIsNone(evidence.execution_version_id)
        html = render_consequential_outcome_evidence_html(evidence)
        self.assertIn("No prior consequential attempt", html)
        self.assertNotIn(self.execution_version.value, html)

    def test_unrelated_newer_execution_attempt_is_not_projected_into_current_execution(self) -> None:
        unrelated_subject = self._id("execution-subject", "unrelated-execution")
        unrelated_version = self._id("execution-version", "unrelated-execution-v9")
        state = RuntimeConsistencyState(
            canonical_records=(self.record,),
            attempts=(
                self._attempt(ConsequentialOutcome.UNCERTAIN),
                self._attempt(
                    ConsequentialOutcome.SUCCEEDED,
                    execution_subject_id=unrelated_subject,
                    execution_version_id=unrelated_version,
                    token="unrelated-token",
                ),
            ),
        )
        evidence = self._inspect(state)
        self.assertEqual(evidence.state, ObservedConsequentialState.UNCERTAIN)
        self.assertEqual(evidence.execution_subject_id, self.execution_subject)
        self.assertNotEqual(evidence.execution_subject_id, unrelated_subject)
        html = render_consequential_outcome_evidence_html(evidence)
        self.assertNotIn(unrelated_version.value, html)

    def test_http_adapter_renders_runtime_outcome_evidence_from_related_execution(self) -> None:
        source = inspect.getsource(ui2)
        self.assertIn("inspect_consequential_outcome_evidence", source)
        self.assertIn("render_consequential_outcome_evidence_html", source)
        self.assertIn("result.runtime_state", source)
        self.assertIn("execution_subject_id", source)


if __name__ == "__main__":
    unittest.main()
