# P6.05-L8 — Cross-role reconstruction Version Identity compatibility repair

* Status: `Implemented / Awaiting independent review`
* Date: `2026-08-16`
* Owner: `ООО «Арвектум»`
* Task classification: `platform` with `product_contract` and `product_specific`
* Operational Environment: `Internal / local owner-operated validation`
* Production-readiness claim: `None`
* Baseline platform SHA: `63d380a4be222a0670f18e5735b74dd6f9b2349b`

## 1. Discovery

During the P6.05-L8-C1 synthetic preflight for governed evidence admission, a platform implementation gap was identified. The P6.05 admission contour is identity-preserving: the exact tender Document Version used as the Governed Execution material input is the same version admitted by CAP-001. When building a `ReconstructionManifest` for this admission, the same exact `GovernedVersionPin` legitimately appears in both `material_inputs` and `results`.

Previous CAP-004 and cross-capability access logic incorrectly assumed that each evidence Version Identity must map to exactly one semantic role.

## 2. Root cause

- **CAP-001 identity-preserving admission**: `admit_document_version()` returns the same `CanonicalRecord` (and thus the same Version Identity) as the input candidate.
- **Cross-role overlap**: P6.05 reconstruction requires the Document Version to be present as both a material input (the candidate) and a result (the admitted version).
- **Global uniqueness assumption**: `AuditReconstructionView` and `reconstruct_audit_for_access()` enforced global uniqueness of Version Identities across all roles, causing a `ValueError` or `CrossCapabilityEnforcementError` when overlap occurred.

## 3. Architecture disposition

**BOUNDED_REFERENCE_IMPLEMENTATION_GAP**. This was a mismatch between the reference platform implementation and the already-accepted RFC-0008/RFC-0005 semantics. No Constitution, RFC, Product Contract or capability-contract change was required. No new Document Version was minted to work around the technical limitation.

## 4. Repair semantics

- **Role multiplicity allowed**: One exact governed Version Identity may now appear in multiple semantic roles in one `ReconstructionManifest` (e.g., as both material-input and result).
- **Conflict preservation**: Conflicting pins under the same Version Identity (e.g., same version ID but different `semantic_type` or `subject_id`) continue to fail closed with a precise conflict message.
- **Single access state**: Evidence constraints and dispositions remain unique per Version Identity. One access context or redaction decision applies consistently to every role occurrence of that version.
- **Derived view preservation**: The role-bearing derived view is preserved, allowing the reconstruction to show exactly how one version participated in the execution.

## 5. Tests

- **Focused regression tests**: `test_p3_06_audit_reconstruction_support.py` (12 tests) and `test_p3_07_cross_capability_enforcement.py` (10 tests) passed.
- **P6.05 end-to-end synthetic regression**: `test_p6_05_exact_tender_attachment_admission.py` (5 tests) passed, proving the complete sequence from execution creation to identity-preserving reconstruction.
- **Full reference suite**: `881` tests passed (historical baseline 874 + 7 new regressions).

## 6. Boundaries preserved

- No real L7 rerun or EIS/SOAP calls occurred.
- Real L8 attempt #2 was NOT consumed or authorized.
- No external actions or product code changes were performed.
- Organization, access, redaction and provenance checks remain fail-closed.

## 7. Exit

The implementation gap is repaired. L8 remains incomplete. The next action is a separately authorized L8 attempt #2 following independent review and merge of this repair.
