# P7.09 — Operator Runbook + Incident / Uncertain-Outcome / Recovery Drills

Status: `Implementation review — selected-Mac drill closure pending`  
Version: `1.0.0`  
Date: `2026-08-19`  
Owner: `ООО «Арвектум»`  
Task classification: `platform` with bounded `governance` and `product_contract` operational concerns  
Operating classification: `Persistent Internal / owner-operated`  
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)  
Predecessors: `P7.02` through `P7.08` — `Complete / PASS`

## 1. Purpose

P7.09 turns the recovery semantics already proved by P7.02–P7.08 into one versioned operator runbook and an executable drill contract.

The runbook does **not** create a new recovery subsystem, incident-management platform, automatic remediation engine or authority path. It composes the existing private owner-operated mechanisms and makes the operator decision boundary explicit:

> **Technical recovery can restore a runtime, host, dependency, credential or verified evidence path. It does not by itself authorize a consequential action.**

When an external effect may already have happened and the outcome is unknown, the operator must preserve an explicit `uncertain / reconciliation-required` state. Blind retry is prohibited. Historical reconstruction must not replay the effect. A later new effect, when permitted at all, must enter through a new or revalidated Governed Execution/authorization path as required by the effective workflow.

## 2. Authority baseline

This runbook is subordinate to and was designed against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0003 separation of Identity, Authentication, Authorization, Organizational Authority and Data Governance; deny-by-default and least privilege;
- RFC-0005 failure, partial completion, retry/idempotency, uncertain-outcome and reconciliation semantics;
- RFC-0006 required evidence-path integrity, telemetry non-authority and side-effect-safe historical replay;
- P7.01 operating baseline `1.0.1`;
- P7.02 supervised runtime/crash recovery;
- P7.03 durable governed state/checkpoint verification and isolated backup restore;
- P7.04 credential lifecycle and exact least-privilege grants;
- P7.05 operational health/alert/audit visibility;
- P7.06 exact-release update/rollback/interrupted-update recovery;
- P7.07 persistent Tender Operator product boundary;
- P7.08 persistent Discount Parser cross-host evidence/reconstruction boundary.

No Accepted ADR selects an incident-management, backup, IAM, deployment, observability or cross-host recovery product. P7.09 remains a private, reversible owner-operated procedure layer and does not cross that stable-boundary threshold.

## 3. Scope and operator boundary

This runbook applies only to the declared `Persistent Internal / owner-operated` Arvectum OS contour for `ООО «Арвектум»`.

Named operating role:

- `Arvectum OS Owner-Operator`.

The operator must be attributable and must operate in the exact Organization scope. Host administration, credential possession, a successful technical repair, or the ability to execute a command does **not** imply Organizational Authority or consequential approval.

The runbook must not be used to claim:

- external/customer `Production`;
- SLA/SLO/MTTR/RTO/RPO/support commitments;
- `Active` status for any Platform Capability;
- `Stable` status for any Product Contract;
- a public/stable incident, recovery, backup, IAM or deployment API;
- generalized disaster recovery or clean-host portability — that is P7.10;
- permission to bypass a Product Contract because its product host is unavailable.

## 4. Non-negotiable incident invariants

For every incident or drill:

1. **Protect people, Organization scope and secrets first.**
   - Do not publish raw identities or reusable credentials into canonical Git history, ordinary logs, issue comments or drill receipts.
   - If a credential may be exposed, revoke/rotate it before restoring ordinary access.

2. **Pause consequential processing when correctness or effect state is uncertain.**
   - Technical liveness alone is never sufficient reason to continue.

3. **Preserve uncertainty.**
   - `unknown` external outcome means `RECONCILIATION_REQUIRED`.
   - Do not convert timeout/network loss/process crash into assumed failure or assumed success.

4. **Never blindly retry a consequential external effect.**
   - Restart, rollback, backup restore, network recovery and reconstruction do not authorize replay.

5. **Keep technical recovery separate from consequential re-authorization.**
   - A successful technical repair only restores the technical preconditions.
   - Any new consequential effect must pass the applicable current Governed Execution/authorization path.

6. **Telemetry is diagnostic, not authority.**
   - P7.05 health/alerts may identify a failure but do not replace canonical execution/evidence state.

7. **Do not overwrite live governed state through P7.03 restore.**
   - The admitted P7.03 restore target is a **new isolated target**.
   - A verified isolated restore can support a later explicit forward/host recovery decision; it is not a convenience live-state replacement.

