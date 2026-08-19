# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.55.9`
Created: `2026-08-07`
Updated: `2026-08-19`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

Future roadmap content is a planning hypothesis until its phase is activated. Roadmap status does not by itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

## 2. Version note

Version `2.55.9` closes `P7.07 — Persistent Tender Operator operational contour` as `Complete / PASS` for the declared selected-Mac `Persistent Internal / owner-operated` scope. Initial repository implementation merged through PR `#75` at `bf1a3047aadf03384c9525eacd4e186a53092c11`. Selected-Mac Attempt 1 passed governed setup but failed closed before the first real product read on a private dynamic-module registration defect; no local release/product/interpreter workaround was accepted. PR `#76` remediated that loader defect by registering the bounded product bridge module in `sys.modules` before execution, added unmocked `@dataclass(frozen=True, slots=True)` regression coverage, merged at `b0c18fba15de6b5abac83a4f583d89eedb5c03d1`, and Reference Python CI `#157` completed with `success`.

Selected-Mac Attempt 2 then advanced the persistent runtime to exact release `b0c18fba15de6b5abac83a4f583d89eedb5c03d1` through P7.06 transaction `7826f811cce4bc88a0e9a915e3806f6d23cb456428f8c53424d024342ebc33ec`, reused the already-admitted exact P7.07 governed item through `PASS_IDEMPOTENT_EXISTING`, retained zero active temporary setup grants and the exact item-scoped persistent read grant, and completed real CAP-001 reliance through the canonical `arvectum/tender-agent` product bridge before and after an actual supervised P7.02 restart. Runtime generation advanced `59 → 60`, instance replacement and `previous_instance_id` continuity passed, and the P7.03 governed-state digest remained byte-stable at `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1`.

Before/after reliance preserved the same exact storage item, Document Subject, exact Version, Artifact, integrity reference, P6.02 Product Contract `0.1.0`, `External Reference` authority and authoritative source `ЕИС / zakupki.gov.ru`. No EIS/SOAP retrieval, P7.07 network action, ordinary-read canonical mutation, tender/email/Telegram/payment/signature or other external effect, raw tender-byte exposure, credential-secret exposure or AI authority expansion occurred. Owner-local evidence remains outside Git; canonical closure records basename `selected-mac-restart-proof.json` and submitted SHA-256 `9613637b06c5d192311bda1eb3096a9cd0b49c016134af887697637a668cf0f8` in [`P7.07 — Selected-Mac Operational Closure`](../reviews/P7-07-selected-mac-operational-closure.md).

`P7.07 = Complete / PASS`; M7 criterion 7 is satisfied for the declared scope. Active Phase 7 advances to `1.2.12`, and the current canonical action becomes `P7.08 — Persistent Discount Parser cross-host operational contour`. This closure does not promote P6.02 beyond `Provisional 0.1.0`, does not promote a Platform Capability, and creates no external/customer Production, public/stable API/SDK/persistence format, SLA/SLO/support or broader conformance claim.

Version `2.55.8` closes `P7.06-UI4 — First real owner interaction proof` and the parent `P7.06-UI — Live operator workspace over persistent runtime` as `Complete / PASS` for the declared selected-Mac `Persistent Internal / owner-operated` scope. Final proof ran on exact canonical/runtime release `1da5600963dcba982d3b1969480fd3f725133e12`. The owner entered the live private workspace in Safari, visibly confirmed Organization `aa4e760c379c8952aba6c6c335f3e233`, attributable human Actor `e4fc60984850106dbfc922ba30ec2332` and healthy exact runtime, navigated Records, Executions, Evidence and Documents, and inspected the real retained `platform.document` from the approved EIS evidence path with distinct Subject/exact Version, `External Reference` authority, ЕИС authoritative source, exact Execution/Event/checkpoint continuity and `CAP-004 reconstruction complete`.

The owner saw Authorization, Organizational Authority, Data Governance and Consequential Approval remain independently `Waiting`, then clicked `Run governed preflight` once. Browser result was `WAITING / fail-closed`; no canonical mutation or external effect was requested. The exact-release selected-Mac technical verifier independently returned `PASS`, observed the browser preflight POST and confirmed technical interaction access without Organizational Authority, consequential approval, canonical mutation or product/external effect. Owner-local minimized evidence is retained canonically only by basename and SHA-256 `63416f1862168d9a464a30d1824198ad52be4439e9f43fba71360c7ac34a9f91`.

