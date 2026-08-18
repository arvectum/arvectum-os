# P7.06 Live Remediation Note

Status: `Bounded remediation / selected-Mac proof pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded operational remediation

This note records the implementation-level consequence of selected-Mac P7.06 Attempt 5 without changing the Accepted architecture or creating a stable deployment contract.

## Runtime activation correction

The P7.02 LaunchAgent declares `RunAtLoad=true`. Initial `launchctl bootstrap` therefore owns first process activation. The install path MUST NOT immediately force-replace that just-starting process with `launchctl kickstart -k`, because the replacement lifecycle can race at the P7.02 single-instance runtime lock. Explicit restart retains `kickstart -k` because replacement is intentional there.

## Failure-evidence correction

P7.06 deployment Git release identity and launchd target identity are distinct. Helper functions MUST NOT reuse the deployment `target` shell variable for launchd targets. Failed-update rollback evidence must retain the exact 40-character Git target SHA from preflight/update context.

## Scope boundary

These corrections are private owner-operated adapter hardening only. They do not change durable schema, authorize migration, mutate canonical state, invoke/replay product or external effects, select permanent deployment technology, create Organizational Authority, promote any Platform Capability, stabilize any Product Contract, or establish Production/SLA/support claims.

Closure remains dependent on the complete selected-Mac P7.06 update/rollback/final-update proof and canonical roadmap synchronization.
