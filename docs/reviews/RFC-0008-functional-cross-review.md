# RFC-0008 Functional Cross-Review

Status: `Complete`
Created: `2026-08-07`
Updated: `2026-08-07`
Subject: `RFC-0008 — Document and Artifact Architecture`
Reviewed version: `0.1.0 Draft`
Maximum review iterations: `7`
Iterations completed: `4`
Result: `Pass after bounded reconciliation`
Formal approval status: `Not an approval artifact`

## 1. Review Method

This review evaluates RFC-0008 from functional analytical perspectives. The perspectives are used to expose architectural, operational, security, privacy, product, legal/rights, engineering and AI-governance failure modes.

They are not claims that named human executives, lawyers, security officers or external reviewers personally reviewed the RFC.

The review baseline is:

- Constitution `1.2.0` — Ratified;
- RFC-0001 through RFC-0007 `1.0.0` — Accepted;
- RFC State Transition Procedure `1.1.0` — Approved;
- Architecture Glossary `1.2.0` — informative navigation baseline;
- Roadmap `1.1.11` — canonical planning source at review start.

The review stops once material objections are reconciled and further iterations would mostly restate already resolved concerns.

## 2. Iteration 1 — Architecture / Kernel / Information Model

### Perspective

CTO / platform architecture / information architecture.

### Material questions

1. Does RFC-0008 accidentally create a sixth Kernel primitive?
2. Does it preserve RFC-0002 identity/version semantics?
3. Does it distinguish a logical document from bytes, location and vendor identifiers?
4. Can it represent multiple renditions without corrupting canonical version semantics?
5. Does it accidentally require a particular DMS, object store or content-addressing model?
6. Can working drafts exist without forcing every keystroke into canonical history?

### Findings

The core model passes the Kernel and technology-independence tests:

- Document and Artifact are semantic roles above Canonical Record/Identity;
- significant Document Versions use RFC-0002 immutable version semantics;
- hashes and locators are correctly prevented from becoming organizational identity or authority;
- multiple renditions are allowed only under declared equivalence semantics;
- external authority modes remain intact;
- no physical storage technology is selected.

Three bounded issues were found.

#### A1. Mutable working-copy state is not explicit enough

The draft correctly says admitted Document Versions are immutable but does not explicitly explain collaborative editing or mutable working copies before admission.

Without clarification, an implementation might either mutate an admitted canonical version or over-engineer every edit into a Canonical Record.

**Required reconciliation:** add a section defining `Working Copy / Draft Candidate` as mutable non-canonical or lighter-governed state by default, with explicit admission/checkpoint rules. A working copy that becomes significant or consequential must be checkpointed/admitted proportionately rather than silently relied upon.

#### A2. Every significant Document Version must resolve to content

The Content Manifest is only `SHOULD`, which could leave a canonical Document Version with no durable content or external retrieval contract.

**Required reconciliation:** state that every significant Document Version MUST resolve to governed content through one or more of: inline payload, immutable content reference, external authoritative reference, or governed replica. A manifest/equivalent is mandatory when multiple materially relevant representations exist or package/rendition relationships require it.

#### A3. `Canonical rendition` terminology risks collision

The phrase could be misread as an additional canonical authority concept.

**Required reconciliation:** rename it to `Designated Rendition Role` and state explicitly that designation never alters Canonical Record or authority semantics.

### Iteration result

`Pass with three bounded corrections`.

## 3. Iteration 2 — Security / Privacy / Rights / Sovereignty

### Perspective

CISO, privacy, data governance, legal/rights architecture.

### Material questions

1. Can derived previews, OCR, embeddings, redactions or AI transformations leak protected content?
2. Does a signature accidentally grant authority?
3. Does immutable history force unlawful indefinite retention?
4. Are external processors and repositories handled without inventing rights?
5. Can redaction or deletion be represented without falsifying history?
6. Are legal ownership and architectural responsibility kept distinct?

### Findings

The draft is well aligned with RFC-0003:

- Organization scope and deny-by-default access propagate to artifacts and derivatives;
- derived data inherits classification/purpose/retention unless a governed transformation permits otherwise;
- external processing is treated as disclosure/processing subject to rights and contract;
- lawful payload deletion may preserve permitted tombstone/lineage metadata;
- signature evidence is explicitly separated from Organizational Authority;
- no legal-signature or evidentiary-admissibility claim is made.

Two bounded improvements are required.

#### S1. Rights metadata should be explicit in the core governed envelope

The draft mentions rights repeatedly but the minimum Document Version content/governance model should explicitly include rights/permitted-use references where relevant.

**Required reconciliation:** add rights/permitted-use constraints to the minimum content/governance resolution for significant Documents where applicable.

#### S2. Redaction must not imply declassification automatically

The draft says a validated redaction can permit broader disclosure, but the architectural distinction between transformed content and classification decision should be sharper.

**Required reconciliation:** state that successful technical redaction does not itself change classification, purpose or disclosure authorization; a governed rule/decision must establish the permitted handling of the redacted derivative.