The real owner session also exposed one material Safari unlock interoperability defect. PR `#73` remediated the browser metadata self-conflict by changing only private UI `Referrer-Policy` from `no-referrer` to `same-origin` while keeping exact loopback Host/Origin, CSRF, P7.04 least-privilege and no-authority/no-direct-mutation checks fail-closed; final Reference Python CI `#150` passed. The selected Mac was updated through the existing canonical P7.06 governed path to the merged release and the same Safari unlock was re-proved successfully. Canonical closure is recorded in [`P7.06-UI4 — First real owner interaction closure`](../reviews/P7.06-UI4-first-real-owner-interaction-closure.md), with four functional review/revise iterations and no remaining material objection.

The overall `P7.06-UI` substream therefore advances from `75%` to `100% / Complete / PASS`, live-workspace substream advances to `0.1.11`, active Phase 7 to `1.2.11`, and the current canonical action becomes `P7.07 — Persistent Tender Operator operational contour`. This closure creates no public/stable UI/API/session/browser contract, external/customer Production, Platform Capability lifecycle promotion, Stable Product Contract, Organizational Authority, consequential approval, SLA/support or broader conformance claim.

Version `2.55.7` closes `P7.06-UI3 — Persistent private operator access` as `Complete / PASS` for the declared selected-Mac `Persistent Internal / owner-operated` scope. The final operational proof ran on exact canonical checkout/runtime release `8451a5cb85c15ceb798438524f46cec87eacc981` after the bounded P7.06 consistency-recovery path repaired the previously forensically classified `UPDATE_COMMAND_FAILED` pointer/live-runtime mismatch. Recovery reconciled `current` from `d5cb521bf2565c42ad8ccf47565dda18cf9106c6` to proven live runtime/observer release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5` without changing P7.03 or P7.04; owner-local recovery evidence is retained canonically only by SHA-256 `0df255294f8cc17f91aca0fc0ac4eb6eb95eb6085be1a78aeaac85d7c2d39ba3`.

The ordinary canonical-checkout P7.06 governed update then advanced source `6d4d07aead603841ecce3c469dd46f5e0d58ccd5` to exact target `8451a5cb85c15ceb798438524f46cec87eacc981` under transaction `5de0529aa4c8d478ae13639b12588815c7dfbe9714f6254a6e7dcfd61344ed4c`; bounded 20-second P7.02/P7.05 stability passed. The complete UI3 proof then passed existing exact P7.04 human UI1/UI2 grant reuse with exactly one active selected human credential, supervised private launchd lifecycle, exact `127.0.0.1:8766` listener/PID attribution, owner-only private material/log minimization, unauthenticated/wrong-secret denial, owner-local unlock, bounded session and restart invalidation, uninstall/reinstall, governed rollback, historical reconciliation and final re-update. Controller evidence confirmed `hardened_controller_runner_verified = true`, `historical_ui3_controller_replayed = false`, `canonical_checkout_deploy_controller_verified = true` and `release_snapshot_deploy_controller_invoked = false`. Final active release, P7.02, P7.05 and UI3 status all passed; P7.03/P7.04 remained unchanged; no real UI4 interaction, Organizational Authority, consequential approval, product/external effect or historical-effect replay occurred. Owner-local UI3 attestation is retained canonically only by SHA-256 `05a30e20d1d6813ae786620fff8eb00544a04b87dfe5dabc07c2078d19b90f66`.

Canonical closure is recorded in [`P7.06-UI3 — Selected-Mac Operational Closure`](../reviews/P7.06-UI3-selected-mac-operational-closure.md). The overall `P7.06-UI` substream remains `Current`, advances from `50%` to `75%`, live-workspace substream advances to `0.1.10`, active Phase 7 to `1.2.10`, and the current canonical action becomes `P7.06-UI4 — First real owner interaction proof`. This closure creates no public/stable UI/API/session contract, external/customer Production, Platform Capability lifecycle promotion, Stable Product Contract, browser support matrix, SLA/support or broader conformance claim.

Version `2.55.6` closes `P7.06-UI2 — Governed interaction and preflight` as `Complete / PASS` for its declared bounded repository implementation/review scope. PR `#56` merged the private loopback governed-interaction adapter and typed preflight composition at merge `a22ba781d32f64b7097aeaf05a90651308533811`; exact implementation head `305faafb790e1387cac2aaafa348fbc4ac583797` passed five functional review/revise iterations and Reference Python CI run `32159051764` / `#107 = success`. The six required UI2 flows are covered: exact Subject/Version opening; provenance plus authorized RFC-0006/CAP-004 reconstruction and related Execution evidence; four independent Authorization / Organizational Authority / Data Governance / Consequential Approval states; transient action intent; entry only through existing R10 operator-safety/Governed Execution/runtime-consistency semantics; and evidence-derived blocked/waiting/observed-uncertain/reconciliation-required/succeeded presentation.

