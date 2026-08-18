# P7.06 — Selected-Mac Governed Deploy Proof — Attempt 8

Status: `Complete / PASS`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance`
Operating classification: `Persistent Internal / owner-operated`
Parent work item: `P7.06 — Governed deploy/update/rollback/version/migration path`
Canonical target at proof start: `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`
Source release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`

## 1. Purpose

This artifact records the successful selected-Mac closure proof for the P7.06 governed deployment boundary after the bounded live-remediation sequence documented in `P7-06-live-remediation-review.md`.

The proof executed from the canonical local checkout `/Users/master/Documents/arvectum-os` after `main` was fast-forwarded from `ae904fe2f4d670a3c7b54f87d63feb2e607f132e` to canonical target `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`.

## 2. Authority and scope

The proof remains bounded by Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, and specifically the RFC-0005/RFC-0006 requirements for exact material version identity, explicit failure/rollback evidence, side-effect-safe historical recovery and non-authoritative operational telemetry.

No Product Contract lifecycle, Platform Capability lifecycle, Organizational Authority, public/stable deployment API or external/customer Production claim is created by this proof.

## 3. Executed proof sequence

The selected Mac executed the canonical wrapper:

`reference/python/p7_06_selected_mac_proof.sh P7.06-selected-mac-owner-operated-proof`

The wrapper completed the required sequence:

`source verification → update → target verification → rollback → source verification → final update → final target verification → status`

and reported final `PASS`.

## 4. First controlled update — PASS

Exact source:

`cf60e52c93bf0ef4158cf2c3e26792850a126c70`

Exact target:

`4df99c4c66a1b7b93a4b05d7768018b03aa4041b`

Observed evidence:

- source observer exact-release status — `PASS`;
- pre-update backup — `PASS`;
- backup SHA-256 — `904374591e1de92cf9dbd868f285b728ec78e9dcb5e849f39f632daab833c9d6`;
- P7.05 observer uninstall — `PASS`;
- P7.02 stop — `PASS`;
- target update — `PASS`;
- immutable update transaction — `a33209268d34b25c1bb8db9c63e835bf6149a404af57f8e77952177f22c5ffb3`.

This successful transition carried the R22-era exact-release runtime/observer hardening through the governed P7.06 update path rather than by an ad-hoc deployment.

## 5. Exact rollback — PASS

The proof then rolled back from target to the exact historical source release.

Observed evidence:

- rollback active release — `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- rollback from target — `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`;
- immutable rollback transaction — `589f282e3e062c1b5aa298f841f044d4d9c6227214c862d45044673a5ce9e951`;
- source observer exact-release status after rollback — `PASS`.

Rollback restored the historical runtime release while retaining the hardened exact-release observer pin. It did not reintroduce the unsafe historical mutable-`current` observer configuration.

No durable backup restore was required because no state-schema migration occurred.

## 6. Final controlled re-update — PASS

The proof performed the required second controlled update from the restored source back to the canonical target.

Observed evidence:

- source observer exact-release status before re-update — `PASS`;
- second pre-update backup — `PASS`;
- backup SHA-256 — `aa3336b8d16937c36f517aaed8202148ed9ce79aace0aab2fa6461ff58be5e92`;
- P7.05 observer uninstall — `PASS`;
- P7.02 stop — `PASS`;
- final update — `PASS`;
- immutable final update transaction — `34470ac05993465155b8048405d1dbb712ffb9387b90a29666b927fcfb9dfdc4`.

The selected Mac was intentionally left on exact target release:

`4df99c4c66a1b7b93a4b05d7768018b03aa4041b`.

## 7. Owner-local attestation

Canonical wrapper result:

`P7.06 selected-Mac proof PASS`

Owner-local non-canonical evidence path:

`/Users/master/Library/Application Support/ArvectumOS/persistent-internal/evidence/p7-06/p7-06-selected-mac-proof-20260818T110007Z.json`

Attestation SHA-256:

`3dec1d1dd34aff960753105e72aa60739c01fb61c0af091a554e93f344418e69`

The raw owner-local evidence remains non-canonical. This review artifact canonically records only the bounded result, exact release/transaction identities and attestation digest necessary for reconstruction.

## 8. Migration, state and effect disposition

Attempt 8 exercised no schema-changing migration. The current P7.03 durable-store schema remained compatible with the target release, so migration mode remained `none` and exact-release rollback remained safe.

The deployment path did not authorize or report:

- canonical organizational-state mutation by deployment itself;
- product-domain consequential action;
- external product effect;
- historical external-effect replay;
- durable backup restore;
- Organizational Authority satisfaction by deployment evidence.

The update/rollback operations changed only the owner-operated runtime release selection and its exact release-coupled service/observer execution state under the existing P7.06 boundary.

## 9. Functional closure review

No new material objection was observed in Attempt 8.

The live behavior now matches the repository contract after the remediation sequence:

- exact source and target release identities are preserved;
- `current` moves to the exact target before activation;
- runtime and observer become one exact-release unit;
- verified backup precedes each destructive lifecycle transition;
- rollback restores the exact historical release and hardened observer pin;
- final re-update is repeatable;
- deployment transaction evidence is retained for update, rollback and final update;
- no migration or effect boundary is broadened.

Result: `PASS`.

## 10. Closure disposition

For the declared `Persistent Internal / owner-operated` scope, the P7.06 selected-Mac closure contract is satisfied.

This evidence is sufficient to close `P7.06 — Governed deploy/update/rollback/version/migration path` as `Complete / PASS` after canonical roadmap/review synchronization, final repository CI and read-after-write verification.

This closure does **not** establish external/customer Production, an `Active` Platform Capability, Stable Product Contract, supported macOS matrix, public/stable installer/updater API, generalized migration framework, automatic fleet rollout, SLA/SLO/support or broader conformance.

Next canonical action after P7.06 closure: `P7.06-UI1 — Live read-only governed workspace`.