### Iteration result

`Pass with two bounded corrections`.

## 4. Iteration 3 — Product / Operations / Engineering / Portability

### Perspective

Product, COO/operations, engineering, integration and migration.

### Material questions

1. Can products use the architecture without importing platform ceremony into every local file?
2. Does the model support external DMS/ERP repositories cleanly?
3. Can upload/generation/signing retries avoid duplicate organizational side effects?
4. Is portability useful rather than a raw blob dump?
5. Are package/attachment semantics reconstructable?
6. Does this RFC pre-select repository/service topology?

### Findings

The draft passes the product/platform and implementation-proportionality tests:

- low-risk product-local files may remain local/transient;
- Product Contracts declare only actual boundary semantics;
- private buckets, blob paths and DMS tables cannot become hidden contracts;
- external authority and stale-cache behavior are explicit;
- package manifests pin material members;
- idempotency follows RFC-0005 rather than inventing a document-specific transaction model;
- export preserves semantic identity, manifests and explicit omissions;
- migration may preserve identity across repository/provider replacement;
- no separate document microservice or DMS is mandated.

Two refinements improve implementability.

#### P1. Distinguish content absence from content unavailability

Deletion, external unavailability, failed retrieval and intentionally non-exportable content have different meanings.

**Required reconciliation:** define representation availability states or equivalent semantics sufficient to distinguish at least `available`, `deleted`, `externally unavailable`, and `not exported/not permitted`, without mandating one status enum in storage.

#### P2. Package completeness should be explicit

A package with missing material members must not appear complete.

**Required reconciliation:** require a package/export manifest to expose completeness state and reasons for unavailable/omitted members where material.

### Iteration result

`Pass with two bounded corrections`.

## 5. Iteration 4 — AI / Evidence / Knowledge Boundary / Commercial Integrity

### Perspective

AI governance, evidence/reconstruction, knowledge governance and commercial integrity.

### Material questions

1. Can AI-generated documents become official silently?
2. Can OCR/extraction or a summary become Knowledge or document authority?
3. Is provenance sufficient without demanding chain-of-thought retention?
4. Can a signed/generated/exported artifact be marketed as a supported platform capability merely because the RFC exists?
5. Does the architecture overclaim reproducibility after lawful deletion or external dependency loss?

### Findings

The draft is aligned with RFC-0005 through RFC-0007:

- AI generation is transient by default;
- promotion to canonical state is explicit through Governed Execution when consequential;
- AI does not become approval authority;
- OCR/extraction/indexes/summaries remain projections or derivatives, not authority;
- provenance may reference model/config/template/source versions while explicitly excluding chain-of-thought and secrets;
- exact Document Version plus exact Artifact/content is pinned where representation matters;
- lawful deletion may reduce reconstructability and the system must not overstate what remains.

One clarification is required.

#### AIG1. RFC acceptance must not imply an Active document capability

The draft says this in acceptance criteria, but the Decision section should repeat the boundary prominently.

**Required reconciliation:** the reviewed proposal must state that even if RFC-0008 is later Accepted, it defines architecture only; no document repository, generation, signing, OCR, export or artifact-management capability becomes `Active` without lifecycle and operational-readiness evidence.

### Iteration result

`Pass with one bounded correction`.

## 6. Reconciliation Summary

The reviewed proposal should incorporate all eight corrections:

1. add explicit mutable Working Copy / Draft Candidate semantics;
2. require every significant Document Version to resolve to governed content/reference;
3. rename `Canonical Rendition` to `Designated Rendition Role`;
4. add explicit rights/permitted-use references where applicable;
5. separate redaction validation from classification/disclosure authorization;
6. distinguish content availability/deletion/external-unavailability/non-exportability states;
7. expose package/export completeness and omission reasons;
8. repeat that RFC acceptance does not activate any document/artifact capability.

None of these corrections changes the fundamental model. They tighten interoperability and prevent predictable accidental architecture.

## 7. Final Cross-Review Result

After the bounded reconciliation above, the analytical perspectives reach:

- Constitution alignment: `Pass`;
- RFC-0001 architectural-law alignment: `Pass`;
- RFC-0002 Kernel/metamodel alignment: `Pass`;
- RFC-0003 security/privacy/sovereignty alignment: `Pass`;
- RFC-0004 Product Contract alignment: `Pass`;
- RFC-0005 Governed Execution alignment: `Pass`;
- RFC-0006 Event/provenance alignment: `Pass`;
- RFC-0007 Memory/Knowledge alignment: `Pass`;
- product/platform boundary: `Pass`;
- technology independence and portability: `Pass`;
- AI authority boundary: `Pass`;
- commercial/lifecycle integrity: `Pass`.

Final result: **`Pass after bounded reconciliation`**.

The RFC may advance from `Draft 0.1.0` to a reviewed `Proposed 0.2.0` after the listed corrections are incorporated and the resulting files are re-fetched from the canonical default branch.

This review is not owner approval and cannot make RFC-0008 `Accepted`.