UI2 does not create a UI-local direct canonical write path, ambient authority, optimistic-success projection, browser-supplied gate/authority evidence, public/stable route/API/session/frontend contract, lifecycle/Product Contract promotion, external/customer Production, browser-support or SLA/support commitment. The overall `P7.06-UI` substream remains `Current`, advances to `50%`, live-workspace substream version `0.1.6`, active Phase 7 `1.2.9`, and the current canonical action becomes `P7.06-UI3 — Persistent private operator access`. UI4 remains responsible for the first real selected-owner interaction proof.

Version `2.55.5` closes `P7.06-UI1 — Live read-only governed workspace` as `Complete / PASS` after selected-Mac Attempt 2 removed the sole blocker preserved by Attempt 1. The selected Mac advanced through the existing P7.06 governed update path to exact canonical/local/runtime release `b1b78ed9772727dda41b2e509675691f978957ec` with deployment transaction `dbaec3d61aecd13a608863b9ae1ad78570a5584d`. The approved retained P6.05-L7 exact EIS attachment-evidence manifest for notice `0344100006426000005` independently verified at SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`; Authorization, Organizational Authority, Data Governance and Consequential Approval remained four distinct passing gate bases; first admission returned `PASS_ADMITTED_AND_PERSISTED`; the second identical execution returned `PASS_IDEMPOTENT_EXISTING`; and the final P7.03 retained set remained exactly one real governed item and one checkpoint.

The real retained `platform.document` item exposed Subject `document-subject/eis-0344100006426000005-exact-attachment-evidence`, exact Version `document-version/eis-0344100006426000005-74e943d855406b04`, `External Reference` authority and `CAP-001 + RFC-0006 + CAP-004` validation/provenance through the live browser workspace. Retained `manifest.json` SHA-256 `d0cd33ac17fcaa91416edcb9526e446b5cbd7c03f75333ecf7055a07ee7f2c38` and `payload.bin` SHA-256 `5486433cc34296859ccfb6a6690803d2b8c9c7c7a554292c3f1d45613e79b27e` were unchanged before/after browsing. Network/external effects were `NONE`; owner-local bounded evidence is recorded canonically only by review result and SHA-256 `104f64790a36511ca30e14edb864d4b2e650ecf62f39f379685e8d893766a506`.

The UI1 presentation adapter itself was byte-identical between Attempt 1 and Attempt 2, so the previously passed wrong-Organization, revoked-grant, mutation-method and security-header negative-path evidence remains applicable without inferring behavior across a changed implementation. `P7.06-UI1 = Complete / PASS`; the live-workspace substream advances to `0.1.5`, active Phase 7 to `1.2.8`, and the current canonical action becomes `P7.06-UI2 — Governed interaction and preflight`. The overall `P7.06-UI` substream remains `Current`, now at `25%`; UI3/UI4 and P7.07/P7.08 remain downstream. This closure creates no lifecycle promotion, Product Contract promotion, public/stable UI/API/browser support promise, external/customer Production, SLA/support or broader conformance claim.

Version `2.55.4` records `P7.06-UI1` selected-Mac live-browser Attempt 1 as `BLOCKED` solely on absence of a qualifying real retained canonical governed item in the persistent P7.03 store. The selected Mac successfully advanced from active release `4df99c4c66a1b7b93a4b05d7768018b03aa4041b` to exact canonical UI1 release `3a2b561a6935a84749552f016db8d1bd69eabf9a` through the existing P7.06 governed update path; preflight/update, verified backup, exact runtime/observer pin, P7.04 human least-privilege access, Safari loopback rendering, wrong-Organization failure closed, grant revocation/re-grant without restart, mutation-method rejection, security headers and zero canonical/external mutation from browsing all passed. Deployment transaction `0a858c2b44709516f49829cde7c8a45c4df6e9316303066ce879f341cbda25c5` and owner-local proof digest `ee153d84917839fb7566794f4227c19ae7eb4efd0de25596a3eaf3dcbb8f5364` preserve bounded non-secret evidence.

The live workspace correctly displayed an authorized empty state: no real `canonical-governed-state` item was available, no `governed-test-fixture` was substituted, and no arbitrary P7.03 record is admitted merely to satisfy UI closure. P7.03 persistence follows applicable Governed Execution/admission; it does not itself create authority or canonical truth. `P7.06-UI1` therefore remains `Current`, `P7.06-UI2` remains `Pending`, and the current canonical action is to establish at least one real retained governed item through a valid applicable Governed Execution/admission path under the existing owner context, persist the admitted item to P7.03, then re-run only the remaining UI1 real-item inspection/closure evidence. The live-workspace substream is synchronized to `0.1.2`. This milestone creates no lifecycle promotion, Product Contract expansion, public/stable UI/API, Production claim, browser matrix or SLA/support commitment.

Version `2.55.3` records the repository-side implementation milestone for `P7.06-UI1 — Live read-only governed workspace` through PR `#51`. The bounded implementation reuses M4 workspace semantics over exact persistent P7.03/P7.05 state, requires an explicit P7.04 human Organization/operation/resource/local grant before protected reads, pins execution to the exact activated P7.06 release, exposes `Discover / Records / Executions / Evidence / Documents / Knowledge`, distinguishes Subject from Exact Version, excludes governed test fixtures, renders no payload bytes, binds only to loopback, exposes only `GET/HEAD`, and fails closed without protected counts/content when authorization, exact release or store integrity is unavailable. Functional repository review required two iterations: iteration 1 found that missing store roots could be represented as empty state and unexpected checkpoint-store entries could be skipped; iteration 2 remediated both conditions and added regression coverage. GitHub `Reference Python CI` run `32132213609` on implementation head `83fb21f19ae99552c8a1a665a94a32e9f008da4c` completed with `success`.

