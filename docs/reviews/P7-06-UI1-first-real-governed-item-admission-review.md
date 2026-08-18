# P7.06-UI1 First Real Governed Item Admission — Functional Cross-Review

Status: `Complete / PASS for repository implementation; selected-Mac execution pending`
Date: `2026-08-18`
Task classification: `platform` with `product_contract` and `governance`
Review iterations: `3 / max 7`

## 1. Scope

This review covers the repository-side one-purpose admission/persistence bridge authorized by:

`DECISION-2026-08-18-P7-06-UI1-FIRST-REAL-GOVERNED-ITEM-ADMISSION.md`.

It does not itself create the selected-Mac real governed item and does not close UI1.

## 2. Authority review

Checked against:

- Constitution `1.2.0`;
- Accepted RFC-0001 through RFC-0008;
- P6.02 Product Contract `Provisional 0.1.0`;
- P6.05-L4/L5/L7/L8 evidence and integration seams;
- P7.03 persistence boundary;
- P7.04 least-privilege access boundary;
- P7.06 exact-release deployment boundary;
- P7.06-UI1 read-only workspace exit evidence;
- canonical roadmap sequencing.

No new ADR is required because the bridge is bounded, private, reversible and one-purpose. It creates no stable/public API, persistence topology or cross-product architectural commitment.

No Product Contract change is required: P6.02 already declares CAP-001 exact external Document/Artifact admission, CAP-004 reconstruction, External Reference authority and governed canonical mutation through four distinct RFC-0005 gates. The bridge remains inside that declared envelope.

## 3. Functional review iteration 1

Result: `REVISE`.

The first implementation established the required substantive boundaries:

- exact active P7.06 release only;
- approved owner-decision presence;
- existing P6.05-L4 Organization/human continuity;
- exact P7.04 human local authorization before admission;
- P7.04 access remains separate from Organizational Authority and consequential approval;
- exact P6.02 `0.1.0` Product Contract continuity;
- independent canonical-body rehash of the retained real P6.05-L7 manifest;
- no EIS/SOAP/network refetch;
- four distinct RFC-0005 gate decisions;
- CAP-001 exact Document Version admission preserving `External Reference`;
- RFC-0006 Event/provenance admission;
- CAP-004 reconstruction before P7.03 persistence;
- minimized governed representation with no raw tender bytes/reusable secrets/external effects;
- exact Subject/Version conflict detection and idempotent retry.

Initial GitHub `Reference Python CI` run `32143213623` found one failing static source-safety assertion. The test rejected the plain text token `getDocsIP`, but the implementation used that token only inside provenance/source-version explanatory text and did not import or invoke an EIS client.

Revision: the static check was narrowed from plain terminology to invocation/import forms such as `getDocsIP(`, socket/requests/urllib/subprocess and external-effect call forms. The safety boundary was not weakened: descriptive provenance terminology remains allowed while executable network/effect adapters remain forbidden by the test.

After revision, GitHub `Reference Python CI` run `32143445055` completed with `success`.

## 4. Functional review iteration 2

Result: `REVISE / harden semantic retry and gate ordering`.

Two repository-side honesty/safety concerns remained even after green CI:

1. the implementation's idempotent path accepted an existing exact Subject/Version after verifying source-manifest digest and authority mode, then reported reconstruction completeness; a separately written but semantically incomplete retained item could therefore match those minimal keys;
2. the hardened selected-Mac wrapper initially performed exact-release/access preflight before checking the owner assertion, making the wrapper's ordering weaker than the underlying admission function even though no mutation could occur.

Revision:

- added the required selected-Mac hardened entrypoint `p7_06_ui1_real_state_admission_entrypoint.py`;
- before idempotent retry it now fail-closes unless the exact retained item also matches semantic/schema identity, External Reference authority scope/source, exact manifest digest, Product Contract `0.1.0`, complete CAP-001/RFC-0006/CAP-004 validation status, governed admission reference, bounded provenance, exact source-release attribution and minimization/no-secret/no-effect flags;
- duplicate exact Subject/Version claims fail closed;
- the entrypoint now checks the exact owner approval assertion before exact-release/access preflight;
- regression tests cover the semantic retry guard and owner-gate ordering.

This preserves the bounded implementation while removing any need to infer reconstruction completeness from a weak metadata match.

## 5. Functional review iteration 3

Result: `PASS — no material repository-side objections remain`.

The post-hardening CI run `32144247462` exposed three errors in newly added test fixtures rather than in the admission implementation. Those fixtures attempted to create P7.03 canonical governed state with conditions that P7.03 already refuses at its own lower-level boundary: `canonical_authority=false`, reusable-secret presence, empty governed-admission reference or invalid exact release attribution.

That result confirmed layered defense rather than an admission bypass. P7.03 already requires canonical governed state to carry valid Subject/Version/authority/admission/provenance metadata, `canonical_authority=true`, valid release attribution and `contains_reusable_secret=false`.

Revision:

- tests now assert P7.03 `BoundaryError` for conditions owned by the P7.03 persistence boundary;
- hardened-entrypoint tests remain focused on semantically incomplete state that P7.03 may legitimately retain but that this exact UI1 admission retry must reject, including incomplete CAP-001/RFC-0006/CAP-004 validation, source/Product Contract/schema drift, raw-document/external-effect drift, bounded-but-insufficient provenance and duplicate exact Subject/Version claims.

Final implementation/test branch head `ac5c340bf7e08d18d816b49feaf710d9a3207e22` passed GitHub `Reference Python CI` run `32144411176` with conclusion `success`.

No material objection remains to the repository-side bridge within its declared private, one-purpose scope.

## 6. Repository disposition

Repository implementation = `Complete / PASS`.

The bridge preserves:

- exact active-release execution;
- explicit bounded owner approval;
- existing human/Organization continuity;
- P7.04 least-privilege technical authorization without authority collapse;
- four distinct RFC-0005 gate decisions and bases;
- exact P6.02 Product Contract `0.1.0` boundary;
- independently verified retained real P6.05-L7 evidence;
- EIS `External Reference` authority;
- CAP-001 admission before P7.03 persistence;
- RFC-0006 Event/provenance and CAP-004 reconstruction;
- minimization, idempotency and fail-closed conflict semantics;
- no EIS/SOAP/network/product/external effect.

## 7. Selected-Mac execution boundary

The repository review does **not** authorize shortcuts around the approved execution path. The selected Mac must:

- deploy the exact merged release through P7.06;
- use the existing P6.05-L4 owner context;
- establish only the exact P7.04 admission grant;
- reuse and verify the existing retained L7 manifest without EIS refetch;
- invoke the hardened exact-release entrypoint with the exact owner assertion;
- prove first-run admission/persistence and second-run idempotency;
- then complete only the remaining UI1 real-item browser inspection and zero-mutation evidence.

No raw opaque owner identity, credential/grant identifiers, credential secret, raw tender bytes or owner-local evidence payload belongs in canonical repository evidence.

## 8. Final non-claims

This repository PASS does not:

- close `P7.06-UI1`;
- start `P7.06-UI2`;
- execute the approved consequential canonical admission on the selected Mac;
- promote any capability lifecycle;
- promote the Product Contract lifecycle;
- establish Production readiness;
- create public/stable UI/API/SDK or SLA/support commitments;
- make Arvectum OS the authoritative source for the externally sourced EIS tender material.
