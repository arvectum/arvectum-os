# P7.07 — Selected-Mac Operational Closure

Date: `2026-08-19`
Status: `Complete / PASS`
Task classification: `governance` with `product_contract`, `platform` and `product_specific`
Constitution: `1.2.0 Ratified`
Applicable Product Contract: P6.02 `Provisional 0.1.0`
Selected environment: `Persistent Internal / owner-operated` selected Mac mini

## 1. Authority and review basis

Checked for closure:

- Constitution `1.2.0` — `Ratified`;
- RFC Index;
- RFC-0001, RFC-0003, RFC-0004, RFC-0005, RFC-0006 and RFC-0008 — `Accepted 1.0.0`;
- no task-relevant Accepted ADR exists;
- [`DECISION-2026-08-19-P7-07-PERSISTENT-TENDER-OPERATOR-CONTOUR`](../governance/decisions/DECISION-2026-08-19-P7-07-PERSISTENT-TENDER-OPERATOR-CONTOUR.md) — `Approved`;
- [`P7.07 implementation`](../implementation/P7-07-PERSISTENT-TENDER-OPERATOR-CONTOUR.md);
- [`P7.07 functional cross-review`](P7-07-persistent-tender-operator-contour-review.md);
- [`P7.07 Selected-Mac Attempt 1 loader blocker`](P7-07-selected-mac-attempt-1-loader-blocker.md);
- canonical P6.02 Product Contract `Provisional 0.1.0`;
- canonical roadmap and Phase 7 exit criteria;
- owner-submitted selected-Mac Attempt 2 final report and its owner-local evidence digest.

No higher-authority conflict was found.

Raw selected-Mac evidence remains owner-local by design. This canonical closure records only the bounded conclusions and the submitted evidence basename/SHA-256. The raw file bytes and credential material were not imported into Git, and this review does not claim an independent recomputation of the owner-local evidence digest by the repository review environment.

## 2. Repository implementation and remediation

Initial P7.07 repository implementation was merged through PR `#75` at:

`bf1a3047aadf03384c9525eacd4e186a53092c11`

The first selected-Mac closure attempt passed setup but failed closed before the first real CAP-001 read because the private dynamic loader executed the product-owned `@dataclass(frozen=True, slots=True)` bridge without first registering its generated module in `sys.modules`.

No local workaround was accepted. PR `#76` applied the bounded platform-side fix, added unmocked regression coverage for the exact dynamic slots-dataclass loading path and merged at:

`b0c18fba15de6b5abac83a4f583d89eedb5c03d1`

Reference Python CI `#157` completed with `success`.

The remediation changed no Product Contract semantics, authority mapping, P7.03 persistence meaning, P7.04 authorization semantics, external-effect behavior or product-owned procurement logic.

## 3. Selected-Mac Attempt 2

Result: `PASS`.

The canonical checkout and active persistent runtime were advanced through the existing P7.06 governed update path to exact release:

`b0c18fba15de6b5abac83a4f583d89eedb5c03d1`

P7.06 update transaction:

`7826f811cce4bc88a0e9a915e3806f6d23cb456428f8c53424d024342ebc33ec`

Runtime and observer exact-release consistency passed. Final P7.02 runtime state was healthy and P7.05 observer state was healthy.

The product checkout remained canonical and clean:

- repository: `arvectum/tender-agent`;
- branch: `main`;
- HEAD: `a1a22c42ee0cdef61efbb8370bdd9be294194062`;
- product-owned bridge AST guard: `PASS`;
- real dynamic `@dataclass(frozen=True, slots=True)` bridge load: `PASS`.

## 4. Persistent context and idempotent setup

The proof reused the existing persistent Organization and attributable owner-operated human Principal. P7.04 integrity passed.

The already-admitted P7.07 governed item remained exactly:

`53061324eec2b46fefd04d6f19bddbcc42d2a3ebfc5e7120f10a616e693a0795`

The guarded setup retry returned:

`PASS_IDEMPOTENT_EXISTING`

No additional governed item or admission checkpoint was created. Active temporary P7.07 setup grants remained zero. The exact item-scoped persistent `p3.08.resolve-document` read grant remained active.

## 5. Exact product reliance before restart

The first real product consumption returned:

`PASS_EXACT_CAP001_RELIANCE`

It preserved the same exact:

