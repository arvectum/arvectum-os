# P7.06 — Governed Deploy / Update / Rollback Implementation Cross-Review

Status: `Repository review PASS / live proof pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance`

## 1. Scope

Functional review covers the repository-side P7.06 deployment/version/migration boundary before selected-Mac execution. Roles considered materially relevant: architecture/governance, engineering, operations/recovery, security/data governance and product/platform boundary.

## 2. Iteration 1 — REVISE

Material finding: an initial failure path could restore the prior runtime/observer release but terminate without a P7.06 transaction record. That would leave a consequential operational transition observable only through process exit/raw diagnostics.

Remediation: failed activation or post-update health/re-pin verification now restores the exact source release and attempts an immutable `ROLLED_BACK` transaction record carrying the plan, backup identity and rollback disposition. Evidence-recording failure remains explicitly visible as an operator-investigation condition rather than a false PASS.

## 3. Iteration 2 — REVISE

Material security/recovery finding: transaction evidence originally trusted an arbitrary backup path/SHA supplied by the adapter.

Remediation: the Python evidence boundary now requires the retained backup to exist directly under the owner-local P7.03 `backups/` directory, validates a full SHA-256 and recomputes the archive digest before accepting a transaction record.

## 4. Iteration 3 — PASS

Architecture/governance: PASS. Exact Git release identity and source/target schema identity are explicit; no Accepted contract is changed; deployment evidence does not claim authority; no public/stable boundary is introduced.

Engineering: PASS for repository stage. One deployment lock prevents concurrent owner-local transitions; target release is prepared/verified before activation; runtime and observer remain one exact-release unit; rollback preserves historical release identity.

Operations/recovery: PASS for unchanged P7.03 schema. Every update requires a fresh verified backup; rollback restores exact service pins but does not restore data unnecessarily; failed updates are fail-closed and recorded. The live update→rollback→re-update behavior still requires selected-Mac proof.

Security/data governance: PASS. No reusable secrets enter deployment evidence/backup; migration cannot use arbitrary executable hooks; schema-changing migration is blocked until a separately bounded executor and authority/rollback proof exist; external-effect replay remains false.

Product/platform: PASS. The adapter is domain-neutral and imports no Tender Operator/Discount Parser logic, databases or private product streams. Product Contract and capability lifecycle remain unchanged.

No material repository-side objection remains. Further refinement before live evidence would be speculative.

## 5. Validation

Repository validation:

- Python P7.06 focused unit tests: PASS;
- macOS deploy adapter `sh -n`: PASS;
- selected-Mac proof adapter `sh -n`: PASS;
- focused P7.06 combined tests: `11/11 PASS`;
- static guard: no curl/wget/ssh/scp/nc remote transport introduced by the P7.06 macOS adapter;
- PR `#40` merged to canonical `main` at `70b0427379d5579e246d9566802c3795df63a46b`;
- GitHub `Reference Python CI` run `32114967673`, job `95642307033`: `975/975 PASS` on the PR merge ref.

Selected-Mac execution remains the only closure evidence still to obtain.

Functional cross-review result: `PASS` after 3 iterations. This is not formal Production/lifecycle approval and does not substitute for the selected-Mac proof.
