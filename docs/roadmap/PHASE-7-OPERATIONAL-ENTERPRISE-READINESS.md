# Arvectum OS Phase 7 — Operational / Enterprise Readiness

Status: `Active`
Version: `1.2.16`
Created: `2026-08-17`
Updated: `2026-08-19`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M7 — Scoped production-grade operating baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 6 — Product-driven Platform Validation`, `M6` achieved
Activation decision: [`DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION`](../governance/decisions/DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION.md)

## 1. Purpose

Phase 7 moves Arvectum OS from bounded real-product validation into persistent, recoverable, observable and governable internal operation.

The phase deliberately begins regular owner-operated use early rather than waiting until all enterprise-readiness work is finished. The selected ООО «Арвектум» Mac mini is the current operational environment, not a platform architecture commitment or supported macOS product promise.

The Phase 7 question is:

> Can Arvectum OS operate continuously enough to become a dependable internal organizational foundation, survive ordinary failures and upgrades, preserve governed state and provenance, and expose sufficient operational evidence to support later scoped production-readiness decisions?

## 2. Starting state inherited from M6

M6 established two materially distinct real product/workflow validation chains, real owner-operated Mac mini execution, explicit Product Contracts before governed reliance and bounded CAP-001/CAP-004 reuse. CAP-001 through CAP-004 remain `Incubating / Provisional`; P6.02 and P6.06 Product Contracts remain `Provisional 0.1.0`; no Stable/public SDK/API/wire/deployment topology, `Active` capability or external/customer Production/SLA/support/full-platform conformance claim exists.

## 3. Operating-mode rule

Phase 7 distinguishes:

- **bounded validation runtime** — task-scoped, started for a specific proof;
- **Persistent Internal / owner-operated runtime** — regularly running internal Arvectum OS environment used by ООО «Арвектум» for ongoing governed work;
- **Production** — an environment with separately approved operational scope and applicable commitments.

P7.02 has passed. The selected Mac mini therefore operates in `Persistent Internal / owner-operated` mode while P7.03–P7.12 harden the live baseline. This does not itself create Production, lifecycle promotion, Stable Product Contracts or support commitments.

## 4. Phase 7 work breakdown

| ID | Work item | Primary execution venue | Status | Progress |
|---|---|---|---:|---:|
| `P7.01` | Persistent internal operating boundary + operational requirements baseline | Chat/GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.02` | Persistent Mac mini runtime + boot/restart/service lifecycle | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.03` | Durable governed state/checkpoint persistence + backup/restore baseline | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.04` | Persistent identity/operator/service access + least-privilege operations | Chat + Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.05` | Health, observability, audit visibility, alerting + retention/minimization | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.06` | Governed deploy/update/rollback/version/migration path | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.06-UI` | Live operator workspace over persistent runtime | Mac mini + browser + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.07` | Persistent Tender Operator operational contour | Mac mini + product environment + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.08` | Persistent Discount Parser cross-host operational contour | Windows + Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.09` | Operator runbook + incident/uncertain-outcome/recovery drills | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | Mac mini + secondary clean environment + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.11` | Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition | Chat/GitHub + evidence | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P7.12` | Phase 7 / M7 closure review | Chat/GitHub | ⬜ | `░░░░░░░░░░ 0%` |

`P7.06-UI` is a subordinate operator-experience substream, not a new lifecycle or public-interface claim. Detailed plan: [`P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md`](P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md).

## 5. Engineering / quality gates

| Gate | Trigger | Status | Purpose |
|---|---|---|---|
| [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) | after `P7.01`, before material persistent-runtime implementation | 🟩 `Complete / PASS` | prevent persistent use from silently selecting unsupported production, public API, storage, IAM or deployment commitments |
| [`R22 — Persistent Runtime Health Review`](../reviews/R22-persistent-runtime-health-review.md) | after `P7.05`, before operational workload expansion | 🟩 `Complete / PASS` | review runtime/service boundaries, durability, access, observability, secrets, dependency direction, failure semantics and operator friction |
| [`R23 — Recovery / Portability Review`](../reviews/R23-recovery-portability-review.md) | after `P7.10`, before lifecycle/readiness decisions | 🟩 `Complete / PASS` | verify backup/restore, host-loss recovery, semantic portability, exact identities/versions/provenance and absence of host-specific hidden authority |
| `R24 — M7 Operational Hardening` | after `P7.11`, before `P7.12` | ⬜ | final bounded architecture/code/security/maintainability/fitness review and required M7 Milestone Code Health Gate |