8. **Keep exact release identity.**
   - Do not “recover” by running arbitrary mutable checkout code against persistent state.
   - Use the P7.02/P7.06 exact-release mechanisms.

9. **Do not fabricate missing evidence.**
   - A provenance/evidence gap must remain explicit until repaired from an attributable retained source.

10. **A drill is non-authoritative evidence.**
    - P7.09 drill receipts are owner-local, non-canonical operational evidence.
    - A receipt proves only that the declared decision rule was exercised against the supplied facts.

## 5. Common operator triage

Before scenario-specific recovery:

### 5.1 Establish the incident boundary

Record locally, without reusable secrets:

- incident/drill scenario;
- UTC time;
- attributable operator;
- affected Organization;
- affected runtime/product/workflow identity or exact release where available;
- whether a consequential external effect was possible;
- whether its outcome is `none`, `confirmed-succeeded`, `confirmed-not-executed`, or `unknown`;
- required evidence that is present/missing;
- current technical state.

If effect state is `unknown`, immediately route to **Scenario 6 — uncertain external effect**.

### 5.2 Check the persistent platform baseline

From a clean canonical checkout on the selected Mac mini:

```sh
export ARVECTUM_P7_02_ROOT="${HOME}/Library/Application Support/ArvectumOS/persistent-internal"

sh reference/python/p7_02_macos_service.sh status

python3 reference/python/p7_05_operational_visibility.py \
  status \
  --runtime-root "${ARVECTUM_P7_02_ROOT}" \
  --json

python3 reference/python/p7_03_durable_state.py \
  verify \
  --runtime-root "${ARVECTUM_P7_02_ROOT}"

sh reference/python/p7_06_macos_deploy.sh status
```

Interpretation:

- any failed/unverifiable required state blocks consequential continuation;
- a healthy process does not resolve an uncertain product/external outcome;
- P7.05 output remains non-canonical diagnostic evidence;
- P7.06 exact-release state must be established before deployment recovery.

### 5.3 Evaluate/record a drill decision

Create a local JSON evidence file from the strict scenario template:

```sh
python3 reference/python/p7_09_operator_recovery_drills.py \
  template \
  --scenario runtime-crash
```

Evaluate without writing any state:

```sh
python3 reference/python/p7_09_operator_recovery_drills.py \
  evaluate \
  --scenario runtime-crash \
  --evidence-json /path/to/local/p7-09-runtime-crash-evidence.json
```

Record immutable owner-local drill evidence:

```sh
HEAD_SHA="$(git rev-parse HEAD)"

python3 reference/python/p7_09_operator_recovery_drills.py \
  record \
  --scenario runtime-crash \
  --evidence-json /path/to/local/p7-09-runtime-crash-evidence.json \
  --repository-sha "${HEAD_SHA}" \
  --output-dir "${ARVECTUM_P7_02_ROOT}/evidence/p7-09" \
  --expect-decision PASS
```

The command writes:

- `p7-09-drill-<scenario>-<timestamp>-<nonce>.json`;
- matching `.json.sha256`.

Verify later with:

```sh
python3 reference/python/p7_09_operator_recovery_drills.py \
  verify-receipt \
  --receipt /path/to/receipt.json \
  --digest /path/to/receipt.json.sha256
```

The evaluator and receipt writer:

- perform no canonical mutation;
- invoke no product/external effect;
- grant no authority;
- never authorize historical replay;
- reject reusable-secret exposure in supplied drill evidence.

## 6. Scenario 1 — Runtime crash

### Detection

Use:

```sh
sh reference/python/p7_02_macos_service.sh status
python3 reference/python/p7_05_operational_visibility.py status \
  --runtime-root "${ARVECTUM_P7_02_ROOT}" --json
```

P7.02 already provides supervised crash replacement and a `crash-proof` operation.

### Recovery

For an ordinary runtime process crash:

```sh
sh reference/python/p7_02_macos_service.sh restart
sh reference/python/p7_02_macos_service.sh status
```

For a controlled drill of actual supervisor recovery:

```sh
sh reference/python/p7_02_macos_service.sh crash-proof
sh reference/python/p7_02_macos_service.sh status
```

Required closure facts:

- final runtime state `healthy`;
- exact runtime release verified;
- supervised generation/process instance advanced for crash proof;
- no historical product/external effect replay.

### Fail-closed condition

Do not resume consequential work if runtime health, release pin or state required by the workload cannot be verified.

A daemon restart is technical recovery only.

