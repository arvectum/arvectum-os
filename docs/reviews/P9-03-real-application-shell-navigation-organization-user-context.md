# P9.03 — Real Application Shell + Navigation + Organization/User Context

Status: `Complete / PASS`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Constitution basis: `1.2.0` — `Ratified`, frozen
RFC basis: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
ADR basis: ADR-0001 — `Productive Workspace Browser Application Topology` — `Accepted`
Application release: `p9.03.1` — `bounded-internal-provisional`, `public_api=false`

## 1. Purpose

P9.03 implements the first real Productive Workspace application boundary under Accepted ADR-0001. It establishes the browser application shell, same-origin BFF, explicit Organization/actor context, bounded server-side session, browser trust controls and exact-release packaging that later P9.04–P9.06 flows may rely on.

This closure does not claim M9-alpha, public/customer Production, a public/stable API, a Stable Product Contract, an Active Platform Capability or Organizational Authority.

## 2. Authority and scope checked

The implementation and final review were checked against, in authority order:

1. Constitution `1.2.0`;
2. Accepted RFC-0001 through RFC-0008;
3. Accepted ADR-0001;
4. current approved engineering/governance constraints;
5. existing P7 persistent runtime/access/deploy/recovery behavior;
6. P9.01 acceptance journeys and P9.02/R29 architecture evidence;
7. implementation, executable tests and CI;
8. canonical Phase 9 and master roadmaps.

No lower-authority artifact was used to override a higher-authority rule.

## 3. Implemented application boundary

P9.03 adds a real React + TypeScript SPA compiled with Vite-class tooling into committed content-hashed static assets, served by a same-origin Python/FastAPI BFF. The BFF remains an internal release-scoped application boundary and is not declared as a public Product Contract/API.

The normal shell exposes domain-neutral navigation only:

- `Home` — available;
- `My Work` — planned for P9.04;
- `Search` — planned for P9.05;
- `Governed actions` — planned for P9.06;
- `Products` — planned for P9.07.

No Tender, Discount, Creative or other product business rules were moved into the platform shell.

## 4. P9.03 implementation-boundary decision

| # | Required boundary | Result | Evidence / disposition |
|---:|---|---|---|
| 1 | Real React + TypeScript shell built to release-pinned static assets | `PASS` | `workspace_frontend`, committed Vite build, package lock, content-hashed assets and asset verification |
| 2 | Same-origin Python BFF without browser private-platform coupling | `PASS` | `workspace_app/main.py`; SPA and `/api/app/v1` share the same application origin |
| 3 | Explicit attributable actor + Organization context | `PASS` | `P704AccessResolver` resolves the exact server-side P7.04 organization/human actor; browser inputs cannot override them |
| 4 | Protected-read Authorization/Data Governance/minimization | `PASS` | every protected context read reauthorizes through P7.04; access revocation or context drift revokes the session; response omits raw governed IDs |
| 5 | Opaque bounded/revocable/rotatable session | `PASS` | in-memory server-side opaque sessions with idle + absolute expiry, revocation and bootstrap rotation; process restart invalidates sessions fail closed |
| 6 | CSRF + configured Host/Origin enforcement | `PASS` | unsafe requests require exact Origin; Host allowlist and CSRF token checks are explicit and negatively tested |
| 7 | No auth/session bearer material in browser Web Storage | `PASS` | source/bundle guard rejects `localStorage` and `sessionStorage`; session identifier is HttpOnly cookie state |
| 8 | Loopback-only HTTP exception or stronger HTTPS profile | `PASS — bounded` | current owner-operated profile permits HTTP only for strict loopback; non-loopback HTTP is rejected; HTTPS uses Secure `__Host-` cookie semantics |
| 9 | Exact application release identity + stale-client failure | `PASS` | frontend bundle carries `p9.03.1`; every app API request must supply exact release identity; mismatch returns `409 RELEASE_MISMATCH` + reload requirement |
| 10 | Domain-neutral navigation without product business logic | `PASS` | shell exposes only generic Workspace destinations and truthful planned states |
| 11 | Existing P4/P7 diagnostic/recovery surface preserved | `PASS` | implementation adds a new P9 application boundary and does not delete or replace P4/P7 diagnostic/recovery paths |

## 5. Exact-release P7.06 deployment coupling

Final review identified one material deployment gap before closure: the P7.06 archive already contained the P9 BFF source, frontend build and exact `workspace_app/requirements.lock`, but a newly prepared release-specific venv did not install that lock.

Commit `c4520513e58a813858a53fb807e01473b9146c26` resolves the gap:

- dependency source is the exact target release's own `workspace_app/requirements.lock`;
- pre-P9 releases without that lock remain valid and no-op for this step;
- each target continues using its own `$RUNTIME_ROOT/venvs/$target`;
- lock SHA-256 is recorded in an owner-local venv stamp to avoid unnecessary reinstall;
- the stamp is atomically replaced only after successful installation;
- install failure is fail closed;
- FastAPI and Uvicorn imports are verified even when the lock stamp already matches;
- existing backup/preflight/update/rollback sequencing is not replaced;
- no new launchd/service lifecycle is created by P9.03.

