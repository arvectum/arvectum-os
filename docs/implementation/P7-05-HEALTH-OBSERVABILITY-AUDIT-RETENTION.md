# P7.05 — Health, Observability, Audit Visibility, Alerting + Retention / Minimization

Status: `Repository implementation / PASS; selected-Mac closure pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor: [`P7.04 Persistent Identity / Operator / Service Access`](P7-04-PERSISTENT-IDENTITY-ACCESS.md) — `Complete / PASS`
Repository implementation PR: `#37`
Selected-Mac closure: `Pending`

## 1. Purpose

P7.05 adds the minimum actionable operational visibility needed by the current persistent owner-operated Arvectum OS contour. It is deliberately narrower than a general monitoring platform: operators can distinguish healthy, degraded and down runtime states; inspect process/restart and bounded resource signals; receive a local actionable alert; inspect authorized governed-state/reconstruction metadata; and enforce bounded telemetry/diagnostic retention without creating a second source of canonical truth.

The implementation remains owner-local, reversible and technology-light. It does not select a permanent metrics/logging/SIEM/alerting backend, public health API, network monitoring topology or organization-wide retention policy.

## 2. Authority checked

Implementation was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 — Observability remains distinct from canonical organizational state and shared platform behavior remains domain-neutral;
- RFC-0003 — least privilege, default denial, minimization, Organization scope, protected access and retention/deletion constraints;
- RFC-0005 — technical/operator access does not satisfy Organizational Authority or consequential approval and does not bypass Governed Execution;
- RFC-0006 — canonical Events/evidence remain distinct from logs, metrics, traces and operational telemetry; telemetry is non-canonical by default;
- RFC-0007 — operational observations do not silently become validated Knowledge;
- P7.01 through P7.04 operating, persistence, recovery and access boundaries.

No relevant Accepted ADR currently selects an observability, logging, alerting or monitoring topology.

### ADR disposition

`ADR required now: NO`.

The current implementation is a bounded stdlib/launchd adapter for one owner-operated internal host. Re-open the ADR/stable-boundary gate before selecting an externally relied-upon observability service, long-lived remote telemetry transport, public/stable health API, organization-wide retention service, multi-Organization monitoring topology or materially constraining vendor/schema commitment.

## 3. Repository implementation

Files:

- `reference/python/p7_05_operational_visibility.py` — health classification, process/resource/restart visibility, structured telemetry, audit projection, alerts and retention cleanup;
- `reference/python/p7_05_macos_observer.sh` — reversible owner-local launchd observer;
- `reference/python/p7_05_selected_mac_proof.py` — selected-Mac closure contract;
- `reference/python/tests/test_p7_05_operational_visibility.py` — health/security/audit/retention regressions;
- `reference/python/tests/test_p7_05_selected_mac_proof.py` — selected-Mac proof-contract regression;
- `reference/python/tests/test_p7_05_macos_observer.py` — shell-syntax and no-network-client guard for the observer adapter.

The default runtime root remains the P7.02 owner-local root:

`~/Library/Application Support/ArvectumOS/persistent-internal`

P7.05 adds only bounded operational state beneath that root:

```text
config/
  p7-05-retention.json          non-canonical owner-local retention/minimization config
logs/
  p7-05/telemetry.jsonl         structured non-canonical telemetry
  p7-05-observer.stdout.log     raw non-canonical observer diagnostic
  p7-05-observer.stderr.log     raw non-canonical observer diagnostic
run/
  p7-05-alert.json              transient actionable alert when degraded/down
```

The existing `state/`, `evidence/`, `backups/` and `secrets/` areas are explicitly outside the P7.05 cleanup boundary.

## 4. Health model

P7.05 consumes the P7.02 local health record rather than creating a parallel liveness truth.

The operator-facing classifier distinguishes:

- `healthy` — current P7.02 heartbeat, live PID and valid persistent access registry when present;
- `degraded` — runtime is alive enough to inspect but an actionable integrity/clock/access condition requires attention;
- `down` — health telemetry is missing, unreadable, stale, schema-invalid, reports a non-healthy runtime, carries an invalid/dead PID or otherwise cannot support a credible liveness assertion.

Every non-healthy result carries an operator action. The classifier does not automatically mutate governed state, grant access, approve a decision or execute a product effect.

## 5. Process, restart and bounded resource visibility

`status` exposes only proportionate owner-local operational facts:

- PID;
- observed P7.02 generation;
- start time when present;
- whether a previous runtime instance is recorded;
- a minimum observed restart count derived from P7.02 generation semantics;
- filesystem total/free bytes;
- bounded telemetry/raw diagnostic byte counts;
- counts of governed storage item directories and recovery checkpoints.

Restart/resource values are diagnostic observations, not SLA/SLO, capacity guarantees or canonical organizational facts. No CPU/memory SLO or automatic resource threshold is invented by P7.05.

## 6. Structured telemetry and minimization

P7.05 telemetry is JSONL and explicitly declares:

- `canonical_authority=false`;
- classification as raw operational telemetry;
- a compact event identifier;
- level and UTC recording timestamp;
- a narrow allow-list of structured attributes.

The ordinary telemetry path rejects reusable-secret fields, authentication material, payload/body/content fields, document/prompt-like content, email/phone/identity-like free-form fields and arbitrary unapproved attribute keys. Attribute size is bounded.

Raw launchd stdout/stderr files remain non-canonical diagnostics and are never promoted to Events, canonical state, Observation, Memory or Knowledge merely because they exist.