`P7.06-UI1` remains `Current`, not `Complete / PASS`, because the canonical exit criteria still require the selected Mac to activate the merged exact release through P7.06, open the loopback workspace in a real browser, inspect real non-fixture governed state/provenance, prove wrong/unresolved Organization and revoked-grant failure closed, and prove that browsing causes zero canonical/external mutation. The current canonical action is therefore the selected-Mac UI1 live-browser closure proof; `P7.06-UI2` has not started. This milestone creates no public/stable UI/API, Production claim, `Active` capability, Stable Product Contract, browser support matrix or SLA/support commitment.

Version `2.55.2` closes `P7.06 — Governed deploy/update/rollback/version/migration path` for the declared `Persistent Internal / owner-operated` scope after selected-Mac Attempt 8 completed the required exact `update → rollback → final update` proof. The proof moved from historical source `cf60e52c93bf0ef4158cf2c3e26792850a126c70` to canonical target/final active release `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`, with first update transaction `a33209268d34b25c1bb8db9c63e835bf6149a404af57f8e77952177f22c5ffb3`, rollback transaction `589f282e3e062c1b5aa298f841f044d4d9c6227214c862d45044673a5ce9e951`, final update transaction `34470ac05993465155b8048405d1dbb712ffb9387b90a29666b927fcfb9dfdc4`, and owner-local attestation SHA-256 `3dec1d1dd34aff960753105e72aa60739c01fb61c0af091a554e93f344418e69`.

The first governed P7.06 transition has therefore carried and verified the R22 exact-release runtime/observer hardening through successful update, exact historical rollback and final re-update. No schema-changing migration, durable backup restore, canonical organizational-state mutation by deployment, product/external effect or historical effect replay occurred. P7.06 is `Complete / PASS`, active Phase 7 is synchronized to `1.2.7`, the live workspace substream is activated at `0.1.1`, and `P7.06-UI1 — Live read-only governed workspace` becomes the current canonical action before P7.07/P7.08 workload expansion.

This closure creates no external/customer Production, `Active` Platform Capability, Stable Product Contract, public/stable deployment or UI API, supported macOS/browser matrix, generalized migration framework, SLA/SLO/support or broader conformance claim.

Version `2.55.1` adds the bounded `P7.06-UI — Live operator workspace over persistent runtime` substream and synchronizes active Phase 7 to `1.2.6`. Phase 4 / M4 already proved the domain-neutral workspace semantics and supplied an inspectable static HTML reference, but it deliberately did not establish a persistent browser application or stable frontend/API boundary. The new Phase 7 substream operationalizes those existing semantics against the live selected-Mac runtime rather than redesigning the workspace.

The substream is explicitly gated by the current `P7.06` core update path because R22 requires the merged exact-release observer/lifecycle and orphan-secret hardening to be deployed and verified through the first controlled P7.06 update before operational surface expansion. After `P7.06 core = PASS`, the sequence is `P7.06-UI1 live read-only workspace → UI2 governed interaction/preflight → UI3 persistent private operator access → UI4 first real owner interaction proof`, then P7.07/P7.08 workload expansion. `P7.06-UI = PASS` requires the owner to open the live workspace in a browser, inspect real governed state/provenance and exercise at least one bounded governed interaction through the existing runtime authority/security boundaries.

This planning update creates no public Arvectum OS UI, stable/public API, frontend-framework commitment, Production claim, `Active` capability transition, Stable Product Contract, browser support matrix or SLA/support commitment.

