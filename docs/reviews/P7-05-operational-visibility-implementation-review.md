# P7.05 — Operational Visibility Implementation Review

Status: `Complete / PASS`
Date: `2026-08-18`
Task classification: `platform`
PR: `#37`
Selected-Mac closure: [`Attempt 1 — PASS`](P7-05-selected-mac-proof-attempt-1.md)

## Authority baseline

Checked before implementation and re-checked at selected-host closure:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 — Arvectum OS Architecture;
- RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty & Portability;
- RFC-0005 — Governed Execution / Workflow Model;
- RFC-0006 — Event, Provenance & Observability Model;
- RFC-0007 — Memory, Knowledge & Governed Learning Lifecycle;
- canonical roadmap `2.54.8` and Phase 7 detailed roadmap.

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

### Iteration 4 — selected-Mac operational closure

Material objection carried from repository review: repository CI cannot establish actual launchd state, live selected-host health, alert behavior or retention isolation on the designated owner-operated Mac.

Selected-host evidence on exact canonical `main` SHA `cf60e52c93bf0ef4158cf2c3e26792850a126c70` established:

- P7.02 persistent runtime loaded and healthy;
- P7.05 observer loaded at `gui/501/com.arvectum.os.p7-05-observer`;
- existing P6.05-L4 owner context reused; no replacement context created;
- exact P7.04 audit grant authorized metadata-only visibility with `audit_projection_payload_bytes_exposed=false`;
- actionable alert path created and cleared correctly;
- one expired telemetry record removed;
- governed-state tree hash unchanged;
- canonical state/evidence deletion both false;
- payload/reusable-secret logging both false;
- canonical mutation and external effects both false;
- final runtime healthy, observer loaded, active alert absent and checkout clean.

Attestation digest: `882a3515d05be05742dc811eab36c2cba943f6838d465222b6e52c1be9c0e630`.

Disposition: `resolved / PASS`.

## Repository evidence

Final code evidence before documentation-only closure commits:

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

No material repository-side functional objection remained after the first three review/revision iterations; selected-host Iteration 4 closes the live-host evidence gap.

## Selected-Mac evidence

Canonical selected-host review:

- [`P7.05 Selected-Mac Operational Visibility Proof — Attempt 1`](P7-05-selected-mac-proof-attempt-1.md) — `Complete / PASS`;
- tested canonical `main`: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- persistent runtime release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- host: `Darwin / arm64`;
- Python: `3.14.7`;
- proof exit code: `0`;
- final runtime state: `healthy`;
- owner-local attestation SHA-256: `882a3515d05be05742dc811eab36c2cba943f6838d465222b6e52c1be9c0e630`.

The raw selected-host attestation remains non-canonical operational evidence. Canonical history retains only the reviewed result and digest, following the P7.03/P7.04 precedent.

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

`P7.05 = Complete / PASS`.

Functional cross-review completed at iteration 4 of maximum 7 with no remaining material objection for the declared `Persistent Internal / owner-operated` scope.

Next canonical action: `R22 — Persistent Runtime Health Review`. `P7.06` remains blocked from advancement until R22 is completed/dispositioned.