The release archive SHA already covers the exact source tree containing the pinned lock and frontend assets. P9.03 therefore proves exact-release dependency coupling for the current internal contour; it does not make a stronger public supply-chain/SBOM guarantee.

## 6. Session, identity, authority and data-governance disposition

Authentication/access material remains server-side. A valid Workspace session does not itself create authorization or Organizational Authority: protected reads re-resolve current P7.04 access, and a changed/revoked access binding invalidates the session.

The browser receives a minimized Organization label, actor label, session CSRF token and non-authoritative shell metadata. It does not receive the P7.04 credential secret, grant identifier, raw Organization identity or raw actor identity as normal shell context.

The P9.03 helper `provision-local-grant` requires explicit `--confirm` and can create only the exact local `workspace.open` / `productive-workspace` operational grant. It does not grant Organizational Authority or consequential approval.

## 7. Release and runtime disposition

Application release `p9.03.1` is classified `bounded-internal-provisional`; `public_api=false`.

P9.03 introduces no second independent production-service lifecycle. The BFF is a foreground application command using the same exact P7.06 release unit and release-specific Python environment. Persistent daily-use activation/dogfooding is not silently claimed by this task and remains later Phase 9 operational evidence.

The current loopback-only HTTP exception is restricted to the selected private owner-operated contour under ADR-0001. It is not evidence for remote/customer browser deployment.

## 8. Regression repair found during implementation

The first full Reference Python run exposed seven stale historical fitness assumptions that froze the repository at an earlier state, including assumptions that no ADR could ever exist after P8.11/P8.12 and that the master roadmap must permanently retain old detailed rows/wording.

Those tests were revised narrowly to preserve their actual historical closure semantics and non-claims while allowing later separately governed ADRs and roadmap compaction. No runtime authority, lifecycle, public-surface or product/platform boundary was weakened to obtain a green suite.

## 9. Main-branch reconciliation

Before closure, canonical `main` advanced with the approved P6.02 repository-locator reconciliation. The P9.03 branch was reconciled with that canonical head through merge commit `8989730d01ae43419d6b5c927b32c8b0ab82dd83`.

The P6.02 additions affect repository locator/provenance governance and do not conflict with ADR-0001 or the P9.03 browser/BFF/session/runtime boundary.

## 10. Functional cross-review

Six focused iterations were completed for final P9.03 closure. The earlier local implementation review is supporting evidence; the disposition below is the final repository-level functional review.

### Iteration 1 — higher authority and topology

Result: `PASS`.

The implementation follows Accepted ADR-0001: built React/TypeScript assets, same-origin Python BFF, bounded internal application surface and no independent public-service lifecycle. No Accepted RFC/ADR amendment is required.

### Iteration 2 — identity, Organization, authorization and data governance

Result: `PASS`.

Organization and human actor are resolved server-side from P7.04, browser override attempts are ignored, protected reads reauthorize current access, raw identities are minimized from normal shell output and operational access is not presented as Organizational Authority.

### Iteration 3 — session and browser trust boundary

Result: `PASS`.

Opaque bounded server-side session state, rotation/revocation, Host/Origin/CSRF checks, loopback HTTP restrictions, security headers and the Web-Storage prohibition are present and negatively tested.

### Iteration 4 — exact release, deployment and rollback

Result: `REVISE → PASS`.

Material finding: the exact release archive included the Workspace runtime lock but P7.06 did not install it into the release-specific venv. Commit `c4520513e58a813858a53fb807e01473b9146c26` added exact-release installation, hash-stamp idempotence, import verification and durable regression guards while preserving older pre-P9 release compatibility and rollback isolation.

Disposition: `resolved`.

### Iteration 5 — product/platform boundary, navigation and recovery continuity

Result: `PASS`.

Navigation is domain-neutral, later features are marked planned rather than simulated, product business logic remains product-owned, and the existing P4/P7 diagnostic/recovery surface is preserved.

### Iteration 6 — final repository regression and canonical-head reconciliation

Result: `PASS`.

Final implementation head before this review/roadmap-only closure edit: `8989730d01ae43419d6b5c927b32c8b0ab82dd83`.

Evidence:

- `Reference Python CI #242` / run `32471453401` — `SUCCESS`;
- full Reference Python suite — `Ran 1301 tests in 24.909s`, `OK`;
- generated Python artifact rejection — `PASS`;
- `Productive Workspace CI #10` / run `32471453388` — `SUCCESS`;
- BFF security/context job — `SUCCESS`;
- SPA typecheck/tests/Web-Storage/reproducibility/release-asset job — `SUCCESS`;
- the CI checkout tested the actual PR merge result against the then-current canonical `main`.

No material objection remains after iteration 6.

Functional cross-review is not formal RFC/ADR acceptance, capability/Product Contract promotion, customer Production approval, conformance certification or commercial authority.

## 11. Final verdict

> **`P9.03 = Complete / PASS`**

The real Productive Workspace application shell and its browser/BFF/session/Organization/release boundary are implemented sufficiently for the next bounded Phase 9 work item to rely on them.

The next canonical action after roadmap synchronization is **`P9.04 — My Work / Needs Attention projection`**. M9-alpha remains unachieved and requires P9.04, P9.05, P9.06 and R30 evidence.