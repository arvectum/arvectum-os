import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import p7_06_ui1_real_state_admission as admission
import p7_06_ui1_real_state_admission_entrypoint as entrypoint


class P706UI1RealStateEntrypointOwnerGateTests(unittest.TestCase):
    def test_wrong_owner_assertion_blocks_before_release_and_access_preflight(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(
            admission, "_verify_exact_release"
        ) as release_check, patch.object(admission, "_authorize_operator") as access_check:
            with self.assertRaisesRegex(
                entrypoint.UI1RealStateEntrypointError,
                "owner approval assertion",
            ):
                entrypoint.run_selected_mac_admission(
                    runtime_root=Path(tmp) / "runtime",
                    access_root=Path(tmp) / "access",
                    state_file=Path(tmp) / "state.json",
                    credential_id="credential",
                    credential_file=Path(tmp) / "credential",
                    l7_manifest=Path(tmp) / "manifest.json",
                    owner_approval="NOT_APPROVED",
                )
        release_check.assert_not_called()
        access_check.assert_not_called()


if __name__ == "__main__":
    unittest.main()
