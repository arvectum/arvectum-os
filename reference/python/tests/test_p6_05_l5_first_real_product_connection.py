import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
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
from p6_05_tender_attachment_ref.contract import (
    P6_02_CANONICAL_BLOB_SHA,
    P6_02_CANONICAL_CONTRACT_PATH,
    P6_02_CONTRACT_SUBJECT_VALUE,
    P6_02_CONTRACT_VERSION_VALUE,
    P6_05_PROJECTION_SUBJECT_VALUE,
    p6_02_canonical_version_pin,
)

class P605L5FirstRealProductConnectionTests(unittest.TestCase):
    def setUp(self) -> None:
        raw_temp_base = Path(tempfile.gettempdir())
        canonical_temp_base = raw_temp_base.resolve(strict=True)

        self.temp_dir = tempfile.TemporaryDirectory(dir=str(canonical_temp_base))
        self.addCleanup(self.temp_dir.cleanup)
        self.test_root = Path(self.temp_dir.name)

        self.external_root = self.test_root / "p6-05-l5-runtime"
        self.auth_token = BOOTSTRAP.REQUIRED_OWNER_ASSERTION
        
        # Create a valid L4 context
        rc, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)
        self.state_file = self.external_root / "local-context" / "organization-operator.json"
        self.l4_ctx = ctx

    # 1. Happy path connection
    def test_01_happy_path_connection_passes(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        
        self.assertEqual(rc, 0)
        self.assertIsNotNone(result)
        self.assertIn("p6_05_l5_status=PASS", lines)
        self.assertIn("product_contract=0.1.0", lines)
        self.assertIn("product_contract_projection=non_authoritative", lines)
        self.assertIn("canonical_source_verified=true", lines)
        self.assertIn("cap_001_contract_version=1.0.0", lines)
        self.assertIn("cap_004_contract_version=1.0.0", lines)
        
        self.assertIn("organization_continuity=true", lines)
        self.assertIn("actor_organization_continuity=true", lines)
        self.assertIn("product_organization_continuity=true", lines)
        self.assertIn("product_contract_organization_continuity=true", lines)
        
        self.assertEqual(result.organization_scope, self.l4_ctx.organization_scope)
        self.assertEqual(result.principal, self.l4_ctx.principal)

    # 2. Exact canonical source pin
    def test_02_exact_canonical_source_pin(self) -> None:
        rc, _, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertIsNotNone(result)
        pin = result.product_contract.version_pin
        self.assertEqual(pin.subject_id.value, P6_02_CONTRACT_SUBJECT_VALUE)
        self.assertEqual(pin.version_id.value, P6_02_CONTRACT_VERSION_VALUE)
        self.assertEqual(pin.subject_id.namespace, "product-contract-subject")
        self.assertEqual(pin.version_id.namespace, "product-contract-version")
        self.assertEqual(pin.semantic_type, "platform.product-contract")
        self.assertEqual(pin.authority_scope, "platform.product-contract/boundary")
        self.assertEqual(pin.lifecycle_status, "Provisional")

    # 3. Projection Subject identity differs from canonical subject
    def test_03_projection_subject_identity_differs_from_canonical_subject(self) -> None:
        rc, _, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertIsNotNone(result)
        contract = result.product_contract
        self.assertNotEqual(contract.record.subject_id, contract.version_pin.subject_id)
        self.assertEqual(contract.record.subject_id.value, P6_05_PROJECTION_SUBJECT_VALUE)

    # 4. Projection Version identity differs from canonical version
    def test_04_projection_version_identity_differs_from_canonical_version(self) -> None:
        rc, _, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertIsNotNone(result)
        contract = result.product_contract
        self.assertNotEqual(contract.record.version_id, contract.version_pin.version_id)
        self.assertTrue(contract.record.version_id.value.startswith("p6-05-p6-02-projection-"))

    # 5. connected_at is actual runtime time, not 2026-08-09 midnight
    def test_05_connected_at_is_actual_runtime_time(self) -> None:
        before = datetime.now(timezone.utc) - timedelta(seconds=1)
        rc, _, result = L5.connect_product(self.state_file)
        after = datetime.now(timezone.utc) + timedelta(seconds=1)
        
        self.assertEqual(rc, 0)
        self.assertIsNotNone(result)
        self.assertNotEqual(result.connected_at, datetime.fromisoformat("2026-08-09T00:00:00+00:00"))
        self.assertTrue(before <= result.connected_at <= after)

    # 6. Canonical P6.02 blob verification PASS
    def test_06_canonical_blob_verification_pass(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertTrue(result.canonical_source_verified)
        self.assertIn("canonical_source_verified=true", lines)

    # 7. Canonical blob mismatch FAIL
    def test_07_canonical_blob_mismatch_fails(self) -> None:
        with patch("p6_05_l5_first_real_product_connection._git_blob_sha", return_value="wrong_sha"):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIsNone(result)
            self.assertIn("p6_05_l5_status=FAIL", lines)
            self.assertIn("failure_code=CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH", lines)
            self.assertIn("canonical_source_verified=not_proven", lines)

    # 8-11. No state mutation and permissions unchanged
    def test_08_to_11_no_state_mutation_and_permissions(self) -> None:
        content_before = self.state_file.read_bytes()
        mtime_before = self.state_file.stat().st_mtime_ns
        
        root_mode_before = stat.S_IMODE(self.external_root.stat().st_mode)
        context_dir_mode_before = stat.S_IMODE(self.external_root.joinpath("local-context").stat().st_mode)
        state_file_mode_before = stat.S_IMODE(self.state_file.stat().st_mode)

        L5.connect_product(self.state_file)
        
        content_after = self.state_file.read_bytes()
        mtime_after = self.state_file.stat().st_mtime_ns
        
        self.assertEqual(content_before, content_after)
        self.assertEqual(mtime_before, mtime_after)

        self.assertEqual(root_mode_before, stat.S_IMODE(self.external_root.stat().st_mode))
        self.assertEqual(context_dir_mode_before, stat.S_IMODE(self.external_root.joinpath("local-context").stat().st_mode))
        self.assertEqual(state_file_mode_before, stat.S_IMODE(self.state_file.stat().st_mode))

    # 12. Missing L4 state safe FAIL
    def test_12_missing_state_fails_safe(self) -> None:
        missing_file = self.external_root / "missing.json"
        rc, lines, result = L5.connect_product(missing_file)
        
        self.assertEqual(rc, 2)
        self.assertIsNone(result)
        self.assertIn("p6_05_l5_status=FAIL", lines)
        self.assertIn("failure_code=CONTEXT_MALFORMED", lines)
        self.assertIn("organization_continuity=not_proven", lines)

    # 13. Wrong canonical Product Contract subject FAIL
    def test_13_wrong_canonical_subject_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            tampered_pin = MagicMock()
            tampered_pin.subject_id.namespace = "product-contract-subject"
            tampered_pin.subject_id.value = "WRONG_SUBJECT"
            tampered_pin.subject_id.scope = self.l4_ctx.organization_scope.organization_id.value
            tampered_pin.version_id.scope = self.l4_ctx.organization_scope.organization_id.value
            
            mock_contract = MagicMock(spec=L5.P605ExecutableProductContractProjection)
            mock_contract.record = base_contract.record
            mock_contract.version_pin = tampered_pin
            mock_contract.product_version = base_contract.product_version
            mock_contract.organization = base_contract.organization
            mock_contract.canonical_source_path = P6_02_CANONICAL_CONTRACT_PATH
            mock_contract.canonical_source_blob_sha = P6_02_CANONICAL_BLOB_SHA
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=WRONG_PRODUCT_CONTRACT_SUBJECT", lines)

    # 14. Wrong canonical Product Contract version identity FAIL
    def test_14_wrong_canonical_version_identity_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            tampered_pin = MagicMock()
            tampered_pin.subject_id.namespace = "product-contract-subject"
            tampered_pin.subject_id.value = P6_02_CONTRACT_SUBJECT_VALUE
            tampered_pin.subject_id.scope = self.l4_ctx.organization_scope.organization_id.value
            tampered_pin.version_id.namespace = "product-contract-version"
            tampered_pin.version_id.value = "WRONG_VERSION"
            tampered_pin.version_id.scope = self.l4_ctx.organization_scope.organization_id.value
            
            mock_contract = MagicMock(spec=L5.P605ExecutableProductContractProjection)
            mock_contract.record = base_contract.record
            mock_contract.version_pin = tampered_pin
            mock_contract.product_version = base_contract.product_version
            mock_contract.organization = base_contract.organization
            mock_contract.canonical_source_path = P6_02_CANONICAL_CONTRACT_PATH
            mock_contract.canonical_source_blob_sha = P6_02_CANONICAL_BLOB_SHA
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=WRONG_PRODUCT_CONTRACT_VERSION_IDENTITY", lines)

    # 15. Wrong lifecycle FAIL
    def test_15_wrong_lifecycle_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            tampered_pin = MagicMock()
            tampered_pin.subject_id.namespace = "product-contract-subject"
            tampered_pin.subject_id.value = P6_02_CONTRACT_SUBJECT_VALUE
            tampered_pin.subject_id.scope = self.l4_ctx.organization_scope.organization_id.value
            tampered_pin.version_id.namespace = "product-contract-version"
            tampered_pin.version_id.value = P6_02_CONTRACT_VERSION_VALUE
            tampered_pin.version_id.scope = self.l4_ctx.organization_scope.organization_id.value
            tampered_pin.semantic_type = "platform.product-contract"
            tampered_pin.authority_scope = "platform.product-contract/boundary"
            tampered_pin.lifecycle_status = "Stable"
            
            mock_contract = MagicMock(spec=L5.P605ExecutableProductContractProjection)
            mock_contract.record = base_contract.record
            mock_contract.version_pin = tampered_pin
            mock_contract.product_version = base_contract.product_version
            mock_contract.organization = base_contract.organization
            mock_contract.canonical_source_path = P6_02_CANONICAL_CONTRACT_PATH
            mock_contract.canonical_source_blob_sha = P6_02_CANONICAL_BLOB_SHA
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=WRONG_PRODUCT_CONTRACT_LIFECYCLE", lines)

    # 16. Wrong product compatibility line FAIL
    def test_16_wrong_product_compatibility_line_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            from dataclasses import replace
            tampered = replace(base_contract, product_version="wrong/compatibility-line")
            mock_build.return_value = tampered
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=WRONG_PRODUCT_COMPATIBILITY_LINE", lines)

    # 17. Wrong Organization FAIL
    def test_17_wrong_organization_fails(self) -> None:
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            base_contract = L5.build_p6_05_product_contract_projection(
                actor=self.l4_ctx.actor_context,
                created_at=datetime.now(timezone.utc),
            )
            # Tamper with pin scope
            tampered_pin = MagicMock()
            tampered_pin.subject_id.namespace = "product-contract-subject"
            tampered_pin.subject_id.value = P6_02_CONTRACT_SUBJECT_VALUE
            tampered_pin.subject_id.scope = "OTHER"
            tampered_pin.version_id.namespace = "product-contract-version"
            tampered_pin.version_id.value = P6_02_CONTRACT_VERSION_VALUE
            tampered_pin.version_id.scope = "OTHER"
            tampered_pin.lifecycle_status = "Provisional"
            
            mock_contract = MagicMock(spec=L5.P605ExecutableProductContractProjection)
            mock_contract.record = base_contract.record
            mock_contract.version_pin = tampered_pin
            mock_contract.product_version = base_contract.product_version
            mock_contract.organization = base_contract.organization
            mock_contract.canonical_source_path = P6_02_CANONICAL_CONTRACT_PATH
            mock_contract.canonical_source_blob_sha = P6_02_CANONICAL_BLOB_SHA
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=ORGANIZATION_MISMATCH", lines)

    # 18. Projection reusing canonical Version Identity FAIL
    def test_18_projection_reusing_canonical_version_identity_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            from dataclasses import replace
            tampered_record = replace(base_contract.record, version_id=base_contract.version_pin.version_id)
            mock_contract = MagicMock(spec=L5.P605ExecutableProductContractProjection)
            mock_contract.record = tampered_record
            mock_contract.version_pin = base_contract.version_pin
            mock_contract.product_version = base_contract.product_version
            mock_contract.organization = base_contract.organization
            mock_contract.canonical_source_path = P6_02_CANONICAL_CONTRACT_PATH
            mock_contract.canonical_source_blob_sha = P6_02_CANONICAL_BLOB_SHA
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=PROJECTION_SOURCE_BOUNDARY_LOST", lines)

    # 19. Dependency set mismatch FAIL
    def test_19_dependency_set_mismatch_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            mock_contract = MagicMock(spec=L5.P605ExecutableProductContractProjection)
            mock_contract.record = base_contract.record
            mock_contract.version_pin = base_contract.version_pin
            mock_contract.product_version = base_contract.product_version
            mock_contract.organization = base_contract.organization
            mock_contract.canonical_source_path = P6_02_CANONICAL_CONTRACT_PATH
            mock_contract.canonical_source_blob_sha = P6_02_CANONICAL_BLOB_SHA
            mock_contract.dependencies = base_contract.dependencies[:1]
            mock_contract.operations = base_contract.operations
            mock_build.return_value = mock_contract
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=DEPENDENCY_SET_MISMATCH", lines)

    # 20. Dependency version mismatch FAIL
    def test_20_dependency_version_mismatch_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            from dataclasses import replace
            dep0 = replace(base_contract.dependencies[0], contract_version="2.0.0")
            tampered = replace(base_contract, dependencies=(dep0,) + base_contract.dependencies[1:])
            mock_build.return_value = tampered
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=DEPENDENCY_VERSION_MISMATCH", lines)

    # 21. Safe output contains no opaque IDs
    def test_21_safe_output_no_ids(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        
        org_id = result.organization_scope.organization_id.value
        prin_id = result.principal.principal_id.value
        proj_ver = result.product_contract.record.version_id.value
        
        for line in lines:
            if line.strip():
                self.assertNotIn(org_id, line)
                self.assertNotIn(prin_id, line)
                self.assertNotIn(proj_ver, line)
                self.assertNotIn("==", line)

    # 22. Arbitrary exception text sanitizes to CONNECTION_FAILED
    def test_22_arbitrary_exception_text_is_sanitized(self) -> None:
        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection") as mock_build:
            mock_build.side_effect = ValueError("internal-path=/private/foo opaque-id=secret-value")
            
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=CONNECTION_FAILED", lines)
            for line in lines:
                self.assertNotIn("/private/foo", line)
                self.assertNotIn("secret-value", line)

    # 23. External Authority happy path
    def test_23_external_authority_happy_path(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertTrue(result.external_authority_preserved)
        self.assertIn("external_authority_preserved=true", lines)

    # 24. Native Document drift FAIL
    def test_24_native_document_authority_drift_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        from dataclasses import replace
        ops = list(base_contract.operations)
        op0 = ops[0]
        accesses = list(op0.canonical_accesses)
        accesses[0] = replace(accesses[0], authority_mode=AuthorityMode.NATIVE)
        ops[0] = replace(op0, canonical_accesses=tuple(accesses))
        tampered_contract = replace(base_contract, operations=tuple(ops))

        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=EXTERNAL_AUTHORITY_DECLARATION_LOST", lines)

    # 25. Wrong Document authority scope FAIL
    def test_25_wrong_document_authority_scope_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        from dataclasses import replace
        ops = list(base_contract.operations)
        op0 = ops[0]
        accesses = list(op0.canonical_accesses)
        accesses[0] = replace(accesses[0], authority_scope="WRONG_SCOPE")
        ops[0] = replace(op0, canonical_accesses=tuple(accesses))
        tampered_contract = replace(base_contract, operations=tuple(ops))

        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=EXTERNAL_AUTHORITY_DECLARATION_LOST", lines)

    # 26. Missing Document access FAIL
    def test_26_missing_document_authority_declaration_fails(self) -> None:
        base_contract = L5.build_p6_05_product_contract_projection(
            actor=self.l4_ctx.actor_context,
            created_at=datetime.now(timezone.utc),
        )
        from dataclasses import replace
        new_ops = []
        for op in base_contract.operations:
            acc = [a for a in op.canonical_accesses if a.semantic_type != "platform.document"]
            new_ops.append(replace(op, canonical_accesses=tuple(acc)))
        tampered_contract = replace(base_contract, operations=tuple(new_ops))

        with patch("p6_05_l5_first_real_product_connection.build_p6_05_product_contract_projection", return_value=tampered_contract):
            rc, lines, result = L5.connect_product(self.state_file)
            self.assertEqual(rc, 1)
            self.assertIn("failure_code=EXTERNAL_AUTHORITY_DECLARATION_LOST", lines)

    # 27-28. CAP-002 / CAP-003 absent
    def test_27_to_28_cap002_cap003_absent(self) -> None:
        rc, lines, result = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertIn("cap_002_present=false", lines)
        self.assertIn("cap_003_present=false", lines)

    # 29. No grants / delegations / Organizational Authority
    def test_29_no_authority_elevation(self) -> None:
        rc, lines, _ = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertIn("authorization_grants_created=false", lines)
        self.assertIn("delegations_created=false", lines)
        self.assertIn("organizational_authority_created=false", lines)

    # 30-31. No canonical mutation / No external action
    def test_30_to_31_no_side_effects_or_actions(self) -> None:
        rc, lines, _ = L5.connect_product(self.state_file)
        self.assertEqual(rc, 0)
        self.assertIn("canonical_mutation=false", lines)
        self.assertIn("eis_invoked=false", lines)
        self.assertIn("soap_invoked=false", lines)
        self.assertIn("network_product_runtime_invoked=false", lines)
        self.assertIn("external_actions=false", lines)


if __name__ == "__main__":
    unittest.main()
