# Arvectum OS Phase 7 — Operational / Enterprise Readiness

Status: `Active`
Version: `1.2.6`
Created: `2026-08-17`
Updated: `2026-08-18`
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
| `P7.06` | Governed deploy/update/rollback/version/migration path | Mac mini + GitHub | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P7.06-UI` | Live operator workspace over persistent runtime | Mac mini + browser + GitHub | ⬜ Planned — gated by P7.06 core | `░░░░░░░░░░ 0%` |
| `P7.07` | Persistent Tender Operator operational contour | Mac mini + product environment + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.08` | Persistent Discount Parser cross-host operational contour | Windows + Mac mini + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.09` | Operator runbook + incident/uncertain-outcome/recovery drills | Mac mini + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | Mac mini + secondary clean environment + GitHub | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.11` | Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition | Chat/GitHub + evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.12` | Phase 7 / M7 closure review | Chat/GitHub | ⬜ | `░░░░░░░░░░ 0%` |

`P7.06-UI` is a subordinate operator-experience substream, not a new lifecycle or public-interface claim. Detailed plan: [`P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md`](P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md).

## 5. Engineering / quality gates

| Gate | Trigger | Status | Purpose |
|---|---|---|---|
| [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) | after `P7.01`, before material persistent-runtime implementation | 🟩 `Complete / PASS` | prevent persistent use from silently selecting unsupported production, public API, storage, IAM or deployment commitments |
| [`R22 — Persistent Runtime Health Review`](../reviews/R22-persistent-runtime-health-review.md) | after `P7.05`, before operational workload expansion | 🟩 `Complete / PASS` | review runtime/service boundaries, durability, access, observability, secrets, dependency direction, failure semantics and operator friction |
| `R23 — Recovery / Portability Review` | after `P7.10`, before lifecycle/readiness decisions | ⬜ | verify backup/restore, host-loss recovery, semantic portability, exact identities/versions/provenance and absence of host-specific hidden authority |
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

R22 did not deploy this remediation ad hoc to the selected Mac mini. The first controlled P7.06 update MUST carry the merged R22 hardening and prove the update/re-pin/health/rollback path before operational workload expansion. This preserves P7.06 as the governed owner of deployment/update semantics rather than silently inventing an update mechanism inside the review gate.

No ADR is required at the current private, reversible owner-local scope. R22 creates no Production, `Active` capability, Stable Product Contract, public/stable interface, permanent IAM/observability/deployment topology, SLA/SLO/support or broader conformance claim.

### P7.06 — Governed deploy/update/rollback/version/migration path

Status: `Current`.

Required evidence includes immutable deployment/release pin, pre-update backup/checkpoint, compatibility/migration checks, controlled stop/update/re-pin/start, post-update runtime and observer exact-release health verification, rollback/unsafe-rollback disposition and exact historical version references. No public release/support promise is implied.

The first controlled P7.06 update MUST include the merged R22 hardening before any P7.06-UI/P7.07/P7.08 operational surface expansion. Historical replay or rollback must not re-invoke prior consequential external effects without fresh applicable authorization/authority.

### P7.06-UI — Live operator workspace over persistent runtime

Status: `Planned / gated by P7.06 core`.

Detailed substream: [`P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md`](P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md).

This substream operationalizes the already-complete Phase 4 / M4 workspace semantics instead of redesigning them. It connects explicit Organization/Actor context, Records, Executions, Evidence, Documents, Knowledge, exact-version/provenance inspection and bounded Governed Execution interaction to the persistent runtime through a private reversible operator surface.

The sequence is `UI1 live read-only workspace → UI2 governed interaction/preflight → UI3 persistent private operator access → UI4 first real owner interaction proof`.

`P7.06-UI = PASS` requires the owner to open the live workspace in a browser against the selected Mac mini, inspect real governed state and exact provenance/reconstruction, and exercise at least one bounded governed interaction without presentation code becoming authority or a direct canonical-mutation path.

Completion creates no public/stable API, frontend framework, browser support promise, public Arvectum OS UI, Production claim, capability promotion or Stable Product Contract.

### P7.07 — Persistent Tender Operator operational contour

Run the first real product as an ongoing consumer of the persistent internal Arvectum OS runtime, preserving the exact Product Contract boundary or creating a justified new version before reliance, external EIS authority, persistent attributable context, restart survivability and no unauthorized external mutation or procurement-domain leakage.

### P7.08 — Persistent Discount Parser cross-host operational contour

Make the Windows product ↔ Mac mini evidence/reconstruction path operationally repeatable while preserving the exact Product Contract or justified revision, CAP-004-only boundary unless evidence proves otherwise, minimized evidence transfer, replay safety, no secret/identity over-transfer and no hidden shared state.

### P7.09 — Operator runbook + incident/uncertain-outcome/recovery drills

Minimum scenarios: runtime crash, Mac restart, unavailable persistent state/backup, network/proxy/TLS failure, product host unavailable, uncertain external effect, partial evidence path, credential revocation/rotation and failed update/rollback. Technical recovery must remain distinct from consequential re-authorization.

### P7.10 — Portability, host-loss and restore-on-clean-environment proof

Prove organizational continuity beyond the selected Mac mini through an export/backup package, clean secondary restore, selected historical reconstruction, explicit host-specific adapters/configuration and honest portability gaps without copying non-exportable secrets merely to claim portability.

**R23 follows P7.10.**

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

M7 does **not** inherently require external customer Production, public multi-tenancy, an `Active` capability, Stable Product Contract, public SDK/API, SLA/support promise or one mandatory storage/IAM/deployment technology.

## 8. Current canonical action

> **P7.06 — Governed deploy/update/rollback/version/migration path.**

R22 is `Complete / PASS` after two functional iterations and GitHub `Reference Python CI` run `32111920701` with `964/964 PASS`. The review closed material mixed-release observer, launchd lifecycle/status and orphan-secret detection defects at repository level without changing higher-level authority or lifecycle boundaries. The remediation is intentionally not claimed as already deployed on the live selected Mac mini: the first P7.06 controlled update must carry and verify it before operator-workspace or P7.07/P7.08 workload expansion.

After `P7.06 core = PASS`, the next canonical operator-experience action is `P7.06-UI1 — Live read-only governed workspace`, followed by the remaining UI substream before P7.07.
