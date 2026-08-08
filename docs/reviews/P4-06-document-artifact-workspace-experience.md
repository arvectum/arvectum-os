# P4.06 — Document / Artifact workspace experience review

Status: `Complete`
Date: `2026-08-08`
Result: **`PASS`**
Task classification: `platform`
Owner: `ООО «Арвектум»`

## 1. Scope

P4.06 implements the smallest bounded operator-facing experience over the existing CAP-001 Document & Artifact Governance incubation slice, the existing P3.07 cross-capability access enforcement, and Accepted RFC-0008 semantics.

The completed slice provides:

- authorized inspection of one logical Document at Canonical Head or one explicitly selected exact historical Document Version;
- explicit separation of logical Document Identity, immutable Document Version Identity, Artifact Identity, content-integrity reference and replaceable storage locator;
- exact governed Artifact reliance only from an explicitly selected exact admitted Document Version, with current access re-evaluation and delegation to existing CAP-001/P3.07 semantic owners;
- separate working/draft candidate presentation that remains non-canonical while withholding unadmitted candidate Artifact metadata;
- explicit governed Artifact state for admitted renditions and non-promotion of transient/generated candidate Artifacts;
- derivation provenance for transformed Artifact renditions;
- current purpose, required right and allowed-classification enforcement before governed Artifact metadata is shown;
- classification, purpose, rights and retention meaning for each visible governed Artifact;
- omission of restricted Artifact metadata without protected counts;
- storage-locator presence without exposing locator values, content references or bytes;
- an inert HTML presentation plus an executable static demonstration.

P4.06 does **not** define a DMS, object store, content-delivery API, upload/download service, OCR provider, signing provider, document-admission workflow, frontend framework, public route/API/BFF, stable wire/serialization contract, durable workspace read model, new Product Contract, new Platform Capability or capability lifecycle transition.

## 2. Canonical authority checked

