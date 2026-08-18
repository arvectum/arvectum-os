# P7.04 — Persistent Identity / Operator / Service Access + Least-Privilege Operations

Status: `Complete / PASS`
Date: `2026-08-17`
Closed: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor: [`P7.03 Durable Governed State / Backup / Restore`](P7-03-DURABLE-GOVERNED-STATE-BACKUP-RESTORE.md) — `Complete / PASS`
Repository implementation PR: `#35`
Selected-Mac closure: [`Attempt 1 — Complete / PASS`](../reviews/P7-04-selected-mac-proof-attempt-1.md)

## 1. Purpose

P7.04 introduces the minimum persistent operational access boundary needed by the current internal owner-operated contour without selecting a permanent IAM/SSO/RBAC product or changing the Accepted identity/authority semantics.

The implementation deliberately keeps four concerns separate:

1. `Identity` — opaque stable identity value only;
2. authentication — proof that a supplied reusable credential matches a principal credential verifier;
3. operational authorization — an exact Organization / operation / resource / access-path grant;
4. Organizational Authority / consequential approval — **never** supplied by P7.04 access.

No role, wildcard, superuser or ambient-admin mechanism is introduced.

## 2. Authority checked

Implementation and closure were checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 — shared platform behavior remains domain-neutral and technology-independent;
- RFC-0002 — identity values stay opaque and are not overloaded with mutable access semantics;
- RFC-0003 — Identity, Authentication, Authorization, Organizational Authority and Data Governance remain distinct; least privilege, Organization scope, secret protection and portability remain mandatory;
- RFC-0005 — technical access does not bypass Governed Execution or consequential approval;
- RFC-0006 — operational access evidence is non-canonical by default and must not silently become authority;
- P7.01 secret/credential and owner/operator boundaries;
- P7.02 persistent runtime health/lifecycle boundary;
- P7.03 durable-state backup rule excluding `secrets/`.

No relevant Accepted ADR selects an IAM, credential vault, remote-administration product or stable access-policy representation.

### ADR disposition

`ADR required now: NO`.

The current adapter is stdlib-only, owner-local, single-Organization, explicitly provisional and removable. Revisit the ADR/stable-boundary gate before cross-Organization use, externally relied-upon IAM behavior, public/stable access APIs, materially constraining credential technology, or a long-lived remote-administration topology.

## 3. Canonical implementation

Repository files:

- `reference/python/p7_04_persistent_access.py` — persistent principal, credential and exact-grant registry;
- `reference/python/p7_04_selected_mac_proof.py` — hardened selected-Mac closure proof wrapper;
- `reference/python/tests/test_p7_04_persistent_access.py` — access/credential/security regressions;
- `reference/python/tests/test_p7_04_selected_mac_proof.py` — proof-contract and runtime-health regressions.

Default operational placement is the existing P7.02 root:

`~/Library/Application Support/ArvectumOS/persistent-internal`

P7.04 uses:

```text
config/
  p7-04-access.json       owner-local non-canonical access registry
secrets/
  p7-04/
    <credential-id>.secret  reusable owner-local credential material
evidence/
  p7-04-selected-mac-attestation-*.json  non-canonical proof evidence
```

The access registry contains salted credential verifiers, not reusable credential plaintext. Reusable material remains under `secrets/`, which P7.03 excludes from ordinary governed-state backup. Re-provisioning/host-loss portability remains subject to the later Phase-7 portability work rather than being silently copied into governed backups.

## 4. Persistent identity continuity

P7.04 does not generate a replacement human owner identity when the P6.05-L4 owner context already exists.

`bootstrap_from_p6_owner_context(...)` accepts only the exact bounded P6.05-L4 context shape and requires the source bootstrap to remain:

- Organization `ООО «Арвектум»`;
- human / owner-operated principal;
- zero authorization grants;
- zero delegations;
- `organizational_authority_claimed=false`;
- zero authentication evidence refs;
- explicit P6.05-L4 owner authorization evidence.

The existing Organization and human Principal identities are reused. One persistent service Principal identity is created once if absent and reused thereafter.

Raw owner/service identity values remain owner-local and are not published in this canonical document or selected-Mac attestation.

## 5. Authorization model

Access is `deny` by default.

A positive operational decision requires all of the following to match simultaneously:

- exact Organization identity;
- exact registered principal identity;
- enabled human/service principal;
- exact active credential bound to that principal;
- credential verifier match;
- exact operation;
- exact resource;
- explicit access path: `local` or `remote`.

A missing/mismatched element denies the request.

