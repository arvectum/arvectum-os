# P6.05-L9 — Dogfooding friction capture

Status: `Complete / PASS`
Date: `2026-08-16`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`
Predecessor: [`P6-05-L8-attempt-2-governed-evidence-admission-and-closure.md`](P6-05-L8-attempt-2-governed-evidence-admission-and-closure.md), `Complete / PASS`
Product Contract: [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`, unchanged

## 1. Decision

**PASS — P6.05-L9 dogfooding friction capture is complete.**

P6.05 resolved the P6.04 product-outcome blocker: the real notice `0344100006426000005` now has exact `7/7` tender attachment evidence admitted under Governed Execution and reconstructed through CAP-004, with manifest SHA `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121` and status **GOVERNED**.

L9 records the friction exposed by actually operating that contour. The register below distinguishes resolved defects/blockers from still-open ergonomics observations. Recording an observation does **not** make it validated Knowledge, an approved Improvement Proposal, an ADR, a Product Contract change, a Platform Capability promotion, or a public compatibility commitment.

## 2. Canonical basis checked

L9 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
- RFC-0001 — evidence over intuition, minimum sufficient platform responsibility, product/platform separation, scoped conformance and no automatic capability promotion;
- RFC-0004 — explicit Product Contract boundary and prohibition on hidden product/platform coupling;
- RFC-0005 — Governed Execution and immutable consequential governance history;
- RFC-0006 — exact Event/provenance evidence, fail-closed evidence paths and non-canonical observability by default;
- RFC-0007 — Observation, Memory, Knowledge Candidate, Improvement Proposal and validated Knowledge remain distinct; observations cannot silently change approved behavior;
- `docs/adrs/README.md` and `docs/adrs/` — no Accepted ADR files currently exist, therefore no ADR conflict applies;
- P6.04, P6.05-L7 attempt #1, P6.05-L8 attempt #1, the CAP-004 cross-role repair, and P6.05-L8 attempt #2 closure evidence;
- P6.02 Product Contract `Provisional 0.1.0` — unchanged.

No higher-priority canonical conflict was identified.

## 3. Evidence discipline

Friction is classified as one of:

- **Observed blocker/defect** — directly caused a bounded attempt to fail or demonstrated incorrect platform behavior;
- **Observed ergonomics friction** — directly required manual orchestration or low-level coordination but did not prove incorrect semantics;
- **Resolved** — a demonstrated blocker/defect has a verified remediation in the exercised contour;
- **Improvement candidate only** — a possible follow-up, not an approved architecture, backlog commitment or public contract.

No active-engineering hours, monetary cost, productivity percentage or customer-value score is inferred from repository timestamps, commit count, retry count or test volume.

## 4. Friction register