Version `2.55.0` closes `R22 — Persistent Runtime Health Review` after two functional review iterations. The cross-cutting P7.02–P7.05 review found three material defects before P7.06: the P7.05 launchd observer could mix an exact-release Python with observer code reached through mutable `current/source`; observer install/uninstall/status could proceed or report through ambiguous launchd state instead of failing closed; and P7.04 store verification did not detect unknown orphan reusable-secret plaintext outside the credential registry. PR `#39` remediates those boundaries by pinning observer Python and script to one exact release, adding bounded fail-closed launchd lifecycle/release-pin checks, requiring selected-Mac proof release consistency, and inspecting the complete owner-only P7.04 secret directory for unrecognized plaintext. GitHub `Reference Python CI` run `32111920701` passed `964/964` tests on the remediation/review head `c8d3dfe3f5bcb22e52a3faf41e1ea630d179d027` through merge-test SHA `5e89e5d46f03f0fd54b12dee2df0f46177f7a77f`.

`R22 = Complete / PASS` for the repository persistent-runtime health boundary. The remediation is deliberately not claimed as already deployed to the selected Mac mini: the first controlled `P7.06` update MUST carry and verify the merged R22 hardening before `P7.07`/`P7.08` operational workload expansion. `P7.06 — Governed deploy/update/rollback/version/migration path` is now the current canonical action. R22 does not create external/customer Production, an `Active` Platform Capability, Stable Product Contract, public/stable runtime/IAM/observability/deployment boundary, permanent monitoring topology, SLA/SLO/support or conformance promotion.

Version `2.54.9` closed `P7.05 — Health, observability, audit visibility, alerting + retention/minimization` after selected-Mac Attempt 1 passed on exact canonical `main` and persistent runtime release `cf60e52c93bf0ef4158cf2c3e26792850a126c70`. GitHub verification confirmed that this SHA was canonical `main` HEAD at proof execution/review. The designated `Darwin / arm64` owner-operated host remained healthy, the independent `com.arvectum.os.p7-05-observer` launchd observer was actually loaded, the existing P6.05-L4 owner context was reused, exact P7.04-authorized metadata-only audit visibility exposed no payload bytes, actionable alert creation/healthy clearing passed, and retention removed an expired non-canonical telemetry record without changing governed-state contents or deleting canonical state/evidence. Payload/reusable-secret logging remained disabled; canonical mutation and external effects remained false. The owner-local non-canonical attestation is recorded canonically only by review result and SHA-256 `882a3515d05be05742dc811eab36c2cba943f6838d465222b6e52c1be9c0e630`. Final P7.05 functional review iteration 4 of maximum 7 is `PASS`.

`P7.05 = Complete / PASS` for the declared `Persistent Internal / owner-operated` scope. `R22 — Persistent Runtime Health Review` became the next gate and is closed by version `2.55.0`. This closure does not create external/customer Production, an `Active` Platform Capability, Stable Product Contract, permanent monitoring/SIEM topology, public/stable health or audit API, remote paging, automatic remediation, SLA/SLO/support, organization-wide legal retention policy or conformance promotion.

Version `2.54.8` records the repository-side implementation milestone for `P7.05 — Health, observability, audit visibility, alerting + retention/minimization` after PR `#37` merged at `9999ce6f93bb2874fd4e43135abd1ffe726bbd2f`. The bounded implementation adds `healthy/degraded/down` classification with explicit operator actions, process/resource/restart visibility, structured minimized non-canonical telemetry, exact P7.04-authorized metadata-only governed/reconstruction visibility, an independent owner-local launchd observer, actionable transient local alerts and allow-listed diagnostic retention/cleanup that cannot traverse canonical governed state or evidence. Final code head `60914ee96793cdf40896e4336ce24f5788247b37` passed GitHub `Reference Python CI` run `32103615123` with `960/960 PASS`. Three functional cross-review iterations closed the material repository-side objections.

P7.05 remained `Current` rather than `Complete / PASS` at version `2.54.8` because the required selected-Mac proof had not yet established the actual live launchd observer state, alert path and cleanup invariants on the designated owner-operated Mac. That gap was closed by version `2.54.9`.

Version `2.54.7` closes `P7.04 — Persistent identity/operator/service access + least-privilege operations` after selected-Mac Attempt 1 passed on exact canonical `main` SHA `218e3762975a2fd6f11e8f13d4445bce5f5d7c94`. The proof reused the existing P6.05-L4 owner context and healthy P7.02 persistent runtime on exact release `73af746f83271b14670fe22db658dfd55cacb291`; all remaining least-privilege, attribution, rotation/revocation, remote-access and authority-separation conditions passed. The owner-local non-canonical attestation is recorded canonically only by review result and SHA-256 `5c0a67b15b7fb469bc5933030db0c2e90adfb47c3eb94411c43ba555b7d98659`. Final P7.04 functional review iteration 6 of maximum 7 is `PASS`. The current canonical action advances to P7.05.