Wildcard `*` operation/resource scopes are rejected. The registry has no `roles`, no superuser bit and no ambient-admin bypass.

## 6. Human and service attribution

The registry distinguishes `human` and `service` principal kinds without moving kind/permissions into `Identity` itself.

Every successful `AccessDecision` carries:

- Organization identity;
- principal identity;
- principal kind;
- credential identifier;
- exact grant identifier;
- exact operation/resource/access path.

This makes significant human and workload/service access attributable while keeping authorization separate from the identity value.

## 7. Credential lifecycle

Credential issuance generates high-entropy owner-local reusable material and stores only a salted PBKDF2-SHA256 verifier in the registry.

The implementation provides:

- initial issue;
- explicit rotation;
- credential revocation;
- principal disablement;
- grant revocation.

Rotation revokes the old credential record, deletes its reusable secret file and creates a new credential generation. Principal disablement revokes its active credentials and grants and removes retained active secret files.

The adapter exposes the secret file path, not the secret value, from issuance. Ordinary registry/evidence output does not contain reusable credential material.

## 8. Remote administration boundary

`remote` is an explicit grant dimension, not an alternate authority path.

The selected-Mac proof established a bounded remote administrative-read path (`runtime.status` on the exact P7.02 runtime resource) while proving that remote `runtime.restart` remains denied without a separate exact grant.

Host/OS administration remains an environment concern and does not become Organizational Authority. P7.04 does not claim that SSH/Tailscale/another transport is a stable platform interface.

## 9. Consequential authority boundary

Every `AccessDecision`, including an allowed one, declares:

- `operational_access_only=true`;
- `organizational_authority_satisfied=false`;
- `consequential_approval_satisfied=false`.

Therefore technical operator/admin access cannot itself approve a governance or business decision, mutate canonical state outside Governed Execution, authorize a product external effect, or replace residual owner/delegated authority.

## 10. Failure behavior

The adapter fails closed for malformed or unavailable access state, broad/symlink-unsafe owner-local state paths, invalid principal/Organization bindings, missing/revoked credentials, failed authentication, missing grants, wrong operation/resource/Organization/access path, wildcard scopes, disabled principals and authority/admin invariant tampering.

The selected-Mac wrapper additionally requires the existing P7.02 runtime to be `healthy` before and after the proof and requires its exact runtime release to remain unchanged during the proof.

## 11. Repository evidence

Focused isolated validation performed while preparing PR `#35`:

- persistent-access suite: `14/14 PASS`;
- selected-Mac proof contract: `2/2 PASS` in an isolated proof fixture.

GitHub `Reference Python CI` was green at the final implementation/documentation head before merge. PR `#35` merged at `2b808c658c19056cef65b69e82152ae12d861679`.

## 12. Selected-Mac closure evidence

Selected-Mac Attempt 1 completed `PASS` on `2026-08-18` from exact canonical `main` SHA:

`218e3762975a2fd6f11e8f13d4445bce5f5d7c94`

The existing P7.02 persistent runtime remained healthy before and after the proof on exact runtime release:

`73af746f83271b14670fe22db658dfd55cacb291`

Canonical review record:

- [`P7.04 Selected-Mac Persistent Access Proof — Attempt 1`](../reviews/P7-04-selected-mac-proof-attempt-1.md) — `Complete / PASS`;
- owner-local attestation basename: `p7-04-selected-mac-attestation-20260818T050134Z-6a13d49b.json`;
- attestation SHA-256: `5c0a67b15b7fb469bc5933030db0c2e90adfb47c3eb94411c43ba555b7d98659`.

The reviewed proof passed human/service attribution, deny-by-default behavior, exact Organization/operation/resource scope, explicit local/remote paths, denied ungranted remote lifecycle administration, credential rotation, grant/credential revocation, absence of ambient service administration, reusable-secret minimization, authority separation, unchanged persistent-runtime release, no canonical mutation and no external/product effect.

The raw attestation remains owner-local non-canonical operational evidence. Canonical history records only the minimum review facts and digest.

`P7.04 = Complete / PASS` for the declared `Persistent Internal / owner-operated` scope.

## 13. Explicit non-claims

P7.04 does not establish:

- external/customer `Production`;
- a permanent IAM/SSO/RBAC/secret-vault choice;
- supported remote-admin transport;
- public/stable access-policy API or wire format;
- multi-Organization access;
- `Active` Platform Capability status;
- Stable Product Contract status;
- Organizational Authority delegation;
- SLA/support/conformance claims.
