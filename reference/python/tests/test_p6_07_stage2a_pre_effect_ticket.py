from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from p6_07_discount_parser_ref.contract import P6_06_CANONICAL_BLOB_SHA
from p6_07_discount_parser_ref.stage2a import (
    DIGEST_FILENAME,
    OPERATION_NAME,
    TICKET_FILENAME,
    Stage2ATicketError,
    build_stage2a_ticket,
    serialize_ticket,
    ticket_sha256,
    verify_stage2a_evidence,
    write_stage2a_evidence,
)


UTC = timezone.utc
REPO_SHA = "ca58ef7a40febdc88dd441077ce7f16ccb344713"


class P607Stage2APreEffectTicketTests(unittest.TestCase):
    def _ticket(self):
        return build_stage2a_ticket(
            organization_id="org/arvectum-internal",
            actor_id="principal/owner-operator",
            canonical_repo_sha=REPO_SHA,
            created_at=datetime(2026, 8, 17, 5, 30, tzinfo=UTC),
            execution_id="p6-07-stage2-test-execution",
        )

    def test_ticket_pins_exact_contract_and_human_operator_boundary(self):
        ticket = self._ticket()
        self.assertEqual(ticket["stage"], "P6.07 Stage 2A")
        self.assertEqual(ticket["status"], "pre-effect-intent-recorded")
        self.assertEqual(ticket["organization"]["organization_id"], "org/arvectum-internal")
        self.assertFalse(ticket["organization"]["ambient_default_permitted"])
        self.assertEqual(ticket["actor"]["principal_id"], "principal/owner-operator")
        self.assertEqual(ticket["actor"]["kind"], "human")
        self.assertTrue(ticket["actor"]["attributable"])
        self.assertEqual(ticket["operation"]["name"], OPERATION_NAME)
        self.assertEqual(ticket["operation"]["max_external_sends"], 1)
        self.assertFalse(ticket["operation"]["scheduler_autopost_permitted"])
        self.assertEqual(ticket["product_contract"]["version"], "0.1.0")
        self.assertEqual(ticket["product_contract"]["blob_sha"], P6_06_CANONICAL_BLOB_SHA)
        self.assertEqual(ticket["product_contract"]["shared_dependencies"], ["CAP-004"])

    def test_ticket_does_not_grant_real_action_authorization(self):
        ticket = self._ticket()
        governance = ticket["governance"]
        self.assertFalse(governance["product_contract_is_authorization"])
        self.assertFalse(governance["ticket_is_authorization"])
        self.assertTrue(governance["explicit_real_action_authorization_required_before_stage2b_send"])
        self.assertTrue(ticket["stage2b_handoff"]["must_record_explicit_real_action_authorization_before_send"])

    def test_stage2b_handoff_requires_product_pre_effect_evidence_and_no_blind_retry(self):
        handoff = self._ticket()["stage2b_handoff"]
        self.assertTrue(handoff["must_bind_exact_ticket_sha256"])
        self.assertTrue(handoff["must_record_candidate_and_target_before_send"])
        self.assertTrue(handoff["must_record_product_pre_effect_reservation_and_intent_before_send"])
        self.assertTrue(handoff["must_perform_at_most_one_external_send"])
        self.assertTrue(handoff["must_not_enable_scheduler_or_autopost"])
        self.assertTrue(handoff["must_not_blind_retry_uncertain_external_outcome"])

    def test_ticket_contains_no_product_candidate_target_or_secret_payload(self):
        payload = serialize_ticket(self._ticket()).decode("utf-8")
        parsed = json.loads(payload)
        self.assertNotIn("publication_candidate", parsed)
        self.assertNotIn("telegram_target", parsed)
        lowered = payload.lower()
        self.assertNotIn("bot_token", lowered)
        self.assertNotIn("api_token", lowered)
        self.assertNotIn("telegram_token", lowered)
        self.assertFalse(parsed["containment"]["reusable_secrets"])
        self.assertFalse(parsed["containment"]["telegram_call"])
        self.assertFalse(parsed["containment"]["network_access"])

    def test_write_is_immutable_and_hash_verifies(self):
        ticket = self._ticket()
        with tempfile.TemporaryDirectory() as temp_dir:
            ticket_path, digest_path, digest = write_stage2a_evidence(
                output_dir=Path(temp_dir),
                ticket=ticket,
            )
            self.assertEqual(ticket_path.name, TICKET_FILENAME)
            self.assertEqual(digest_path.name, DIGEST_FILENAME)
            self.assertEqual(digest, ticket_sha256(ticket_path.read_bytes()))
            self.assertTrue(verify_stage2a_evidence(ticket_path=ticket_path, digest_path=digest_path))
            with self.assertRaises(Stage2ATicketError):
                write_stage2a_evidence(output_dir=Path(temp_dir), ticket=ticket)

    def test_tamper_breaks_digest_verification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            ticket_path, digest_path, _ = write_stage2a_evidence(
                output_dir=Path(temp_dir),
                ticket=self._ticket(),
            )
            ticket_path.write_bytes(ticket_path.read_bytes() + b" ")
            self.assertFalse(verify_stage2a_evidence(ticket_path=ticket_path, digest_path=digest_path))

    def test_rejects_ambient_or_unattributable_inputs_and_noncanonical_sha(self):
        common = dict(created_at=datetime(2026, 8, 17, 5, 30, tzinfo=UTC))
        with self.assertRaises(Stage2ATicketError):
            build_stage2a_ticket(
                organization_id="",
                actor_id="principal/operator",
                canonical_repo_sha=REPO_SHA,
                **common,
            )
        with self.assertRaises(Stage2ATicketError):
            build_stage2a_ticket(
                organization_id="org/arvectum",
                actor_id="",
                canonical_repo_sha=REPO_SHA,
                **common,
            )
        with self.assertRaises(Stage2ATicketError):
            build_stage2a_ticket(
                organization_id="org/arvectum",
                actor_id="principal/operator",
                canonical_repo_sha="main",
                **common,
            )

    def test_rejects_naive_time(self):
        with self.assertRaises(Stage2ATicketError):
            build_stage2a_ticket(
                organization_id="org/arvectum",
                actor_id="principal/operator",
                canonical_repo_sha=REPO_SHA,
                created_at=datetime(2026, 8, 17, 5, 30),
            )


if __name__ == "__main__":
    unittest.main()