This closure does not create external/customer Production, an `Active` Platform Capability, Stable Product Contract, permanent IAM/credential-vault/remote-administration topology, public/stable access API, SLA/support or conformance promotion.

Version `2.54.6` synchronized the master roadmap with active Phase 7 `1.2.2` after the P7.04 repository implementation milestone. No additional implementation or lifecycle claim was introduced by that synchronization.

Version `2.54.5` recorded the repository-side implementation milestone for `P7.04 — Persistent identity/operator/service access + least-privilege operations` after PR `#35` merged at `2b808c658c19056cef65b69e82152ae12d861679`.

The bounded repository implementation provides exact P6.05-L4 Organization/human identity continuity, one attributable persistent service principal, deny-by-default exact Organization/operation/resource/access-path grants, owner-local credential issuance/rotation/revocation, principal/grant revocation, explicit local/remote access scoping and a hardened selected-Mac proof wrapper. Technical access remains explicitly separate from Organizational Authority and consequential approval. No roles, wildcard grants, superuser or ambient-admin bypass were introduced.

Repository evidence for PR `#35`:

- focused persistent-access tests: `14/14 PASS`;
- selected-Mac proof-contract tests: `2/2 PASS`;
- GitHub `Reference Python CI` on final implementation/documentation head `b9c46646324d5d4bccf384196efa3670b828c6af`: `success`, run `32063442269`;
- canonical implementation: [`P7.04 Persistent Identity / Operator / Service Access`](../implementation/P7-04-PERSISTENT-IDENTITY-ACCESS.md) — `Complete / PASS`;
- repository functional cross-review: [`P7.04 Persistent Access Implementation Cross-Review`](../reviews/P7-04-persistent-access-implementation-review.md) — `Complete / PASS`;
- selected-Mac closure: [`P7.04 Selected-Mac Persistent Access Proof — Attempt 1`](../reviews/P7-04-selected-mac-proof-attempt-1.md) — `Complete / PASS`.

Version `2.54.4` closed `P7.03 — Durable governed state/checkpoint persistence + backup/restore baseline` after repository implementation, proof-contract hardening, preserved failed attempts, successful hardened selected-Mac Attempt 3 and final six-iteration functional cross-review.

Repository implementation PR `#30` merged at `e2440b6f8afc7e0f21b20d370047bfa3ac803017` and full Reference Python CI passed `932/932`. After Attempt 1 exposed an evidence-contract inconsistency, PR `#31` added the dedicated hardened selected-Mac wrapper and merged at `5d33f874beb38f773ecf816ecd6d35e5fcb26c97`; full Reference Python CI passed `935/935`.

`P7.03 = Complete / PASS` for the declared `Persistent Internal / owner-operated` scope. The bounded owner-local filesystem/tar adapter remains private, reversible and non-stable. No Accepted ADR is required at this scope, and no external/customer Production, `Active` Platform Capability, Stable Product Contract, SLA/SLO/RPO/RTO/support or permanent persistence technology claim is created.

Version `2.54.3` closed `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle` after remediated selected-Mac Attempt 2 passed. The selected Mac mini entered regular `Persistent Internal / owner-operated` Arvectum OS operation. This is an operational-mode transition only and does not create external/customer Production, an `Active` Platform Capability, a Stable Product Contract, SLA/support, a supported macOS matrix or stable deployment/service topology.

Version `2.54.0` closed `P7.01 — Persistent internal operating boundary + operational requirements baseline` and recorded `R21 — Operational Boundary Review = PASS`.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- no Accepted ADR currently selects a persistence, IAM, service, deployment, public API, broker or storage topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 real Product Contracts remain `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because later phases consume or validate it;
- no Stable/public SDK/API/wire/service/deployment compatibility boundary has been established;
- no external Production/SLA/support/full-platform conformance claim is implied.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Internal workspace/operator baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Executed | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Executed | 🟩 Complete / PASS | `M6` Real-product validation across two materially distinct workflows |
| `Phase 7` | Operational / Enterprise Readiness | Active | 🟨 Active | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 6 / M6

Detailed roadmap: [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md).

Phase 6 completed with two materially distinct real-product/workflow chains: Tender Operator exact real tender evidence and Discount Parser real Telegram publication evidence reconstructed through CAP-004 without effect replay. The M6 Milestone Code Health Gate is `Complete / PASS`.

`M6 = achieved for the declared bounded scope.`

## 6. Active Phase 7 — Operational / Enterprise Readiness

Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Active 1.2.12`.

