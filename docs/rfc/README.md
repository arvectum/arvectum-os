# Arvectum OS RFC Index

RFCs define major architectural, governance and product-contract decisions for Arvectum OS.

The Constitution has higher authority than every RFC. Accepted RFCs have higher authority than ADRs and implementation details.

## Statuses

- `Draft` — incomplete working document;
- `Proposed` — complete proposal awaiting approval;
- `Accepted` — approved and binding;
- `Rejected` — considered and not accepted;
- `Superseded` — replaced by a later accepted RFC;
- `Withdrawn` — removed by its proposer before decision.

## RFCs

| RFC | Title | Category | Status | Version |
|---|---|---|---|---|
| [RFC-0001](RFC-0001-arvectum-os-architecture.md) | Arvectum OS Architecture | platform | Proposed | 0.7.0 |

## Acceptance Integrity

An RFC is validly `Accepted` only when:

1. its canonical Approval Record references an owner-approved decision that already exists independently of the acceptance commit;
2. the canonical RFC and this index are updated consistently in one repository change;
3. the resulting repository commit or release tag is preserved as external repository evidence.

A status label without the required approval evidence does not constitute acceptance.

An RFC must not require its acceptance commit hash to be embedded inside the same commit as a self-reference.

## Governance Notes

The canonical Constitution is version `1.2.0`.

The repository currently does not contain an indexed accepted amendment RFC documenting the transition to Constitution `1.2.0`. This provenance gap is recorded in [`docs/governance/CONSTITUTION-PROVENANCE.md`](../governance/CONSTITUTION-PROVENANCE.md) and must be resolved from confirmed owner-approved records rather than reconstructed by assumption.
