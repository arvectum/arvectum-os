# P6.05-L3 — Owner-authorized tender-app legacy source recovery

Status: `Prepared / owner-operated authorization and local evidence required`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Context

The fixed P6.05-L3 discovery manifest contains seven verified `arutyunoveth/ai-corporation` checkouts and seven explicit legacy env sources.

Safe local diagnostics established the source classification without reading env contents:

- two sources are repo-local to supplied verified `ai-corporation` checkouts;
- four sources are standalone non-Git local files;
- one source is an untracked env owned by a valid Git worktree whose origin is exactly `arutyunoveth/tender-app`;
- that source is not tracked by `tender-app`;
- no secret value or hash was read or emitted during classification.

`tender-app` is a separate historical procurement repository. Its repository identity does not by itself grant Arvectum OS authority to mutate files inside its worktree.

## 2. Canonical basis

Applicable authority remains:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`;
- RFC-0004/0005/0006 boundaries unchanged.

The Constitution requires security and organizational control to remain structural, requires material decisions to preserve decision authority or approval proportionate to impact, and permits bounded reversible implementation where it does not compromise security or governance.

RFC-0003 requires reusable secrets to receive sensitivity-appropriate handling, to remain out of ordinary logs/canonical payloads/model prompts, and keeps Organizational Authority distinct from technical access.

No new RFC or ADR is required because this recovery does not define a general repository trust model, secret manager, public contract, Product Contract, capability lifecycle change, production topology, or cross-cutting irreversible architecture.

## 3. Bounded authorization decision

The only newly admitted source class is:

```text
exact Git origin: arutyunoveth/tender-app
source state: untracked env already present in the fixed P6.05-L3 discovery manifest
operation: remove only ZAKUPKI_GOV_RU_SOAP_TOKEN after full in-memory consistency proof and safe destination creation/reuse
```

Repository identity alone is insufficient. The owner-operated invocation must include the exact assertion:

```text
OWNER_APPROVES_TENDER_APP_LEGACY_SECRET_SCRUB
```

Absence or alteration of that assertion fails closed before secret reading or mutation.

This assertion is deliberately operation-specific. It does not authorize:

- future `tender-app` files;
- tracked `tender-app` files;
- `tender-ai`;
- another repository under the same GitHub account;
- an external repository;
- arbitrary Git-owned env files;
- credential rotation, revocation or reissue;
- product or EIS execution.

## 4. Recovery invariants

Use:

```text
reference/python/p6_05_l3_recover_owner_authorized_tender_app.py
```

The helper must:

1. consume only the existing fixed discovery manifest;
2. preserve expected 7 checkout / 7 env counts;
3. independently verify all supplied `ai-corporation` checkouts;
4. require exactly one Git-owned out-of-set source and require its origin to be exactly `arutyunoveth/tender-app`;
5. require that source to be untracked;
6. require the exact owner authorization assertion before secret reading/mutation;
7. capture HEAD and tracked status for all seven `ai-corporation` checkouts and the `tender-app` owner before migration;
8. allow unrelated pre-existing tracked dirtiness but require exact before/after equality;
9. compare all configured source secret values only in memory;
10. require all configured values to agree before creating a new destination or scrubbing any source;
11. create or safely reuse only the external owner-only destination;
12. scrub the token assignment from every explicit matching legacy source;
13. require zero supplied envs to retain the EIS token key afterward;
14. emit only safe counts, booleans and failure codes.

## 5. Security properties

The recovery must not emit:

- checkout or env paths;
- env filenames;
- Git worktree paths;
- remote URLs;
- Git diffs or tracked filenames;
- secret values;
- secret hashes;
- environment dumps.

It must not:

- stage, commit, reset, stash or clean any repository;
- create a secret-bearing backup;
- invoke `ai-corporation` or `tender-app` application code;
- call EIS/SOAP;
- perform network requests;
- change PAC/TLS/proxy settings;
- rotate, revoke, reissue or otherwise change credential lifecycle state;
- start P6.05-L4.

## 6. Failure semantics

The helper fails closed if:

- authorization assertion is absent or wrong;
- the Git owner is not exactly `arutyunoveth/tender-app`;
- the tender-app env is tracked;
- more or fewer than one authorized tender-app source is present;
- source counts changed;
- a verified product checkout changed identity;
- any source permissions or filename scope are unsafe;
- configured secrets differ;
- destination is unsafe or mismatching;
- any tracked state or HEAD changes during recovery;
- any supplied source retains the secret key after a claimed successful migration.

## 7. Closure rule

This document does not complete L3.

L3 may proceed to secure local configuration preflight only after owner-operated recovery returns PASS with safe evidence proving:

- explicit authorization asserted;
- exact `tender-app` source count = 1;
- all 7 env sources untracked;
- all product and tender-app HEAD/tracked states unchanged;
- secret consistency true;
- all sources scrubbed;
- zero source envs retain the EIS token key;
- no secret output/hash/commit/backup;
- no product/EIS/network/external action.

Only subsequent preflight, negative tests and canonical closure may advance P6.05 to L4.
