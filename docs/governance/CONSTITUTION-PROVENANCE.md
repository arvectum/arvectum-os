# Constitution 1.2.0 Provenance Record

Status: `Closed`
Recorded: `2026-08-06`
Resolved: `2026-08-07`
Category: `governance`
Canonical Constitution: `1.2.0`
Resolution decision: `DECISION-2026-08-07-CONSTITUTION-1.2-PROVENANCE-REPAIR`

## Purpose

This document records and resolves the governance provenance gap for the transition to Constitution `1.2.0`.

It does not amend, reinterpret or weaken the Constitution.

The canonical repository contains Constitution version `1.2.0` with status `Ratified`. Constitution `1.2.0` remains the frozen governing baseline.

## Resolution

The provenance gap is closed using confirmed immutable evidence from repository history plus explicit current owner approval of the governance repair.

The historical constitutional amendment chain is:

```text
Constitution 1.0.0
        ↓
legacy RFC-0000 constitutional amendment
commit 611278850e2af5e159332650858574a3c647330b
        ↓
Constitution 1.1.0
        ↓
legacy constitutional amendment RFC-0001
commit bd012cc435461fe903d6f9420282a0f906ca5bbd
        ↓
Constitution 1.2.0 — Ratified, current and frozen
```

The historical amendment artifacts contain the required amendment substance and explicit owner approval.

## Confirmed evidence

### Constitution 1.0.0 → 1.1.0

Historical artifact:

- title: `RFC-0000: Amend the Arvectum OS Constitution to Version 1.1.0`;
- historical path: `docs/rfcs/RFC-0000-constitution-1.1.md`;
- status recorded in the artifact: `Accepted`;
- resulting version: `1.1.0`;
- commit: `611278850e2af5e159332650858574a3c647330b`;
- blob SHA: `835425ca01705adf07da724389038ea2228f15ce`;
- owner approval is explicitly stated in the historical artifact on `2026-08-06`.

The amendment introduces and strengthens organizational intelligence, product experimentation before platformization, domain boundaries, organizational control and portability, governed organizational assets, value proportionality and architecture-before-irreversible-implementation rules.

### Constitution 1.1.0 → 1.2.0

Historical artifact:

- title: `RFC-0001: Amend the Arvectum OS Constitution to Version 1.2.0`;
- historical path: `docs/rfcs/RFC-0001-constitution-1.2.md`;
- status recorded in the artifact: `Accepted`;
- resulting version: `1.2.0`;
- commit: `bd012cc435461fe903d6f9420282a0f906ca5bbd`;
- blob SHA: `85b3cc9895dc4a398a0e30428926fe486f62062a`;
- owner approval is explicitly stated in the historical artifact on `2026-08-06`.

The amendment identifies the constitutional areas changed, explains the rationale, records preserved invariants, addresses compatibility/migration, defines acceptance criteria and increments the Constitution to `1.2.0`.

It strengthens security/privacy/isolation, proportional decision governance, replaceable vendor-specific workflow dependencies and architecture-neutral domain-boundary wording.

## Historical identifier collision

Repository history also confirms a governance migration anomaly.

Before the current canonical RFC index was finalized, the repository used a historical `docs/rfcs/` RFC sequence in which the Constitution `1.1.0 → 1.2.0` amendment was labeled `RFC-0001`.

The later current canonical RFC index under `docs/rfc/` uses `RFC-0001` for `Arvectum OS Architecture`.

The historical identifier reuse is preserved truthfully rather than erased or retroactively renumbered.

Canonical reference rule:

- `legacy RFC-0000 constitutional amendment` refers to the historical Constitution `1.0.0 → 1.1.0` artifact pinned by the commit/blob above;
- `legacy constitutional amendment RFC-0001` refers to the historical Constitution `1.1.0 → 1.2.0` artifact pinned by the commit/blob above;
- unqualified `RFC-0001` means the current Accepted `RFC-0001 — Arvectum OS Architecture`;
- current Accepted RFC-0001 through RFC-0008 identifiers remain unchanged.

This interpretation is approved in [`DECISION-2026-08-07-CONSTITUTION-1.2-PROVENANCE-REPAIR`](decisions/DECISION-2026-08-07-CONSTITUTION-1.2-PROVENANCE-REPAIR.md).

## Compatibility and impact

The repair changes provenance and indexing only.

It does not:

- amend or re-ratify Constitution `1.2.0`;
- change current RFC numbering;
- alter any Accepted RFC normative substance;
- create or modify an ADR, Product Contract, policy, standard or capability lifecycle state;
- require implementation migration.

Current Accepted RFC-0001 through RFC-0008 already declare Constitution `1.2.0` as their governing baseline and remain compatible with the historical amendment substance.

## Current authority

- Constitution `1.2.0` is the canonical, Ratified and frozen governing document.
- Current Accepted RFC-0001 through RFC-0008 remain the canonical RFC architecture/product-contract sequence.
- Historical constitutional amendment identifiers are provenance references only and do not compete with the current RFC index.
- No older Constitution version should be used for new architectural work.

## Decision

This provenance record is `Closed`.

Closure basis:

1. original amendment artifacts were located in immutable Git history;
2. their amendment content and owner approval were verified;
3. the historical identifier collision was explicitly recorded rather than hidden;
4. the Owner approved the current governance repair on `2026-08-07`;
5. the RFC Index and canonical roadmap are synchronized as part of this repair;
6. read-after-write verification is required to complete operational closure.
