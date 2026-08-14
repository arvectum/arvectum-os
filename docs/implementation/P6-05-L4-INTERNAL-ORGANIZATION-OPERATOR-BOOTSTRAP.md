# P6.05-L4 — Internal Organization + Operator Bootstrap Implementation Runbook

Status: `Prepared / owner-operated execution required for PASS`
Version: `0.1.0`
Date: `2026-08-14`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent work item: `P6.05 — Platform-gap remediation from first real use`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Purpose

This runbook specifies the mechanism, security invariants, state schema, and operational procedures for `P6.05-L4 — Internal Organization + operator bootstrap`.

The purpose of P6.05-L4 is to prepare the smallest bounded internal context needed for later P6.05-L5 product connection:
1. One explicit Organization Identity representing ООО «Арвектум»;
2. One attributable human Principal Identity representing the owner-operator;
3. Valid canonical `OrganizationScope`, `Principal`, and `ActorContext` references;
4. Explicit, owner-operated bootstrap provenance in an external, owner-only local state file.

## 2. Canonical Basis and Architecture Boundaries

The implementation strictly preserves the canonical architecture:
- Constitution `1.2.0` = Ratified / frozen;
- RFC-0001 (Architecture) = Accepted `1.0.0`;
- RFC-0002 (Canonical Record Kernel Metamodel) = Accepted `1.0.0`;
- RFC-0003 (Identity, Security, Privacy, Tenant Sovereignty) = Accepted `1.0.0`;
- RFC-0005 (Governed Execution and Workflow Model) = Accepted `1.0.0`;
- Reuses existing canonical reference types (`Identity`, `OrganizationScope`, `Principal`, `ActorContext`) without introducing competing models.

### Strict Non-Goals (What L4 MUST NOT Implement)
P6.05-L4 is an internal operational validation mechanism only. It MUST NOT implement:
- General IAM, SSO, OAuth, OIDC, SAML;
- Password management, sessions, or user databases;
- RBAC or ABAC frameworks;
- Permission catalogs, organization membership services, or tenant provisioning engines;
- Admin consoles or delegation engines;
- Product Contract changes or capability promotions.

### Identity vs Authority Boundary
- Identity represents context and attribution only.
- P6.05-L4 creates **no** authorization, **no** Organizational Authority, **no** consequential approval, and **no** capability promotion.
- No permission/role fields (`authorized`, `permissions`, `roles`, `is_admin`, `organizational_authority`, `approval_authority`, `delegations`) are added to `Identity`, `Principal`, or `ActorContext`.

## 3. Authority Note

[`DECISION-AUTHORITY-POLICY.md`](../governance/DECISION-AUTHORITY-POLICY.md) is currently `Proposed` and has no normative delegation effect.

Therefore, L4 creates **NO** delegated organizational authority. Residual decision authority remains with the Arvectum OS owner under Accepted architecture and governance until a canonical approved delegation exists.

The owner-operated actor is **NOT** "admin" merely because it is the current owner operator. Owner authority is never encoded into Principal Identity.

## 4. Local Operational State

The local state is stored in an external, owner-only directory structure:

```text
$HOME/.arvectum-os/p6-05-l4-runtime/
  local-context/
    organization-operator.json
```

### Storage Controls
- **Location:** Outside every Git worktree and outside the Arvectum OS checkout.
- **Permissions:** Directories `0700` or stricter; state file `0600` or stricter. Existing broad permissions are never auto-repaired and fail closed.
- **Symlinks:** Symlinks in target paths, parents, or state files are strictly rejected across all components.
- **Exact Bounded Schema:** Unknown fields fail closed (`CONTEXT_SCHEMA_UNEXPECTED_FIELD`).
- **Secrets/Credentials:** Zero secrets, zero credentials, zero EIS tokens, zero passwords. PASS claims are guaranteed by exact-schema admission.
- **Operational Nature:** The L4 local context is operational state for this bounded internal runtime. It is not a Stable/public identity-management contract or Production IAM system.

