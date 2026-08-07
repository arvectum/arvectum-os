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
| [RFC-0001](RFC-0001-arvectum-os-architecture.md) | Arvectum OS Architecture | platform | Accepted | 1.0.0 |
| [RFC-0002](RFC-0002-canonical-record-kernel-metamodel.md) | Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model | platform | Accepted | 1.0.0 |
| [RFC-0003](RFC-0003-identity-security-privacy-tenant-sovereignty-portability.md) | Identity, Security, Privacy, Tenant Sovereignty and Portability | platform | Accepted | 1.0.0 |
| [RFC-0004](RFC-0004-product-contract-product-experiment-extension-model-v1.0.0.md) | Product Contract, Product Experiment and Extension Model | product_contract | Accepted | 1.0.0 |
| [RFC-0005](RFC-0005-governed-execution-workflow-model-v0.3.0.md) | Governed Execution and Workflow Model | platform | Proposed | 0.3.0 |

## Acceptance Integrity

An RFC is validly `Accepted` only when:

1. its canonical Approval Record references an owner-approved decision that already exists independently of the acceptance commit;
2. the canonical RFC and this index are updated consistently as part of the acceptance publication;
3. the resulting repository commit or release tag is preserved as external repository evidence.

A status label without the required approval evidence does not constitute acceptance.

An RFC must not require its acceptance commit hash to be embedded inside the same commit as a self-reference.

## RFC-0001 Approval Evidence

Canonical owner approval:

- [`DECISION-2026-08-07-RFC-0001-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0001-ACCEPTANCE.md) — `Approved`.

Accepted RFC publication commit:

- `214faf049990a9475da66ca52f7327728c9a49eb`.

## RFC-0002 Approval Evidence

Canonical owner approval:

- [`DECISION-2026-08-07-RFC-0002-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0002-ACCEPTANCE.md) — `Approved`.

Approved proposal:

- RFC-0002 `0.10.0`.

Accepted RFC publication commit on the acceptance branch:

- `ed936fcaa118368f81d2329b8f1ffa70d219ec4f`.

Accepted RFC publication merge commit on `main`:

- `8d247402db1b869fcca7bc1dc634cbb2f585c89a`.

The merge commit preserves the independent approval commit and subsequent acceptance publication commits in repository history.

## RFC-0003 Approval Evidence

Canonical owner approval:

- [`DECISION-2026-08-07-RFC-0003-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0003-ACCEPTANCE.md) — `Approved`.

Approved proposal:

- RFC-0003 `0.2.0`.

Accepted RFC publication commit:

- `1552970e2107bf1c3bbbe20353747f3b9a4361ce`.

RFC-0003 `1.0.0` is binding architecture within its declared scope.

## RFC-0004 Approval Evidence

Canonical owner approval repair record:

- [`DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR`](../governance/decisions/DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR.md) — `Approved`.

Approved reviewed proposal:

- RFC-0004 `0.3.0`;
- immutable proposal blob SHA `5a413a240588677211ad56f3a23b30a65d1c4334`.

Compatibility re-check against Accepted RFC-0003 `1.0.0`:

- [`RFC-0004 compatibility re-check`](../reviews/RFC-0004-accepted-rfc0003-compatibility-review.md) — `Complete`, review iteration 4 of maximum 7;
- result: no material conflict; stale RFC-0003 lifecycle wording reconciled for acceptance publication.

Accepted RFC publication:

- [`RFC-0004 v1.0.0`](RFC-0004-product-contract-product-experiment-extension-model-v1.0.0.md) — `Accepted`;
- publication commit: `3b3f72a01bd76d9cfb6a1ef78e7ec6a627173ee2`.

RFC-0004 `1.0.0` is binding architecture within its declared product-contract scope.

## RFC-0005 Proposal Evidence

Current reviewed proposal:

- [`RFC-0005 v0.3.0`](RFC-0005-governed-execution-workflow-model-v0.3.0.md) — `Proposed`;
- incorporated reviewed baseline RFC-0005 `0.2.0` blob SHA `67e739ceacdbd308618f4fdfffd914dc65e99f09`;
- original functional cross-review: [`docs/reviews/RFC-0005-functional-cross-review.md`](../reviews/RFC-0005-functional-cross-review.md) — `Complete`, 3 iterations;
- additional cross-review against Accepted RFC-0004 and Roadmap `1.1.2`: [`RFC-0005 iteration 4`](../reviews/RFC-0005-cross-review-iteration-4.md) — `Complete`;
- total review iterations: 4 of maximum 7;
- iteration 4 result: `Pass with bounded reconciliation`;
- RFC-0005 `0.3.0` publication commit: `b9d678456d2fe526c5a2d637001a970321240305`.

RFC-0005 `0.3.0` now normatively depends on Accepted RFC-0001, RFC-0002, RFC-0003 and RFC-0004. Product Contract version attribution and boundary enforcement have been reconciled with RFC-0004 `1.0.0`.

RFC-0005 is ready for owner decision. Until explicitly approved and canonically published as `Accepted`, it has no normative force.

## Related Governance

RFC-0001 v1.0.0 requires an approved decision-authority policy before the first `Active` capability or external production conformance claim.

It also requires operational-readiness approval before a capability becomes `Active`, and requires externally relied-upon commercial claims to remain within approved lifecycle, contract and conformance scope.

Current proposed policy:

- [`Decision Authority Policy`](../governance/DECISION-AUTHORITY-POLICY.md) — `Proposed` v0.2.1.

Until that policy or a replacement is approved, the owner of Arvectum OS retains residual decision authority.

## Governance Notes

The canonical Constitution is version `1.2.0`.

The repository currently does not contain an indexed accepted amendment RFC documenting the transition to Constitution `1.2.0`. This provenance gap is recorded in [`docs/governance/CONSTITUTION-PROVENANCE.md`](../governance/CONSTITUTION-PROVENANCE.md) and must be resolved from confirmed owner-approved records rather than reconstructed by assumption.

The approved [`RFC State Transition Procedure`](../governance/RFC-STATE-TRANSITION-PROCEDURE.md) requires owner approval, canonical publication, RFC Index synchronization, roadmap synchronization and read-after-write consistency verification to close each RFC status transition before substantive work proceeds to the next RFC.