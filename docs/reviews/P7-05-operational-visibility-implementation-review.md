# P7.05 — Operational Visibility Implementation Review

Status: `Repository implementation / PASS; selected-Mac closure pending`
Date: `2026-08-18`
Task classification: `platform`
PR: `#37`

## Authority baseline

Checked before implementation:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 — Arvectum OS Architecture;
- RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty & Portability;
- RFC-0005 — Governed Execution / Workflow Model;
- RFC-0006 — Event, Provenance & Observability Model;
- RFC-0007 — Memory, Knowledge & Governed Learning Lifecycle;
- canonical roadmap `2.54.7` and Phase 7 detailed roadmap.

No relevant Accepted ADR currently selects an observability/logging/alerting backend or stable monitoring topology. P7.05 therefore remains a bounded owner-local implementation and does not create such a commitment.

## Functional cross-review

### Iteration 1 — operations / failure visibility

Material objection: a `status` command executed by the same runtime contour is insufficient when that runtime has already stopped.

Revision:

- added independent owner-local launchd observer `com.arvectum.os.p7-05-observer`;
- observer runs one bounded health + retention cycle periodically;
- observer has no network listener or remote alert transport;
- degraded/down state creates an actionable local non-canonical alert;
- healthy state clears the transient alert.

Disposition: `resolved`.

### Iteration 2 — roadmap scope / audit semantics

Material objection: initial scope did not fully cover the canonical P7.05 roadmap requirement for process/resource/restart visibility and recent governed execution/reconstruction visibility.

Revision:

- added PID, P7.02 generation, start/previous-instance visibility and minimum observed restart count;
- added bounded filesystem/resource/diagnostic counters without inventing SLO/SLA thresholds;
- added exact P7.04-authorized metadata-only projections for governed P7.03 records and recovery checkpoints;
- preserved checkpoint `canonical_authority=false` and `external_effect_replay_authorized=false` semantics;
- labelled filesystem modification timestamps strictly as non-canonical storage observations rather than canonical event/execution time.

Disposition: `resolved`.

### Iteration 3 — security / privacy / selected-host closure

Material objection: a synthetic alert-path proof alone would not demonstrate that an independent persistent observer was actually installed on the selected Mac.

Revision:

- selected-Mac proof now fails closed on Darwin unless `launchctl print gui/<uid>/com.arvectum.os.p7-05-observer` succeeds;
- added regression coverage for POSIX shell syntax and the absence of network-client behavior in the observer adapter;
- telemetry uses a structured attribute allow-list and rejects reusable-secret, payload/body/content and arbitrary free-form fields;
- retention config cannot widen cleanup beyond the fixed diagnostic allow-list or convert telemetry into canonical authority;
- cleanup hard-protects `state/`, `evidence/`, `backups/` and `secrets/` and refuses symlink diagnostic targets.

Disposition: `resolved`.

## Final repository evidence

Final code evidence before documentation-only commits:

- implementation head: `60914ee96793cdf40896e4336ce24f5788247b37`;
- GitHub Actions workflow: `Reference Python CI`;
- workflow run: `32103615123`;
- job: `95608711370`;
- result: `PASS`;
- tests: `960/960 PASS` (`Ran 960 tests in 11.366s`, `OK`).

The passing set includes:

- P7.05 health `healthy/degraded/down` classification and actionable response;
- structured non-canonical telemetry and minimization rejection paths;
- exact P7.04-authorized audit/reconstruction projection with no payload exposure;
- alert creation/clear behavior;
- retention cleanup preserving governed state and evidence;
- tampered-retention-policy fail-closed behavior;
- selected-Mac proof-contract regression;
- macOS observer shell/no-network-client guards;
- all accumulated prior reference architecture tests.

No material repository-side functional objection remains after the three review/revision iterations.

## Remaining closure evidence

Repository CI cannot prove the actual launchd state or current runtime state of the designated owner-operated Mac. The selected-Mac execution remains required before canonical `P7.05 = Complete / PASS` closure.

The selected-host proof must establish:

- exact deployed release is current and healthy;
- independent P7.05 launchd observer is loaded;
- actionable alert path works and clears on healthy state;
- authorized audit/reconstruction visibility works without payload exposure or authority elevation;
- retention removes expired diagnostics without changing governed-state tree contents or deleting evidence;
- no canonical mutation, external product effect, reusable-secret logging or payload logging occurs.

Raw selected-host attestation is non-canonical operational evidence. Canonical closure should retain only the minimum reviewed result/digest necessary for auditability, following the P7.03/P7.04 precedent.

## Non-claims

This review does not establish or promote:

- external/customer `Production` readiness;
- an SLA/SLO or uptime guarantee;
- remote paging/notification delivery;
- automatic incident remediation;
- a stable/public observability API;
- a permanent monitoring vendor/backend/topology;
- organization-wide legal retention policy;
- Product Contract lifecycle promotion;
- Platform Capability lifecycle promotion;
- broader Arvectum OS conformance.

## Review conclusion

`Repository implementation: PASS`.

`Selected-Mac closure: PENDING`.

Therefore P7.05 must remain the current Phase 7 task until selected-host evidence is produced and canonically reviewed; R22 must not advance yet.