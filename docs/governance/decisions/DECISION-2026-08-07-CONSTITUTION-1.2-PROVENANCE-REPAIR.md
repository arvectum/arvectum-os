# DECISION-2026-08-07 — Constitution 1.2.0 Provenance Repair

Status: `Approved`
Decision date: `2026-08-07`
Effective date: `2026-08-07`
Decision authority: `Owner of Arvectum OS / ООО «Арвектум»`
Task classification: `governance`
Canonical Constitution: `1.2.0`
Affected governance record: `docs/governance/CONSTITUTION-PROVENANCE.md`
Affected index: `docs/rfc/README.md`

## Decision

The Owner approves closure of the Constitution `1.2.0` provenance gap using confirmed immutable repository evidence discovered in Git history.

The repair records the following historical chain without changing, recreating or backdating any historical artifact:

1. Constitution `1.0.0 → 1.1.0` was approved through the historical amendment document titled `RFC-0000: Amend the Arvectum OS Constitution to Version 1.1.0`.
2. Constitution `1.1.0 → 1.2.0` was approved through the historical amendment document titled `RFC-0001: Amend the Arvectum OS Constitution to Version 1.2.0`.
3. Both historical amendment documents contain explicit owner approval and were committed together with the resulting Constitution transitions.
4. A later repository-governance migration established the current canonical RFC index under `docs/rfc/` and reused identifier `RFC-0001` for `Arvectum OS Architecture`.
5. That identifier reuse is recorded as a historical governance migration defect. It does not change the content, approval or authority of either the historical constitutional amendment or the current Accepted `RFC-0001 — Arvectum OS Architecture`.
6. Current Accepted RFC identifiers are not renumbered by this repair because doing so would destabilize the already accepted dependency graph, approval evidence and canonical references without changing architectural meaning.
7. The historical amendment with identifier `RFC-0001` MUST therefore always be referenced as `legacy constitutional amendment RFC-0001` together with its immutable commit or blob reference. Unqualified `RFC-0001` in current architecture and governance means `RFC-0001 — Arvectum OS Architecture`.
8. `docs/governance/CONSTITUTION-PROVENANCE.md` may be closed after the historical evidence, this decision and the RFC Index are synchronized and read-after-write verification succeeds.

## Confirmed immutable evidence

### Constitution 1.0.0 → 1.1.0

Historical artifact:

- path at historical commit: `docs/rfcs/RFC-0000-constitution-1.1.md`;
- title: `RFC-0000: Amend the Arvectum OS Constitution to Version 1.1.0`;
- status in artifact: `Accepted`;
- resulting Constitution version: `1.1.0`;
- commit: `611278850e2af5e159332650858574a3c647330b`;
- artifact blob SHA: `835425ca01705adf07da724389038ea2228f15ce`;
- the artifact states that the owner explicitly approved the amendments on `2026-08-06`.

### Constitution 1.1.0 → 1.2.0

Historical artifact:

- path at historical commit: `docs/rfcs/RFC-0001-constitution-1.2.md`;
- title: `RFC-0001: Amend the Arvectum OS Constitution to Version 1.2.0`;
- status in artifact: `Accepted`;
- resulting Constitution version: `1.2.0`;
- commit: `bd012cc435461fe903d6f9420282a0f906ca5bbd`;
- artifact blob SHA: `85b3cc9895dc4a398a0e30428926fe486f62062a`;
- the artifact states that the owner explicitly approved the amendments on `2026-08-06`.

The second amendment identifies the changed constitutional areas, rationale, invariants, compatibility/migration consequences, acceptance criteria and resulting version. It therefore supplies the substantive amendment provenance required by the current Constitution's amendment-process expectations.

## Identifier collision interpretation

Repository history shows that the earlier RFC process used the path namespace `docs/rfcs/` and assigned amendment identifiers `RFC-0000` and `RFC-0001` before the current canonical RFC index and architecture sequence were finalized.

The current canonical RFC namespace is the index at `docs/rfc/README.md`, where `RFC-0001` means `Arvectum OS Architecture` and RFC-0001 through RFC-0008 are the Accepted architecture/product-contract sequence.

This repair does not claim that the historical identifier reuse complied with the earlier no-reuse rule. It records the reuse truthfully as a governance migration defect and resolves the resulting ambiguity prospectively without rewriting history.

Canonical reference rule from this decision onward:

- `legacy RFC-0000 constitutional amendment` means the historical Constitution `1.0.0 → 1.1.0` artifact pinned to commit/blob evidence above;
- `legacy constitutional amendment RFC-0001` means the historical Constitution `1.1.0 → 1.2.0` artifact pinned to commit/blob evidence above;
- `RFC-0001` without the `legacy constitutional amendment` qualifier means the current Accepted `RFC-0001 — Arvectum OS Architecture`;
- current RFC-0001 through RFC-0008 identifiers remain unchanged.

## Compatibility and impact analysis

The repair changes governance provenance only. It does not amend Constitution `1.2.0`, any Accepted RFC, ADR, Product Contract, policy, standard, catalog, implementation contract or capability lifecycle state.

The historical Constitution `1.2.0` amendment strengthened security/privacy/isolation, proportional decision records, replaceable vendor-specific workflow dependencies and architecture-neutral domain-boundary wording. Current Accepted RFC-0001 through RFC-0008 already use Constitution `1.2.0` as their governing baseline and are compatible with those amendments.

No implementation migration is required by this repair.

No RFC renumbering is required or approved.

## Closure actions

The repair is complete when all of the following are true:

1. this decision exists canonically with status `Approved`;
2. `docs/governance/CONSTITUTION-PROVENANCE.md` records the confirmed evidence and status `Closed`;
3. `docs/rfc/README.md` indexes the historical constitutional amendments in a clearly separate legacy-provenance section and records the identifier-collision interpretation;
4. `docs/roadmap/ROADMAP.md` no longer lists Constitution `1.2.0` provenance as open governance debt and records the repair as complete;
5. all affected files are re-fetched from the default branch and cross-source consistency is verified.

## Non-claims

This decision does not:

- amend or re-ratify Constitution `1.2.0`;
- fabricate a historical approval record;
- pretend that the historical RFC identifier collision did not occur;
- renumber current Accepted RFCs;
- alter the normative substance of RFC-0001 through RFC-0008;
- make any Platform Capability `Active`;
- establish production or operational readiness;
- approve the currently Proposed Decision Authority Policy.

## Approval record

Decision: `Approved`
Approved by: `Owner of Arvectum OS`
Approval evidence: explicit owner direction in the Arvectum OS project conversation on `2026-08-07` to perform the required repair and confirm Phase 0 readiness
Canonical decision reference: `docs/governance/decisions/DECISION-2026-08-07-CONSTITUTION-1.2-PROVENANCE-REPAIR.md`