## 5. Real Identity Issuance Model

Identities are issued according to RFC-0002 principles:
- **Opaque Values:** Identity values are opaque, stable, randomly generated identifiers (e.g. 128-bit hex tokens).
- **Independence:** Identities are strictly independent of company name, INN, OGRN, email, GitHub username, hostname, or personal names.
- **Semantic Structure:**
  - **Organization Identity:** `namespace = "organization"`, `value = <opaque>`, `scope = "platform"`
  - **Principal Identity:** `namespace = "principal"`, `value = <opaque>`, `scope = <organization identity value>`
- **Category:** `human`
- **Operating Mode:** `owner-operated`
- **Display Label:** `context_label = "ООО «Арвектум»"` is non-authoritative presentation metadata only.

## 6. Owner Authorization Gate

Execution requires the exact owner assertion:
```text
OWNER_APPROVES_P6_05_L4_INTERNAL_ORGANIZATION_OPERATOR_BOOTSTRAP
```
This is an execution gate, not a credential. Any missing or incorrect assertion fails closed before generating identities, creating files, or performing any filesystem mutations with `OWNER_AUTHORIZATION_REQUIRED`.

## 7. State File Schema

The bounded schema version is `p6.05-l4-local-context-1`:

```json
{
  "schema_version": "p6.05-l4-local-context-1",
  "organization": {
    "identity": {
      "namespace": "organization",
      "value": "<opaque>",
      "scope": "platform"
    },
    "context_label": "ООО «Арвектум»"
  },
  "operator": {
    "identity": {
      "namespace": "principal",
      "value": "<opaque>",
      "scope": "<organization identity value>"
    },
    "principal_category": "human",
    "operating_mode": "owner-operated"
  },
  "authority": {
    "authorization_grants": [],
    "delegations": [],
    "organizational_authority_claimed": false
  },
  "authentication": {
    "evidence_refs": []
  },
  "bootstrap": {
    "scope": "P6.05-L4",
    "owner_authorization_asserted": true
  }
}
```

## 8. Tenant Boundary

Tenant context is explicitly not introduced in P6.05-L4:
- `tenant_context = not introduced in P6.05-L4`
- The current bounded runtime is single-Organization.
- In accordance with RFC-0003, if multi-tenant partitioning is introduced in later stages, the one-tenant-to-one-governing-Organization invariant applies.

## 9. Idempotent Reuse and Continuity

When the state file already exists:
- The helper strictly verifies permissions and schema invariants.
- It reuses existing Organization and Principal identities without regeneration.
- It returns `context_reused=true, context_created=false`.
- If the state file is malformed, inconsistent, or permissions are too broad, it **fails closed**. It never silently repairs or overwrites.

### Continuity Rule
If the local context file is lost after later P6.05 execution has relied on those identities:
**DO NOT silently generate a replacement.** Fail closed and require explicit owner-approved rebootstrap and reconciliation of identity continuity.

## 10. Operational Tools

### Bootstrap Helper
```bash
python3 reference/python/p6_05_l4_bootstrap_internal_context.py \
  --target-root "$HOME/.arvectum-os/p6-05-l4-runtime" \
  --owner-authorization "OWNER_APPROVES_P6_05_L4_INTERNAL_ORGANIZATION_OPERATOR_BOOTSTRAP"
```

### Read-Only Preflight
```bash
python3 reference/python/p6_05_l4_operator_context_preflight.py \
  --state-file "$HOME/.arvectum-os/p6-05-l4-runtime/local-context/organization-operator.json"
```

