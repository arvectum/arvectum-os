# R23 — Recovery / Portability Review

Status: `Complete / PASS`
Date: `2026-08-19`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` review
Trigger: after `P7.10`, before `P7.11`
Reviewed contour: `P7.03`, `P7.06`, `P7.09`, `P7.10`
Operating scope: `Persistent Internal / owner-operated`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)

## 1. Purpose

R23 is the cross-cutting recovery and portability gate after the bounded durable-state baseline, governed deploy/update/rollback path, incident/recovery drills and real host-loss clean-environment restore have all been exercised.

The gate asks whether those mechanisms compose into one coherent recovery model that preserves governed organizational meaning and exact historical identity/provenance, fails closed on uncertainty or integrity loss, avoids implicit transfer of secrets or Organizational Authority, and is sufficiently portable within the declared internal scope to permit `P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition`.

R23 is an engineering/governance review. It is not a Production approval, lifecycle transition, Product Contract stabilization, Platform Capability activation, stable/public backup or migration interface, supported-host declaration, SLA/SLO/RPO/RTO/support commitment or external conformance claim.

## 2. Authority baseline checked

Checked before and during review:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with acceptance evidence;
- RFC-0001 — organizational control/portability, security/isolation, technology independence, reconstruction and stable-boundary constraints;
- RFC-0002 — stable Subject/Version identity, immutable canonical history, authority modes, technology-independent persistence and reconstructable payload/reference semantics;
- RFC-0003 — security/privacy/tenant sovereignty, deny-by-default, secret handling, governed portability packages, migration/handover and separation of technical recovery from Authorization and Organizational Authority;
- RFC-0005 — exact material version pinning, Governed Execution, failure/uncertainty/reconciliation and side-effect-safe recovery/retry behavior;
- RFC-0006 — append-only canonical Events, provenance/evidence integrity, explicit incomplete evidence and side-effect-safe historical replay;
- RFC-0008 — Document/Artifact identity, governed export/manifest semantics and semantic portability independent of storage locators;
- Accepted ADRs — none exist; `docs/adrs/` contains only the ADR process/index, so no persistence, backup, restore, deployment, host or portability technology is canonically selected by ADR;
- canonical Phase 7 and master roadmap sequencing;
- `P7.03`, `P7.06`, `P7.09` and `P7.10` canonical implementation/review/closure evidence.

No higher-authority conflict was found for the declared `Persistent Internal / owner-operated` scope.

## 3. Reviewed recovery chain

The accumulated evidence forms four complementary layers rather than competing recovery mechanisms:

1. **P7.03 — durable-state and backup/restore semantic owner.** Required governed state and checkpoints are persisted with integrity verification; backup/restore is isolated, replay-safe and excludes reusable secrets, runtime/log/cache material and accidental authority. The private filesystem/tar implementation remains reversible and non-stable.
2. **P7.06 — governed operational version transition and rollback.** Update, exact historical rollback and final re-update preserve exact release identity, verified pre-update backup, runtime/observer consistency and failure-closed recovery. Deployment does not mutate canonical organizational state or authorize historical product/external effects.
3. **P7.09 — executable incident/recovery behavior.** Runtime crash, actual host restart, unavailable backup/state, network/TLS failure, unavailable product host, uncertain external outcome, partial evidence, credential revocation/rotation and failed update/rollback are exercised under one operator runbook. Unknown outcomes remain `RECONCILIATION_REQUIRED`; incomplete evidence fails closed; technical recovery does not grant authority or approval.
4. **P7.10 — host-loss and semantic portability proof.** The actual selected-Mac P7.03 governed store crosses the source-host loss boundary through an owner-controlled encrypted off-host medium and restores on a separate clean MacBook Air at the exact embedded release. Integrity, governed-state digest, selected historical reconstruction, exclusions, no-replay and no-authority conditions all pass.

The chain therefore covers both ordinary operational recovery and loss of the original host without turning host configuration, credentials, service-manager state or storage locators into canonical organizational meaning.

## 4. Functional review iterations

Functional review completed in three iterations of the maximum seven.

### Iteration 1 — architecture / recovery-model composition

Result: `REVISE`.

Material review finding:

The individual P7.03 and P7.10 closure language is correct within each task, but a cross-cutting reader could overgeneralize `portability` into a claim that the complete operating host is portable or self-contained. That would conflict with the evidence: P7.10 proves governed-state portability and historical reconstruction, while machine-local credentials, runtime roots, service-manager configuration, network/proxy/TLS configuration and OS-specific plumbing are intentionally outside the handoff.

Disposition in R23:

- define the recovery model explicitly as **semantic governed-state portability plus separately reprovisioned host/runtime prerequisites**;
- treat P7.03 local backup and P7.10 off-host handoff as layered responsibilities, not competing backup topologies;
- preserve exact release identity as reconstruction evidence without turning one Git release, host, Python version or macOS layout into a stable platform contract;
- carry release-source availability/retention, supported recovery environments and any stronger self-contained restore requirement into P7.11 stable-boundary/readiness disposition rather than inventing them here;
- preserve all P7.10 non-claims for universal host portability, Production, SLA/SLO/RPO/RTO and public format/API support.

No implementation change is required by this clarification; the accumulated mechanism evidence already behaves according to the bounded model.

Result after revision: `PASS` for architecture/composition.

### Iteration 2 — security / authority / replay / evidence review

Result: `PASS`.

Security and authority findings:

- reusable secrets remain excluded from P7.03 backups and P7.10 handoff/restore; restore does not silently recreate credentials or broaden access;
- technical recovery remains distinct from Authentication, Authorization, Organizational Authority, Data Governance and consequential approval;
- P7.06 recovery/rollback and P7.09 drills preserve existing exact release/evidence state rather than selecting arbitrary newer code or granting an operator undeclared release authority;
- uncertain external outcomes remain reconciliation-required rather than blind retry candidates;
- historical Event/execution reconstruction does not authorize replay of an external effect;
- failed/incomplete evidence paths remain visible and fail closed;
- negative operational evidence is preserved rather than rewritten: P7.03 unhealthy-runtime attempt, P7.06 live remediation history, P7.09 simulated restart limitation and P7.10 owner-parent failure all remain part of the evidence trail;
- canonical closure evidence is minimized; raw secrets, personal identity material, hostnames and unnecessary local absolute paths are not promoted merely to make the review more detailed.

No material security, privacy, authority, replay or evidence objection remains.

### Iteration 3 — operations / host-loss / portability / P7.11 handoff

Result: `PASS with bounded downstream requirements`.

Operational conclusions:

- local restore integrity and tamper detection are proven by P7.03;
- governed update, exact rollback and final re-update are proven by P7.06;
- actual restart and the required incident/recovery scenarios are executable under P7.09;
- actual governed state survives loss of the selected source host and restores on a distinct clean secondary environment under P7.10;
- the `/var` versus `/private/var` discrepancy is not hidden: portability uses physical filesystem identity where equivalence matters and does not weaken restore-parent permissions;
- the clean restore preserves exact Subject/Version/authority/provenance/history meaning while machine-local material remains outside the portability package;
- no reviewed path depends on a mutable shared product database, hidden product stream or cross-product persistence contract.

R23 therefore does not require another recovery implementation before P7.11. The remaining questions are disposition questions, not unclosed R23 defects.

P7.11 must explicitly disposition at least:

1. the exact scope of operational readiness and conformance that the current owner-operated evidence supports;
2. whether any current private recovery/deployment/export mechanism remains intentionally private/reversible or crosses an ADR/stable-boundary trigger;
3. release-source retention/availability assumptions needed to reproduce an exact-release restore in the declared supported scope;
4. supported recovery-environment boundaries versus the already-proven but non-promised macOS/Linux CI and clean-secondary evidence;
5. host prerequisites that remain reprovisioned separately: credentials/secrets, service-manager configuration, runtime roots, network/proxy/TLS and OS-specific ownership/filesystem plumbing;
6. whether any RTO/RPO/SLO/SLA/support or customer-facing portability commitment is actually authorized — none exists today;
7. lifecycle and Product Contract/Platform Capability status independently of the fact that recovery mechanisms work.

No material R23 objection remains after this bounded handoff is made explicit.

## 5. Evidence matrix

| Recovery property | Primary evidence | R23 result |
|---|---|---|
| durable governed-state integrity | P7.03 selected-Mac Attempt 3 + implementation review | `PASS` |
| isolated verified restore | P7.03 | `PASS` |
| tamper / malformed archive failure closed | P7.03 | `PASS` |
| exact update / rollback / re-update | P7.06 selected-Mac Attempt 8 | `PASS` |
| mixed-release / inconsistent pointer recovery | P7.06 bounded live remediation | `PASS` |
| runtime crash recovery | P7.09 | `PASS` |
| actual host restart continuity | P7.09 real restart receipt | `PASS` |
| unavailable state/backup handling | P7.09 | `PASS` |
| uncertain external outcome | P7.09 | `PASS — RECONCILIATION_REQUIRED` |
| partial/unverifiable evidence | P7.09 | `PASS — fail closed` |
| credential revoke/rotation recovery | P7.09 + P7.04 boundary | `PASS` |
| selected-host loss boundary | P7.10 | `PASS` |
| clean secondary restore | P7.10 Attempt 3 | `PASS` |
| exact historical identity/version/provenance reconstruction | P7.10 + P7.03 | `PASS` |
| reusable-secret exclusion | P7.03 / P7.10 | `PASS` |
| excluded runtime/log/cache paths | P7.03 / P7.10 | `PASS` |
| historical external-effect replay | P7.06 / P7.09 / P7.10 | `NO — correctly prohibited` |
| Organizational Authority created by recovery | P7.09 / P7.10 | `NO — correctly prohibited` |

## 6. Cross-cutting residual risks and bounded deferrals

The following are real boundaries, but are not R23 failures within the declared scope:

- **Release source availability.** P7.10 proves exact-release restore from a clean environment, not indefinite availability of every future release source independently of repository hosting. P7.11 must disposition the supported retention/mirroring expectation before stronger commitments.
- **Secrets and credentials.** Their exclusion is a security property, not missing portability evidence. A restored host must re-establish applicable current credentials through governed credential/identity procedures.
- **Host bootstrap.** launchd/systemd configuration, runtime installation, filesystem roots and network/proxy/TLS setup remain environmental prerequisites rather than canonical governed-state payload.
- **Recovery objectives.** No measured or approved RTO/RPO/SLO/SLA/support commitment exists. Successful drills do not create one implicitly.
- **Supported environment matrix.** Successful macOS and CI portability evidence does not create universal host/OS compatibility.
- **Public/stable format.** The current filesystem/tar/handoff representations remain private implementation mechanisms. Cross-product/external reliance would reopen ADR/stable-boundary review.
- **Full service resumption on a replacement host.** P7.10 proves state restoration/reconstruction after host loss; it does not claim that a complete replacement runtime with all machine-local credentials/integrations is automatically activated by the handoff itself.

These limits are consistent with the existing non-claims and are intentionally passed to P7.11.

## 7. ADR / stable-boundary disposition

`ADR required by R23 itself: NO`.

The reviewed mechanisms remain owner-local, private, reversible and technology-specific adapters beneath stable organizational semantics. R23 does not select a permanent persistence engine, backup product, archive format, service manager, repository host, recovery orchestration system, public migration API or supported OS matrix.

P7.11 must re-open the ADR/stable-boundary gate if it proposes to make any of those mechanisms materially constraining, cross-product, externally relied upon, expensive to reverse or part of an explicit compatibility/support promise.

## 8. Gate result

**R23 result: `Complete / PASS`.**

The accumulated P7.03/P7.06/P7.09/P7.10 evidence composes into a coherent, fail-closed recovery and semantic-portability model for the declared `Persistent Internal / owner-operated` scope. Governed organizational state can be preserved, backed up, recovered through ordinary failure/update scenarios, transferred beyond loss of the original selected host and reconstructed on a clean secondary environment without silently transferring secrets, Organizational Authority or permission to replay historical external effects.

R23 has no remaining material objection that requires another recovery/portability implementation before P7.11.

This PASS does not establish external/customer Production, an `Active` Platform Capability, a Stable Product Contract, a public/stable backup/restore/export/migration boundary, a supported host/OS matrix, universal portability, full replacement-host service activation, SLA/SLO/RPO/RTO/support commitments or broader conformance.

Next canonical action:

> **P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition.**
