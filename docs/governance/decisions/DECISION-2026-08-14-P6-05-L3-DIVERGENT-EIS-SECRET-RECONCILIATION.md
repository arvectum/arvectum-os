# DECISION-2026-08-14 — P6.05-L3 Divergent Legacy EIS Secret Reconciliation

Status: `Approved`
Date: `2026-08-14`
Decision owner: `ООО «Арвектум»`
Task classification: `platform`
Scope: `P6.05-L3 only`
Constitution: `1.2.0`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Related roadmap: `docs/roadmap/P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`

## 1. Context

During owner-operated execution of `P6.05-L3 — Secure local configuration + secrets boundary`, canonical multi-source secret recovery executed across the seven fixed discovered legacy env sources and safely failed closed with `CANONICAL_MIGRATION_FAILED` / `SOURCE_SECRETS_DIFFER`.

In-memory constant-time equality diagnostic of the seven secret-bearing sources was subsequently executed under owner authorization to establish the exact divergence structure without exposing, hashing, encoding or persisting secret values.

## 2. Diagnostic Facts

The read-only in-memory diagnostic established:

- fixed source checkout count: 7;
- fixed source env count: 7;
- exactly 2 distinct credential equality classes were observed in memory;
- class sizes were 5 and 2;
- exactly 4 sources were `.env.local`;
- all four `.env.local` sources belonged to the same 5-source equality class;
- the 5-source equality class corresponded to diagnostic label `C2`;
- the 2-source equality class corresponded to diagnostic label `C1`;
- source ownership structure: 2 manifest `ai-corporation` repo-local sources, 4 standalone sources, and 1 source inside another local Git worktree;
- no source was modified during classification;
- no secret was printed, hashed, encoded, or persisted;
- no product, EIS, network, or external action occurred.

## 3. Owner Decision

### 3.1 Credential Selection

The owner explicitly approves the 5-source equality class containing all four `.env.local` sources as the single authorized credential to establish the `P6.05-L3` external local secret boundary (`<local-root>/local-secrets/eis-soap-token`).

The diagnostic label `C2` is recorded for provenance, but implementation must select by the structural invariant (the unique equality class containing all 4 `.env.local` sources in the 5+2 distribution), not merely by label.

### 3.2 Legacy Source Scrub

The owner explicitly authorizes removal of the `ZAKUPKI_GOV_RU_SOAP_TOKEN` assignment from all seven fixed legacy sources only after the approved selected value has been safely established in the external owner-only destination.

The two values belonging to the other 2-source equality class (`C1`) are authorized to be treated as stale local legacy copies for the purpose of this bounded local cleanup.

Deleting local stale copies does NOT mean:

- EIS credential revocation;
- credential rotation;
- proof that the other credential is externally invalid;
- a general secret lifecycle policy.

### 3.3 GitHub Migration Context and Repository Boundaries

Current active repositories relevant to this workflow:

- `arvectum/arvectum-os`
- `arvectum/ai-corporation`

The historical account identity `arutyunoveth` is migration-era provenance and must no longer be an operational dependency for current L3 execution.

No active `arvectum/tender-app` repository is established by this decision.

The single fixed legacy env source located inside another local Git worktree is authorized ONLY as a source already contained in the owner-approved fixed L3 discovery manifest and subject to the exact bounded structural checks defined by this correction. This does not create a general trust rule for arbitrary local Git worktrees.

## 4. Non-goals

This decision does not:

- change any Product Contract;
- promote capability lifecycle state;
- make a Production readiness claim;
- authorize live EIS action or network requests;
- establish a permanent/public secret-management contract.