Phase 7 converts validated owner-operated use into a persistent, recoverable, observable and operator-accessible internal operating baseline before considering stronger production/lifecycle claims.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P7.01` | Persistent internal operating boundary + operational requirements baseline | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.02` | Persistent Mac mini runtime + boot/restart/service lifecycle | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.03` | Durable governed state/checkpoint persistence + backup/restore baseline | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.04` | Persistent identity/operator/service access + least-privilege operations | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.05` | Health, observability, audit visibility, alerting + retention/minimization | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.06` | Governed deploy/update/rollback/version/migration path | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.06-UI` | Live operator workspace over persistent runtime | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.07` | Persistent Tender Operator operational contour | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.08` | Persistent Discount Parser cross-host operational contour | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P7.09` | Operator runbook + incident/uncertain-outcome/recovery drills | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.11` | Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.12` | Phase 7 / M7 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Detailed operator-workspace plan: [`P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md`](P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md) — `Complete / PASS 0.1.11`.

Engineering/quality gates:

- [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) — 🟩 `Complete / PASS` after P7.01;
- [`R22 — Persistent Runtime Health Review`](../reviews/R22-persistent-runtime-health-review.md) — 🟩 `Complete / PASS` after P7.05, two functional iterations, remediation PR `#39`, `964/964 PASS`;
- `R23 — Recovery / Portability Review` — after P7.10;
- `R24 — M7 Operational Hardening + required Milestone Code Health Gate` — after P7.11 and before P7.12.

### Persistent Mac mini and operator interaction transition

```text
P7.01 operational boundary — PASS
        ↓
R21 boundary review — PASS
        ↓
P7.02 persistent Mac mini runtime — PASS
        ↓
ARVECTUM OS ENTERS REGULAR PERSISTENT INTERNAL USE
        ↓
P7.03 durable-state/backup-restore baseline — PASS
        ↓
P7.04 persistent identity/access — PASS
        ↓
P7.05 operational visibility — PASS
        ↓
R22 Persistent Runtime Health Review — PASS
        ↓
P7.06 governed deploy/update/rollback/version/migration — PASS
        ↓
P7.06-UI1 live read-only workspace — PASS
        ↓
P7.06-UI2 governed interaction/preflight — PASS
        ↓
P7.06-UI3 persistent private operator access — PASS
        ↓
P7.06-UI4 first real owner interaction proof — PASS
        ↓
P7.07 persistent Tender Operator operational contour — PASS
        ↓
P7.08 persistent Discount Parser cross-host operational contour ← current
        ↓
P7.09–P7.12 hardening + closure
```

P7.02 passed on exact selected-Mac release `73af746f83271b14670fe22db658dfd55cacb291`. P7.03 subsequently established the bounded durable-state/checkpoint and backup/restore baseline. P7.04 is `Complete / PASS` after repository implementation, six-iteration functional review and selected-Mac Attempt 1. P7.05 is `Complete / PASS` after PR `#37`, `960/960` Reference Python CI, four-iteration functional review and selected-Mac Attempt 1 on exact canonical release `cf60e52c93bf0ef4158cf2c3e26792850a126c70`. R22 is `Complete / PASS` after remediation PR `#39` and `964/964` Reference Python CI. P7.06 is `Complete / PASS` after PR #49 repository hardening and selected-Mac Attempt 8 proved exact update, rollback and final re-update to `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`.

P7.06-UI1 repository implementation and cross-review passed through PR `#51`; the owner-approved bounded real-state bridge passed through PR `#53`. Selected-Mac Attempt 2 then closed the final real-state blocker on exact canonical/local/runtime release `b1b78ed9772727dda41b2e509675691f978957ec`: the approved retained manifest verified, four independent gate bases passed, one real governed item/checkpoint was admitted and persisted, the second execution was idempotent, the real Subject/exact Version/provenance was browser-visible, and before/after retained-byte digests were unchanged with no network/external effect. `P7.06-UI1 = Complete / PASS`. UI2 then passed through PR `#56`, five functional review/revise iterations and Reference Python CI run `32159051764 = success`; `P7.06-UI2 = Complete / PASS`.

UI3 is `Complete / PASS`. The selected-Mac final proof first recovered the pointer/live-runtime mismatch without changing P7.03/P7.04, then used the ordinary canonical-checkout P7.06 governed update to exact target `8451a5cb85c15ceb798438524f46cec87eacc981`, passed exact-release stability, and completed private listener/access/session/lifecycle/rollback/re-update evidence with final UI3 SHA-256 `05a30e20d1d6813ae786620fff8eb00544a04b87dfe5dabc07c2078d19b90f66`.

