# P4.09 — Security, rights, minimization and authority-safe UX

Status: `Complete`
Version: `1.0.1`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Phase: `Phase 4 — Workspace / Operator Experience`
Result: **`PASS — the bounded operator presentation boundary fails closed for missing/denied/ambiguous/wrong-Organization access, does not expose protected counts, does not let derived previews outlive source visibility, requires re-inspection after source-authorization replacement, and uses action labels that do not manufacture approval or Organizational Authority.`**

## 1. Canonical authority checked

P4.09 was evaluated against Constitution `1.2.0` (`Ratified`, frozen), the RFC Index, Accepted RFC-0001 through RFC-0008 `1.0.0`, `docs/adrs/README.md`, R10 and R11. The relevant binding semantics are deny-by-default authorization, Organization isolation, least privilege, purpose limitation/minimization, separation of Authorization from Organizational Authority/approval, exact-version/provenance honesty, attributable consequential execution, retrieval non-authority and Document/Artifact rights/classification handling.

No conflict with the Constitution or Accepted RFC baseline was identified. The Decision Authority Policy remains `Proposed` and is not treated as normative.

## 2. Scope

P4.09 hardens the already established P4.02–P4.08 workspace semantics. It does not introduce a new IAM/PDP/PEP, policy language, role hierarchy, public API, frontend framework, Product Contract, Platform Capability or canonical-state owner.

The executable addition is `authority_safe_ux.py`, a narrow internal decision-consumption helper. It consumes `CurrentSourceAuthorization` evidence already produced elsewhere and may only derive minimized non-authoritative presentation state from it. It deliberately does not decide permissions, Organizational Authority, approval, purpose/right/classification eligibility, Knowledge freshness or exact-reliance eligibility. Existing semantic owners retain those responsibilities.

## 3. Required-check disposition

### P4.09-C1 — Wrong-Organization and unauthorized disclosure

`PASS`. Matching is exact on current workspace Organization, actual Principal, represented Principal and protected Subject. Missing, denied, duplicate/ambiguous and wrong-Organization evidence collapse to the same non-content `Not available` state. Blocked state exposes no governed content, derived preview or protected count.

### P4.09-C2 — Hidden action / alternate client-state invocation

`PASS within the bounded Phase 4 action path`. P4.09 creates no action executor. Consequential action remains routed through R10 `operator_safety.py` and P4.05/Governed Execution. When a caller pins the authorization decision used for prior inspection, replacement yields `Re-inspection required` and no content/preview, so stale presentation cannot become continuing action authority.

### P4.09-C3 — Authority-safe labels

`PASS`. The labels are `Request governed action`, `Re-inspect current access` and `Action unavailable`. They describe intent/state and do not claim approval, permission, Organizational Authority or guaranteed commit. Runtime gate truth remains owned by P4.05/RFC-0005.

### P4.09-C4 — Classification, purpose, rights and minimization

`PASS with preserved semantic ownership`. P4.09 does not replace P3.07/CAP-001/CAP-002 handling enforcement. Document/Artifact and Memory/Knowledge surfaces continue their existing purpose/right/classification/freshness/exact-reliance checks before protected content is passed to presentation. The helper only adds presentation minimization: protected counts are not exposed and a derived preview cannot outlive governed-content visibility.

### P4.09-C5 — Derived preview/summaries cannot bypass source access

`PASS`. Denied, missing, ambiguous, wrong-Organization or replaced source decisions force preview visibility to false. The helper generates no content and persists no summary as an alternate governed source.

### P4.09-C6 — Expired/revoked/stale authority or knowledge

`PASS within declared ownership boundaries`. Revoked/replaced source authorization becomes unavailable or requires re-inspection. Knowledge freshness remains owned by P4.07/CAP-002; P4.09 creates no generic `trusted/current/approved` state that could override stale/review-required semantics.

### P4.09-C7 — Audit-sensitive operator attribution

`PASS`. Decisions remain bound to current `WorkspaceShellState` Actor/Organization and preserve the exact consumed authorization decision Version Identity when available. P4.09 performs no consequential mutation; R10/P4.05/RFC-0005/RFC-0006 remain the attributable execution/evidence path.

## 4. R11 refactoring trigger

P4.09 provides positive evidence that repeated P4.03–P4.07/R10 source-authorization matching can be expressed as a narrow internal decision-consumption primitive without becoming a new authorization-policy owner. The helper consumes but never produces authorization decisions; knows only Organization/Actor/represented-Actor/resource/decision-version continuity; owns no purpose/right/classification/freshness/exact-reliance policy; grants no Organizational Authority/approval; executes no action; and is internal/non-public.

P4.09 intentionally does not migrate all existing callers. Broader refactoring remains deferred until P4.10 validates architecture fitness and deterministic critical-state behavior across the whole workspace.

## 5. Executable evidence

Added:

- `reference/python/arvectum_os_ref/authority_safe_ux.py`;
- `reference/python/tests/test_p4_09_security_rights_authority_safe_ux.py`.

The tests cover unique current allow evidence; missing/denied/ambiguous/wrong-Organization fail-closed behavior; protected-count suppression; derived-preview suppression when source visibility is blocked; exact authorization-decision replacement requiring re-inspection; and labels that do not claim approval/permission/authority.

A test-harness constructor mismatch was found during pre-merge review and corrected before completion evidence was recorded.

GitHub-hosted `Reference Python CI #188` on the P4.09 PR completed with `failure` at the separately tracked runner/account provisioning problem represented by issue #54. No green hosted P4.09 run or test-suite failure is claimed from that run. P4.10 must account for deterministic testability rather than treating documentation as a substitute.

## 6. ADR / lifecycle / contract disposition

No ADR threshold is crossed. P4.09 selects no durable frontend, route/API/wire format, IAM provider, policy engine, storage topology or deployment boundary. No Product Contract changes are required; the P4.08 Product Contract remains `Provisional 0.1.0`. No Platform Capability is created or promoted. No production, operational-readiness, SLA, support or broad conformance claim is made.

## 7. Exit criterion

**PASS.** The P4.09 required checks are represented by bounded executable/reference evidence without moving authority into presentation state or weakening existing semantic-owner controls.

The next canonical Phase 4 action is `P4.10 — Workspace architecture fitness + accessibility/usability baseline` after roadmap synchronization.
