# P6.05-L3 — Nested Checkout Legacy Source Ownership

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Context

The owner-operated P6.05-L3 recovery discovered seven verified `ai-corporation` checkouts and seven legacy env sources containing the EIS credential key. A previous recovery implementation mapped an env to a checkout by plain filesystem containment. That is insufficient when one valid Git checkout is physically nested inside another: the same env path can then be contained by more than one supplied checkout even though Git has one nearest working-tree owner.

The observed safe blocker was `ENV_CHECKOUT_MAPPING_AMBIGUOUS`. No secret was read, migrated, printed, hashed, exported or committed before that blocker.

## 2. Canonical basis

The applicable authority remains Constitution `1.2.0`, Accepted RFC-0001 `1.0.0`, and Accepted RFC-0003 `1.0.0`. RFC-0004, RFC-0005 and RFC-0006 boundaries remain unchanged. No Accepted ADR governs this bounded local mapping mechanism.

This correction does not create a new secret-management architecture, Git topology contract, Product Contract change, capability lifecycle decision, Production claim or external action.

## 3. Ownership rule

For each explicitly discovered legacy env source, recovery now asks Git for the nearest worktree root using `git rev-parse --show-toplevel` from the env's containing directory.

The returned root must:

1. resolve successfully as a Git worktree root;
2. exactly equal one of the already supplied and repository-remote-verified discovery checkouts;
3. contain the env source after path resolution;
4. retain the existing requirement that the env itself is untracked by that worktree.

This is stronger than choosing the longest containing path heuristically. Git's own nearest-worktree semantics determine local ownership, while the complete verified discovery set remains the allowed boundary.

If the nearest Git owner is not present in the supplied discovery set, recovery fails closed with `ENV_GIT_OWNER_NOT_IN_DISCOVERY`. It does not silently attach the env to an outer checkout.

Each supplied checkout is also required to be its own Git worktree root. A supplied subdirectory that merely happens to sit inside a repository is rejected.

## 4. Security and evidence properties

The ownership probe uses only Git metadata and filesystem paths already present in the local-only discovery manifest. Safe output still contains only counts, booleans and failure codes.

Recovery does not emit checkout paths, env paths, tracked filenames, diffs, remote URLs, token values, token hashes or environment contents.

No reset, stash, checkout, restore, stage, commit or cleanup of product work is performed. Existing tracked state and `HEAD` remain protected by the baseline-before/after equality check already defined for P6.05-L3.

## 5. Test evidence

`reference/python/tests/test_p6_05_l3_nested_checkout_mapping.py` proves that:

- an outer verified `ai-corporation` checkout and an inner verified `ai-corporation` checkout can both be in the discovery set;
- an env in the outer checkout maps to the outer worktree;
- an env in the nested checkout maps to the nested worktree;
- both matching secrets can migrate through the existing canonical multi-source helper without secret output;
- an env whose nearest Git owner is a nested repository omitted from the discovery set fails closed before migration and without path or secret disclosure.

## 6. Closure rule

This correction does not complete P6.05-L3. L3 remains open until the owner-operated Mac repeats canonical recovery against the same complete seven-checkout/seven-env discovery set, the secure local configuration preflight passes, and the bounded L3 synthetic tests pass.

No product, EIS, SOAP, TLS/proxy, network, credential-rotation/revocation or external action is authorized by this note.
