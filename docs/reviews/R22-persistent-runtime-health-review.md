# R22 — Persistent Runtime Health Review

Status: `Complete / PASS`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and bounded `product_contract` review
Trigger: after `P7.05`, before `P7.06` and before operational workload expansion
Reviewed contour: `P7.02` through `P7.05`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)

## 1. Purpose

R22 is the first cross-cutting health review of the persistent owner-operated runtime after the runtime, durability, access and observability layers have all become real.

The gate asks whether the combined P7.02–P7.05 implementation is sufficiently coherent and fail-closed to permit P7.06 governed deployment/update/rollback work without carrying forward hidden mixed-version execution, secret-lifecycle drift, misleading health signals, accidental product/platform coupling or unsupported operational commitments.

R22 is an engineering/governance checkpoint. It is not a Production approval, lifecycle transition, Product Contract stabilization, Platform Capability activation, public API commitment, SLA/SLO decision or external conformance claim.

## 2. Authority baseline checked

Checked before and during review:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with acceptance evidence;
- RFC-0001 — platform architecture, technology independence, product/platform separation, operational-readiness and stable-boundary constraints;
- RFC-0002 — canonical identities/versions, Event and Execution Context semantics, technology-independent persistence;
- RFC-0003 — identity/authentication/authorization/Organizational Authority/data-governance separation, deny-by-default, least privilege, secrets, minimization, retention/deletion and portability;
- RFC-0004 — Product Contract boundary and prohibition on hidden product/platform coupling;
- RFC-0005 — exact material version pinning, Governed Execution, failure/uncertainty/retry and replay-safe consequential effects;
- RFC-0006 — canonical Event/evidence versus non-canonical telemetry, provenance, observability minimization and evidence-path failure semantics;
- RFC-0007 — operational observations do not silently become validated Knowledge;
- RFC-0008 — Document/Artifact handling, transient-output default and retention/provenance propagation;
- Accepted ADRs — none exist; `docs/adrs/` contains only the ADR process/index;
- Arvectum Engineering Standard — canonical closure requires implementation, tests, CI, documentation and roadmap synchronization;
- Decision Authority Policy — remains `Proposed 0.2.1`; no delegation was inferred;
- P6.02 Tender Operator Product Contract — `Provisional 0.1.0`;
- P6.06 Discount Parser Product Contract — `Provisional 0.1.0`;
- P7.01 baseline and R21 — `Complete / PASS`;
- P7.02 through P7.05 implementation and selected-Mac closure evidence — `Complete / PASS` before this cross-cutting review.

No higher-authority conflict was found in the intended persistent-internal scope.

## 3. Review method

The review was performed across the combined implementation rather than treating the four prior closure documents as sufficient evidence by themselves.

Review dimensions:

1. runtime/service lifecycle and exact-release boundaries;
2. durability, backup/restore and recovery authority;
3. identity/access/secrets and least-privilege failure behavior;
4. health/observability/audit/retention authority separation;
5. dependency direction and hidden coupling;
6. failure, retry, uncertainty and crash consistency;
7. operator friction and false-PASS/false-health risks;
8. P7.06 update/migration handoff;
9. Product Contract and lifecycle/commercial non-claims.

Functional review completed in two iterations of the maximum seven. Iteration 1 returned `REVISE`; iteration 2 returned `PASS` after remediation and full Reference Python CI.

## 4. Iteration 1 — cross-cutting implementation review

Result: `REVISE`.

Three material findings were identified.

### F1 — observer could silently become a mixed-release process

Severity: `material`.

Before R22 remediation, the P7.05 launchd adapter pinned its Python executable through the exact P7.02 release venv, but resolved its observer script through:

`current/source/reference/python/p7_05_operational_visibility.py`.

Because `current` is the mutable selected-release symlink, a later runtime update could move `current` while the already-loaded observer retained the old venv path. Its next periodic launch could therefore execute observer/application modules from a different Git release than the interpreter/service configuration originally installed.

This is incompatible with the exact-version/reconstructability intent carried by RFC-0005 and creates a P7.06 bypass: changing `current` could change operational code without an explicit observer reinstall/re-pin.

Disposition implemented on the R22 branch:

- observer Python and observer script are both pinned to the same exact `releases/<sha>` contour;
- `/current/` is rejected in the installed observer script path;
- `status` verifies the installed plist against the exact current release and fails closed on mismatch;
- selected-Mac proof now requires runtime health release SHA to equal the exact proof SHA;
- selected-Mac proof on macOS additionally requires the launchd observer plist to pin the exact proof release.

### F2 — observer lifecycle could report or proceed through ambiguous launchd state

Severity: `material`.

Before R22 remediation:

- `status` printed that the observer was not loaded but still continued to runtime status and could exit successfully;
- `install` used one-shot `launchctl bootout ... || true` and ignored `kickstart` failure;
- `uninstall` used one-shot `bootout` without the bounded asynchronous unload handling already proven necessary by the P7.02 launchd race discovered during P7.02 closure.

This created an operator-facing false-health/false-PASS risk and reintroduced a known environment-specific failure mode.

Disposition implemented on the R22 branch:

- bounded `wait_unloaded` / `unload_observer` semantics mirror the already-proven P7.02 pattern;
- install fails if an existing observer does not unload within the bounded wait;
- install requires successful bootstrap/kickstart, loaded state and exact release-pin verification;
- uninstall fails if the observer remains loaded;
- status fails closed when the observer is not loaded or its exact release pin is inconsistent.

### F3 — unknown orphan reusable secret material was not detected by access-store verification

Severity: `material security/minimization finding`.

P7.04 already rejected a retained secret file for a credential recorded as revoked. However `verify_store` iterated only credential IDs present in the registry. A crash during credential issue/rotation could theoretically leave a secret file that has no registry record at all. Such plaintext would not authorize access because authorization remains registry-bound and deny-by-default, but the reusable secret would remain unnecessarily retained and invisible to the previous verifier.

Disposition implemented on the R22 branch:

- `verify_store` now validates the complete owner-only `secrets/p7-04` directory;
- symlinks, non-files, unrecognized filenames and secret files without a registry credential are rejected;
- existing active-credential verifier matching and revoked-secret rejection remain intact;
- regression coverage creates an orphan secret and requires fail-closed detection.

The fix intentionally detects and blocks silent drift rather than automatically deleting unknown secret material. Incident cleanup remains an explicit operator action and belongs in the later P7.09 runbook/recovery work.

## 5. Iteration 2 — post-remediation architecture/security review

Result: `PASS`.

The revised implementation was re-read across the R22 dimensions and then exercised by the complete Reference Python test suite.

### 5.1 Runtime/service and exact-version boundary

Result: `PASS`.

The P7.02 runtime remains exact-release pinned and the P7.05 observer now follows the same coherent-release rule. A changed `current` symlink can no longer silently redirect an already-installed observer script because the launchd plist contains an immutable release path.

A release mismatch becomes visible/fail-closed rather than an implicit update mechanism. P7.06 remains responsible for the controlled sequence that intentionally changes runtime/observer release pins.

### 5.2 Durability and recovery authority

Result: `PASS`.

P7.03 continues to preserve the required separation between already-governed durable state, non-authoritative checkpoints, telemetry/cache/secrets exclusions and isolated verified restore. R22 found no reason to change the bounded filesystem/tar adapter or introduce a persistence ADR.

No backup/restore path authorizes external-effect replay or converts recovery state into canonical authority.

### 5.3 Access, secrets and authority

Result: `PASS`.

P7.04 still preserves exact Organization/operation/resource/access-path grants and denial by default. Operational access remains explicitly unable to satisfy Organizational Authority or consequential approval.

The added full secret-directory verification closes the observed minimization blind spot without inventing a secret-vault architecture, changing credential technology or broadening the access contract.

### 5.4 Observability, audit and retention

Result: `PASS`.

P7.05 telemetry, raw diagnostics, local alerts and filesystem-recency observations remain non-canonical. Authorized audit visibility continues to require an exact P7.04 decision and remains metadata-only over verified P7.03 records/checkpoints.

Retention cleanup remains restricted to the explicit diagnostic allow-list and cannot delete governed state, evidence, backups or reusable secrets.

### 5.5 Dependency direction and hidden coupling

Result: `PASS with bounded maintainability note`.

The dependency direction is monotonic for the current Phase-7 adapter stack:

`P7.05 operational visibility -> P7.04 access + P7.03 durable-state verification -> existing reference semantics`.

No product repository, product-owned database, private product stream or product schema is imported into the platform runtime contour.

P7.05 still uses a small number of underscore-prefixed P7.04 helper functions in the bounded internal implementation/proof code. This is not a Product Contract/public API and is not a current architectural violation, but P7.06+ must not treat those private helpers as a stable compatibility boundary. If cross-module reliance grows or becomes externally/cross-product relied upon, introduce an explicit internal interface or ADR as appropriate rather than freezing incidental helpers.

### 5.6 Product/platform and workload boundary

Result: `PASS`.

R22 creates no new product reliance. Tender Operator remains bounded by P6.02 `Provisional 0.1.0`; Discount Parser remains bounded by P6.06 `Provisional 0.1.0` and its existing admitted capability surface.

No persistent Tender Operator or Discount Parser operational contour is claimed by R22. Those remain P7.07 and P7.08 work after P7.06.

## 6. Verification evidence

Repository remediation and review evidence:

- branch: `review/r22-persistent-runtime-health`;
- PR: `#39 — R22 — Persistent Runtime Health Review remediation`;
- remediation/review head tested by PR merge ref: `c8d3dfe3f5bcb22e52a3faf41e1ea630d179d027`;
- PR merge-test SHA used by GitHub Actions: `5e89e5d46f03f0fd54b12dee2df0f46177f7a77f`;
- GitHub `Reference Python CI` run: `32111920701`;
- result: `964/964 PASS`;
- architecture fitness job: `Full reference test suite` — `success`.

New regression evidence observed green in that run includes:

- exact-release P7.05 observer pin;
- fail-closed observer lifecycle/unloaded-state handling;
- selected-Mac proof rejection on runtime-release mismatch;
- fail-closed detection of orphan/unrecognized reusable credential plaintext.

No material objection remained after iteration 2.

## 7. P7.06 handoff requirements

R22 does not itself deploy the remediation to the live selected Mac mini, because doing so before P7.06 would turn an ad-hoc reinstall into the very update path that P7.06 exists to govern.

Therefore the first P7.06 controlled update candidate MUST include the merged R22 hardening before any operational workload expansion.

P7.06 must preserve at least:

1. one exact release identity for the runtime and all installed release-coupled adapters;
2. pre-update durable-state/backup/checkpoint evidence required by its scope;
3. explicit compatibility/migration checks;
4. controlled stop/update/re-pin/start sequencing;
5. post-update runtime health and observer-loaded/exact-release-pin verification;
6. explicit rollback or unsafe-rollback disposition;
7. exact historical release references for reconstruction;
8. no automatic replay of prior product/external consequential effects;
9. no Product Contract or Platform Capability lifecycle promotion by implication.

Until that first P7.06 controlled update is proven, the existing selected Mac remains in the already-proven P7.05 owner-operated state and operational workload expansion stays blocked by roadmap sequencing.

## 8. ADR / stable-boundary disposition

`ADR required now: NO`.

R22 remediation does not select a permanent deployment manager, observability backend, IAM product, persistence technology, public API, stable wire/storage schema or cross-product service topology.

Re-open the ADR/stable-boundary gate before any of the existing R21/P7.01 triggers are crossed, including materially constraining cross-product persistence, stable/public service boundaries, shared IAM/key management, public ingress, externally relied-upon observability, Stable Product Contract transition, Active Platform Capability transition or customer Production reliance.

## 9. Gate result

**R22 result: `Complete / PASS`.**

The combined P7.02–P7.05 persistent-runtime boundary is sufficiently coherent and fail-closed to proceed to the governed deployment/update/rollback work of P7.06, subject to the explicit handoff constraints above.

This PASS means only that the reviewed repository contour has no remaining material R22 objection. It does not claim that the R22 remediation has already been deployed to the selected Mac mini; that deployment is intentionally reserved for the first controlled P7.06 update. It also does not create Production readiness, an `Active` Platform Capability, a Stable Product Contract, a public/stable service or observability boundary, SLA/SLO/support commitments or broader conformance.

Next canonical action:

> **P7.06 — Governed deploy/update/rollback/version/migration path.**
