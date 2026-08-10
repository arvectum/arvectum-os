# P6.05-L3 — Mixed Legacy Source Recovery

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Context

The existing P6.05-L3 discovery manifest contains seven verified `ai-corporation` checkouts and seven explicit legacy env sources containing the EIS credential key.

The owner-operated retry after PR #93 proved that at least one of those seven env sources is outside every supplied verified checkout. The safe failure was `ENV_OUTSIDE_VERIFIED_CHECKOUTS`. No secret value was read, migrated, printed, hashed, exported or committed before that blocker.

Earlier L3 recovery notes assumed that every discovered source was repo-local. The observed manifest shows that this assumption is too narrow for the already-created bounded discovery set. This note refines the implementation recovery path without changing the L3 exit condition or creating a general filesystem secret-discovery policy.

## 2. Canonical basis

The applicable authority remains:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`, including sensitivity-appropriate reusable-secret handling, least privilege, minimization and fail-closed behavior;
- RFC-0004, RFC-0005 and RFC-0006 boundaries remain unchanged.

No Accepted ADR governs this bounded local migration mechanism. No new RFC or ADR is required because this correction is local, reversible, non-public, non-production and does not establish a cross-cutting platform technology contract.

## 3. Source classes

For the existing explicit discovery manifest, recovery distinguishes two classes:

1. **Repo-local legacy source** — an eligible `.env.local` / `*.env` source physically inside one of the independently verified `ai-corporation` checkouts.
2. **Standalone legacy source** — an eligible explicit env source outside all supplied verified checkouts and not owned by any valid Git worktree.

The second class does **not** mean that arbitrary local env files are generally authorized for mutation. It applies only to env paths already present in the bounded local-only discovery manifest whose expected source count is fixed for this recovery.

If an apparent standalone source is owned by any valid Git worktree outside the supplied verified `ai-corporation` set, recovery fails closed with `STANDALONE_ENV_OWNED_BY_UNVERIFIED_GIT_REPO`.

Invalid/orphaned non-symlink `.git` debris is not treated as repository authority. Ancestor inspection continues so broken debris cannot hide an outer valid Git repository. A symlinked `.git` marker fails closed.

## 4. Canonical helper for the observed mixed set

Use:

```text
reference/python/p6_05_l3_recover_mixed_legacy_sources.py
```

The helper:

- verifies the existing discovery file and exact expected checkout/env counts;
- independently verifies every supplied checkout as its own Git worktree root and expected `arutyunoveth/ai-corporation` origin;
- sanitizes Git location-affecting environment variables for Git subprocesses;
- classifies every env as repo-local or standalone without emitting paths;
- requires repo-local sources to be untracked by their selected verified checkout;
- rejects a standalone source owned by any valid unverified Git repository;
- makes each accepted source owner-only before secret reliance;
- compares all configured secret values only in memory and requires exact agreement before destination creation or source scrubbing;
- treats only actual verified product checkout roots as source-control exclusion roots for destination placement;
- preserves the Arvectum OS checkout exclusion rule;
- removes only the EIS token assignment from accepted supplied env sources while preserving unrelated content;
- captures every verified product checkout HEAD and tracked status before and after migration and requires exact equality;
- verifies no supplied source retains the EIS token key after migration;
- emits only safe counts, booleans and failure codes.

Safe output additionally includes:

```text
repo_local_source_count=<number>
standalone_source_count=<number>
```

These are classification counts only. They do not disclose paths or filenames.

## 5. Security boundary

This correction does not authorize:

- broad filesystem secret discovery;
- rewriting arbitrary env files outside the explicit manifest;
- modifying files owned by an unverified Git repository;
- choosing among differing credential values;
- token rotation, reissue or revocation;
- product invocation;
- EIS/SOAP requests;
- network/TLS/proxy actions;
- Product Contract or capability lifecycle changes.

If configured source values differ, migration fails before destination creation or source scrubbing. If a source is owned by an unverified Git repository, recovery fails before secret reliance.

## 6. Test evidence

`reference/python/tests/test_p6_05_l3_mixed_legacy_sources.py` proves with synthetic credentials that:

- one repo-local and one standalone non-Git source can migrate together into the same external owner-only destination;
- destination placement remains valid even when the standalone source parent shares a broader local filesystem ancestor with the destination;
- a standalone-looking source inside an unverified Git repository fails closed before migration;
- differing repo-local and standalone secret values fail before destination creation or source mutation;
- secret values do not appear in safe output.

Existing L3 migration, baseline-preservation, filename-boundary, nested-checkout, verified-container and secure-local-config tests remain applicable.

## 7. Closure rule

This correction does not complete P6.05-L3. L3 remains open until the owner-operated Mac executes this mixed-source recovery against the same seven-checkout/seven-env discovery manifest, secure local configuration preflight passes, all bounded L3 synthetic tests pass, and the Arvectum OS execution checkout remains clean.

P6.05 does not advance to L4 until that safe PASS evidence is canonically reviewed.
