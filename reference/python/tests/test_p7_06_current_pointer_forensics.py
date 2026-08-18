import json
import tempfile
import unittest
from pathlib import Path

import p7_06_current_pointer_forensics as f


class P706CurrentPointerForensicsTests(unittest.TestCase):
    def test_validate_sha(self):
        value = "a" * 40
        self.assertEqual(f._validate_sha(value), value)
        with self.assertRaises(f.ForensicsError):
            f._validate_sha("abc")

    def test_inventory_and_new_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base = root / "evidence" / "p7-06" / "work-1"
            base.mkdir(parents=True)
            path = base / "transaction-payload.json"
            path.write_text('{"result":"PASS"}\n', encoding="utf-8")
            before = f._inventory_p706_evidence(root)
            self.assertIn("work-1/transaction-payload.json", before)
            path.write_text('{"result":"ROLLED_BACK"}\n', encoding="utf-8")
            after = f._inventory_p706_evidence(root)
            changed = f._new_evidence(before, after)
            self.assertEqual([x.relative_path for x in changed], ["work-1/transaction-payload.json"])

    def test_classifies_explicit_rollback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base = root / "evidence" / "p7-06" / "work-1"
            base.mkdir(parents=True)
            path = base / "rollback-payload-20260819T000000Z.json"
            path.write_text(json.dumps({"result":"ROLLED_BACK","source_release":"a"*40,"target_release":"b"*40,"rollback_disposition":"executed"}), encoding="utf-8")
            inventory = f._inventory_p706_evidence(root)
            classification, facts = f._classify_evidence(root, inventory.values())
            self.assertEqual(classification, "EXPLICIT_P7_06_ROLLBACK_EVIDENCE")
            self.assertEqual(facts[0]["kind"], "rollback")

    def test_classifies_interrupted_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base = root / "evidence" / "p7-06" / "work-1"
            base.mkdir(parents=True)
            path = base / "interrupted-recovery-20260819T000000Z.json"
            path.write_text(json.dumps({"source_release_restored":"a"*40,"observed_current_before_recovery":"b"*40}), encoding="utf-8")
            inventory = f._inventory_p706_evidence(root)
            classification, facts = f._classify_evidence(root, inventory.values())
            self.assertEqual(classification, "EXPLICIT_P7_06_RECOVERY_EVIDENCE")
            self.assertEqual(facts[0]["kind"], "interrupted-recovery")

    def test_last_success_is_minimized(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run = root / "run"
            run.mkdir()
            (run / "p7-06-last-success.json").write_text(json.dumps({"transaction_id":"tx1","source_release":"a"*40,"target_release":"b"*40,"plan_id":"plan1","backup_path":"/sensitive/local/path","backup_sha256":"c"*64}), encoding="utf-8")
            value = f._load_last_success(root)
            self.assertEqual(set(value), {"transaction_id","source_release","target_release","plan_id"})
            self.assertNotIn("backup_path", value)

    def test_current_observation_handles_transitional_absence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertEqual(f._current_observation(root), "ABSENT")
            target = root / ("a" * 40)
            target.mkdir()
            (root / "current").symlink_to(target)
            self.assertEqual(f._current_observation(root), "a" * 40)

    def test_current_observation_marks_invalid_non_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "current").write_text("not-a-symlink", encoding="utf-8")
            self.assertEqual(f._current_observation(root), "NON_SYMLINK")

    def test_protected_digests_detect_change(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            governed = root / "state" / "governed"
            checkpoints = root / "state" / "checkpoints"
            governed.mkdir(parents=True)
            checkpoints.mkdir(parents=True)
            (governed / "x").write_text("one", encoding="utf-8")
            before = f._p703_digest(root)
            (governed / "x").write_text("two", encoding="utf-8")
            self.assertNotEqual(before, f._p703_digest(root))

    def test_sanitize_tail_redacts_local_roots(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime root"
            repo = Path(td) / "repo"
            text = f"path={root}/x repo={repo}/y"
            value = f._sanitize_tail(text, root, repo)
            self.assertIn("<RUNTIME_ROOT>/x", value)
            self.assertIn("<REPO_ROOT>/y", value)
            self.assertNotIn(str(root), value)


    def test_explicit_evidence_takes_precedence_over_stable_shape(self):
        self.assertIn("EXPLICIT_P7_06_ROLLBACK_EVIDENCE", f.CLASSIFICATIONS)
        # Classification precedence is intentionally encoded in run_forensics:
        # explicit new rollback/recovery evidence must not be hidden by a final target pointer.
        source = Path(f.__file__).read_text(encoding="utf-8")
        self.assertLess(source.index('elif evidence_classification is not None:'), source.index('elif final_release == after_command_release == origin_main'))
        self.assertLess(source.index('elif during_update_classification is not None:'), source.index('elif final_release == after_command_release == origin_main'))

    def test_classification_constants_are_bounded(self):
        self.assertIn("UNATTRIBUTED_CURRENT_MUTATION", f.CLASSIFICATIONS)
        self.assertNotIn("AUTO_FIX", f.CLASSIFICATIONS)


if __name__ == "__main__":
    unittest.main()
