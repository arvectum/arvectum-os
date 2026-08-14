import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    WorkspaceShellState,
    open_workspace_shell,
)
import p6_05_l4_bootstrap_internal_context as BOOTSTRAP
import p6_05_l4_operator_context_preflight as PREFLIGHT


class P605L4InternalOrgOperatorBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.external_root = Path(self.temp_dir.name) / "p6-05-l4-runtime"
        self.auth_token = BOOTSTRAP.REQUIRED_OWNER_ASSERTION

    # Minimum Requirement 1: missing owner assertion fails before creation
    def test_01_missing_owner_assertion_fails_before_creation(self) -> None:
        rc, lines, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization="",
        )
        self.assertEqual(rc, 2)
        self.assertIsNone(ctx)
        self.assertIn("p6_05_l4_status=FAIL", lines)
        self.assertIn("failure_code=OWNER_AUTHORIZATION_REQUIRED", lines)
        self.assertIn("authorization_grants=not_proven", lines)
        self.assertFalse(self.external_root.exists())

    # Minimum Requirement 2: wrong owner assertion fails before creation
    def test_02_wrong_owner_assertion_fails_before_creation(self) -> None:
        rc, lines, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization="WRONG_ASSERTION",
        )
        self.assertEqual(rc, 2)
        self.assertIsNone(ctx)
        self.assertIn("p6_05_l4_status=FAIL", lines)
        self.assertIn("failure_code=OWNER_AUTHORIZATION_REQUIRED", lines)
        self.assertIn("authorization_grants=not_proven", lines)
        self.assertFalse(self.external_root.exists())

    # Minimum Requirement 3: valid owner assertion creates context
    def test_03_valid_owner_assertion_creates_context(self) -> None:
        rc, lines, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)
        self.assertIsNotNone(ctx)
        self.assertTrue(ctx.context_created)
        self.assertFalse(ctx.context_reused)
        self.assertIn("p6_05_l4_status=PASS", lines)
        self.assertIn("context_created=true", lines)
        self.assertIn("context_reused=false", lines)
        self.assertIn("authorization_grants=0", lines)
        self.assertIn("delegations=0", lines)
        self.assertIn("organizational_authority_claimed=false", lines)
        self.assertIn("authentication_evidence_refs=0", lines)
        self.assertIn("tenant_context_introduced=false", lines)
        self.assertIn("product_context_introduced=false", lines)
        self.assertIn("credentials_present=false", lines)
        self.assertIn("secrets_present=false", lines)

    # Minimum Requirement 4: root/directories owner-only
    def test_04_root_and_directories_owner_only(self) -> None:
        rc, _, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)
        root_mode = stat.S_IMODE(self.external_root.stat().st_mode)
        self.assertEqual(root_mode, 0o700)
        context_dir = self.external_root / "local-context"
        context_dir_mode = stat.S_IMODE(context_dir.stat().st_mode)
        self.assertEqual(context_dir_mode, 0o700)

    # Minimum Requirement 5: state file 0600 or stricter
    def test_05_state_file_0600_or_stricter(self) -> None:
        rc, _, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        self.assertTrue(state_file.exists())
        file_mode = stat.S_IMODE(state_file.stat().st_mode)
        self.assertEqual(file_mode, 0o600)

    # Minimum Requirement 6: atomic exclusive creation
    def test_06_atomic_exclusive_creation(self) -> None:
        rc1, _, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc1, 0)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        self.assertTrue(state_file.exists())

    # Minimum Requirement 7: creation race never overwrites existing state
    def test_07_creation_race_never_overwrites_existing_state(self) -> None:
        # Prepare context directory
        self.external_root.mkdir(parents=True, mode=0o700)
        context_dir = self.external_root / "local-context"
        context_dir.mkdir(parents=True, mode=0o700)
        state_file = context_dir / "organization-operator.json"
        
        # Simulate state file created by concurrent process with valid content
        org_id = Identity("organization", "org-existing", "platform")
        prin_id = Identity("principal", "prin-existing", "org-existing")
        payload = {
            "schema_version": BOOTSTRAP.SCHEMA_VERSION,
            "organization": {
                "identity": {
                    "namespace": org_id.namespace,
                    "value": org_id.value,
                    "scope": org_id.scope,
                },
                "context_label": BOOTSTRAP.CONTEXT_LABEL,
            },
            "operator": {
                "identity": {
                    "namespace": prin_id.namespace,
                    "value": prin_id.value,
                    "scope": prin_id.scope,
                },
                "principal_category": BOOTSTRAP.PRINCIPAL_CATEGORY,
                "operating_mode": BOOTSTRAP.OPERATING_MODE,
            },
            "authority": {
                "authorization_grants": [],
                "delegations": [],
                "organizational_authority_claimed": False,
            },
            "authentication": {"evidence_refs": []},
            "bootstrap": {
                "scope": BOOTSTRAP.BOOTSTRAP_SCOPE,
                "owner_authorization_asserted": True,
            },
        }
        state_file.write_text(json.dumps(payload), encoding="utf-8")
        os.chmod(state_file, 0o600)

        # Bootstrap should reuse rather than overwrite
        rc, lines, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)
        self.assertIsNotNone(ctx)
        self.assertFalse(ctx.context_created)
        self.assertTrue(ctx.context_reused)
        self.assertEqual(ctx.organization_scope.organization_id.value, "org-existing")

    # Minimum Requirement 8: target inside Git fails
    def test_08_target_inside_git_fails(self) -> None:
        git_repo = Path(self.temp_dir.name) / "mock_git_repo"
        git_repo.mkdir(mode=0o700)
        subprocess.run(["git", "init", str(git_repo)], check=True, capture_output=True)

        target_inside = git_repo / "sub" / "l4-runtime"
        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            target_inside,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("p6_05_l4_status=FAIL", lines)
        self.assertIn("failure_code=TARGET_INSIDE_GIT_WORKTREE", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 9: target inside Arvectum OS fails
    def test_09_target_inside_arvectum_os_fails(self) -> None:
        repo_root = Path(self.temp_dir.name) / "arvectum-os"
        repo_root.mkdir(mode=0o700)
        target_inside = repo_root / "local-runtime"

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            target_inside,
            owner_authorization=self.auth_token,
            arvectum_repo_root=repo_root,
        )
        self.assertEqual(rc, 2)
        self.assertIn("p6_05_l4_status=FAIL", lines)
        self.assertIn("failure_code=TARGET_INSIDE_ARVECTUM_CHECKOUT", lines)

    # Minimum Requirement 10: symlink root/file fails
    def test_10_symlink_root_fails(self) -> None:
        real_target = Path(self.temp_dir.name) / "real_target"
        real_target.mkdir(mode=0o700)
        symlink_target = Path(self.temp_dir.name) / "symlink_target"
        os.symlink(real_target, symlink_target)

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            symlink_target,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=TARGET_SYMLINK_NOT_ALLOWED", lines)

    def test_10b_symlink_file_fails(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        real_backup = self.external_root / "local-context" / "real_backup.json"
        state_file.rename(real_backup)
        os.symlink(real_backup, state_file)

        rc, lines, _ = PREFLIGHT.inspect_operator_context_file(state_file)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_FILE_SYMLINK_NOT_ALLOWED", lines)

    # Intermediate symlink tests
    def test_10c_intermediate_symlink_parent_bootstrap_fails(self) -> None:
        real_parent = Path(self.temp_dir.name).resolve() / "real_parent"
        real_parent.mkdir(mode=0o700)
        (real_parent / "nested").mkdir(mode=0o700)

        alias_parent = Path(self.temp_dir.name).resolve() / "alias_parent"
        os.symlink(real_parent, alias_parent)

        target_through_alias = alias_parent / "nested" / "p6-05-l4-runtime"
        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            target_through_alias,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=TARGET_SYMLINK_NOT_ALLOWED", lines)
        self.assertFalse(target_through_alias.exists())

    def test_10d_intermediate_symlink_parent_preflight_fails(self) -> None:
        real_parent = Path(self.temp_dir.name).resolve() / "real_parent_pre"
        real_parent.mkdir(mode=0o700)
        target_root = real_parent / "p6-05-l4-runtime"

        rc, _, _ = BOOTSTRAP.bootstrap_internal_context(
            target_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 0)

        alias_parent = Path(self.temp_dir.name).resolve() / "alias_parent_pre"
        os.symlink(real_parent, alias_parent)

        state_through_alias = alias_parent / "p6-05-l4-runtime" / "local-context" / "organization-operator.json"
        rc, lines, _ = PREFLIGHT.inspect_operator_context_file(state_through_alias)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_FILE_SYMLINK_NOT_ALLOWED", lines)

    # Minimum Requirement 11: generated Organization Identity is non-empty and opaque
    def test_11_generated_organization_identity_is_non_empty_and_opaque(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        org_id = ctx.organization_scope.organization_id
        self.assertEqual(org_id.namespace, "organization")
        self.assertEqual(org_id.scope, "platform")
        self.assertTrue(len(org_id.value) >= 16)

    # Minimum Requirement 12: generated Principal Identity is non-empty and opaque
    def test_12_generated_principal_identity_is_non_empty_and_opaque(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        prin_id = ctx.principal.principal_id
        self.assertEqual(prin_id.namespace, "principal")
        self.assertEqual(prin_id.scope, ctx.organization_scope.organization_id.value)
        self.assertTrue(len(prin_id.value) >= 16)

    # Minimum Requirement 13: identity does not derive from company label
    def test_13_identity_does_not_derive_from_company_label(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        org_val = ctx.organization_scope.organization_id.value.lower()
        prin_val = ctx.principal.principal_id.value.lower()
        for term in ("арвектум", "arvectum", "ооо", "llc", "operator", "admin"):
            self.assertNotIn(term, org_val)
            self.assertNotIn(term, prin_val)

    # Minimum Requirement 14: principal scope binds to generated Organization
    def test_14_principal_scope_binds_to_generated_organization(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        self.assertEqual(
            ctx.principal.principal_id.scope,
            ctx.organization_scope.organization_id.value,
        )

    # Minimum Requirement 15: Principal category = human
    def test_15_principal_category_is_human(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("principal_category=human", lines)

    # Minimum Requirement 16: ActorContext construction succeeds
    def test_16_actor_context_construction_succeeds(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        self.assertIsInstance(ctx.actor_context, ActorContext)
        self.assertEqual(ctx.actor_context.actual_principal, ctx.principal)
        self.assertEqual(ctx.actor_context.organization, ctx.organization_scope)
        self.assertIsNone(ctx.actor_context.represented_principal)
        self.assertEqual(ctx.actor_context.authentication_evidence_refs, ())

    # Minimum Requirement 17: no role/permission fields added to Principal/ActorContext
    def test_17_no_role_or_permission_fields_added_to_principal_or_actor_context(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        for forbidden in (
            "authorized",
            "permissions",
            "roles",
            "is_admin",
            "organizational_authority",
            "approval_authority",
            "delegations",
        ):
            self.assertFalse(hasattr(ctx.principal, forbidden))
            self.assertFalse(hasattr(ctx.actor_context, forbidden))
            self.assertFalse(hasattr(ctx.organization_scope, forbidden))

    # Minimum Requirement 18: authorization grants must be empty
    def test_18_authorization_grants_must_be_empty(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("authorization_grants=0", lines)

    # Minimum Requirement 19: delegations must be empty
    def test_19_delegations_must_be_empty(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("delegations=0", lines)

    # Minimum Requirement 20: organizational authority claim must be false
    def test_20_organizational_authority_claim_must_be_false(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("organizational_authority_claimed=false", lines)

    # Minimum Requirement 21: authentication evidence refs must be empty
    def test_21_authentication_evidence_refs_must_be_empty(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("authentication_evidence_refs=0", lines)

    # Minimum Requirement 22: product context absent
    def test_22_product_context_absent(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("product_context_introduced=false", lines)

    # Minimum Requirement 23: tenant context absent
    def test_23_tenant_context_absent(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("tenant_context_introduced=false", lines)

    # Minimum Requirement 24: valid existing context is reused without changing IDs
    def test_24_valid_existing_context_is_reused_without_changing_ids(self) -> None:
        _, _, ctx1 = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        _, _, ctx2 = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(
            ctx1.organization_scope.organization_id,
            ctx2.organization_scope.organization_id,
        )
        self.assertEqual(
            ctx1.principal.principal_id,
            ctx2.principal.principal_id,
        )

    # Minimum Requirement 25: idempotent retry does not rewrite file
    def test_25_idempotent_retry_does_not_rewrite_file(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        mtime1 = state_file.stat().st_mtime_ns

        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        mtime2 = state_file.stat().st_mtime_ns
        self.assertEqual(mtime1, mtime2)

    # Minimum Requirement 26: malformed JSON fails closed
    def test_26_malformed_json_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        state_file.write_text("{invalid json", encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_MALFORMED", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 27: unsupported schema fails closed
    def test_27_unsupported_schema_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["schema_version"] = "p6.05-l4-unsupported-version-99"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNSUPPORTED", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 28: Organization Identity mutation/drift fails
    def test_28_organization_identity_invalid_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["organization"]["identity"]["namespace"] = "invalid-ns"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=ORGANIZATION_IDENTITY_INVALID", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 29: Principal scope mismatch fails
    def test_29_principal_scope_mismatch_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["operator"]["identity"]["scope"] = "mismatching-org-id"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=PRINCIPAL_ORGANIZATION_SCOPE_MISMATCH", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 30: invalid principal category fails
    def test_30_invalid_principal_category_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["operator"]["principal_category"] = "machine"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=PRINCIPAL_CATEGORY_UNSUPPORTED", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 31: non-empty grant list fails
    def test_31_non_empty_grants_fail_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["authority"]["authorization_grants"] = ["grant-admin"]
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=AUTHORIZATION_GRANTS_NOT_EMPTY", lines)
        self.assertIn("authorization_grants=not_proven", lines)

    # Minimum Requirement 32: non-empty delegation list fails
    def test_32_non_empty_delegations_fail_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["authority"]["delegations"] = ["delegation-full"]
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=DELEGATIONS_NOT_EMPTY", lines)
        self.assertIn("delegations=not_proven", lines)

    # Minimum Requirement 33: authority=true fails
    def test_33_authority_claimed_true_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["authority"]["organizational_authority_claimed"] = True
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=ORGANIZATIONAL_AUTHORITY_NOT_ALLOWED", lines)
        self.assertIn("organizational_authority_claimed=not_proven", lines)

    # Minimum Requirement 34: auth evidence present fails
    def test_34_auth_evidence_present_fails_closed(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["authentication"]["evidence_refs"] = ["authn-token-ref"]
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=AUTHENTICATION_EVIDENCE_NOT_EMPTY", lines)
        self.assertIn("authentication_evidence_refs=not_proven", lines)

    # Minimum Requirement 35: broad permissions fail and are not auto-repaired
    def test_35_broad_file_permissions_fail_closed_and_not_repaired(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        os.chmod(state_file, 0o644)

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_PERMISSIONS_TOO_BROAD", lines)
        self.assertEqual(stat.S_IMODE(state_file.stat().st_mode), 0o644)

    def test_35b_broad_root_permissions_fail_closed_and_not_repaired(self) -> None:
        self.external_root.mkdir(parents=True, mode=0o755)
        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_PERMISSIONS_TOO_BROAD", lines)
        self.assertEqual(stat.S_IMODE(self.external_root.stat().st_mode), 0o755)

    def test_35c_broad_context_dir_permissions_fail_closed_and_not_repaired(self) -> None:
        self.external_root.mkdir(parents=True, mode=0o700)
        context_dir = self.external_root / "local-context"
        context_dir.mkdir(parents=True, mode=0o755)
        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_PERMISSIONS_TOO_BROAD", lines)
        self.assertEqual(stat.S_IMODE(context_dir.stat().st_mode), 0o755)

    def test_35d_preflight_broad_permissions_fail_and_not_repaired(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"

        # Test state file broad mode
        os.chmod(state_file, 0o644)
        rc, lines, _ = PREFLIGHT.inspect_operator_context_file(state_file)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_PERMISSIONS_TOO_BROAD", lines)
        self.assertEqual(stat.S_IMODE(state_file.stat().st_mode), 0o644)
        os.chmod(state_file, 0o600)

        # Test local-context dir broad mode
        context_dir = self.external_root / "local-context"
        os.chmod(context_dir, 0o755)
        rc, lines, _ = PREFLIGHT.inspect_operator_context_file(state_file)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_PERMISSIONS_TOO_BROAD", lines)
        self.assertEqual(stat.S_IMODE(context_dir.stat().st_mode), 0o755)
        os.chmod(context_dir, 0o700)

        # Test target root dir broad mode
        os.chmod(self.external_root, 0o755)
        rc, lines, _ = PREFLIGHT.inspect_operator_context_file(state_file)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_PERMISSIONS_TOO_BROAD", lines)
        self.assertEqual(stat.S_IMODE(self.external_root.stat().st_mode), 0o755)

    # Negative Schema Tests: Unexpected Fields and Label Mismatch
    def test_negative_schema_extra_top_level_product_context(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["product_context"] = {"id": "prod-1"}
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)
        self.assertNotIn("prod-1", "".join(lines))

    def test_negative_schema_extra_top_level_tenant_context(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["tenant_context"] = {"id": "tenant-1"}
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_top_level_password(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["password"] = "secret123"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)
        self.assertNotIn("secret123", "".join(lines))

    def test_negative_schema_extra_top_level_credential(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["credential"] = "token-xyz"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)
        self.assertNotIn("token-xyz", "".join(lines))

    def test_negative_schema_extra_top_level_secret(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["secret"] = "mysecret"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)
        self.assertNotIn("mysecret", "".join(lines))

    def test_negative_schema_extra_field_inside_organization(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["organization"]["extra"] = "val"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_field_inside_organization_identity(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["organization"]["identity"]["extra"] = "val"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_field_inside_operator(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["operator"]["role"] = "admin"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_field_inside_operator_identity(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["operator"]["identity"]["extra"] = "val"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_field_inside_authority(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["authority"]["extra"] = "val"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_field_inside_authentication(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["authentication"]["token"] = "xyz"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_extra_field_inside_bootstrap(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["bootstrap"]["extra"] = "val"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD", lines)

    def test_negative_schema_context_label_mismatch(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        state_file = self.external_root / "local-context" / "organization-operator.json"
        data = json.loads(state_file.read_text(encoding="utf-8"))
        data["organization"]["context_label"] = "Other Company LLC"
        state_file.write_text(json.dumps(data), encoding="utf-8")

        rc, lines, _ = BOOTSTRAP.bootstrap_internal_context(self.external_root, owner_authorization=self.auth_token)
        self.assertEqual(rc, 2)
        self.assertIn("failure_code=ORGANIZATION_CONTEXT_LABEL_MISMATCH", lines)
        self.assertNotIn("Other Company LLC", "".join(lines))

    # Minimum Requirement 36: preflight performs no mutation
    def test_36_preflight_performs_no_mutation(self) -> None:
        BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        state_file = self.external_root / "local-context" / "organization-operator.json"
        content_before = state_file.read_bytes()
        mtime_before = state_file.stat().st_mtime_ns
        mode_before = stat.S_IMODE(state_file.stat().st_mode)

        rc, lines, ctx = PREFLIGHT.inspect_operator_context_file(state_file)
        self.assertEqual(rc, 0)
        self.assertIsNotNone(ctx)

        content_after = state_file.read_bytes()
        mtime_after = state_file.stat().st_mtime_ns
        mode_after = stat.S_IMODE(state_file.stat().st_mode)
        self.assertEqual(content_before, content_after)
        self.assertEqual(mtime_before, mtime_after)
        self.assertEqual(mode_before, mode_after)

    # Minimum Requirement 37: workspace smoke preserves Organization and Actor
    def test_37_workspace_smoke_preserves_organization_and_actor(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        shell = open_workspace_shell(ctx.actor_context)
        self.assertIsInstance(shell, WorkspaceShellState)
        self.assertEqual(shell.organization, ctx.organization_scope)
        self.assertEqual(shell.actor, ctx.actor_context)

    # Minimum Requirement 38: workspace remains non-authoritative
    def test_38_workspace_remains_non_authoritative(self) -> None:
        _, _, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        shell = open_workspace_shell(ctx.actor_context)
        self.assertIsInstance(shell, WorkspaceShellState)
        self.assertEqual(
            shell.presentation_authority.value,
            "Non-authoritative presentation",
        )

    # Minimum Requirement 39: no identity values printed in normal safe report
    def test_39_no_identity_values_printed_in_normal_safe_report(self) -> None:
        _, lines, ctx = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIsNotNone(ctx)
        org_val = ctx.organization_scope.organization_id.value
        prin_val = ctx.principal.principal_id.value

        for line in lines:
            self.assertNotIn(org_val, line)
            self.assertNotIn(prin_val, line)

    # Minimum Requirements 40-43: product/eis/network/external actions false
    def test_40_to_43_product_eis_network_and_external_actions_are_false(self) -> None:
        _, lines, _ = BOOTSTRAP.bootstrap_internal_context(
            self.external_root,
            owner_authorization=self.auth_token,
        )
        self.assertIn("product_invoked=false", lines)
        self.assertIn("eis_invoked=false", lines)
        self.assertIn("network_invoked=false", lines)
        self.assertIn("external_actions=false", lines)


if __name__ == "__main__":
    unittest.main()
