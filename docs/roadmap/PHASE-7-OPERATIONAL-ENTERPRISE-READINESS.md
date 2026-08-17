# Arvectum OS Phase 7 — Operational / Enterprise Readiness

Status: `Active`
Version: `1.2.1`
Created: `2026-08-17`
Updated: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M7 — Scoped production-grade operating baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 6 — Product-driven Platform Validation`, `M6` achieved
Activation decision: [`DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION`](../governance/decisions/DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION.md)

## 1. Purpose

Phase 7 moves Arvectum OS from bounded real-product validation into persistent, recoverable, observable and governable internal operation.

The phase deliberately begins regular owner-operated use early rather than waiting until all enterprise-readiness work is finished. The platform should accumulate operational evidence while it is being hardened.

The primary near-term operating environment is the selected ООО «Арвектум» Mac mini. The Mac mini is an **operational environment**, not a platform architecture commitment or a supported macOS product promise.

The Phase 7 question is:

> Can Arvectum OS operate continuously enough to become a dependable internal organizational foundation, survive ordinary failures and upgrades, preserve governed state and provenance, and expose sufficient operational evidence to support later scoped production-readiness decisions?

## 2. Starting state inherited from M6

M6 established:

- two materially distinct real product/workflow validation chains;
- Tender Operator governed exact-document admission/reconstruction;
- Discount Parser real Telegram publication evidence reconstructed through CAP-004 without effect replay;
- real Organization/human Actor continuity in owner-operated execution;
- Product Contracts before governed platform reliance;
- successful Mac mini owner-operated execution;
- final Reference Python regression evidence of `911` tests / `PASS` in the P6.07 Stage 2C contour;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 Product Contracts remain `Provisional 0.1.0`;
- no Stable/public SDK/API/wire/deployment topology;
- no Platform Capability is `Active`;
- no external/customer Production, SLA/support or full-platform conformance claim.

M6 also exposed operational/developer friction including low-level provenance assembly, owner-local checkpoint persistence, manual exact execution-version/gate linkage and task-specific evidence orchestration. Those observations are evidence inputs, not automatically approved shared platform requirements.

## 3. Operating-mode rule

Phase 7 distinguishes:

- **bounded validation runtime** — task-scoped, started for a specific proof;
- **Persistent Internal / owner-operated runtime** — regularly running internal Arvectum OS environment used by ООО «Арвектум» for ongoing governed work;
- **Production** — an environment with separately approved operational scope and applicable external/customer/internal commitments.

Passing `P7.02` moves the selected Mac mini from bounded validation use into **Persistent Internal / owner-operated** use.

P7.02 has passed. The selected Mac mini therefore operates in the declared `Persistent Internal / owner-operated` mode while P7.03–P7.12 harden the live baseline.

That transition does not itself make the environment Production and does not change capability or Product Contract lifecycle. It also does not by itself prove the repeatable product operational contours that remain assigned to P7.07 and P7.08.

## 4. Phase 7 work breakdown

| ID | Work item | Primary execution venue | Status | Progress |
|---|---|---|---:|---:|
| `P7.01` | Persistent internal operating boundary + operational requirements baseline | Chat/GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.02` | Persistent Mac mini runtime + boot/restart/service lifecycle | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.03` | Durable governed state/checkpoint persistence + backup/restore baseline | Mac mini + GitHub | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.04` | Persistent identity/operator/service access + least-privilege operations | Chat + Mac mini + GitHub | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P7.05` | Health, observability, audit visibility, alerting + retention/minimization | Mac mini + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.06` | Governed deploy/update/rollback/version/migration path | Mac mini + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.07` | Persistent Tender Operator operational contour | Mac mini + product environment + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.08` | Persistent Discount Parser cross-host operational contour | Windows + Mac mini + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.09` | Operator runbook + incident/uncertain-outcome/recovery drills | Mac mini + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | Mac mini + secondary clean environment + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.11` | Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition | Chat/GitHub + evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.12` | Phase 7 / M7 closure review | Chat/GitHub | ⬜ | `░░░░░░░░░░ 0%` |

## 5. Engineering / quality gates

| Gate | Trigger | Status | Purpose |
|---|---|---|---|
| [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) | after `P7.01`, before material persistent-runtime implementation | 🟩 `Complete / PASS` | prevent the persistent-use requirement from silently selecting unsupported production, public API, storage, IAM or deployment commitments |
| `R22 — Persistent Runtime Health Review` | after `P7.05`, before operational workload expansion | ⬜ | review runtime/service boundaries, durability, access, observability, secrets, dependency direction, failure semantics and operator friction |
| `R23 — Recovery / Portability Review` | after `P7.10`, before lifecycle/readiness decisions | ⬜ | verify backup/restore, host-loss recovery, semantic portability, exact identities/versions/provenance and absence of host-specific hidden authority |
| `R24 — M7 Operational Hardening` | after `P7.11`, before `P7.12` | ⬜ | final bounded architecture/code/security/maintainability/fitness review and the required M7 Milestone Code Health Gate |

These gates are engineering/governance checkpoints. They are not Platform Capability lifecycle transitions or formal production approvals.

## 6. Work-item intent and exit evidence

### P7.01 — Persistent internal operating boundary + operational requirements baseline

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.01 Persistent Internal Operating Boundary and Operational Requirements Baseline`](P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) — `Complete / Baseline 1.0.1`;
- [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) — `Complete / PASS`, two iterations.