## 7. Scenario 2 — Mac restart

A full host restart is a stronger operational drill than process crash and must be operator-initiated outside this runbook automation.

### Before restart

1. Stop starting new consequential product work.
2. Record the exact current release:
   ```sh
   sh reference/python/p7_06_macos_deploy.sh status
   ```
3. Verify durable state:
   ```sh
   python3 reference/python/p7_03_durable_state.py verify \
     --runtime-root "${ARVECTUM_P7_02_ROOT}"
   ```

### After owner-initiated host restart/login

Run:

```sh
sh reference/python/p7_02_macos_service.sh status

python3 reference/python/p7_05_operational_visibility.py \
  status \
  --runtime-root "${ARVECTUM_P7_02_ROOT}" \
  --json

python3 reference/python/p7_03_durable_state.py \
  verify \
  --runtime-root "${ARVECTUM_P7_02_ROOT}"

sh reference/python/p7_06_macos_deploy.sh status
```

PASS requires:

- P7.02 healthy;
- P7.05 observer/operational health available;
- same expected exact release unit;
- durable-state integrity verified;
- no historical effect replay caused by restart.

If any requirement fails, remain fail-closed for consequential work.

## 8. Scenario 3 — Persistent state or backup unavailable

### Live state fails verification

Immediately pause processing whose correctness depends on that state.

Run:

```sh
python3 reference/python/p7_03_durable_state.py verify \
  --runtime-root "${ARVECTUM_P7_02_ROOT}"
```

Do not create new canonical facts to “fill the gap”.

### Backup recovery

For a retained backup:

```sh
python3 reference/python/p7_03_durable_state.py verify-backup \
  --archive /path/to/p7-03-backup-....tar.gz
```

Restore only to a new isolated location:

```sh
python3 reference/python/p7_03_durable_state.py restore \
  --archive /path/to/p7-03-backup-....tar.gz \
  --target-root /new/private/isolated/p7-09-restore
```

Then verify the isolated restored store.

### Decision

- valid live state → no restore required;
- invalid/unavailable live state + verified isolated restore → `FORWARD_RECOVERY_REQUIRED`;
- no verified live state and no verified isolated recovery → `FAIL_CLOSED`.

P7.09 does not invent a live overwrite operation. Clean-host/host-loss restoration is P7.10.

Any later consequential effect must re-enter the applicable current governed path; isolated restore itself authorizes nothing.

## 9. Scenario 4 — Network / proxy / TLS failure

Treat DNS, proxy, PAC/bypass, TLS root/certificate and external dependency failure as a technical dependency incident.

Do **not** weaken TLS verification, add broad trust exceptions, or bypass the declared network boundary merely to make a request succeed.

### First question: could an effect have happened?

- `none` — request/effect was never attempted or was proven not to reach the effect boundary;
- `confirmed-succeeded` — authoritative external/product evidence confirms success;
- `confirmed-not-executed` — authoritative evidence confirms no effect;
- `unknown` — any ambiguity remains.

If `unknown`, do not retry. Route to Scenario 6.

### After repairing connectivity

Verify both:

- connectivity/proxy behavior;
- required TLS trust/certificate semantics.

Then:

- `none` → normal governed processing may be re-entered;
- `confirmed-succeeded` → reconstruct/record without replay;
- `confirmed-not-executed` → a later new effect requires the applicable new/revalidated authorization;
- `unknown` → reconciliation first.

Network recovery itself never grants consequential authority.

## 10. Scenario 5 — Product host unavailable

The platform must not absorb product behavior or bypass the declared Product Contract because a product host is offline.

### Tender Operator

Restore the product host/repository and use the existing P7.07 guarded operational entrypoint. Do not replace product-owned procurement semantics with direct platform-table/filesystem access.

### Discount Parser

Restore the Windows/product-host side independently. Raw product evidence and mutable product state remain product-owned/local. Do not create a hidden shared database/filesystem/broker as an incident shortcut.

### Decision

- product host + declared Product Contract boundary restored, no uncertain effect → normal guarded product entry may resume;
- product host still unavailable → `FAIL_CLOSED` for product-dependent work;
- external effect outcome unknown → `RECONCILIATION_REQUIRED`;
- any undeclared platform bypass → `FAIL_CLOSED` and hidden-coupling review.

## 11. Scenario 6 — Uncertain external effect

This is the highest-risk P7.09 scenario.

Examples:

- timeout after send request;
- process/host/network loss after effect initiation but before trustworthy confirmation;
- conflicting product ledger and external confirmation;
- partial cross-host evidence where effect completion cannot be established.

### Required behavior

1. Mark the affected execution/attempt as uncertain or reconciliation-required through the applicable product/governed mechanism.
2. Preserve retained evidence and exact material/version references.
3. **Do not repeat the historical effect.**
4. Reconcile against the authoritative external/product source.
5. Do not treat telemetry as proof of success/failure.
6. Do not fabricate confirmation.

### Resolution A — confirmed succeeded

When verified authoritative evidence confirms success:

- close/reconstruct the historical outcome;
- never replay it;
- do not use a “retry” to improve evidence completeness.

For P7.08, reconstruction may consume only the verified completed handoff/evidence path; historical reconstruction does not invoke Telegram/publication effects.

### Resolution B — confirmed not executed

When verified authoritative evidence confirms no effect:

- close the uncertain historical attempt as not executed;
- any future effect is a **new** attempt/execution;
- obtain/revalidate the applicable consequential authorization before that new effect where required.

### Resolution C — still unknown

Remain `RECONCILIATION_REQUIRED`.

No operational urgency, host recovery, restart or retry counter changes this rule.

## 12. Scenario 7 — Partial evidence path

A required evidence path is partial when, for example:

- a required receipt/report/digest is absent;
- digest verification fails;
- exact release/version reference cannot be established;
- product and platform evidence disagree;
- a required provenance source is unavailable.

### Recovery

1. Pause affected consequential processing/reconstruction.
2. Determine which required evidence is absent or unverifiable.
3. Search only attributable retained/canonical/product-authoritative sources permitted by the governing boundary.
4. Verify recovered material and digests.
5. Preserve the provenance gap if it cannot be repaired.

### Prohibited

- fabricate a replacement receipt;
- infer a historical platform gate decision that was never recorded;
- mark a partial reconstruction as complete;
- use ordinary telemetry as a canonical substitute.

PASS requires complete required evidence, verified integrity and an attributable source.

Otherwise remain fail-closed/reconciliation-required as applicable.

## 13. Scenario 8 — Credential revocation / rotation

Credential incidents are technical access incidents. They do not alter Organizational Authority.

Use the P7.04 exact principal/credential/grant model:

1. identify the exact affected credential locally;
2. revoke it if compromised, stale or no longer needed;
3. rotate only for the same attributable principal where appropriate;
4. verify old credential is denied;
5. verify replacement credential only retains the intended exact Organization/operation/resource/access-path grant;
6. remove reusable secret material from ordinary evidence/logs;
7. if a secret was exposed in an inappropriate location, treat cleanup and revocation as separate obligations.

Required PASS facts:

- old credential denied;
- replacement credential verified;
- exact grant scope verified;
- no reusable secret in the drill receipt/evidence;
- no Organizational Authority inferred from technical access.

P7.09 deliberately does not add wildcard roles, a superuser or a second access registry.

## 14. Scenario 9 — Failed update / rollback

Begin with exact deployment state:

```sh
sh reference/python/p7_06_macos_deploy.sh status
```

### Rollback-safe, known latest transaction

If P7.06 establishes that the latest successful transition is rollback-safe:

```sh
sh reference/python/p7_06_macos_deploy.sh rollback-last
sh reference/python/p7_06_macos_deploy.sh status
```

PASS requires:

- exact active release known;
- latest transaction known;
- no state-schema change;
- rollback declared safe;
- rollback completed;
- runtime healthy afterward;
- observer pinned consistently to the recovered exact release;
- no historical product/external effect replay.

### Interrupted failed-update recovery

When bounded retained P7.06 work evidence identifies the exact source release:

```sh
sh reference/python/p7_06_macos_deploy.sh recover-interrupted-latest
sh reference/python/p7_06_macos_deploy.sh status
```

This path does not fabricate a successful deployment transaction, restore durable backup, mutate canonical state, or replay product/external effects.

### Schema-changing or rollback-unsafe state

Current P7.06 does not admit automatic rollback after a schema-changing migration.

Result:

- `FORWARD_RECOVERY_REQUIRED`;
- do not force rollback;
- require an explicit governed migration/forward-recovery disposition before further consequential reliance.

## 15. Drill matrix and closure evidence

P7.09 repository implementation must exercise all nine scenarios.