The implementation and review were performed against the current canonical repository state:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
- RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- RFC-0002 `Canonical Record Kernel Metamodel` `1.0.0` — `Accepted`;
- RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability` `1.0.0` — `Accepted`;
- RFC-0005 `Governed Execution / Workflow Model` `1.0.0` — `Accepted`;
- RFC-0006 `Event / Provenance / Observability Model` `1.0.0` — `Accepted`;
- RFC-0008 `Document / Artifact Architecture` `1.0.0` — `Accepted`;
- CAP-001 Document & Artifact Governance implementation and Phase 3 executable evidence;
- P3.07 cross-capability Organization / purpose / right / classification enforcement;
- completed P4.01–P4.05 and R9 workspace-boundary evidence;
- current Phase 4 detailed roadmap and canonical roadmap.

No conflict with the Constitution or Accepted RFC baseline was found.

No applicable Accepted ADR constrains this bounded internal implementation. The existing ADR gate remains open for any future durable/external/stable document-storage, frontend, API, content-delivery or provider commitment.

## 3. Implementation

Primary implementation:

- `reference/python/arvectum_os_ref/document_artifact_experience.py`;
- `reference/python/tests/test_p4_06_document_artifact_workspace.py`;
- `reference/python/tests/test_p4_06_demo.py`;
- `reference/python/examples/p4_06_document_artifact_workspace_demo.py`.

### 3.1 Document, Version, Artifact and locator remain distinct

`inspect_document_workspace` consumes the P4.02 scoped workspace state, one explicit Subject or exact-Version navigation reference, current source-access evidence, an explicit P3.07 `AccessRequest`, existing `CanonicalLineage` state and existing CAP-001 admitted manifests.

For a Subject reference the surface resolves the Document Canonical Head. For an exact-Version reference it preserves that exact historical Document Version and never silently redirects to Head.

For governed Artifacts permitted by the current access context, the presentation exposes separate fields for:

- logical Document Subject Identity;
- displayed exact Document Version Identity;
- Canonical Head Version Identity;
- Artifact Identity;
- Artifact integrity reference;
- rendition role and visible designated-rendition status;
- derivation provenance and transformation;
- classification, purpose, rights and retention rule;
- only whether a storage locator exists, not its value.

Neither Artifact hash nor storage locator is used as logical Document or Version identity.

### 3.2 Exact consequential reliance stays with existing semantic owners

A Subject/Head browse is sufficient for inspection but intentionally insufficient for consequential reliance.

`resolve_workspace_exact_reliance` requires that the operator has explicitly selected an exact Document Version and one governed Artifact that was visible under the inspected access context. Before reliance it re-evaluates:

1. current Actor/Organization-bound Document source authorization;
2. current P3.07 `AccessRequest` Actor/Organization binding;
3. Artifact purpose, required right and allowed classification through existing `resolve_document_for_access`;
4. exact Document Version / Artifact structural reliance through existing CAP-001 `resolve_exact_document_reliance`.

P4.06 therefore does not create a second version-resolution, access-policy or Artifact-admission mechanism, and it never follows a later Head when exact reliance is requested.

### 3.3 Working candidates and generated Artifacts remain non-canonical

Working/draft `DocumentVersionCandidate` values are presented separately from the admitted canonical Document Version.

The workspace exposes only bounded candidate-level facts needed to keep canonical state understandable: candidate Version Identity, lifecycle text, that it is non-canonical, whether it contains Artifacts/transient Artifacts, and that promotion is unavailable. Unadmitted candidate Artifact identities, integrity references, handling metadata, content references and storage locators are not exposed by the P4.06 surface.

This is intentional. CAP-001 already has bounded semantic admission logic, but the current operator workspace has no accepted document-admission Governed Execution path that would authorize a consequential promotion action. P4.06 therefore does not call `admit_document_version` from the presentation/action layer or invent a UI-side approval shortcut.

A future admission action, if required, must enter through an applicable Governed Execution path with the appropriate authorization/Organizational Authority/consequential-approval semantics rather than through mere operator visibility.

### 3.4 Derivation provenance and handling constraints

For each governed Artifact that passes the current P3.07 access context, transformed renditions preserve and expose:

- source Artifact Identity references;
- transformation description;
- media/rendition role;
- classification;
- purpose;
- rights;
- retention rule.

Artifact metadata that does not satisfy the current purpose/right/classification context is omitted without exposing its identity, handling values or a protected count. If no governed Artifact is accessible, the surface returns a fail-closed handling-access state instead of exposing the admitted manifest.

The static reference presentation shows permitted governance attributes without exposing content bytes or storage-location details. Retention is presented as governance meaning; the surface has no deletion/retention mutation action.

### 3.5 Authority source honesty

The current bounded `CanonicalRecord` reference harness admits only `Native` authority mode. P4.06 therefore renders the native governed Document source explicitly when Native authority is present.

It does **not** infer an external authoritative system from a vendor name, file path, storage locator, import mechanism or Artifact metadata.

If a future `External Reference` or `Governed Replica` Document reaches this adapter without the governed external-authority metadata required to identify the authoritative source honestly, the adapter fails closed with `UNSUPPORTED_AUTHORITY` rather than fabricating source meaning.

This is a bounded implementation constraint, not a claim that RFC-0008 lacks external-authority support. The Accepted architecture supports external authority; the current reference `CanonicalRecord` harness simply has not implemented that mode yet.

## 4. Security, minimization and authority ordering

For protected Document inspection the bounded order is:

1. explicit workspace Document reference and matching workspace Actor/Organization context;
2. explicit P3.07 `AccessRequest` bound to the same Actor/Organization;
3. current Actor/Organization-bound Document source-access authorization;
4. governed source resolution using source-owned Organization scope;
5. exact requested Version resolution, if any;
6. exact CAP-001 admitted-manifest resolution;
7. per-Artifact P3.07 purpose/right/classification enforcement;
8. non-authoritative presentation of only permitted governed Artifact metadata;
9. for exact reliance, re-evaluation of source authorization and P3.07 Artifact access before CAP-001 exact-reliance resolution.

Missing, denied, duplicate, actor-mismatched or Organization-mismatched source authorization fails closed before protected source/version existence is distinguished. A mismatched `AccessRequest` also fails closed before protected document metadata is rendered.

The renderer intentionally withholds:

- restricted Artifact metadata and protected Artifact counts;
- unadmitted working-candidate Artifact metadata;
- Artifact `content_ref` values;
- content bytes;
- storage-locator values;
- any upload/download/content-retrieval control.

This avoids turning document metadata visibility into implicit content access and prevents storage topology from becoming operator-facing identity or authority.

Presentation authority remains explicitly non-authoritative. Source access or Artifact visibility does not create Organizational Authority, admission authority, signing authority or permission to mutate canonical state.

## 5. Functional cross-review

Per repository engineering policy, P4.06 was reviewed iteratively until no material objection remained. One material security finding was discovered before merge and was resolved rather than being hidden by a premature `PASS`.

### Iteration 1 — architecture / semantic ownership

**Question:** did the workspace create a second DMS, document identity model, admission authority or canonical-state owner?

**Result:** `PASS`.

The surface reuses `CanonicalLineage`, CAP-001 admitted manifests and the CAP-001 exact-reliance resolver. Logical Document, Version, Artifact and storage locator remain distinct. No DMS, object store, content repository, document-admission workflow or duplicate canonical state is introduced.

### Iteration 2 — security / handling enforcement

**Question:** was current Document source authorization sufficient to expose governed Artifact metadata and permit exact Artifact reliance?

**Result:** `FINDING — remediation required`.

The first implementation correctly checked current Actor/Organization-bound source authorization before protected source/version resolution and hid content references/storage-locator values, but it did not independently reuse the existing P3.07 purpose/right/classification enforcement before rendering admitted Artifact metadata or resolving exact reliance.

That was insufficient because Document visibility must not silently broaden Artifact handling rights.

**Remediation:** P4.06 now requires an explicit P3.07 `AccessRequest`, applies existing `resolve_document_for_access` independently to each governed Artifact, omits restricted Artifact metadata without counts, hides unadmitted candidate Artifact metadata, and rechecks both current source authorization and P3.07 handling constraints before exact reliance.

### Iteration 3 — security re-review / minimization / cross-Organization disclosure

**Question:** after remediation, can document/version existence, restricted Artifact metadata, storage details or content references leak outside the current governed context?

**Result:** `PASS`.

Current source authorization is Actor-bound and Organization-bound and is evaluated before protected source/version resolution. The access request must match the workspace Actor/Organization. The governed source's Organization scope is checked independently of identifier syntax. Each Artifact must independently satisfy purpose/right/classification constraints; denied Artifacts are omitted without metadata/count. Locator values, content references and bytes are not rendered. Exact reliance repeats the current source and Artifact-access checks.

### Iteration 4 — operator UX / authority / provenance honesty

**Question:** can an operator distinguish the object/version/rendition being viewed, understand permitted provenance and handling constraints, and avoid mistaking a draft/generated Artifact for canonical state?

**Result:** `PASS`.

The renderer names Document Subject, displayed Version, Canonical Head, reference basis, canonical state, authority mode/source, current access purpose/right/classification, permitted Artifact state/rendition/integrity, derivation chain and handling constraints. Working candidates are labeled non-canonical, expose no unadmitted Artifact metadata and have no promotion action. Exact historical Version selection remains explicit.

### Iteration 5 — engineering / regression / ADR boundary

**Question:** did implementation or demo stabilize an infrastructure/public boundary or regress the existing reference runtime after security remediation?

**Result:** `PASS`.

The module remains internal and unexported from the package root. It selects no server/frontend/network/database/object-storage/OCR/signing dependency and creates no public route or wire contract. The static demo starts no server.

An early demo smoke execution exposed only a subprocess import-path issue (`ModuleNotFoundError` for the sibling reference package); the smoke environment was corrected without changing P4.06 semantics. A later cross-review then found the P3.07 handling-enforcement gap described above; that gap was remediated and covered by additional negative-path tests. The complete reference suite passed after the remediation.

No sixth review iteration was necessary because the fifth iteration produced no material finding.

## 6. Executable evidence

Completion semantic evidence after the security remediation:

- GitHub Actions `Reference Python CI #154` — `PASS`;
- Python `3.12.13`;
- `495` tests;
- `OK`.