- Document Subject;
- Document Version;
- governed Artifact;
- integrity reference `sha256:74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- P6.02 Product Contract `0.1.0`;
- authority mode `External Reference`;
- authoritative source `ЕИС / zakupki.gov.ru`.

Tender Operator relied on the declared CAP-001 seam through the product-owned bridge and did not read P7.03 internals as a product dependency.

## 6. Supervised restart survivability

The proof performed an actual P7.02 supervised restart.

Runtime continuity evidence:

- generation: `59 → 60`;
- instance before: `35a597ee-d7bc-4aa4-84e8-2e047a5c0a3e`;
- instance after: `a84e1136-6a0d-48d8-90e4-bb903038949c`;
- runtime instance replaced: `true`;
- `previous_instance_id` after restart matched the pre-restart instance: `true`;
- exact release remained `b0c18fba15de6b5abac83a4f583d89eedb5c03d1`.

P7.03 governed-state digest before and after restart was identical:

`da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1`

Therefore:

`P7_03_STATE_UNCHANGED=true`

## 7. Exact product reliance after restart

The second real product consumption again returned:

`PASS_EXACT_CAP001_RELIANCE`

Before/after values matched for storage item, Subject, Version, Artifact, integrity reference, Product Contract version, authority mode and authoritative source.

Therefore:

`SAME_EXACT_RELIANCE_AFTER_RESTART=true`

This satisfies the P7.07 restart-survivability requirement rather than merely demonstrating a one-shot read.

## 8. Authority, security and effect boundary

Selected-Mac evidence reports all of the following as preserved:

- EIS/SOAP invoked by P7.07: `NO`;
- network invoked by P7.07: `NO`;
- canonical mutation from ordinary reads: `NO`;
- tender submission / email / Telegram / payment / signature or other external action: `NO`;
- raw tender bytes exposed: `NO`;
- credential secret exposed: `NO`;
- AI Organizational Authority introduced: `NO`.

P7.04 remains technical authorization only. Completion does not grant Organizational Authority, consequential approval, standing canonical-write authority or external-effect authority.

EIS remains the authoritative system for the procurement facts. Arvectum OS retains an exact governed `External Reference`; it does not become a competing source of truth.

## 9. Owner-local evidence

Owner-local evidence basename:

`selected-mac-restart-proof.json`

Submitted SHA-256:

`9613637b06c5d192311bda1eb3096a9cd0b49c016134af887697637a668cf0f8`

The raw evidence remains owner-only and outside Git. Canonical history intentionally stores only this minimized reference and the bounded conclusions above.

## 10. Closure criteria review

The approved P7.07 decision requires repository implementation/tests/review, merged CI, governed exact-release activation, idempotent setup or exact admission, temporary-grant revocation, effective exact read grant, real product bridge reliance before and after supervised restart, unchanged exact reliance, unchanged P7.03 governed state, bounded retained evidence and roadmap synchronization.

Result before roadmap synchronization: `PASS` on every technical/operational criterion.

This closure change synchronizes the remaining canonical status/roadmap state.

## 11. Functional review — closure iteration

### Product Contract boundary

Result: `PASS`.

P6.02 remains `Provisional 0.1.0`; no hidden product access to P7.03 and no Product Contract version/lifecycle promotion is introduced.

### External authority

Result: `PASS`.

`ЕИС / zakupki.gov.ru` remains authoritative under `External Reference` semantics.

### Identity / authorization / authority separation

Result: `PASS`.

The same persistent Organization/human Principal and exact item-scoped read grant were reused; temporary setup privilege is absent; authorization is not represented as Organizational Authority or consequential approval.

### Restart and state integrity

Result: `PASS`.

Actual supervised restart replaced the runtime instance, advanced generation, preserved `previous_instance_id`, kept the exact release and left the P7.03 state digest unchanged.

### Real product reliance

Result: `PASS`.

The actual canonical product bridge loaded and produced exact CAP-001 reliance both before and after restart.

### Security / effects / minimization

Result: `PASS`.

No new network/EIS retrieval, external effect, ordinary-read canonical mutation, raw tender-byte exposure or credential-secret exposure is claimed or permitted.

### ADR / lifecycle / commercial boundary

Result: `PASS`.

The private loader/persistence/guard/runtime shape remains bounded and reversible. No new Accepted ADR is required at this scope. No capability becomes `Active`, no Product Contract becomes `Stable`, and no external/customer Production, SLA/SLO/support or broader conformance claim is created.

No material objection remains.

## 12. Conclusion

`P7.07 — Persistent Tender Operator operational contour = Complete / PASS` for the declared selected-Mac `Persistent Internal / owner-operated` scope.

M7 criterion 7 — repeatable persistent Tender Operator reliance through its explicit Product Contract boundary — is satisfied for that scope.

The next canonical work item is `P7.08 — Persistent Discount Parser cross-host operational contour` after roadmap synchronization.