The baseline defines the `Persistent Internal / owner-operated` operating classification, current ООО «Арвектум» Organization scope, owner/operator authority boundary, bounded admitted workloads, data/secret/retention/network/recovery constraints, ADR/stable-boundary triggers and reversible removal path.

No customer SLA/SLO promise, Production claim, lifecycle promotion, Stable Product Contract, public API or permanent persistence/IAM/service/deployment choice was created.

**Exit:** satisfied — canonical P7.01 baseline + `R21 PASS`.

### P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.02 Persistent Mac mini Runtime and Service Lifecycle`](../implementation/P7-02-MAC-MINI-PERSISTENT-RUNTIME.md) — `Complete / PASS`;
- [`P7.02 Persistent Runtime Implementation Cross-Review`](../reviews/P7-02-persistent-runtime-implementation-review.md) — `Complete / PASS`, five iterations;
- [`P7.02 Selected Mac mini Proof Attempt 1`](../reviews/P7-02-selected-mac-proof-attempt-1.md) — failed operational attempt preserved, defect remediated;
- [`P7.02 Selected Mac mini Proof Attempt 2`](../reviews/P7-02-selected-mac-proof-attempt-2.md) — `Complete / PASS`;
- exact proven release: `73af746f83271b14670fe22db658dfd55cacb291`;
- repository remediation PR `#27`: `920/920` Reference Python tests PASS.

Proven evidence includes predictable stop/start/restart, owner-login launchd supervision, actual crash replacement, health generation advance, no observed runtime-owned network listener, no product-effect replay, no canonical-state mutation by the runtime envelope, no reusable P7.02 secret requirement and a reversible service removal path.

A concrete macOS service mechanism such as `launchd` remains an environment-specific adapter, not a stable platform contract.

**Operational transition:** satisfied. Arvectum OS entered **regular persistent internal operation on the selected Mac mini**.

**Exit:** satisfied — repository implementation/remediation + selected-Mac lifecycle/crash/listener proof + cross-review PASS.

### P7.03 — Durable governed state/checkpoint persistence + backup/restore baseline

Status: `Complete / PASS`.

Canonical evidence:

- [`P7.03 Durable Governed State / Checkpoint Persistence and Backup / Restore Baseline`](../implementation/P7-03-DURABLE-GOVERNED-STATE-BACKUP-RESTORE.md) — `Complete / PASS`;
- [`P7.03 Durable State Implementation Cross-Review`](../reviews/P7-03-durable-state-implementation-review.md) — `Complete / PASS`, six iterations;
- [`P7.03 Selected Mac mini Proof Attempt 1`](../reviews/P7-03-selected-mac-proof-attempt-1.md) — rejected as closure evidence because reported `PASS` conflicted with stopped runtime state; scoped backup/restore observations retained;
- [`P7.03 Selected Mac mini Proof Attempt 2`](../reviews/P7-03-selected-mac-proof-attempt-2.md) — hardened proof correctly failed closed while P7.02 runtime was `stopped`;
- [`P7.03 Selected Mac mini Proof Attempt 3`](../reviews/P7-03-selected-mac-proof-attempt-3.md) — `Complete / PASS` after owner-authorized ordinary P7.02 `start` recovery;
- repository implementation PR `#30`, merge `e2440b6f8afc7e0f21b20d370047bfa3ac803017`, full Reference Python CI `932/932 PASS`;
- proof-contract hardening PR `#31`, merge `5d33f874beb38f773ecf816ecd6d35e5fcb26c97`, full Reference Python CI `935/935 PASS`.