Earlier `Reference Python CI #147` passed `490` tests before the final P3.07 handling-enforcement review hardening. It is retained as intermediate evidence, not the final semantic completion claim.

The P4.06 additions include explicit negative-path coverage for:

- unauthorized and cross-Organization Document access;
- Actor/Organization-mismatched Artifact access context;
- duplicate authorization evidence;
- hidden exact-Version existence before source authorization;
- purpose mismatch, required-right mismatch and classification mismatch;
- restricted Artifact omission without metadata/count leakage;
- exact reliance rechecking current source authorization and Artifact handling context;
- absent/ambiguous admitted manifests;
- Head-versus-exact reliance;
- non-Document sources;
- transient candidate non-promotion and unadmitted candidate Artifact metadata minimization;
- locator/content minimization;
- framework/infrastructure non-selection.

A later CI run caused only by final review/roadmap/README synchronization is completion-integrity evidence and adds no new P4.06 semantic requirement.

## 7. ADR / Product Contract / capability disposition

**New RFC required:** no.

**New ADR required:** no.

P4.06 does not materially select or rely on a durable or externally constraining implementation choice. Re-open the ADR gate before selecting a document/object-storage topology, DMS, OCR/signing provider, content-delivery mechanism, stable frontend/runtime boundary, public route/API/BFF or wire schema, durable workspace/read-model cache, stable cross-product package, or separately deployable UI/API topology.