| Scenario | Expected safe decision exercised |
|---|---|
| runtime crash | `PASS` after exact-release supervised recovery; replay variant `FAIL_CLOSED` |
| Mac restart | `PASS` only after runtime/observer/release/state verification |
| persistent state/backup unavailable | isolated restore → `FORWARD_RECOVERY_REQUIRED`; no verified state → `FAIL_CLOSED` |
| network/proxy/TLS failure | unknown effect → `RECONCILIATION_REQUIRED` |
| product host unavailable | no platform bypass; unknown effect → `RECONCILIATION_REQUIRED` |
| uncertain external effect | unknown → `RECONCILIATION_REQUIRED`; confirmed outcomes never replay history |
| partial evidence path | incomplete/unverifiable → `FAIL_CLOSED`; fabricated evidence rejected |
| credential revocation/rotation | old denied + exact replacement grant → `PASS`; authority/secret leakage rejected |
| failed update/rollback | exact safe rollback → `PASS`; schema change → `FORWARD_RECOVERY_REQUIRED` |

Repository CI proves the decision/drill contract.

Selected-Mac operational closure must additionally record owner-local non-canonical drill receipts for the environment-specific scenarios that cannot be established by CI alone, including at minimum:

1. actual P7.02 runtime crash/supervisor replacement;
2. actual owner-initiated Mac restart/login continuity check;
3. live P7.03 verify + backup verify + isolated restore drill;
4. live P7.05 incident visibility during a controlled runtime-down/crash condition;
5. live P7.04 rotation/revocation drill using owner-local identities/secrets without publishing them;
6. P7.06 failed/interrupted update or rollback-safe controlled drill against bounded non-schema-changing state, if it can be performed without introducing a false deployment record;
7. simulated `unknown external effect` and partial-evidence decisions through P7.09 evaluator, proving `RECONCILIATION_REQUIRED` / `FAIL_CLOSED` without invoking a real external effect;
8. product-host-unavailable decision drill without creating a platform bypass.

A real uncertain external effect must **not** be manufactured merely to prove the runbook. The safe drill uses synthetic/non-authoritative incident facts and proves the fail-closed decision.

## 16. Drill receipt handling

P7.09 receipts are:

- owner-local;
- non-canonical;
- minimized;
- secret-free;
- content-integrity covered by SHA-256;
- tied to exact repository SHA and runbook version.

Do not commit raw receipts containing local host paths, identities or operational details to the public repository.

Canonical closure evidence should record only minimized facts:

- tested canonical repository SHA;
- runbook version;
- scenarios executed;
- final decision results;
- raw local receipt basenames where useful;
- receipt SHA-256 digests;
- explicit statement that raw identities/reusable credentials were not published;
- runtime/product effect/canonical-mutation non-claims.

A SHA-256 receipt digest proves byte identity only. It does not prove truth, authority, approval or legal validity.

## 17. Escalation / stop conditions

Stop ordinary recovery and require explicit owner/governance/architecture disposition when:

- Organization scope cannot be established;
- a required canonical/evidence path is inconsistent and cannot be repaired from attributable retained sources;
- an uncertain consequential external outcome remains unresolved;
- recovery would require bypassing a Product Contract or private platform boundary;
- recovery would require copying non-exportable secrets merely to restore a host;
- a state-schema migration has occurred and rollback safety is not proven;
- the only path forward requires rewriting canonical history;
- recovery technology is becoming a durable cross-product/external dependency that crosses the ADR/stable-boundary trigger;
- incident response would broaden access, retention or public ingress beyond the approved contour.

## 18. Relationship to P7.10

P7.09 proves executable/versioned incident and recovery procedures on the current declared operating contour.

It intentionally does not claim host-loss portability. `P7.10` must separately prove restoration/reconstruction on a clean secondary environment and identify host-specific adapters, non-exportable secrets and portability gaps.

A successful isolated P7.03 restore in P7.09 is evidence for recovery mechanics, not a substitute for P7.10.

## 19. Closure rule

P7.09 may be marked `Complete / PASS` only after:

1. this versioned runbook and the P7.09 executable drill harness are merged to canonical `main`;
2. focused and full Reference Python CI pass;
3. functional cross-review has no remaining material objection;
4. selected-Mac owner-operated drill evidence covers the required environment-specific scenarios without manufacturing a real consequential external effect;
5. raw secrets/identity values are not published;
6. minimized canonical closure evidence is recorded;
7. `ROADMAP.md` and the detailed Phase 7 roadmap are synchronized and the next canonical action is advanced to `P7.10`.

Until those conditions are satisfied, repository implementation may be ready while P7.09 remains `Current`.