These gates are engineering/governance checkpoints, not lifecycle transitions or formal Production approvals.

## 6. Work-item status and exit evidence

### P7.01 — Persistent internal operating boundary + operational requirements baseline

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.01 Persistent Internal Operating Boundary and Operational Requirements Baseline`](P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) — `Complete / Baseline 1.0.1`;
- [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) — `Complete / PASS`.

The baseline fixes the `Persistent Internal / owner-operated` classification, Organization/owner boundary, admitted workload classes, data/secret/retention/network/recovery constraints, ADR/stable-boundary triggers and reversible removal path without choosing permanent persistence, IAM, service, storage, API or deployment topology.

### P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.02 Persistent Mac mini Runtime and Service Lifecycle`](../implementation/P7-02-MAC-MINI-PERSISTENT-RUNTIME.md) — `Complete / PASS`;
- [`P7.02 Persistent Runtime Implementation Cross-Review`](../reviews/P7-02-persistent-runtime-implementation-review.md) — `Complete / PASS`;
- selected-Mac proof Attempt 2 — `Complete / PASS`;
- exact proven runtime release: `73af746f83271b14670fe22db658dfd55cacb291`;
- P7.02 remediation CI: `920/920 PASS`.

Arvectum OS entered regular persistent internal operation on the selected Mac mini. `launchd` remains an environment-specific reversible adapter, not a stable platform contract.

### P7.03 — Durable governed state/checkpoint persistence + backup/restore baseline

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.03 Durable Governed State / Checkpoint Persistence and Backup / Restore Baseline`](../implementation/P7-03-DURABLE-GOVERNED-STATE-BACKUP-RESTORE.md) — `Complete / PASS`;
- [`P7.03 Durable State Implementation Cross-Review`](../reviews/P7-03-durable-state-implementation-review.md) — `Complete / PASS`, six iterations;
- selected-Mac Attempt 3 — `Complete / PASS`;
- repository CI: `932/932 PASS`; hardened proof-contract CI: `935/935 PASS`.

Live backup/isolated restore integrity passed, restored state digest matched live state, deliberate tamper detection failed closed, and `run/`, `logs/`, `cache/`, `secrets/` remained excluded. The filesystem/tar adapter remains private, reversible and non-stable; no persistence ADR is required yet at this bounded scope.

### P7.04 — Persistent identity/operator/service access + least-privilege operations

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.04 Persistent Identity / Operator / Service Access + Least-Privilege Operations`](../implementation/P7-04-PERSISTENT-IDENTITY-ACCESS.md) — `Complete / PASS`;
- repository implementation PR `#35`, merged at `2b808c658c19056cef65b69e82152ae12d861679`;
- focused persistent-access tests: `14/14 PASS`;
- selected-Mac proof-contract tests: `2/2 PASS`;
- GitHub `Reference Python CI` on final implementation/documentation head `b9c46646324d5d4bccf384196efa3670b828c6af`: `success`, run `32063442269`;
- [`P7.04 Persistent Access Implementation Cross-Review`](../reviews/P7-04-persistent-access-implementation-review.md) — `Complete / PASS`, six iterations;
- [`P7.04 Selected-Mac Persistent Access Proof — Attempt 1`](../reviews/P7-04-selected-mac-proof-attempt-1.md) — `Complete / PASS`;
- tested canonical `main`: `218e3762975a2fd6f11e8f13d4445bce5f5d7c94`;
- exact persistent runtime release: `73af746f83271b14670fe22db658dfd55cacb291`;
- selected-Mac attestation SHA-256: `5c0a67b15b7fb469bc5933030db0c2e90adfb47c3eb94411c43ba555b7d98659`.

P7.04 now establishes, for the declared bounded owner-operated scope, exact P6.05-L4 Organization/human identity continuity, a separate attributable service principal, deny-by-default exact Organization/operation/resource/access-path grants, owner-local credential issue/rotation/revocation, principal/grant revocation, explicit local/remote access scoping, and executable selected-Mac evidence that ungranted remote lifecycle administration and service ambient administration fail closed.

