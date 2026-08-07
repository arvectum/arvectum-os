# Reference Implementation Readiness — Functional Cross-review

Status: `Complete`
Date: `2026-08-07`
Subject: `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`
Task classification: `platform`
Constitution: `1.2.0`
Architecture baseline: RFC-0001 through RFC-0007 `1.0.0` (`Accepted`)
Roadmap block: `0H — Reference implementation readiness`
Review iterations completed: `3 of maximum 7`
Result: `Pass after bounded reconciliation`
Formal approval status: `Not an approval artifact`

## 1. Review method

This review applies the repository's functional role cross-review method to the readiness baseline.

The perspectives are analytical roles used to test the artifact. They do not represent claims that named executives, employees, counsel or external reviewers personally performed the review.

The review asks whether the readiness baseline is sufficient for the current lifecycle stage while remaining compatible with the Constitution, Accepted architecture, delivery value, reversibility and risk.

## 2. Sources checked

The review was performed against the current canonical repository state, including:

- Constitution `1.2.0` — `Ratified`;
- RFC Index;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0002 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`;
- RFC-0004 `1.0.0` — `Accepted`;
- RFC-0005 `1.0.0` — `Accepted`;
- RFC-0006 `1.0.0` — `Accepted`;
- RFC-0007 `1.0.0` — `Accepted`;
- Architecture Glossary;
- Canonical Roadmap `1.1.8` as the pre-change planning baseline;
- RFC State Transition Procedure `1.1.0` — `Approved`;
- Decision Authority Policy `0.2.1` — `Proposed`;
- repository agent rules.

No current Accepted ADR was found in the repository during the readiness preflight. Repository commit search also returned no ADR history.

## 3. Initial proposal reviewed

The initial readiness design proposed:

- a small modular-monolith reference implementation;
- logical modules for Kernel, security/sovereignty, Product Contracts, Governed Execution, Event/Provenance and Memory/Knowledge;
- adapters outside domain-neutral semantic modules;
- in-memory persistence and in-process invocation for the first executable slice;
- a domain-neutral end-to-end fixture exercising canonical versioning, Governed Execution, Event evidence and Observation semantics;
- no database, broker, IAM, API protocol, vector engine or LLM commitment before evidence requires one.

## 4. Review iteration 1 — Architecture and engineering

Perspectives:

- architecture;
- engineering;
- maintainability;
- migration/portability.

### Findings

#### Finding A — Risk of turning logical modules into permanent service boundaries

The first wording could have been read as prescribing future Platform Service topology.

**Correction:** the readiness baseline now states that modules are logical implementation boundaries only and that a future physical split may change deployment topology without changing organizational semantics.

#### Finding B — Readiness could remain too abstract without an executable slice

A list of modules alone would not prove that implementation can begin without inventing architecture in code.

**Correction:** the baseline now defines a concrete domain-neutral first executable scenario and failure cases covering immutable versioning, Governed Execution, Event admission/evidence, authorization/authority separation and Observation non-promotion.

#### Finding C — Premature persistence/API ADRs would create speculative commitments

The Accepted RFCs explicitly leave storage, broker, workflow runtime, API and retrieval technology subordinate and replaceable.

**Correction:** the first slice may use in-memory persistence ports and in-process invocation. Durable persistence or a public protocol becomes an ADR/contract question only when the choice becomes materially constraining.

### Iteration result

`Pass with required bounded corrections`.

## 5. Review iteration 2 — Security, privacy, authority and operations

Perspectives:

- security;
- privacy/data governance;
- tenant sovereignty;
- operations/reliability;
- AI governance.

### Findings

#### Finding D — Simple bootstrap must not collapse RFC-0003 distinctions

A local reference implementation could accidentally treat authentication, authorization and Organizational Authority as one boolean.

**Correction:** the readiness baseline requires distinct interfaces/evidence for authentication context, deny-by-default authorization, Organizational Authority/approval and data-governance handling from the first slice.

#### Finding E — Organization scope must fail closed from the start

Using a convenient default tenant in tests would normalize a non-conforming pattern.

**Correction:** unresolved Organization scope is an explicit first-slice failure case and no default-tenant fallback is permitted.

#### Finding F — Observability and AI adapters could create shadow authority or data leakage

Raw logs, prompts, retrieval indexes or model context must not become canonical state or unrestricted cross-Organization data.

**Correction:** adapter rules now preserve Organization/classification constraints, prohibit reusable secrets in ordinary records/logs/prompts/fixtures, and treat telemetry/retrieval projections as non-authoritative.

#### Finding G — Readiness must not be confused with operational readiness

The current Decision Authority Policy is still `Proposed`, and RFC-0001 requires approved operational-readiness governance before the first `Active` capability.

**Correction:** the baseline now explicitly states that Block 0H creates no `Active` lifecycle state, production-readiness claim, SLA, support commitment or external full-platform conformance claim.

### Iteration result

`Pass with required bounded corrections`.

## 6. Review iteration 3 — Product, governance and commercial integrity

Perspectives:

- product/platform boundary;
- governance;
- organizational value;
- commercial integrity.

### Findings

#### Finding H — User shorthand “RFC-0008 readiness” conflicts with the canonical follow-up sequence

RFC-0001 reserves RFC-0008 for `Document and Artifact Architecture`, while the roadmap defines readiness as Block 0H and directs implementation work toward the minimum subordinate ADRs/structure.

Creating an RFC-0008 for readiness would create a numbering/scope conflict and use a higher governance level than necessary.

**Correction:** the readiness artifact explicitly records that this is Block 0H, not RFC-0008, and preserves the RFC-0008 reservation.

#### Finding I — A Product Contract example could accidentally import procurement/domain semantics

A fabricated domain Product Contract would risk turning readiness work into product-specific architecture.

**Correction:** the baseline defines only the entry condition and minimal Product Contract capability; the first real Product Contract must be driven by an actual product integration.

#### Finding J — “Minimum ADRs” could be misread as requiring ceremonial ADR creation

The roadmap says ADRs are used when concrete choices become necessary and sufficiently constraining. No such technology/public-contract choice is necessary for the in-memory/in-process first slice.

**Correction:** the minimum readiness ADR set is explicitly `zero`; objective ADR triggers are recorded so implementation cannot use that conclusion to hide a later constraining decision.

#### Finding K — Glossary is stale relative to RFC-0003 through RFC-0007

The pre-readiness Architecture Glossary still listed several now-Accepted areas as deferred and described Organization/Tenant semantics as awaiting later RFC work.

This conflicts with Phase 0's language-alignment exit criterion.

**Correction required before Block 0H closure:** synchronize the Architecture Glossary to Accepted RFC-0003 through RFC-0007 and update the roadmap link/version.

### Iteration result

`Pass after bounded reconciliation, subject to glossary and roadmap synchronization in the same work cycle`.

## 7. Final cross-role result

| Perspective | Final result | Material unresolved objection |
|---|---|---|
| Architecture | Pass | none |
| Engineering | Pass | none |
| Security | Pass | none |
| Privacy / sovereignty | Pass | none |
| Operations | Pass for readiness stage | no operational-readiness approval is implied |
| Product | Pass | none |
| Governance | Pass subject to canonical synchronization | none after glossary/roadmap update |
| Commercial integrity | Pass | no lifecycle/conformance overclaim permitted |
| AI governance | Pass | AI remains adapter/execution mechanism, not authority |

No fourth review iteration is justified if the required glossary and roadmap synchronization is completed without introducing new architecture.

## 8. Readiness-stage decisions supported by review

The review supports the following conclusions for Roadmap Block 0H:

1. the reference implementation can start without a new architecture RFC;
2. RFC-0008 remains reserved for Document and Artifact Architecture;
3. no ADR is required before the first bounded in-memory/in-process executable slice;
4. a modular-monolith logical structure is the simplest reversible starting shape;
5. technology/vendor choices remain deferred until they cross an explicit ADR trigger;
6. the first implementation should prove Accepted semantic invariants with executable fixtures before adding infrastructure;
7. product interaction begins through a real minimal Provisional Product Contract, not a fabricated universal product schema;
8. Block 0H completion is not an `Active` capability or production-readiness decision.

## 9. Remaining work required to close Block 0H

Within this same work cycle:

- synchronize `docs/architecture/GLOSSARY.md` to Accepted RFC-0003 through RFC-0007;
- publish this review and the readiness baseline;
- update `docs/roadmap/ROADMAP.md` to record Block 0H completion and the next implementation action;
- refresh the changed files from the default branch and verify consistency.

No owner approval or RFC acceptance transition is being claimed by this review because the work introduces no new fundamental architecture or capability lifecycle promotion.