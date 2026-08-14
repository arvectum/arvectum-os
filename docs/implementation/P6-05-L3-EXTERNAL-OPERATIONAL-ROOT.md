# P6.05-L3 External Operational Root Correction

Status: `Implementation correction`
Scope: `P6.05-L3 only`
Constitution: `1.2.0`
Relevant Accepted RFCs: `RFC-0001 1.0.0`, `RFC-0003 1.0.0`

## Context

Owner-operated P6.05-L3 diagnostics proved that the originally selected local root is contained by exactly one verified `arutyunoveth/ai-corporation` checkout. Consequently, the intended secret destination fails the existing `DESTINATION_INSIDE_SOURCE_CHECKOUT` control before any secret source is read.

The containment control is correct and remains unchanged. The correction is to place the L3 operational configuration, secret destination and future local-only evidence under a separate owner-only root outside every Git worktree.

## Decision

For the remaining P6.05-L3 owner-operated work, use a dedicated external operational root that:

- is outside every valid Git worktree;
- is outside the Arvectum OS checkout;
- uses owner-only directories (`0700` or stricter);
- contains a fixed non-secret configuration file with owner-only permissions (`0600` or stricter);
- contains a separate owner-only secret destination;
- contains local-only evidence output that never includes secret values or hashes.

The helper `reference/python/p6_05_l3_prepare_external_operational_root.py` prepares this structure without reading or writing the EIS secret. It creates only the exact bounded non-secret configuration required for P6.05-L3 and fails closed if existing content differs.

## Migration continuity

The existing fixed discovery manifest remains the input authority for the seven already-discovered legacy env sources. It is not regenerated merely because the output root changes.

Under the 2026-08-14 owner decision (`DECISION-2026-08-14-P6-05-L3-DIVERGENT-EIS-SECRET-RECONCILIATION.md`), the single fixed legacy env source located inside another local Git worktree is authorized as part of the bounded 2/4/1 fixed source structure. Reconciliation uses `reference/python/p6_05_l3_reconcile_owner_selected_divergent_sources.py` against the external secret destination. The source-containment checks for all 8 repositories (7 manifest checkouts + 1 other local Git worktree) and Arvectum OS remain mandatory and must pass without exception.

The old local root is not deleted, moved, cleaned or rewritten as part of this correction. Any later cleanup is a separate bounded operation after L3 closure evidence is complete.

## Non-goals

This correction does not:

- weaken `DESTINATION_INSIDE_SOURCE_CHECKOUT` or other fail-closed controls;
- authorize any new repository or credential source;
- read, print, hash, export or back up the EIS token;
- invoke the product, EIS, SOAP, network or another external system;
- rotate, revoke or reissue credentials;
- establish a general platform secret-management architecture;
- promote a capability lifecycle state;
- create a Product Contract, production claim or external conformance claim.

## Closure condition

P6.05-L3 remains open until owner-operated evidence proves all of the following:

1. external operational root preparation passes;
2. the owner-approved seven-source divergent reconciliation passes using the external secret destination;
3. all source token assignments are scrubbed and the selected 5-source class was established;
4. product and other local Git worktree HEAD/tracked states remain unchanged;
5. secure local config preflight passes against the external config and secret files;
6. the bounded L3 regression set passes;
7. no product, EIS, network or external action occurred.