Every allowed operational decision remains explicitly separate from Organizational Authority and consequential approval. The selected-Mac proof preserved a healthy unchanged P7.02 runtime and performed no canonical mutation or external/product effect. The raw attestation remains owner-local non-canonical operational evidence; canonical history stores only the review result and digest.

ADR disposition remains `NO` at the current owner-local, single-Organization, reversible scope. Re-open the ADR/stable-boundary gate before externally relied-upon IAM behavior, cross-Organization access, public/stable access APIs, materially constraining credential technology or a long-lived remote-administration topology.

P7.04 closure does not establish external/customer Production, an `Active` Platform Capability, Stable Product Contract, public/stable access API, supported remote-admin transport, SLA/support or conformance promotion.

### P7.05 — Health, observability, audit visibility, alerting + retention/minimization

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.05 Health, Observability, Audit Visibility, Alerting + Retention / Minimization`](../implementation/P7-05-HEALTH-OBSERVABILITY-AUDIT-RETENTION.md) — `Complete / PASS`;
- repository implementation PR `#37`, merged at `9999ce6f93bb2874fd4e43135abd1ffe726bbd2f`;
- final repository implementation head: `60914ee96793cdf40896e4336ce24f5788247b37`;
- GitHub `Reference Python CI` run `32103615123`: `960/960 PASS`;
- [`P7.05 Operational Visibility Implementation Review`](../reviews/P7-05-operational-visibility-implementation-review.md) — `Complete / PASS`, four iterations;
- [`P7.05 Selected-Mac Operational Visibility Proof — Attempt 1`](../reviews/P7-05-selected-mac-proof-attempt-1.md) — `Complete / PASS`;
- exact tested canonical `main` and persistent runtime release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- selected host: `Darwin / arm64`, Python `3.14.7`;
- selected-Mac attestation SHA-256: `882a3515d05be05742dc811eab36c2cba943f6838d465222b6e52c1be9c0e630`.

The selected-Mac proof established an actually loaded independent P7.05 launchd observer, final healthy runtime, actionable alert creation/healthy clearing, exact P7.04-authorized metadata-only audit visibility with no payload exposure, and retention cleanup that removed expired non-canonical telemetry without changing the governed-state tree or deleting canonical state/evidence. Payload and reusable-secret logging remained disabled; no canonical mutation or external/product effect occurred.

Telemetry, raw diagnostics and local alerts remain non-canonical. The `168`-hour diagnostic retention default is owner-local implementation policy rather than an organization-wide legal retention policy. The launchd/stdlib observer remains private and reversible; no observability ADR is required at the current bounded scope.

P7.05 closure does not establish external/customer Production, an `Active` Platform Capability, Stable Product Contract, public/stable observability API, permanent monitoring backend/topology, remote paging, automatic remediation, SLA/SLO/support or conformance promotion.

### R22 — Persistent Runtime Health Review

Status: `Complete / PASS`.

Canonical evidence:

- [`R22 — Persistent Runtime Health Review`](../reviews/R22-persistent-runtime-health-review.md) — `Complete / PASS`, two functional iterations;
- remediation PR `#39`;
- tested remediation/review head: `c8d3dfe3f5bcb22e52a3faf41e1ea630d179d027`;
- GitHub `Reference Python CI` run `32111920701`: `964/964 PASS`.

R22 found and remediated three material cross-cutting defects before P7.06: mutable-`current` mixed-release observer execution, fail-open/ambiguous launchd observer lifecycle/status behavior, and incomplete detection of orphan reusable P7.04 secret plaintext. The revised observer is pinned as one coherent exact-release unit; observer lifecycle/status and selected-Mac release matching fail closed; P7.04 verification inspects the complete secret directory for unknown plaintext.

