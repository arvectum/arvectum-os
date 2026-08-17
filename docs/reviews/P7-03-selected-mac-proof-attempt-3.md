# P7.03 — Selected Mac mini Proof Attempt 3

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Canonical checkout release tested: `e20b7801cf389b1afe7f513182d352a566809c55`
Observed P7.02 runtime release: `73af746f83271b14670fe22db658dfd55cacb291`

## 1. Purpose

This artifact preserves the successful hardened selected-Mac P7.03 closure proof after the two earlier attempts were truthfully retained.

- Attempt 1 was rejected as closure evidence because its reported `PASS` contradicted `persistent_runtime_state=stopped`.
- PR `#31` hardened the selected-Mac proof contract and passed `935/935` Reference Python tests.
- Attempt 2 then correctly failed closed because the existing P7.02 persistent runtime was actually `stopped`.
- The human owner/operator authorized the minimum existing P7.02 lifecycle recovery action, `start`, without install, upgrade, migration or release change.
- Attempt 3 executed only after the runtime returned to `healthy` and completed the hardened proof successfully.

## 2. Service recovery result

The existing P7.02 service was recovered through the already-defined owner-operated lifecycle command. No P7.02 installation, release migration or service-topology change was performed.

Observed result after recovery:

- service label: `com.arvectum.os.persistent-internal`;
- supervision: owner `launchd` LaunchAgent;
- runtime state: `healthy`;
- exact runtime release before proof: `73af746f83271b14670fe22db658dfd55cacb291`;
- exact runtime release after proof: `73af746f83271b14670fe22db658dfd55cacb291`;
- runtime release changed during recovery/proof: `false`.

The recovery is an ordinary P7.02 lifecycle operation within the existing `Persistent Internal / owner-operated` contour. It does not itself authorize product/external consequential effects or canonical-state mutation.

## 3. Hardened attestation

The hardened selected-Mac wrapper produced:

- schema: `arvectum.p7_03.selected-mac-attestation/1`;
- classification: `non-canonical operational proof evidence`;
- status: `PASS`;
- `required_runtime_enforced=true`;
- tool release SHA: `e20b7801cf389b1afe7f513182d352a566809c55`;
- runtime state before: `healthy`;
- runtime state after: `healthy`;
- runtime release before: `73af746f83271b14670fe22db658dfd55cacb291`;
- runtime release after: `73af746f83271b14670fe22db658dfd55cacb291`.

Local evidence basenames:

- selected-Mac attestation: `p7-03-selected-mac-attestation-20260817T192924Z-9fa8f43b.json`;
- core proof summary: `p7-03-summary-20260817T192924Z-a4d188c7.json`.

## 4. Backup / restore evidence

Live backup:

- basename: `p7-03-backup-20260817T192924Z-a8b80b0fe41809da.tar.gz`;
- SHA-256: `6b2661050a2d777c9cae0bada8c584c2e426489156505dc30e6ce5756de97765`;
- live restore integrity: `PASS`;
- live state digest equals restored state digest: `true`.

Non-authoritative fixture proof:

- fixture backup integrity: `PASS`;
- fixture restore integrity: `PASS`;
- deliberate tamper detection failed closed: `true`.

Minimization and separation:

- explicit excluded paths absent: `true`;
- reusable secrets in backup: `false`;
- telemetry in backup: `false`;
- cache in backup: `false`.

Authority and replay boundary:

- checkpoint canonical authority: `false`;
- proof fixture canonical authority: `false`;
- external-effect replay authorized: `false`.

The hashes above establish byte/archive integrity only. They do not create truth, Organizational Authority, approval, legal validity or canonical admission.

## 5. Execution integrity

Operator-reported final execution result:

```text
RESULT: PASS
canonical_sha: e20b7801cf389b1afe7f513182d352a566809c55
p7_02_runtime_release: 73af746f83271b14670fe22db658dfd55cacb291
working_tree_clean: YES
p7_02_service_recovery: PASS
hardened_selected_mac_p7_03_proof: PASS
```

The source checkout remained clean after proof.

The hardened wrapper therefore established the lifecycle precondition before and after the core proof instead of relying on an operator-supplied interpretation of runtime health.

## 6. Governance disposition

Attempt 3 satisfies the selected-Mac operational evidence obligation for P7.03 within the declared bounded scope.

It does **not** establish:

- external/customer `Production`;
- an `Active` Platform Capability;
- a Stable Product Contract;
- SLA/SLO/RPO/RTO/support commitments;
- a permanent database/object-store/backup technology;
- a public/stable persistence or backup format;
- multi-writer/distributed durability;
- off-host disaster recovery or clean-host portability;
- persistent product operational proof for Tender Operator or Discount Parser;
- generalized update/migration behavior;
- final IAM/secret lifecycle.

No Accepted ADR is required for closure because the filesystem/tar persistence adapter remains bounded, owner-local, reversible, private and non-stable. The ADR/stable-boundary gate must be revisited before materially constraining, cross-product or externally relied-upon persistence reliance.

## 7. Closure contribution

Together with the repository implementation/CI, proof-contract hardening, preserved failed attempts, final functional cross-review and roadmap synchronization, this Attempt 3 evidence permits P7.03 to close as `Complete / PASS`.
