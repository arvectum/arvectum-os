# P6.05-L3 — Unverified Git Owner Diagnostic

Status: `Prepared / owner-operated Mac diagnostic required`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Context

The fixed P6.05-L3 discovery manifest contains seven verified `ai-corporation` checkouts and seven explicit legacy env sources. Owner-operated recovery evidence classified two sources as repo-local and four as standalone non-Git sources before stopping on the seventh source with `STANDALONE_ENV_OWNED_BY_UNVERIFIED_GIT_REPO`.

This proves that the seventh source is outside every supplied verified product checkout but is owned by another valid local Git worktree. The repository identity of that owner is not yet known from safe evidence.

L3 must not weaken fail-closed behavior by treating arbitrary Git-owned files as authorized migration sources. The next bounded step is therefore read-only ownership classification, not migration.

## 2. Canonical basis

Applicable authority remains:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`, including secret handling, minimization, least privilege and fail-closed requirements;
- RFC-0004/0005/0006 boundaries remain unchanged.

No new RFC or ADR is required for this diagnostic because it is local, reversible, non-public, does not define a durable secret-management or repository-discovery contract, and performs no mutation.

## 3. Diagnostic helper

Use:

```text
reference/python/p6_05_l3_diagnose_unverified_env_owner.py
```

The helper consumes the existing local-only discovery manifest and expected 7/7 counts.

It:

1. verifies the supplied seven `ai-corporation` checkouts through the existing sanitized Git verification path;
2. classifies each manifest env as:
   - inside a supplied verified product checkout;
   - standalone with no valid Git owner;
   - owned by a valid Git worktree not present in the supplied checkout set;
3. for an unverified Git owner, classifies only the remote category as:
   - `ai_corporation`;
   - `arvectum_os`;
   - `other_remote`;
   - `no_origin`;
4. reports only whether the env is tracked or untracked by that owner;
5. emits counts and booleans only.

## 4. Security properties

The diagnostic does **not** read env file contents. Therefore it does not read, compare, print or hash the EIS token.

It does not emit:

- checkout or env paths;
- env filenames;
- remote URLs;
- Git diffs or tracked filenames;
- secret values or hashes;
- environment dumps.

It does not chmod, rewrite, delete, move, stage, commit, reset, stash or clean any source. It does not invoke the product, EIS, SOAP, network, TLS/proxy path or any external action.

## 5. Interpretation

The diagnostic does not itself authorize migration.

- `unverified_owner_ai_corporation_count > 0` means the manifest omitted at least one valid `ai-corporation` Git owner. A subsequent canonical correction may explicitly verify and include that owner in the bounded recovery proof before migration.
- `unverified_owner_arvectum_os_count > 0` means a legacy source is inside the Arvectum OS repository boundary. L3 must stop and inspect whether the source is tracked/untracked and why discovery included it; it must not migrate it as a product source automatically.
- `unverified_owner_other_remote_count > 0` means another repository owns the source. L3 remains blocked unless a separate bounded authority decision proves that repository is an authorized credential source.
- `unverified_owner_no_origin_count > 0` means repository identity cannot be established from origin metadata; L3 remains blocked.
- any tracked env requires separate canonical review before any source mutation.

## 6. Test evidence

`reference/python/tests/test_p6_05_l3_unverified_owner_diagnostic.py` proves with synthetic repositories that:

- an omitted `ai-corporation` owner is classified without path, remote or secret output;
- an Arvectum OS owner is distinguished from product ownership;
- an unrelated remote is not accepted as `ai-corporation`;
- a repository without `origin` remains unresolved rather than guessed;
- tracked/untracked state is emitted only as counts;
- env contents and secret values are not read by the diagnostic.

All test credentials are synthetic and have no external authority.

## 7. Closure rule

This diagnostic does not complete L3 and does not advance P6.05 to L4. The next action depends only on the safe owner-category result from the owner-operated Mac.