R22 deliberately did not deploy this remediation ad hoc to the selected Mac mini. [`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](../reviews/P7-06-selected-mac-governed-deploy-proof-attempt-8.md) has now carried and verified the merged R22 hardening through governed update, exact rollback and final re-update before operator-workspace or product workload expansion.

No ADR is required at the current private, reversible owner-local scope. R22 creates no Production, `Active` capability, Stable Product Contract, public/stable interface, permanent IAM/observability/deployment topology, SLA/SLO/support or broader conformance claim.

### P7.06 — Governed deploy/update/rollback/version/migration path

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.06 Governed Deploy / Update / Rollback / Version / Migration Path`](../implementation/P7-06-GOVERNED-DEPLOY-UPDATE-ROLLBACK-MIGRATION.md) — `Complete / PASS`;
- [`P7.06 Governed Deploy / Update / Rollback Implementation Cross-Review`](../reviews/P7-06-governed-deploy-implementation-review.md) — `Complete / PASS`, configured seven-iteration repository/live-readiness review;
- [`P7.06 Selected-Mac Live Remediation Review`](../reviews/P7-06-live-remediation-review.md) — `Complete / PASS`, seven bounded remediation iterations;
- [`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](../reviews/P7-06-selected-mac-governed-deploy-proof-attempt-8.md) — `Complete / PASS`;
- exact source release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- exact target/final active release: `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`;
- first update transaction: `a33209268d34b25c1bb8db9c63e835bf6149a404af57f8e77952177f22c5ffb3`;
- rollback transaction: `589f282e3e062c1b5aa298f841f044d4d9c6227214c862d45044673a5ce9e951`;
- final update transaction: `34470ac05993465155b8048405d1dbb712ffb9387b90a29666b927fcfb9dfdc4`;
- selected-Mac attestation SHA-256: `3dec1d1dd34aff960753105e72aa60739c01fb61c0af091a554e93f344418e69`;
- final PR #49 repository CI before merge: `998/998 PASS`.

Attempt 8 proved fresh verified backup before both update transitions, exact source→target update, exact target→source rollback with hardened observer re-pin, healthy source recovery, final controlled source→target re-update and final exact target health. No schema-changing migration or backup restore occurred; the deploy path performed no canonical organizational-state mutation, product/external effect or historical effect replay.

The R22 first-update obligation is therefore satisfied. The current private owner-local adapter remains reversible and does not establish a permanent deployment technology or public updater contract.

P7.06 closure does not establish external/customer Production, an `Active` Platform Capability, Stable Product Contract, supported macOS matrix, public/stable deployment API, generalized migration framework, automatic fleet rollout, SLA/SLO/support or broader conformance.

### P7.06-UI — Live operator workspace over persistent runtime

Status: `Complete / PASS`.

Detailed substream: [`P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md`](P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md) — `Complete / PASS 0.1.11`.

This substream operationalizes the already-complete Phase 4 / M4 workspace semantics instead of redesigning them. It connects explicit Organization/Actor context, Records, Executions, Evidence, Documents, Knowledge, exact-version/provenance inspection and bounded Governed Execution interaction to the persistent runtime through a private reversible operator surface.

`P7.06-UI1 — Live read-only governed workspace` is `Complete / PASS` after selected-Mac Attempt 2 on exact canonical/local/runtime release `b1b78ed9772727dda41b2e509675691f978957ec`. The approved retained P6.05-L7 manifest was verified at SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`; four distinct Governed Execution gate bases passed; one real P7.03 item/checkpoint was admitted/persisted; the second identical execution was idempotent; the real Subject/exact Version/provenance was browser-visible; and before/after governed-byte digests were unchanged. Network/external effects were `NONE`. Canonical closure evidence is [`P7.06-UI1 Selected-Mac Live-Browser Proof — Attempt 2`](../reviews/P7-06-UI1-selected-mac-proof-attempt-2.md).

`P7.06-UI2 — Governed interaction and preflight` is `Complete / PASS` through PR `#56`, exact reviewed head `305faafb790e1387cac2aaafa348fbc4ac583797`, five functional review/revise iterations and Reference Python CI run `32159051764 = success`. The boundary preserves four independent RFC-0005 gate concepts, authorized RFC-0006/CAP-004 reconstruction, related Execution evidence, uncertain-versus-reconciliation semantics and entry only through existing Governed Execution/operator-safety semantics.

`P7.06-UI3 — Persistent private operator access` is `Complete / PASS` after the final selected-Mac operational proof on exact canonical/runtime release `8451a5cb85c15ceb798438524f46cec87eacc981`. Bounded recovery first reconciled the previously inconsistent pointer to proven live release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5`, with recovery SHA-256 `0df255294f8cc17f91aca0fc0ac4eb6eb95eb6085be1a78aeaac85d7c2d39ba3`; the ordinary P7.06 governed update then advanced to target `8451a5cb85c15ceb798438524f46cec87eacc981` under transaction `5de0529aa4c8d478ae13639b12588815c7dfbe9714f6254a6e7dcfd61344ed4c` and passed the bounded stability window. The final UI3 proof passed least-privilege reuse, private loopback listener/PID attribution, HTTP/session negative and positive paths, uninstall/reinstall, governed rollback, historical reconciliation and final re-update. P7.03/P7.04 remained unchanged; no Organizational Authority, consequential approval, product/external effect or historical-effect replay occurred. Final UI3 attestation SHA-256: `05a30e20d1d6813ae786620fff8eb00544a04b87dfe5dabc07c2078d19b90f66`. Canonical closure: [`P7.06-UI3 — Selected-Mac Operational Closure`](../reviews/P7.06-UI3-selected-mac-operational-closure.md).

`P7.06-UI4 — First real owner interaction proof` is `Complete / PASS` on exact canonical/runtime release `1da5600963dcba982d3b1969480fd3f725133e12`. The owner successfully entered the live Safari workspace after the bounded PR `#73` browser-Origin remediation, confirmed explicit Organization/Actor and healthy exact runtime, navigated Records, Executions, Evidence and Documents over the real retained `platform.document`, inspected exact Subject/Version plus Execution/Event/checkpoint provenance/reconstruction, saw Authorization / Organizational Authority / Data Governance / Consequential Approval independently `Waiting`, and executed `Run governed preflight` once. Browser outcome: `WAITING / fail-closed`; no canonical mutation or external effect was requested. The exact-release technical verifier independently returned `PASS`, observed the browser POST and confirmed no Organizational Authority, consequential approval, canonical mutation or product/external effect. Owner-local minimized evidence SHA-256: `63416f1862168d9a464a30d1824198ad52be4439e9f43fba71360c7ac34a9f91`. Canonical closure: [`P7.06-UI4 — First real owner interaction closure`](../reviews/P7.06-UI4-first-real-owner-interaction-closure.md).

The Safari defect found by the owner proof is part of the closure evidence rather than an omitted transient issue. PR `#73` preserved exact loopback Host/Origin/CSRF/P7.04 fail-closed checks, changed only `Referrer-Policy` to `same-origin`, added regression coverage, passed final Reference Python CI `#150`, was deployed through the existing governed update path and was successfully re-proved in Safari.

`P7.06-UI = Complete / PASS` at `100%` for the declared private owner-operated scope. Completion creates no public/stable API, frontend framework, browser support promise, public Arvectum OS UI, Production claim, capability promotion or Stable Product Contract.

### P7.07 — Persistent Tender Operator operational contour

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.07 implementation`](../implementation/P7-07-PERSISTENT-TENDER-OPERATOR-CONTOUR.md) — `Complete / PASS`;
- [`P7.07 functional cross-review`](../reviews/P7-07-persistent-tender-operator-contour-review.md) — repository review complete with no remaining material repository-design objection;
- [`P7.07 Selected-Mac Attempt 1 product-bridge loader blocker`](../reviews/P7-07-selected-mac-attempt-1-loader-blocker.md) — fail-closed blocker preserved and remediated canonically;
- initial implementation PR `#75`, merge `bf1a3047aadf03384c9525eacd4e186a53092c11`;
- loader remediation PR `#76`, merge `b0c18fba15de6b5abac83a4f583d89eedb5c03d1`;
- Reference Python CI `#157 = success`;
- [`P7.07 — Selected-Mac Operational Closure`](../reviews/P7-07-selected-mac-operational-closure.md) — `Complete / PASS`;
- exact selected-Mac active release: `b0c18fba15de6b5abac83a4f583d89eedb5c03d1`;
- P7.06 update transaction: `7826f811cce4bc88a0e9a915e3806f6d23cb456428f8c53424d024342ebc33ec`;
- exact retained P7.07 storage item: `53061324eec2b46fefd04d6f19bddbcc42d2a3ebfc5e7120f10a616e693a0795`;
- selected-Mac evidence SHA-256: `9613637b06c5d192311bda1eb3096a9cd0b49c016134af887697637a668cf0f8`.

Selected-Mac Attempt 2 reused the existing persistent Organization/human Principal and exact item-scoped P7.04 read grant, returned `PASS_IDEMPOTENT_EXISTING` without creating a new governed item/checkpoint, loaded the real canonical product-owned bridge and returned `PASS_EXACT_CAP001_RELIANCE` both before and after an actual supervised P7.02 restart. Runtime generation advanced `59 → 60`, the runtime instance changed, `previous_instance_id` continuity passed, and P7.03 governed-state digest remained byte-stable at `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1`.

The two reads preserved the same exact storage item, Document Subject, exact Version, Artifact, integrity reference, P6.02 `0.1.0`, `External Reference` authority and authoritative source `ЕИС / zakupki.gov.ru`. No new EIS/SOAP retrieval, contour network action, ordinary-read canonical mutation, external effect, raw tender-byte exposure, credential-secret exposure or AI authority expansion occurred.

P7.07 closure does not promote P6.02 beyond `Provisional 0.1.0`, does not promote a Platform Capability and does not establish external/customer Production, public/stable persistence/API/SDK boundaries, SLA/SLO/support or broader conformance.

### P7.08 — Persistent Discount Parser cross-host operational contour

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.08 — Canonical Closure`](../reviews/P7-08-canonical-closure.md) — `Complete / PASS`;
- implementation/review PR `#78`, canonical merge `fefbea71a1f3941275faa6313e162f0040fecb8d`;
- final implementation head `8934b44c8156faf937fc3e1cfaf793d05508414e`;
- Reference Python CI `#159` / run `32245986650` — `success`;
- exact P6.06 Discount Parser Product Contract remains `Provisional 0.1.0`;
- shared platform dependency set remains exactly `{CAP-004}`.

The repeatable contour is explicitly asymmetric. Mac mini creates and retains the identity-bearing P6.07-compatible Stage 2A ticket, sending Windows only an immutable minimized dispatch containing execution/ticket digest, exact Product Contract pin and safety boundary. Windows verifies owner-local raw pre-effect/outcome evidence by SHA-256, retains those raw files and product database state locally, and returns only minimized exact references and digests. Mac mini verifies exact dispatch/ticket/handoff continuity and performs CAP-004 reconstruction as `ReadOnly` without calling Telegram, Discount Parser publication code or any other external mutation.

Organization/Actor identity, reusable secrets, raw Windows evidence and mutable product state do not cross the host boundary. No shared mutable database/filesystem/broker, platform transport service or stable cross-host API is introduced. Same verified completed handoff is idempotent; uncertain outcome, digest mismatch, partial reconstruction state and conflicting completed-execution replay fail closed. Historical reconstruction never replays the external effect and does not fabricate a retroactive platform gate decision.

P7.08 closure does not promote P6.06 beyond `Provisional 0.1.0`, does not promote CAP-004 or any Platform Capability, and does not establish external/customer Production, public/stable transport/API/persistence format, SLA/SLO/support or broader conformance.

### P7.09 — Operator runbook + incident/uncertain-outcome/recovery drills

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.09 — Canonical Closure`](../reviews/P7-09-canonical-closure.md) — `Complete / PASS`;
- versioned runbook: [`P7.09 Operator Runbook`](../implementation/P7-09-OPERATOR-RUNBOOK-INCIDENT-RECOVERY.md) `1.0.0`;
- implementation/review PR `#81`, canonical merge `e67af1c45b91eb265d36f8dd4fda440c0ff36b12`;
- final implementation head `c1dcc6d18f7f1f98204ec21c4c28db0dbb06fa02`;
- Reference Python CI `#160` / run `32248311483` — `success`;
- focused P7.09 tests: `23/23 PASS`;
- repository functional cross-review: four iterations, no remaining material objection;
- aggregate selected-Mac attestation basename `p7-09-selected-mac-drill-attestation-20260819T145500Z-aa5d.json`, SHA-256 `39b7987fc9d3e85926ba89125d2eb045f6e474995bd605284975628213ab6e34`;
- actual owner-initiated reboot receipt basename `p7-09-drill-mac-restart-20260819T152141Z-412ee082.json`, SHA-256 `bf54e903c9fae0d5468fa8b08acdee1f0c4354b549c8753d82357d0f7621a16a`.

The selected-Mac drill package covers runtime crash, actual Mac restart/login continuity, unavailable state/backup, network/proxy/TLS failure, product-host outage, uncertain external effect, partial evidence, credential rotation/revocation and failed-update/rollback behavior. The actual restart advanced runtime PID `35508 → 787` and generation `61 → 62` while preserving exact active release `b0c18fba15de6b5abac83a4f583d89eedb5c03d1`, automatically loaded P7.05 observer, P7.03 integrity `PASS` and consistent P7.06 state. No manual service start was needed after reboot.

Unknown external outcomes remain `RECONCILIATION_REQUIRED`; incomplete/unverifiable evidence fails closed; technical recovery grants neither Organizational Authority nor consequential approval; historical reconstruction/replay never repeats an external effect; no real consequential external effect was manufactured for a drill. The aggregate attestation's earlier simulated restart observation remains preserved rather than rewritten and is superseded for restart closure only by the actual-reboot receipt.

The selected Mac's local full unittest discovery reported environment-specific `/var` symlink/path failures while the exact implementation head passed the canonical full Reference Python CI. The discrepancy is non-blocking for P7.09 and is carried into P7.10 as portability evidence to test explicitly on the clean secondary environment.

P7.09 closure satisfies M7 criterion 9 for the declared scope. It creates no Production claim, lifecycle promotion, Stable Product Contract, public/stable recovery API, SLA/SLO/support commitment or clean-host portability claim.

### P7.10 — Portability, host-loss and restore-on-clean-environment proof

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.10 — Implementation Readiness Review`](../reviews/P7-10-implementation-readiness.md) — repository implementation and automated mechanism proof;
- [`P7.10 — Selected-Mac Operational Attempt 2`](../reviews/P7-10-selected-mac-attempt-2-clean-parent-failure.md) — preserved fail-closed secondary-parent failure;
- [`P7.10 — Canonical Closure`](../reviews/P7-10-canonical-closure.md) — final operational closure;
- implementation PR `#83`, merge `393cc5bff98cc87553b96d282f4bf618621fd87a`;
- restore-parent remediation PR `#86`, merge `16621a1abc814a92e8fed0d0a3451946be6f8303`, final full CI `1192 tests / OK`;
- exact-release procedure correction PR `#87`, merge `de59771281ce1b4c58d943bd003560384e332270`;
- exact retained handoff/tool release `fbab170ab337c1631b40d0d36ea58a02f6512f6e`;
- archive SHA-256 `074f2a4e84e222bd26d6ed21a829aa0dcc1c91834479345cfa652405b721bfbd`;
- handoff manifest SHA-256 `fe0d2c7d9460f9da4356a3a3f7419b825b8aef3a8d18123ab35fb0281db3ada9`;
- owner-local receipt basename `p7-10-clean-restore-receipt-attempt-3.json`, SHA-256 `ab7bf132d3d3a1304e3582c25fbd80a783d36c7bee9e5e6439ed4c54780aa341`.

The actual selected-Mac P7.03 governed store crossed the host-loss boundary through the unchanged verified four-member handoff and restored successfully on a separate clean MacBook Air environment. P7.03 integrity remained `PASS`; governed-state SHA-256 `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1` matched the source handoff; selected historical reconstruction passed; two governed items and two checkpoints were retained; reusable secrets, excluded runtime paths, external-effect replay and Organizational Authority grant remained absent.

Attempt 2 remains fail-closed evidence: a target directly beneath a macOS home directory with mode `0750` was rejected before publication. Closure used a dedicated non-symlink `0700` immediate restore parent without weakening the home-directory policy. The same handoff was restored at its exact embedded release rather than rebuilt or relabelled after documentation/test-only corrections.

The P7.09 `/var` versus `/private/var` discrepancy is dispositioned as a host path-presentation/environment issue only when physical filesystem identity proves equivalence. Lexical aliases resolving to different objects remain material and fail closed where same-location identity is required. The actual selected-Mac persistent source was the established owner-local runtime root, not `/var/lib/arvectum-os`.

P7.10 satisfies M7 criterion 10. Host/service-manager paths, machine-local credentials/secrets, network/proxy/TLS configuration and OS-specific ownership plumbing remain target-environment reprovisioning responsibilities rather than portable semantic state.

P7.10 closure creates no Production claim, lifecycle promotion, Stable Product Contract, Active Platform Capability, public/stable recovery/export format, permanent persistence technology, SLA/SLO/RPO/RTO/support commitment or broader conformance claim.

**R23 follows P7.10 and is `Complete / PASS`; P7.11 is now Current.**

### R23 — Recovery / Portability Review

Status: `Complete / PASS`.

Canonical evidence:

- [`R23 — Recovery / Portability Review`](../reviews/R23-recovery-portability-review.md) — `Complete / PASS`, three functional review/revise iterations;
- reviewed contour: P7.03, P7.06, P7.09 and P7.10;
- no Accepted ADR was required for the current private/reversible owner-operated recovery mechanisms.

R23 confirms that the accumulated recovery evidence composes into one fail-closed model: P7.03 owns durable governed-state backup/isolated restore semantics; P7.06 owns exact governed update/rollback/re-update behavior; P7.09 makes ordinary incident, uncertainty and recovery procedures executable; and P7.10 proves semantic governed-state portability beyond loss of the selected source host onto a clean secondary environment.

Portability is intentionally bounded to governed organizational state and historical identity/version/authority/provenance meaning. Machine-local credentials/secrets, service-manager configuration, runtime roots, network/proxy/TLS setup and OS-specific filesystem/ownership plumbing remain separately reprovisioned host prerequisites. Recovery does not grant Organizational Authority or consequential approval and never authorizes replay of a historical external effect.

R23 found no remaining material recovery/portability defect requiring implementation before P7.11. Release-source availability/retention, supported recovery-environment scope, any stable/public recovery boundary, lifecycle/conformance status and any RTO/RPO/SLO/SLA/support commitment are explicitly downstream P7.11 disposition questions rather than inferred R23 outcomes.

### P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition

Use accumulated evidence to decide whether the internal environment is fit for its declared scope; whether Product Contracts remain Provisional or justify separate Stable transitions; whether any CAP-001..CAP-004 capability justifies a separate `Active` admission process; which concrete boundaries crossed ADR/stable-boundary thresholds; and what Production/customer readiness remains unproven. No lifecycle transition occurs automatically inside P7.11.

### P7.12 — Phase 7 / M7 closure review

Close M7 only after declared Phase 7 work and R21–R24 findings are dispositioned, with exact scope and non-claims stated explicitly.

## 7. M7 exit criteria

`M7 — Scoped production-grade operating baseline` is achieved only when the declared scope demonstrates:

1. persistent owner-operated Arvectum OS runtime on the selected Mac mini with supervised start/restart behavior;
2. required governed state survives restart and has verified backup/restore behavior;
3. persistent identity/access/secrets handling preserves least privilege and authority separation;
4. actionable health/observability exists without turning telemetry into canonical authority;
5. upgrades and rollback/migration have a tested governed path;
6. the owner can inspect live governed state and perform a bounded governed interaction through the private live workspace without bypassing runtime authority/security boundaries;
7. Tender Operator can rely on the persistent runtime under its explicit Product Contract boundary;
8. Discount Parser can use a repeatable cross-host evidence/reconstruction contour without effect replay or hidden coupling;
9. incident/recovery procedures are executable and versioned;
10. host-loss/portability has been tested on a clean secondary environment within declared scope;
11. lifecycle/conformance/stable-boundary decisions are explicitly dispositioned rather than inferred;
12. all R21–R24 material findings are closed or accepted by appropriate authority;
13. the required M7 Milestone Code Health Gate passes before closure.

M7 criteria 9 and 10 are satisfied by P7.09 and P7.10 respectively for the declared `Persistent Internal / owner-operated` scope. R23 is `Complete / PASS`. Criteria 11–13 remain downstream.

M7 does **not** inherently require external customer Production, public multi-tenancy, an `Active` capability, Stable Product Contract, public SDK/API, SLA/support promise or one mandatory storage/IAM/deployment technology.

## 8. Current canonical action
> **P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition.**

R23 is `Complete / PASS`: the accumulated P7.03/P7.06/P7.09/P7.10 evidence forms a coherent, fail-closed recovery and semantic-portability model for the declared `Persistent Internal / owner-operated` scope. Governed state survives ordinary recovery paths and actual selected-host loss without implicit secret transfer, Organizational Authority grant, consequential approval or historical external-effect replay.

P7.11 now performs the explicit scoped operational-readiness, lifecycle, conformance and stable-boundary disposition. It must address private/reversible recovery mechanisms, release-source retention/availability assumptions, supported recovery-environment boundaries and separately reprovisioned host prerequisites without inferring Production, lifecycle promotion, Stable Product Contracts, `Active` capabilities, SLA/SLO/RPO/RTO/support or broader conformance from R23.