**New Product Contract required for P4.06 itself:** no. This is an internal platform workspace/reference implementation. The Phase 4 bounded Product Contract-backed product entry proof remains P4.08.

**Platform Capability lifecycle change:** none. CAP-001 remains `Incubating / Provisional`; P4.06 uses it but does not promote it to `Active`. CAP-002 through CAP-004 remain unchanged. P4.06 creates no additional Platform Capability.

**Operational/conformance claim:** none. A green bounded reference slice is not a production-readiness, SLA, full-platform conformance or commercial-support claim.

## 8. Exit assessment

P4.06 exit expectations are satisfied for the bounded reference scope:

- logical Document identity remains separate from rendition/file/storage identity;
- exact Document Version and permitted material Artifact Identity are visible when relied upon;
- Subject/Head browsing cannot silently substitute for exact consequential reliance;
- exact historical Document Versions remain inspectable;
- working/draft candidates remain visibly non-canonical;
- unadmitted candidate Artifact metadata remains minimized;
- transient/generated Artifacts are not silently promoted;
- authority mode/source meaning is shown where the current harness can support it, and unsupported external-source metadata fails closed rather than being guessed;
- derivation provenance is visible for permitted transformed Artifact renditions;
- classification/purpose/rights/retention meaning is preserved for permitted Artifacts;
- current purpose/right/classification is enforced before Artifact metadata presentation and exact reliance;
- restricted Artifact metadata is omitted without protected counts;
- storage-locator values and content references/bytes are minimized from this surface;
- source authorization precedes protected source/version resolution;
- exact reliance rechecks current source and handling access instead of trusting stale presentation state;
- presentation remains internal and non-authoritative;
- no DMS/object-store/OCR/signing/public API/durable read-model boundary is selected;
- executable negative-path evidence is green.

**Final P4.06 decision: `PASS`.**

## 9. Carried boundaries

The following remain intentionally outside P4.06 rather than hidden gaps:

1. P4.07 owns Memory / Knowledge / Search discovery experience.
2. P4.08 owns the bounded Product Contract-backed product entry composition proof.
3. P4.09 must revalidate cross-surface rights, minimization, hidden-action safety and authority-safe UX before M4 closure.
4. A document-admission/promotion operator action remains absent until an applicable Governed Execution path owns that consequential mutation.
5. External-authority rendering beyond Native mode requires governed source metadata from an implementation that actually supports the RFC-0008 authority mode; it must not be inferred from storage or import metadata.
6. Stable frontend/API/content-delivery/DMS/object-storage/OCR/signing choices remain behind the existing ADR gate.

## 10. Next canonical action

Proceed to **`P4.07 — Memory / Knowledge / Search discovery experience`**.
