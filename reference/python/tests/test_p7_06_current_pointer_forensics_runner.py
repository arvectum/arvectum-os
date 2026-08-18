import unittest

import p7_06_current_pointer_forensics_runner as runner


class P706CurrentPointerForensicsRunnerTests(unittest.TestCase):
    def test_during_update_rollback_overrides_stable_shape(self):
        result = {
            "classification": "STABLE_AFTER_UPDATE",
            "status": "PASS",
            "update_exit_code": 0,
            "during_update_rollback_or_recovery_classification": "EXPLICIT_P7_06_ROLLBACK_EVIDENCE",
        }
        observed = runner._prioritize_explicit_evidence(result)
        self.assertEqual(observed["classification"], "EXPLICIT_P7_06_ROLLBACK_EVIDENCE")
        self.assertEqual(observed["status"], "OBSERVED")

    def test_during_update_recovery_overrides_unattributed_shape(self):
        result = {
            "classification": "UNATTRIBUTED_CURRENT_MUTATION",
            "status": "OBSERVED",
            "update_exit_code": 0,
            "during_update_rollback_or_recovery_classification": "EXPLICIT_P7_06_RECOVERY_EVIDENCE",
        }
        observed = runner._prioritize_explicit_evidence(result)
        self.assertEqual(observed["classification"], "EXPLICIT_P7_06_RECOVERY_EVIDENCE")

    def test_update_failure_keeps_failure_classification(self):
        result = {
            "classification": "UPDATE_COMMAND_FAILED",
            "status": "OBSERVED",
            "update_exit_code": 1,
            "during_update_rollback_or_recovery_classification": "EXPLICIT_P7_06_ROLLBACK_EVIDENCE",
        }
        observed = runner._prioritize_explicit_evidence(result)
        self.assertEqual(observed["classification"], "UPDATE_COMMAND_FAILED")

    def test_existing_explicit_after_command_classification_is_preserved(self):
        result = {
            "classification": "EXPLICIT_P7_06_ROLLBACK_EVIDENCE",
            "status": "OBSERVED",
            "update_exit_code": 0,
            "during_update_rollback_or_recovery_classification": "EXPLICIT_P7_06_RECOVERY_EVIDENCE",
        }
        observed = runner._prioritize_explicit_evidence(result)
        self.assertEqual(observed["classification"], "EXPLICIT_P7_06_ROLLBACK_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
