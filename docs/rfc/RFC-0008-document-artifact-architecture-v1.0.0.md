# RFC-0008: Document and Artifact Architecture

Status: `Accepted`
Version: `1.0.0`
Accepted: `2026-08-07`
Published: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`; `RFC-0005 v1.0.0`; `RFC-0006 v1.0.0`; `RFC-0007 v1.0.0`
Supersedes: `RFC-0008 v0.2.0 reviewed proposal`
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Owner approval: `DECISION-2026-08-07-RFC-0008-ACCEPTANCE`
Cross-review: `docs/reviews/RFC-0008-functional-cross-review.md`

## 1. Acceptance Publication

This document is the canonical Accepted publication of RFC-0008 `1.0.0`.

The owner-approved normative substance is the reviewed RFC-0008 `0.2.0` proposal preserved in repository history and identified by canonical proposal blob SHA:

`0de6a1dead4e06605d72d0781505bb44598d752a`

Historical proposal path:

`docs/rfc/RFC-0008-document-artifact-architecture.md`

RFC-0008 `0.2.0` is incorporated into this Accepted publication in full by immutable content reference. No normative substance of the owner-approved proposal is changed by this acceptance publication.

## 2. Accepted Architecture Baseline

RFC-0008 `1.0.0` refines, without changing, the architectural laws and contracts of:

- Constitution `1.2.0`;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0002 `1.0.0` — Accepted;
- RFC-0003 `1.0.0` — Accepted;
- RFC-0004 `1.0.0` — Accepted;
- RFC-0005 `1.0.0` — Accepted;
- RFC-0006 `1.0.0` — Accepted;
- RFC-0007 `1.0.0` — Accepted.

Where this RFC conflicts with a higher-authority source, the higher-authority source prevails.

## 3. Accepted Model

RFC-0008 `1.0.0` establishes binding domain-neutral Document and Artifact architecture, including:

1. Document and Artifact as semantic roles above the existing five Kernel primitives rather than new Kernel primitives;
2. logical Document identity separated from files, bytes, storage locators and vendor identifiers;
3. stable Document Subject Identity and immutable Document Version Identity for significant Documents;
4. mutable Working Copies/Draft Candidates outside canonical history with immutable governed checkpoint/admission before consequential reliance;
5. mandatory governed content resolution for significant Document Versions through payload, immutable reference, `External Reference` or `Governed Replica` semantics;
6. explicit Content Manifest/equivalent semantics when multiple materially relevant representations, attachments or package relationships exist;
7. distinct Document, Document Version, Artifact/content identity, storage locator and external authority identity semantics;
8. limited hash semantics: byte/content integrity does not create organizational identity, authority, approval, provenance, legal validity or truth;
9. multiple renditions under explicit equivalence and Designated Rendition Role semantics without creating competing canonical authority;
10. preservation of RFC authority modes for Native, External Reference and Governed Replica document subjects;
11. separation of receipt/generation from canonical admission;
12. generated Artifacts as Transient Outputs by default with explicit governed promotion into canonical Document state or Governed Organizational Asset status;
13. derivation provenance for conversion, OCR, extraction, summarization, translation, redaction, rendering, signing, packaging and normalization where material;
14. propagation of Organization, classification, purpose, rights, retention and deletion constraints to derived artifacts unless a governed transformation establishes a permitted different rule;
15. technical redaction separated from declassification, disclosure authorization and Organizational Authority;
16. signature/seal evidence separated from authorization, Organizational Authority and governed approval state;
17. exact Document Version and exact Artifact/content pinning where materially relied upon in consequential execution;
18. explicit version-aware attachment/package membership, purpose-scoped completeness and material omission/unavailability semantics;
19. search, OCR, extraction, embeddings, previews, summaries and indexes as non-authoritative projections by default;
20. explicit Product Contract artifact surfaces without hidden storage/DMS implementation coupling;
21. manifest-based governed export preserving identities, versions, authority, lawful content/references, provenance, relationships, handling constraints and explicit omissions;
22. semantic portability and migration across repositories/storage technologies without changing organizational identity merely because physical locators change;
23. bounded AI participation without independent authority, silent promotion, declassification, retention expansion or cross-Organization scope expansion;
24. technology independence and proportional implementation, including permission to use simple reversible storage and modular-monolith structures;
25. scoped conformance through the normative fitness tests incorporated from the approved proposal.

## 4. Product, Security, Execution, Event and Knowledge Boundaries

Accepted RFC-0003 remains authoritative for identity/security/privacy/Organization sovereignty, authorization, Organizational Authority, classification, purpose, rights, retention/deletion and portability constraints.

Accepted RFC-0004 remains authoritative for Product Contract boundaries. Product-specific document types, templates, taxonomies, approval rules and business workflows remain product-owned by default unless separately promoted through Accepted platform-admission rules.

Accepted RFC-0005 remains authoritative for Governed Execution. Consequential document/artifact mutation, promotion and reliance must preserve the materially relied-upon exact versions and normal authorization/authority/approval gates.

Accepted RFC-0006 remains authoritative for Event, provenance and observability semantics. Storage notifications, parser logs, conversion traces and DMS telemetry do not automatically become canonical Events.

Accepted RFC-0007 remains authoritative for Memory, Knowledge and Governed Learning. Documents, generated artifacts, OCR, summaries and AI-derived representations do not automatically become validated Knowledge.

## 5. Capability and Commercial Boundary

Acceptance of RFC-0008 defines architecture only.

It does **not** by itself:

- create or promote a document/artifact Platform Capability to `Active`;
- establish production or operational readiness;
- select a DMS, object store, database, file format, OCR engine, signing provider, search/index technology, workflow engine or service topology;
- create an SLA, support commitment, archival guarantee, compatibility promise or other customer-facing commercial obligation;
- approve product-specific document taxonomies, templates, workflows or legal-signature rules;
- determine legal validity, enforceability, evidentiary admissibility, copyright, records-management compliance or contractual rights.

Any capability lifecycle promotion remains subject to RFC-0001 lifecycle and operational-readiness requirements and applicable later decisions.

## 6. Review and Approval Evidence

Functional cross-review:

- `docs/reviews/RFC-0008-functional-cross-review.md` — `Complete`;
- iterations completed: 4 of maximum 7;
- result: `Pass after bounded reconciliation`.

Approved reviewed proposal:

- RFC-0008 `0.2.0`;
- immutable proposal blob SHA `0de6a1dead4e06605d72d0781505bb44598d752a`.

Owner approval:

- `docs/governance/decisions/DECISION-2026-08-07-RFC-0008-ACCEPTANCE.md` — `Approved`;
- approval record was canonically created before this acceptance publication.

## 7. Acceptance Result

RFC-0008 `1.0.0` is binding architecture within its declared Document and Artifact scope from this publication onward.

The full normative proposal remains the incorporated RFC-0008 `0.2.0` content identified by the immutable blob SHA above.

This acceptance completes the RFC-0008 architecture transition but does not supersede the independently ready reference-implementation delivery track defined by Roadmap Block 0H.