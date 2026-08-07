# Decision: RFC-0008 Acceptance

Status: `Approved`
Date: `2026-08-07`
Owner: `ООО «Арвектум»`
Category: `governance`
Decision subject: `RFC-0008 — Document and Artifact Architecture`
Approved proposal: `RFC-0008 v0.2.0 Proposed`
Approved proposal path: `docs/rfc/RFC-0008-document-artifact-architecture.md`
Approved proposal blob SHA: `0de6a1dead4e06605d72d0781505bb44598d752a`
Cross-review: `docs/reviews/RFC-0008-functional-cross-review.md`

## Decision

The Owner explicitly approves RFC-0008 `0.2.0` — `Document and Artifact Architecture` for acceptance as the binding Arvectum OS architecture within its declared scope.

The approval applies to the reviewed proposal identified by immutable blob SHA:

`0de6a1dead4e06605d72d0781505bb44598d752a`

The functional cross-review is complete after 4 of maximum 7 iterations with result `Pass after bounded reconciliation`.

## Approved normative decisions

The Owner approves the acceptance criteria stated in RFC-0008 `0.2.0`, including that:

1. Document and Artifact remain semantic roles above the existing five Kernel primitives;
2. significant Documents use stable Subject Identity and immutable Canonical Record versions;
3. mutable Working Copies may exist outside canonical history but cannot be consequentially relied upon as admitted immutable versions;
4. every significant Document Version resolves to governed content or an explicit authoritative content reference;
5. Document, Document Version, Artifact/content identity and storage locator remain distinct;
6. hashes do not establish semantic identity, authority, approval or truth;
7. one Document Version may have multiple governed renditions under explicit equivalence semantics;
8. material semantic change creates a new immutable Document Version;
9. external document systems preserve Accepted authority modes and do not become competing local authority;
10. receipt/generation and canonical admission remain distinct;
11. generated Artifacts are transient by default and promotion is explicit;
12. transformations preserve source provenance and applicable data-governance/rights constraints;
13. successful redaction does not itself create declassification or disclosure authority;
14. signature evidence is distinct from Organizational Authority and approval;
15. consequential reliance pins exact Document Version and exact Artifact/content where representation matters;
16. packages/exports expose material completeness and availability/omission state;
17. Product Contract artifact surfaces are explicit and storage internals are not hidden contracts;
18. portability uses documented manifests plus lawful content or explicit external/non-exportable references;
19. deletion may remove payload while preserving permitted historical/tombstone semantics without rewriting history;
20. search/OCR/extraction/index/AI projections remain non-authoritative by default;
21. product-domain document semantics remain product-owned by default;
22. implementation technology remains replaceable and proportional;
23. scoped conformance uses the normative fitness tests in RFC-0008;
24. acceptance does not make any document repository, generation, signing, OCR, export or artifact-management capability `Active` and does not establish production, operational, SLA, support or commercial commitments.

## Authority and boundaries

This decision does not amend Constitution `1.2.0` and does not supersede RFC-0001 through RFC-0007.

RFC-0008 remains subordinate to the Constitution and earlier Accepted RFCs according to canonical authority order.

This approval does not:

- select a DMS, object store, database, file format, OCR engine, signing provider, search engine, workflow engine or service topology;
- approve product-specific document taxonomies, templates, workflows or business rules;
- determine legal validity of signatures, evidentiary admissibility, copyright, records-management compliance or contractual rights;
- make any Platform Capability `Active`;
- establish operational readiness, production conformance, SLA or support commitments.

## Required publication closure

Under the Approved RFC State Transition Procedure, this approval must be followed in the same working cycle by:

1. publication of RFC-0008 as `Accepted 1.0.0`;
2. RFC Index synchronization;
3. canonical roadmap synchronization;
4. Architecture Glossary synchronization to Accepted RFC-0008 semantics;
5. repository navigation/README synchronization where stale;
6. read-after-write verification of the accepted RFC, approval evidence, RFC Index and roadmap.

Until those steps are complete, this approval record alone must not be represented as a completed RFC state transition.