Attempt 3 executed clean exact canonical tool release `e20b7801cf389b1afe7f513182d352a566809c55` against unchanged P7.02 runtime release `73af746f83271b14670fe22db658dfd55cacb291`.

Selected-Mac PASS evidence includes:

- hardened runtime requirement enforced before and after proof;
- runtime state `healthy` before and after;
- exact P7.02 runtime release unchanged;
- live backup and isolated restore integrity `PASS`;
- restored state digest equal to live state digest;
- separate non-authoritative fixture backup/restore `PASS`;
- deliberate tamper detection fail-closed;
- `run/`, `logs/`, `cache/`, `secrets/` absent from backup;
- no reusable secrets, telemetry or cache in backup;
- checkpoint and proof fixture non-authoritative;
- no external-effect replay authorization;
- clean source checkout after proof.

Selected live backup:

- `p7-03-backup-20260817T192924Z-a8b80b0fe41809da.tar.gz`;
- SHA-256 `6b2661050a2d777c9cae0bada8c584c2e426489156505dc30e6ce5756de97765`.

The implementation remains a bounded owner-local reversible filesystem/tar adapter. No Accepted ADR is required at this scope; the ADR/stable-boundary gate remains mandatory before materially constraining, cross-product or externally relied-upon persistence reliance.

P7.03 does not establish external/customer Production, an Active Platform Capability, a Stable Product Contract, SLA/SLO/RPO/RTO/support, permanent persistence technology, off-host disaster recovery, product persistent contours, generalized update/migration or final IAM/secret lifecycle.

**Exit:** satisfied — durable-state implementation + CI + hardened selected-Mac backup/restore proof + final cross-review PASS.

### P7.04 — Persistent identity/operator/service access + least-privilege operations

Status: `Current`.

Evolve the P6 owner-operated identity proof into an operational access model without conflating identity, authentication, authorization and Organizational Authority.

Required evidence:

- attributable human operator identity;
- attributable workload/service identity where machine execution is operationally significant;
- deny-by-default access behavior;
- least-privilege operation/resource/Organization scope;
- secret/credential storage and rotation path;
- revocation/disablement path;
- no ambient admin access to organization content;
- explicit boundary for consequential approvals and residual owner authority;
- remote administration that does not create an undocumented authority path.

### P7.05 — Health, observability, audit visibility, alerting + retention/minimization

Make persistent operation inspectable without turning logs/metrics into canonical authority.

Required evidence:

- liveness/readiness or equivalent health indicators;
- process/runtime resource visibility proportionate to internal use;
- failure and restart visibility;
- bounded operational logs with rotation/retention;
- separation of canonical Events/evidence from telemetry;
- no reusable secret/raw sensitive material in ordinary logs;
- alerts for actionable persistent-runtime failures;
- operator ability to inspect recent governed execution/reconstruction status;
- documented blind spots and degradation behavior.

**R22 follows P7.05.**

### P7.06 — Governed deploy/update/rollback/version/migration path

Make upgrades repeatable and reversible while preserving exact historical interpretation.

Required evidence:

- immutable deployment/release pin;
- pre-update backup/checkpoint;
- compatibility/migration checks where governed state changes;
- controlled stop/update/start sequence;
- health verification after update;
- rollback to last-known-good version;
- explicit disposition when rollback would be unsafe due to state migration;
- historical execution reconstruction keeps exact version references.

No public release/support promise is implied.

### P7.07 — Persistent Tender Operator operational contour

Run the first real product as an ongoing consumer of the persistent internal Arvectum OS environment rather than through one-off validation harnesses.

Required evidence:

- exact P6.02 Product Contract continuity or a justified new Product Contract version before reliance;
- persistent Organization/Actor/service context;
- external EIS authority preserved;
- governed evidence/admission/reconstruction survives restart and ordinary operating cadence;
- no procurement semantics migrate into platform behavior;
- operator friction and failure/recovery evidence captured;
- no unauthorized external mutation.

The goal is repeatable real internal operation, not a fixed transaction quota.

### P7.08 — Persistent Discount Parser cross-host operational contour

Make the Windows product ↔ Mac mini Arvectum OS evidence/reconstruction path operationally repeatable without forcing the product onto the Mac mini.

