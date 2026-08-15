# P6.05-L8 attempt #1 — reconstruction harness / retained-evidence blocker

* Status: `Blocked / FAIL-CLOSED`
* Date: `2026-08-15`
* Owner: `ООО «Арвектум»`
* Task classification: `platform` with `product_contract` and `product_specific`
* Operational Environment: `Internal / local owner-operated runtime`
* Production-readiness claim: `None`
* Platform SHA: `e98b7c091198e0ff2e962a7d915da15d7d9a4cc3`
* L8 attempt: `1`

## 1. Attempt #1 facts

- Exactly one bounded admission attempt was consumed under explicit owner instruction.
- L7 input integrity was independently reverified: manifest SHA `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`, member_count `7`, all file hashes and sizes confirmed PASS.
- All pre-run gates (offline focused tests, full reference suite, L4 context, L5 connection) passed.
- The Governed Execution for `OP_ADMIT_DOCUMENT_VERSION` reached `Ready` after all four required gates (Authorization, OrganizationalAuthority, DataGovernance, ConsequentialApproval) were explicitly set to `ALLOW`.
- One CAP-001 `admit_document_version` call completed successfully in-process: authority mode `External Reference` was preserved, member_count `7` and manifest integrity were maintained, and no raw tender document bytes were platformized.
- No network procurement requests, EIS/SOAP calls, archive downloads or external actions occurred during this attempt.

## 2. Failure location and root cause

- The owner-local orchestration harness failed while constructing the canonical admission Event needed for the RFC-0006/CAP-004 evidence chain.
- Exception: `ValueError: Canonical Event provenance must preserve actor, execution and related governed references` raised at line 274 of `l8_admission_orchestration.py` within `CanonicalEvent.__init__`.
- Root cause: The harness Event construction omitted required provenance references (producer, exact execution version and result subject identity) while declaring the result as a related governed reference.
- Canonical code behaved correctly and failed closed to preserve provenance integrity. This was not a CAP-001/CAP-004 or platform implementation defect.

## 3. Forensic assessment (P6.05-L8-A1)

- Synthetic reproduction confirmed that the incomplete provenance shape produces the exact same `ValueError` and that adding the missing references allows construction to pass.
- Persistence analysis:
  - Candidate input: DERIVABLE from L7 evidence.
  - Execution lineage: NOT PERSISTED (survived only in process memory).
  - Gate decisions: NOT PERSISTED.
  - CAP-001 admitted result: STDOUT_ONLY (the admitted version and artifacts were not retained as exact governed runtime state).
  - Post-admission execution state: NOT PERSISTED (never reached terminal `Succeeded`).
  - Event evidence: NOT CREATED (construction failed).
  - CAP-004 reconstruction: NOT PERFORMED.

## 4. Independent governance disposition

The forensic assessment initially explored `RECOVERABLE_WITH_DETERMINISTIC_REHYDRATION`. However, independent canonical review has rejected this for the following reasons:

- RFC-0001 requires all consequential changes to occur through Governed Execution; rehydrating state outside the platform mutation seam bypasses this governance.
- RFC-0005 requires governance-significant transitions to be immutable history and prohibits retry behavior that silently rewrites consequential effects.
- Attempt #1 results existed only in ephemeral process memory and were not retained as governed history. Manufacturing new objects from old inputs and reusing identities would manufacture history rather than reconstruct retained evidence.
- CAP-004 is derived and cannot invent missing source evidence.

Disposition: **NOT_RECOVERABLE_WITHOUT_NEW_ADMISSION**. Attempt #1 remains a truthful partial/fail-closed L8 attempt. A separately authorized attempt #2 is required.

## 5. Boundaries preserved

- No token, secrets, archive URLs or SOAP/XML committed or exposed.
- No raw document bytes platformized.
- Constitution, RFC baseline and P6.02 Product Contract remain unchanged.
- Reference implementation code remains unchanged.

## 6. Minimal remediation required before attempt #2

1. Fix the owner-local L8 harness provenance construction to include all required references (producer, initiator, execution subject/version, result subject/version).
2. Add owner-only checkpoint persistence to the harness so that every governance-significant object (lineage versions, gate decisions, admitted result, Event, reconstruction manifest) is saved to safe, mode 600 files before moving to the next stage.
3. Locally reverify L7 manifest SHA and file integrity immediately before attempt #2.

## 7. Retry authorization boundary

- Attempt #2 must use a NEW execution/attempt identity lineage and preserve explicit causation to attempt #1.
- Attempt #2 requires a separate explicit owner authorization.
- Attempt #2 remains one-shot: no automatic retry after a second consumed failure.
- P6.05 remains **Active / In Progress**; real `7/7` remains **OBSERVED** from L7 but is **NOT yet GOVERNED**.
