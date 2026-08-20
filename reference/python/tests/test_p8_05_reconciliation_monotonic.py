from datetime import UTC, datetime
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    RetrySemantics,
    RuntimeConsistencyState,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from p8_05_external_boundary_evidence import (
    ExternalEffectLedger,
    ExternalReconciliation,
    ReconciliationResolution,
    RetryAfterReconciliationNotAllowedError,
    require_retry_allowed_after_reconciliation,
)


class P805ReconciliationMonotonicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = "org-a"
        self.organization = OrganizationScope(Identity("organization", self.scope, "platform"))
        self.principal = Principal(Identity("principal", "operator", self.scope))
        self.actor = ActorContext(self.principal, self.organization)
        self.attempt = ConsequentialAttempt(
            execution_subject_id=self._id("execution-subject", "original"),
            execution_version_id=self._id("execution-version", "original-v4"),
            operation_name="external-apply",
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="effect-1",
            fingerprint=("external-apply", "target-a", "effect-1"),
            outcome=ConsequentialOutcome.UNCERTAIN,
        )
        base = CanonicalRecord(
            subject_id=self._id("canonical-subject", "base"),
            version_id=self._id("canonical-version", "base-v1"),
            semantic_type="platform.p8-05-test-base",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.p8-05/test",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 20, 8, 0, tzinfo=UTC),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "synthetic-bounded-test"),),
            lifecycle_status="Active",
        )
        self.state = RuntimeConsistencyState(
            canonical_records=(base,),
            attempts=(self.attempt,),
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.scope)

    def _reconciliation(
        self,
        suffix: str,
        resolution: ReconciliationResolution,
        minute: int,
    ) -> ExternalReconciliation:
        return ExternalReconciliation(
            reconciliation_id=self._id("reconciliation-subject", suffix),
            version_id=self._id("reconciliation-version", f"{suffix}-v1"),
            organization=self.organization,
            uncertain_attempt_fingerprint=self.attempt.fingerprint,
            uncertain_retry_token="effect-1",
            original_execution_subject_id=self.attempt.execution_subject_id,
            original_execution_version_id=self.attempt.execution_version_id,
            reconciliation_execution_subject_id=self._id("execution-subject", f"reconcile-{suffix}"),
            reconciliation_execution_version_id=self._id("execution-version", f"reconcile-{suffix}-v4"),
            evidence_ref=self._id("evidence", f"{suffix}-evidence"),
            resolution=resolution,
            resolved_at=datetime(2026, 8, 20, 8, minute, tzinfo=UTC),
        )

    def test_confirmed_success_cannot_be_overridden_by_later_not_applied_observation(self) -> None:
        confirmed = self._reconciliation(
            "confirmed-success",
            ReconciliationResolution.CONFIRMED_SUCCEEDED,
            30,
        )
        contradictory_later = self._reconciliation(
            "later-not-applied",
            ReconciliationResolution.CONFIRMED_NOT_APPLIED,
            31,
        )
        ledger = ExternalEffectLedger(
            runtime_state=self.state,
            reconciliations=(confirmed, contradictory_later),
        )

        with self.assertRaises(RetryAfterReconciliationNotAllowedError):
            require_retry_allowed_after_reconciliation(ledger, self.attempt)


if __name__ == "__main__":
    unittest.main()
