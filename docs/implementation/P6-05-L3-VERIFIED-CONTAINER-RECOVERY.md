# P6.05-L3 — Verified-container Legacy Secret Recovery

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Context

The owner-operated P6.05-L3 source set remains seven verified `ai-corporation` checkouts and seven explicitly discovered legacy env sources containing the EIS credential key.

The previous nested-checkout correction used `git rev-parse --show-toplevel` from each env directory to infer its nearest worktree owner. The safe owner-operated retry proved a narrower limitation of that mechanism: all seven supplied checkouts passed independent worktree-root and remote verification, but Git discovery from at least one env directory failed with `GIT_WORKTREE_ROOT_NOT_VERIFIED` before any source was read or migrated.

That failure can occur when the env path contains an orphaned or broken nested `.git` marker, or when ambient Git location variables affect repository discovery. Neither condition invalidates an already independently verified containing checkout or authorizes arbitrary repository discovery.

This note replaces the env-directory Git-discovery assumption for the current L3 recovery path. It does not change the L3 exit condition or establish a general Git topology or secret-management architecture.

## 2. Canonical basis

The applicable authority remains:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`, including sensitivity-appropriate reusable-secret handling, least privilege, minimization and fail-closed behavior;
- RFC-0004, RFC-0005 and RFC-0006 boundaries remain unchanged.

No Accepted ADR governs this bounded local mapping mechanism. No new RFC or ADR is required because this is a reversible, local, non-public implementation correction and does not select a durable cross-cutting platform technology contract.

## 3. Verified-container rule

Use:

```text
reference/python/p6_05_l3_recover_verified_containers.py
```

The helper preserves the complete explicit discovery set and applies these rules:

1. every supplied checkout must independently resolve as its own Git worktree root;
2. every supplied checkout `origin` must identify `arutyunoveth/ai-corporation`;
3. Git location-affecting ambient variables such as `GIT_DIR`, `GIT_WORK_TREE` and `GIT_CEILING_DIRECTORIES` are removed from the helper's Git subprocess environment;
4. each env must be a bounded `.env.local` / `*.env` regular source already present in the explicit discovery manifest;
5. the env is attached to the most specific supplied verified checkout path that contains it after path resolution;
6. the env must be untracked by that selected verified checkout;
7. any **valid** intervening Git worktree not present in the supplied discovery set fails closed with `ENV_GIT_OWNER_NOT_IN_DISCOVERY`;
8. an invalid/orphaned non-symlink `.git` marker that Git cannot resolve is not treated as a verified repository boundary and does not override the explicit verified-container mapping;
9. a symlinked intervening `.git` marker fails closed;
10. the existing before/after `HEAD` and tracked-status equality proof remains mandatory.

The most-specific verified container is not claimed to be a universal Git ownership model. It is only the bounded source container for this explicit migration operation after every supplied checkout has already been independently verified.

## 4. Why invalid `.git` debris may be tolerated

L3 is not trying to repair repository topology. It is removing one reusable credential assignment from an explicitly discovered owner-only untracked env while preserving all unrelated file content.

A broken `.git` pointer can prevent `git rev-parse` from walking upward even when the file is physically contained by a separately verified `ai-corporation` checkout. Treating that broken marker as authoritative would leave a known reusable secret copy in place without adding a meaningful security control.

The helper therefore distinguishes:

- **valid unsupplied nested Git repository** — security boundary is not proven; fail closed;
- **invalid/orphaned non-symlink `.git` marker** — not a verified repository authority; continue only through the already verified containing checkout and explicit untracked-source checks.

No broken marker is deleted, repaired or rewritten by L3.

## 5. Security and evidence properties

The helper does not emit:

- checkout or env paths;
- remote URLs;
- tracked filenames or diffs;
- environment dumps;
- secret values or hashes.

It does not reset, stash, restore, stage, commit or clean product work. It does not invoke the product, EIS, SOAP, network, TLS/proxy checks or external actions.

The secret migration still requires all configured source values to agree in memory before destination creation or source scrubbing. The external destination is never overwritten with a differing value.

## 6. Test evidence

`reference/python/tests/test_p6_05_l3_verified_container_recovery.py` proves that:

- an explicitly discovered untracked env beneath an orphaned/broken nested `.git` marker can migrate through the verified containing checkout without secret output;
- a valid nested repository omitted from the discovery set still fails closed before migration;
- ambient Git location variables do not redirect checkout verification or env mapping.

Existing P6.05-L3 migration, baseline-preservation, filename-boundary, nested-checkout and secure-local-config tests remain applicable.

All test credentials are synthetic and carry no external authority.

## 7. Closure rule

This correction does not complete P6.05-L3. L3 remains open until the owner-operated Mac runs the verified-container recovery against the same complete seven-checkout/seven-env discovery set, secure local configuration preflight passes, all bounded L3 tests pass, and the Arvectum OS execution checkout remains clean.

P6.05 does not advance to L4 until that safe PASS evidence is canonically reviewed.