## 7. Audit and reconstruction visibility

Governed audit visibility is not ambient filesystem browsing.

A projection requires an exact allowed P7.04 `AccessDecision` for:

- operation: `audit.inspect`;
- resource: `state:governed`;
- access path: explicit `local` or `remote` as granted.

The decision must remain `operational_access_only=true`, with Organizational Authority and consequential approval unsatisfied.

For authorized callers, P7.05 exposes metadata-only views over verified P7.03 governed item manifests and recovery checkpoints. Governed payload bytes are not copied into telemetry or the audit projection. Subject/version identities, schema/classification, authority mode and bounded provenance refs may be visible only through the authorized projection.

Filesystem modification time is exposed, where useful, solely as a `non-canonical filesystem observation` for local recency ordering. It does not replace event occurrence/recording time, governed execution time or canonical lineage.

Recovery checkpoint visibility preserves the P7.03 facts that checkpoints are non-authoritative and do not authorize external-effect replay.

## 8. Alerting

P7.05 uses a deliberately small owner-local alert path rather than introducing a monitoring service.

A degraded/down observation writes `run/p7-05-alert.json` with:

- severity;
- state/code;
- bounded detail;
- explicit operator action;
- runtime release reference when available.

A healthy observation clears that transient alert.

The macOS adapter `com.arvectum.os.p7-05-observer` runs independently of the P7.02 runtime process through launchd. By default it evaluates health and retention once per minute. This matters because the runtime cannot report its own failure after it has stopped. The adapter has no network listener or alert transport.

The selected-Mac proof fails closed on macOS unless this observer is actually loaded in launchd.

## 9. Retention / minimization

Default owner-local P7.05 diagnostic retention is `168` hours. This is a bounded implementation default for the current internal contour, not an organization-wide legal records policy.

Cleanup is allow-listed to:

- `logs/p7-05/telemetry.jsonl`;
- `logs/stdout.log`;
- `logs/stderr.log`;
- `logs/p7-05-observer.stdout.log`;
- `logs/p7-05-observer.stderr.log`.

Structured telemetry is compacted by age, record count and byte ceiling. Raw diagnostics are deleted when stale and truncated when they exceed the bounded diagnostic ceiling. The implementation intentionally prefers minimization over indefinite archive rotation.

`state/`, `evidence/`, `backups/` and `secrets/` are protected prefixes. P7.05 cleanup cannot claim authority to delete canonical/governed state or audit evidence. A tampered configuration that attempts to widen the cleanup/authority boundary fails validation.

Canonical retention/deletion remains owned by the relevant governed data policy/path; P7.05 diagnostic cleanup is not that path.

## 10. Failure and degradation behavior

The implementation fails closed when:

- health telemetry cannot be trusted;
- P7.04 access state fails validation;
- telemetry attributes attempt to exceed the minimization allow-list;
- an audit caller lacks the exact P7.04 grant;
- a retention config attempts to change telemetry authority, protected prefixes or the fixed cleanup allow-list;
- malformed telemetry would make cleanup ambiguous;
- a diagnostic cleanup target is a symlink;
- selected-Mac closure is attempted without the independent launchd observer loaded.

A detected service incident does not make the observer process itself fail merely because the observed runtime is down: the durable local signal is the actionable non-canonical alert/status. Observer execution failure remains separately visible through launchd/raw diagnostic state.

## 11. Known blind spots and explicit non-claims

P7.05 intentionally does not claim:

- external/customer `Production` readiness;
- remote pager/email/SMS/chat delivery;
- an SLO/SLA, MTTR, uptime or response-time guarantee;
- automatic incident remediation;
- CPU/memory/resource threshold policy;
- a durable observability vendor/backend;
- multi-host aggregation;
- public/stable health, audit, telemetry or retention API/schema;
- canonical ordering from filesystem timestamps;
- complete historical reconstruction when governed source evidence is absent or lawfully unavailable;
- conversion of diagnostics into validated Knowledge;
- lifecycle promotion of any Platform Capability;
- Stable Product Contract or conformance promotion.

The launchd observer interval is an operational detection interval, not an availability promise. Telemetry is best-effort diagnostic evidence; authoritative history must still come from the appropriate canonical Event/governed-state path.

## 12. Repository validation

GitHub `Reference Python CI` on hardened implementation commit `8e40f80aad577fa6cc4580ada80b480faa7eb687` passed `958/958` tests (run `32103561028`). That run includes the P7.05 operational visibility and selected-Mac proof-contract regressions.

A final adapter-specific regression was then added for the macOS observer shell contract; its final CI result is recorded in the implementation review before merge.

## 13. Selected-Mac closure contract

Repository CI cannot establish the actual selected-host launchd state. P7.05 is therefore not canonically complete until the owner-operated selected Mac executes the exact merged release and produces a PASS attestation showing, at minimum:

- live P7.02 runtime remains healthy;
- P7.05 launchd observer is loaded;
- healthy/degraded/down classification works;
- exact P7.04-authorized audit projection works without payload exposure or authority elevation;
- actionable alert creation and healthy clearing work;
- expired telemetry cleanup occurs;
- governed-state tree hash is unchanged by cleanup;
- canonical state and audit evidence are not deleted;
- no reusable secret/payload logging is enabled;
- no canonical mutation or external/product effect occurs.

The raw attestation remains owner-local non-canonical operational evidence. Canonical closure should store only the minimum reviewed result and digest, consistent with P7.03/P7.04 precedent.