Required evidence:

- exact P6.06 Product Contract continuity or justified revision before reliance;
- CAP-004-only boundary remains valid unless evidence proves otherwise;
- durable/repeatable minimized evidence handoff;
- no raw-secret or unnecessary identity migration between hosts;
- external Telegram effects remain product-owned and separately authorized where required;
- replay-safe CAP-004 reconstruction;
- host/network interruption behavior and reconciliation path;
- no hidden shared-state dependency.

### P7.09 — Operator runbook + incident/uncertain-outcome/recovery drills

Turn operational knowledge into versioned procedures rather than tacit memory.

Minimum scenarios:

- runtime process crash;
- Mac mini restart;
- unavailable persistent state/backup location;
- network/proxy/TLS failure;
- product host unavailable;
- uncertain external-effect outcome;
- failed/partial governed evidence path;
- credential revocation/rotation;
- failed update/rollback.

The runbook must distinguish technical recovery from consequential re-authorization. Historical replay must not repeat an external effect without new authorization.

### P7.10 — Portability, host-loss and restore-on-clean-environment proof

Prove that organizational continuity does not depend on the specific Mac mini.

Required evidence:

- export/backup package with governed identities, versions, authority/provenance references and explicit omissions as applicable;
- restore on a clean secondary environment appropriate to the current scope;
- no copying of non-exportable secrets merely to claim portability;
- reconstruction of selected historical governed outcomes after restore;
- documented host-specific adapters/configuration;
- documented recovery gaps rather than overstated portability.

The clean secondary environment may be another Mac, VM or other appropriate host. Passing the test does not create a supported hardware/OS matrix.

**R23 follows P7.10.**

### P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition

Use accumulated operating evidence to decide what, if anything, is ready for stronger lifecycle or conformance claims.

Required dispositions:

- whether the persistent internal environment is fit for its declared operating scope;
- whether any Product Contract should remain Provisional or has evidence for a separate Stable transition;
- whether any CAP-001..CAP-004 capability has evidence for an `Active` admission process;
- whether a concrete persistence, service, API, IAM, serialization or deployment boundary crossed the ADR/stable-boundary threshold;
- what operational support/compatibility claims are actually justified;
- what production/customer readiness remains unproven;
- whether Decision Authority Policy approval or another explicit delegation is required before a proposed lifecycle/production claim.

No lifecycle transition occurs automatically inside P7.11. Each material promotion requires its own governed decision and required evidence.

### P7.12 — Phase 7 / M7 closure review

Close M7 only after all declared Phase 7 work and R21–R24 findings are dispositioned.

The closure must state exactly what is operationally proven and what remains outside scope.

## 7. M7 exit criteria

`M7 — Scoped production-grade operating baseline` is achieved only when the declared scope demonstrates:

1. a persistent owner-operated Arvectum OS runtime operates on the selected Mac mini with supervised start/restart behavior;
2. required governed state survives restart and has verified backup/restore behavior;
3. persistent identity/access/secrets handling preserves least privilege and authority separation;
4. actionable health/observability exists without turning telemetry into canonical authority;
5. upgrades and rollback/migration have a tested governed path;
6. Tender Operator can rely on the persistent runtime under its explicit Product Contract boundary;
7. Discount Parser can use a repeatable cross-host evidence/reconstruction contour without effect replay or hidden coupling;
8. incident/recovery procedures are executable and versioned;
9. host-loss/portability has been tested on a clean secondary environment within declared scope;
10. lifecycle/conformance/stable-boundary decisions are explicitly dispositioned rather than inferred;
11. all R21–R24 material findings are closed or accepted by appropriate authority;
12. the required M7 Milestone Code Health Gate passes before closure.

M7 does **not** inherently require:

- an external customer Production deployment;
- a public multi-tenant service;
- an `Active` Platform Capability;
- a Stable Product Contract;
- a public SDK/API;
- an SLA/support promise;
- one mandatory storage/IAM/deployment technology.

## 8. Current canonical action

> **P7.04 — Persistent identity/operator/service access + least-privilege operations.**

P7.01/R21, P7.02 and P7.03 are complete. The selected Mac mini remains in regular `Persistent Internal / owner-operated` use with a verified bounded durable-state/checkpoint and backup/restore baseline. P7.04 now establishes persistent attributable human/workload identity and least-privilege access/secret operations without conflating technical access with Organizational Authority.