| ID | Observed friction | Evidence / impact | Classification | Current disposition | Bounded improvement candidate — not approved |
|---|---|---|---|---|---|
| `L9-F01` | Complete exact tender source-package evidence was absent from the first real contour | P6.04 real case stopped truthfully because exact `7/7` attachment bytes/digests were not retained | product/platform delivery blocker | **Resolved by P6.05** — L7 observed exact `7/7`; L8 admitted/reconstructed it as GOVERNED | none required for P6.05 closure; reuse should be re-evaluated on the second real target |
| `L9-F02` | EIS TLS trust-policy suitability was not discoverable early enough in the owner-operated path | L7 attempt #1 failed before application response because the active Python default CA store did not trust the Russian PKI chain while macOS system trust did | product/operator configuration friction | **Resolved for the exercised host** using the existing owner-operated `authority: system` trust path; no platform defect demonstrated | earlier preflight that reports effective trust authority and host-policy match without weakening verification |
| `L9-F03` | Canonical Event provenance construction requires several exact governed references to be assembled correctly | L8 attempt #1 failed closed when producer/execution/result references were incomplete | platform developer-experience / orchestration friction | **Open, non-blocking** after corrected attempt #2 | typed/high-level Event provenance builder or preflight validator, if reuse justifies it |
| `L9-F04` | Governance-significant intermediate state required explicit owner-local checkpoint persistence | L8 attempt #1 left execution lineage, gate decisions and admitted result ephemeral, so the attempt was correctly classified `NOT_RECOVERABLE_WITHOUT_NEW_ADMISSION` | internal runtime / orchestration friction | **Open, non-blocking**; attempt #2 retained 12 checkpoint stages successfully | reusable safe checkpoint helper/pattern for internal evidence harnesses; no general persistence contract selected |
| `L9-F05` | Identity-preserving admission required manual execution-version and pin alignment when one Document Version Identity occupied material-input and result roles | Explicitly recorded as an L9 candidate in L8 closure | platform developer-experience friction | **Open, non-blocking** | high-level admission orchestration that derives exact immutable pins while preserving identity semantics |
| `L9-F06` | Gate decisions had to be manually linked across exact execution versions | Explicitly recorded as an L9 candidate in L8 closure; incorrect lineage would undermine reconstruction | governance ergonomics friction | **Open, non-blocking** | helper that advances execution versions and emits/pins gate-decision lineage consistently |
| `L9-F07` | CAP-004 originally treated legitimate cross-role reuse of the exact same immutable Version Identity as an ambiguity | Synthetic L8 preflight exposed a real platform implementation gap | platform implementation defect | **Resolved** in PR #13; role multiplicity is allowed only for identical `GovernedVersionPin` state and conflicting reuse still fails closed | retain regression coverage; no new capability or public API implied |
| `L9-F08` | The successful identity-preserving admission path still depends on low-level composition of execution versions, gates, admission, Event provenance, checkpoints and reconstruction | L8 attempt #2 succeeded, but its own closure explicitly records lack of high-level orchestration | aggregate platform developer-experience friction | **Open, non-blocking** | evaluate a bounded orchestration helper only after reuse evidence; do not stabilize an API from one product case |

## 5. Blocking versus non-blocking disposition

The blockers that prevented the original declared product outcome are closed within P6.05:

- the exact source-package gap is closed by truthful real `7/7` capture plus governed admission;
- the EIS TLS trust configuration blocker is closed for the exercised environment without weakening verification;
- the CAP-004 cross-role reconstruction defect is repaired and regression-tested.

The remaining items `L9-F03`, `L9-F04`, `L9-F05`, `L9-F06` and `L9-F08` are genuine dogfooding friction, but they do not invalidate the completed evidence path. Attempt #2 demonstrated that the path can preserve exact authority, governance, provenance, identity, checkpoint evidence and reconstruction while ending in `Succeeded`.

They therefore remain **observations / improvement candidates**, not closure blockers and not pre-approved platform work.

## 6. What L9 does not conclude

L9 does **not** establish or authorize:

- a Stable Product Contract or Product Contract expansion;
- CAP-002 or CAP-003 adoption;
- promotion of CAP-001 or CAP-004 to `Active`;
- a public SDK/API or stable orchestration interface;
- product-domain procurement semantics in shared platform behavior;
- a platform-wide TLS trust capability;
- one mandatory persistence/checkpoint technology;
- a production-readiness, SLA, support or full-platform conformance claim;
- an economic, time-saving, quality-uplift or customer-usefulness claim;
- automatic promotion of these observations to Organizational Memory, Knowledge, policy, standard or operational behavior.

If later evidence shows that one of the open friction items deserves durable shared behavior, the minimum sufficient implementation/ADR/standard/Product Contract/RFC decision must be chosen at that time under the normal authority hierarchy.

## 7. P6.05 closure

P6.05-L9 is **Complete / PASS**.

With L9 complete:

- P6.05-L1 through P6.05-L9 are complete;
- the real exact tender evidence remains `7/7` and **GOVERNED**;
- P6.05 — Platform-gap remediation is **Complete / PASS**;
- Phase 6 remains `Active / In Progress` because later validation work remains;
- `P6.06 — Second real target` remains pending and is the next top-level Phase 6 item in the canonical roadmap.