UI4 is also `Complete / PASS`. On exact canonical/runtime release `1da5600963dcba982d3b1969480fd3f725133e12`, the owner successfully entered the private Safari workspace after PR `#73` remediation, confirmed Organization/Actor/healthy exact runtime, navigated Records/Executions/Evidence/Documents, inspected the retained EIS `platform.document` exact Subject/Version plus Execution/Event/checkpoint provenance/reconstruction, saw all four action gates independently `Waiting`, and executed a real browser preflight with `WAITING / fail-closed`. The technical verifier independently passed and confirmed browser POST observation, technical interaction access only, no Organizational Authority or consequential approval, no canonical mutation and no product/external effect. Owner-local minimized evidence SHA-256: `63416f1862168d9a464a30d1824198ad52be4439e9f43fba71360c7ac34a9f91`. The material Safari unlock defect found during proof was remediated, regression-covered, CI-passed, governed-update deployed and re-proved. `P7.06-UI = Complete / PASS` at `100%`.

P7.07 is `Complete / PASS`. Repository implementation merged through PR `#75`; selected-Mac Attempt 1 correctly failed closed on a dynamic product-bridge module-registration defect; remediation PR `#76` merged at `b0c18fba15de6b5abac83a4f583d89eedb5c03d1` with Reference Python CI `#157 = success`. Attempt 2 then governed-updated the selected Mac to that exact release, reused the exact existing P7.07 governed item idempotently, proved the actual canonical Tender Agent bridge and CAP-001 exact reliance before and after supervised restart, advanced runtime generation `59 → 60`, preserved `previous_instance_id`, left the P7.03 governed-state digest unchanged, preserved exact P6.02 `0.1.0` and EIS `External Reference` authority, and produced no network/EIS retrieval, ordinary-read canonical mutation or external effect. Owner-local evidence SHA-256: `9613637b06c5d192311bda1eb3096a9cd0b49c016134af887697637a668cf0f8`.

## 7. M7 milestone definition

`M7 — Scoped production-grade operating baseline` requires, within the declared scope:

1. persistent supervised owner-operated Arvectum OS runtime on the selected Mac mini;
2. durable required governed state with tested backup/restore;
3. persistent least-privilege identity/access/secrets operations;
4. actionable health/observability without telemetry becoming authority;
5. governed deploy/update/rollback/version/migration path;
6. live private operator workspace over the persistent runtime, with owner proof of real governed-state inspection and at least one bounded governed interaction;
7. repeatable persistent Tender Operator reliance through its Product Contract;
8. repeatable Discount Parser cross-host evidence/reconstruction through its Product Contract;
9. executable incident/recovery procedures;
10. host-loss/portability proof on a clean secondary environment;
11. explicit lifecycle/conformance/stable-boundary dispositions;
12. R21–R24 material findings closed or accepted by appropriate authority;
13. pre-closure M7 Milestone Code Health Gate PASS.

M7 does not inherently require an external customer Production deployment, public multi-tenant service, `Active` capability, Stable Product Contract, public SDK/API or SLA/support promise.

## 8. Draft Phase 8 — Ecosystem and External Integration

Detailed draft: [`PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`](PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md) — `Draft / Exploratory 0.1.0`.

Phase 8 remains Draft until M7 closes and its external boundary is revalidated.

## 9. ADR, lifecycle and stable-boundary rule

Phase 7 may create pressure to choose concrete durable persistence, service-management, IAM, serialization, API, storage or deployment mechanisms. Use the lowest sufficient decision level. If a choice becomes materially constraining, cross-product, externally relied upon or expensive to reverse, stop at the applicable ADR/stable-boundary gate before further reliance.

No capability becomes `Active` and no Product Contract becomes `Stable` through roadmap progress alone.

## 10. Phase transition rule

Phase 8 remains `Draft / Exploratory` until Phase 7 / M7 closes and the external ecosystem boundary is revalidated against actual operational evidence, external demand, rights, Organization isolation, portability and commercial commitments.

A roadmap phase transition does not itself change lifecycle, production readiness, conformance or commercial status.

## 11. Current canonical action

> **P7.08 — Persistent Discount Parser cross-host operational contour.**

P7.07 is `Complete / PASS` for the declared selected-Mac `Persistent Internal / owner-operated` scope. The exact P6.02 `Provisional 0.1.0` boundary, attributable persistent owner context, `External Reference` EIS authority, item-scoped P7.04 read authorization, real product-owned bridge, exact CAP-001 Subject/Version/Artifact/integrity reliance and byte-stable P7.03 state survived an actual supervised runtime restart with no unauthorized canonical or external effect.

The next canonical action is P7.08: make the Discount Parser Windows ↔ Mac mini evidence/reconstruction path operationally repeatable while preserving the exact applicable Product Contract boundary or justified revision, CAP-004-only reliance unless evidence proves otherwise, minimized evidence transfer, replay safety, no secret/identity over-transfer and no hidden shared state. P7.09 remains downstream.