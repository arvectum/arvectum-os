import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import p6_05_l4_bootstrap_internal_context as BOOTSTRAP
import p6_05_l5_first_real_product_connection as L5
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import OrganizationScope
from arvectum_os_ref.canonical import AuthorityMode

class P605L5FirstRealProductConnectionTests(unittest.TestCase):
    def setUp(self) -> None:
        # Use a canonical physical temp base to avoid macOS symlink aliases
        raw_temp_base = Path(tempfile.gettempdir())
        canonical_temp_base = raw_temp_base.resolve(strict=True)

        self.temp_dir = tempfile.TemporaryDirectory(dir=str(canonical_temp_base))
        self.addCleanup(self.temp_dir.cleanup)
        self.test_root = Path(self.temp_dir.name)

        self.external_root = self.test_root / "p6-05-l5-runtime"
        self.auth_token = BOOTSTRAP.REQUIRED_OWNER_ASSERTION
        
        # Create a valid L4 context to start with
        rc, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)
        self.state_file = self.external_root / "local-context" / "organization-operator.json"
        self.l4_ctx = ctx

    def test_01_happy_path_connection_passes(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        
        self.assertEqual(rc, 0)
        self.assertIsNotNone(result)
        self.assertIn("p6_05_l5_status=PASS", lines)
        self.assertIn("product_contract=0.1.0", lines)
        self.assertIn("cap_001_contract_version=1.0.0", lines)
        self.assertIn("cap_004_contract_version=1.0.0", lines)
        
        # Continuity checks
        self.assertIn("organization_continuity=true", lines)
        self.assertIn("actor_organization_continuity=true", lines)
        self.assertIn("product_organization_continuity=true", lines)
        self.assertIn("product_contract_organization_continuity=true", lines)
        
        # Verify internal objects
        self.assertEqual(result.organization_scope, self.l4_ctx.organization_scope)
        self.assertEqual(result.principal, self.l4_ctx.principal)
        # Verify non-authoritative projection timestamp
        self.assertEqual(result.connected_at, datetime.fromisoformat("2026-08-09T00:00:00+00:00"))

    def test_02_no_state_mutation_and_permissions(self) -> None:
        content_before = self.state_file.read_bytes()
        mtime_before = self.state_file.stat().st_mtime_ns
        
        # Capture modes
        root_mode_before = stat.S_IMODE(self.external_root.stat().st_mode)
        context_dir_mode_before = stat.S_IMODE(self.external_root.joinpath("local-context").stat().st_mode)
        state_file_mode_before = stat.S_IMODE(self.state_file.stat().st_mode)

        L5.connect_product(self.state_file)
        
        content_after = self.state_file.read_bytes()
        mtime_after = self.state_file.stat().st_mtime_ns
        
        self.assertEqual(content_before, content_after)
        self.assertEqual(mtime_before, mtime_after)

        # Permissions check
        self.assertEqual(root_mode_before, stat.S_IMODE(self.external_root.stat().st_mode))
        self.assertEqual(context_dir_mode_before, stat.S_IMODE(self.external_root.joinpath("local-context").stat().st_mode))
        self.assertEqual(state_file_mode_before, stat.S_IMODE(self.state_file.stat().st_mode))

    def test_03_missing_state_fails_safe(self) -> None:
        missing_file = self.external_root / "missing.json"
        rc, lines, result = L5.connect_product(missing_file)
        
        self.assertEqual(rc, 2)
        self.assertIsNone(result)
        self.assertIn("p6_05_l5_status=FAIL", lines)
        self.assertIn("failure_code=CONTEXT_MALFORMED", lines)
        self.assertIn("organization_continuity=not_proven", lines)

    def test_04_wrong_contract_subject_fails(self) -> None:
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            mock_contract = MagicMock()
            mock_contract.record.subject_id.value = "WRONG_SUBJECT"
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=WRONG_PRODUCT_CONTRACT_SUBJECT", lines)

    def test_05_wrong_organization_fails(self) -> None:
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            mock_contract = MagicMock()
            mock_contract.record.subject_id.value = "p6-02-arvectum-tender-operator"
            mock_contract.record.version_id.value = "p6-02-arvectum-tender-operator-v0.1.0"
            mock_contract.record.lifecycle_status = "Provisional"
            mock_contract.product_version = "restricted-paid-pilot/44fz-prebid-v1"
            
            # Tamper with organization
            other_org = OrganizationScope(Identity("organization", "OTHER", "platform"))
            mock_contract.organization = other_org
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=ORGANIZATION_MISMATCH", lines)

    def test_06_dependency_set_mismatch_fails(self) -> None:
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            mock_contract = MagicMock()
            mock_contract.record.subject_id.value = "p6-02-arvectum-tender-operator"
            mock_contract.record.version_id.value = "p6-02-arvectum-tender-operator-v0.1.0"
            mock_contract.record.lifecycle_status = "Provisional"
            mock_contract.product_version = "restricted-paid-pilot/44fz-prebid-v1"
            mock_contract.organization = self.l4_ctx.organization_scope
            
            # Tamper with dependencies
            mock_contract.dependencies = []
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=DEPENDENCY_SET_MISMATCH", lines)

    def test_07_provider_version_mismatch_fails(self) -> None:
        from arvectum_os_ref.product_contract import ProductContract
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.fromisoformat("2026-08-09T00:00:00+00:00")
        )
        
        from dataclasses import replace
        dep0 = replace(base_contract.dependencies[0], contract_version="2.0.0")
        tampered_contract = replace(base_contract, dependencies=(dep0,) + base_contract.dependencies[1:])
        
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("p6_05_l5_status=FAIL", lines)
            self.assertIn("failure_code=CONNECTION_FAILED", lines)

    def test_08_safe_output_no_ids(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        
        org_id = result.organization_scope.organization_id.value
        prin_id = result.principal.principal_id.value
        
        for line in lines:
            if line.strip():
                self.assertNotIn(org_id, line)
                self.assertNotIn(prin_id, line)
                self.assertNotIn("==", line)

    def test_09_external_authority_happy_path(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertTrue(result.external_authority_preserved)
        self.assertIn("external_authority_preserved=true", lines)

    def test_10_native_document_authority_drift_fails(self) -> None:
        from dataclasses import replace
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.fromisoformat("2026-08-09T00:00:00+00:00")
        )
        
        # Tamper with operation access mode
        ops = list(base_contract.operations)
        op0 = ops[0]
        accesses = list(op0.canonical_accesses)
        a0 = accesses[0]
        if a0.semantic_type == "platform.document":
            accesses[0] = replace(a0, authority_mode=AuthorityMode.NATIVE)
        ops[0] = replace(op0, canonical_accesses=tuple(accesses))
        tampered_contract = replace(base_contract, operations=tuple(ops))

        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=EXTERNAL_AUTHORITY_DECLARATION_LOST", lines)

    def test_11_wrong_document_authority_scope_fails(self) -> None:
        from dataclasses import replace
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.fromisoformat("2026-08-09T00:00:00+00:00")
        )
        
        # Tamper with authority scope
        ops = list(base_contract.operations)
        op0 = ops[0]
        accesses = list(op0.canonical_accesses)
        a0 = accesses[0]
        if a0.semantic_type == "platform.document":
            accesses[0] = replace(a0, authority_scope="WRONG_SCOPE")
        ops[0] = replace(op0, canonical_accesses=tuple(accesses))
        tampered_contract = replace(base_contract, operations=tuple(ops))

        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=EXTERNAL_AUTHORITY_DECLARATION_LOST", lines)

    def test_12_missing_document_authority_declaration_fails(self) -> None:
        from dataclasses import replace
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.fromisoformat("2026-08-09T00:00:00+00:00")
        )
        
        # Remove document access
        ops = list(base_contract.operations)
        op0 = ops[0]
        accesses = [a for a in op0.canonical_accesses if a.semantic_type != "platform.document"]
        ops[0] = replace(op0, canonical_accesses=tuple(accesses))
        # Do it for all operations
        new_ops = []
        for op in base_contract.operations:
            acc = [a for a in op.canonical_accesses if a.semantic_type != "platform.document"]
            new_ops.append(replace(op, canonical_accesses=tuple(acc)))
            
        tampered_contract = replace(base_contract, operations=tuple(new_ops))

        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=EXTERNAL_AUTHORITY_DECLARATION_LOST", lines)

    def test_13_arbitrary_exception_text_is_sanitized(self) -> None:
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            mock_build.side_effect = ValueError("internal-path=/private/foo opaque-id=secret-value")
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=CONNECTION_FAILED", lines)
            for line in lines:
                self.assertNotIn("/private/foo", line)
                self.assertNotIn("secret-value", line)

    def test_14_no_side_effects_summary(self) -> None:
        rc, lines, _ = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        
        self.assertIn("authorization_grants_created=false", lines)
        self.assertIn("delegations_created=false", lines)
        self.assertIn("organizational_authority_created=false", lines)
        self.assertIn("canonical_mutation=false", lines)
        self.assertIn("eis_invoked=false", lines)
        self.assertIn("soap_invoked=false", lines)
        self.assertIn("network_product_runtime_invoked=false", lines)
        self.assertIn("external_actions=false", lines)

if __name__ == "__main__":
    unittest.main()
