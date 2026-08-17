# P7.03 — Selected Mac mini Proof Attempt 2

Status: `Blocked / persistent runtime stopped`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Canonical checkout release tested: `a04f6e6caa90c8f078ab1383be14f83b4f47ad3b`
Observed P7.02 runtime release: `73af746f83271b14670fe22db658dfd55cacb291`

## 1. Purpose

This artifact preserves the second selected-Mac P7.03 closure attempt. Unlike Attempt 1, the hardened selected-Mac proof contract behaved correctly and failed closed before backup/restore proof because the existing P7.02 persistent runtime was not healthy.

## 2. Reported result

Operator output:

```text
P7.03 selected-Mac FAIL: selected-Mac attestation requires healthy persistent runtime, got 'stopped'
```

Diagnostics reported:

- repository SHA: `a04f6e6caa90c8f078ab1383be14f83b4f47ad3b` — matching expected canonical SHA;
- working tree: clean;
- runtime state: `stopped`;
- last heartbeat: `2026-08-17T17:51:04.883917Z`;
- P7.02 runtime release remains `73af746f83271b14670fe22db658dfd55cacb291` from the existing P7.02 runtime state.

## 3. Interpretation

The hardened proof contract introduced by PR `#31` behaved as intended:

- it did not accept stale or stopped runtime telemetry;
- it did not fabricate a PASS result;
- it did not start, restart, update or reinstall the runtime;
- it did not proceed to closure evidence under an invalid lifecycle precondition.

This is therefore an operational lifecycle blocker, not a P7.03 persistence-integrity failure and not a regression in the backup/restore mechanism.

P7.02 canonical lifecycle documentation defines `start` as the normal owner-operated command for loading/starting the already-installed LaunchAgent and waiting until exact-release health becomes healthy. The P7.02 runtime envelope performs no product/external consequential effect and no canonical-state mutation.

## 4. Required remediation

Do not run `install`, do not change the selected P7.02 release, and do not bypass health checks.

The minimum recovery action is the existing P7.02 lifecycle command:

```sh
sh reference/python/p7_02_macos_service.sh start
```

After `start` succeeds, verify:

```sh
sh reference/python/p7_02_macos_service.sh status
```

The expected service release remains the already-installed exact P7.02 release `73af746f83271b14670fe22db658dfd55cacb291` unless a separately governed update is later performed under P7.06.

Then rerun the hardened P7.03 selected-Mac proof from the current exact canonical `main` SHA.

## 5. Governance disposition

Attempt 2 is retained as truthful operational evidence and does not advance the roadmap.

- `P7.03` remains current and open;
- `P7.04` must not be represented as current yet;
- no Product Contract or Platform Capability lifecycle changes occur;
- no ADR is triggered by this lifecycle recovery;
- the human owner/operator remains the authority for the local operational action; AI may recommend or execute only within explicitly authorized bounds.