### Safe PASS Preflight Output Sample
```text
p6_05_l4_status=PASS
context_created=false
context_reused=true
organization_context=configured
operator_principal=configured
principal_category=human
actor_context=configured
organization_scope_explicit=true
principal_attributable=true
authorization_grants=0
delegations=0
organizational_authority_claimed=false
authentication_evidence_refs=0
tenant_context_introduced=false
product_context_introduced=false
context_outside_source_control=true
context_owner_only=true
credentials_present=false
secrets_present=false
canonical_mutation=false
product_invoked=false
eis_invoked=false
network_invoked=false
external_actions=false
```

### Truthful Safe FAIL Output Sample
When any invariant fails, unproven facts are reported as `not_proven`:
```text
p6_05_l4_status=FAIL
failure_code=CONTEXT_SCHEMA_UNEXPECTED_FIELD
context_created=false
context_reused=false
organization_context=unconfigured
operator_principal=unconfigured
principal_category=unconfigured
actor_context=unconfigured
organization_scope_explicit=not_proven
principal_attributable=not_proven
authorization_grants=not_proven
delegations=not_proven
organizational_authority_claimed=not_proven
authentication_evidence_refs=not_proven
tenant_context_introduced=not_proven
product_context_introduced=not_proven
context_outside_source_control=false
context_owner_only=false
credentials_present=not_proven
secrets_present=not_proven
canonical_mutation=false
product_invoked=false
eis_invoked=false
network_invoked=false
external_actions=false
```

## 11. Fail-Closed Error Codes

| Error Code | Meaning |
|---|---|
| `OWNER_AUTHORIZATION_REQUIRED` | Missing or mismatching owner authorization assertion |
| `TARGET_INSIDE_GIT_WORKTREE` | Target path is located inside a git worktree |
| `TARGET_INSIDE_ARVECTUM_CHECKOUT` | Target path is inside the Arvectum OS checkout |
| `TARGET_SYMLINK_NOT_ALLOWED` | Target directory or ancestor is a symlink |
| `CONTEXT_FILE_SYMLINK_NOT_ALLOWED` | State file is a symlink |
| `CONTEXT_PERMISSIONS_TOO_BROAD` | Directory is not 0700 or file is not 0600 |
| `CONTEXT_SCHEMA_UNSUPPORTED` | Unsupported schema version or bootstrap scope |
| `CONTEXT_SCHEMA_UNEXPECTED_FIELD` | Unknown or unexpected field in state file schema |
| `ORGANIZATION_CONTEXT_LABEL_MISMATCH` | Context label does not match exact bounded internal label |
| `CONTEXT_MALFORMED` | Malformed JSON or invalid structural shape |
| `ORGANIZATION_IDENTITY_INVALID` | Invalid namespace/value/scope for Organization Identity |
| `PRINCIPAL_IDENTITY_INVALID` | Invalid namespace/value for Principal Identity |
| `PRINCIPAL_ORGANIZATION_SCOPE_MISMATCH` | Principal scope does not match Organization Identity value |
| `PRINCIPAL_CATEGORY_UNSUPPORTED` | Principal category is not `human` |
| `OPERATING_MODE_UNSUPPORTED` | Operating mode is not `owner-operated` |
| `AUTHORIZATION_GRANTS_NOT_EMPTY` | Grants list is non-empty |
| `DELEGATIONS_NOT_EMPTY` | Delegations list is non-empty |
| `ORGANIZATIONAL_AUTHORITY_NOT_ALLOWED` | `organizational_authority_claimed` is not `false` |
| `AUTHENTICATION_EVIDENCE_NOT_EMPTY` | `evidence_refs` list is non-empty |
| `CONTEXT_ALREADY_EXISTS_RACE` | State file was created concurrently |
| `LOCAL_FILESYSTEM_OPERATION_FAILED` | Filesystem IO or permission failure |

## 12. Current Status and Next Steps

P6.05-L4 mechanisms, helpers, and verification tests are prepared and verified under synthetic test fixtures. Real owner-operated execution against `$HOME/.arvectum-os/p6-05-l4-runtime` remains required to establish real local operational context and record final L4 PASS evidence.
