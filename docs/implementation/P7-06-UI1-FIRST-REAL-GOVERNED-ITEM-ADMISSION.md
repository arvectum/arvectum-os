# P7.06-UI1 — First Real Governed Item Admission / Persistence Bridge

Status: `Repository implementation ready; selected-Mac execution pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Operating scope: `Persistent Internal / owner-operated`

## 1. Purpose

This is a one-purpose internal bridge for the sole remaining `P7.06-UI1` blocker: the persistent P7.03 store currently contains no real retained `canonical-governed-state` item for browser inspection.

The bridge does not create sample truth and does not turn a fixture into production-like state. It reuses the already-retained real P6.05-L7 exact EIS attachment evidence, performs a new bounded Governed Execution/admission under the actual persistent owner context, and persists only the admitted minimized governed representation after successful admission.

Owner authorization is recorded by:

`docs/governance/decisions/DECISION-2026-08-18-P7-06-UI1-FIRST-REAL-GOVERNED-ITEM-ADMISSION.md`

Exact owner assertion:

`OWNER_APPROVES_P7_06_UI1_FIRST_REAL_GOVERNED_ITEM_ADMISSION`

## 2. Source evidence boundary

The only approved real source for this bridge is the already-retained P6.05-L7 exact evidence manifest for notice `0344100006426000005`.

Approved manifest SHA-256:

`74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`

The adapter independently rebuilds the canonical JSON body hash and verifies:

- P6.05 evidence schema/purpose/status;
- notice identity;
- expected/exact count `7/7`;
- no missing or duplicate expected documents;
- each document has exact digest/size evidence;
- exact external source version and timezone-aware retrieval time;
- `external_actions=false`;
- `ЕИС / zakupki.gov.ru` remains the authoritative external source.

The manifest file must be an owner-only regular file and must not be a symlink. No EIS/SOAP/network refetch is part of this path.

## 3. Existing owner and Product Contract continuity

The bridge reuses, rather than recreates:

- the existing P6.05-L4 Organization context;
- the existing attributable human owner-operated Principal;
- the P6.02 Tender Operator Product Contract `Provisional 0.1.0`;
- CAP-001 Document/Artifact admission and CAP-004 Reconstruction surfaces already declared by that Product Contract.

The Product Contract is verified from the exact release source through the existing P6.05-L5 product connection preflight.

This bridge does not broaden the Product Contract or introduce product-domain business logic into shared platform semantics. The concrete notice/digest exists only as bounded operational proof input.

## 4. Authorization and authority separation

Before the retained evidence is read for admission, P7.04 must independently authorize the existing human Principal with the exact tuple:

- operation: `governed.item.admit`;
- resource: `p7-06-ui1:first-real-governed-item`;
- access path: `local`.

The P7.04 decision must still report:

- `organizational_authority_satisfied = false`;
- `consequential_approval_satisfied = false`.

The RFC-0005 execution then records four separate ALLOW decisions with separate bases:

1. Authorization — exact P7.04 local human grant basis;
2. Organizational Authority — bounded approved owner decision;
3. Data Governance — P6.02 Product Contract plus exact retained P6.05-L7 restrictions;
4. Consequential Approval — bounded approved owner decision.

Technical access therefore never becomes Organizational Authority by implication.

## 5. Governed admission flow

The implementation follows:

```text
exact active P7.06 release
        ↓
owner assertion + approved decision verification
        ↓
P7.04 exact human local authorization
        ↓
P6.05-L4 identity + P6.02 Product Contract continuity
        ↓
independent retained L7 manifest verification
        ↓
Governed Execution Created → AwaitingGate
        ↓
four distinct RFC-0005 ALLOW decisions
        ↓
Ready
        ↓
CAP-001 exact External Reference Document Version admission
        ↓
Running → Succeeded
        ↓
RFC-0006 canonical Event admission / provenance
        ↓
CAP-004 reconstruction complete
        ↓
P7.03 minimized canonical-governed-state persistence
        ↓
P7.03 non-authoritative recovery checkpoint
```

P7.03 is deliberately downstream of Governed Execution/admission. It is not the authority source.

## 6. Persisted representation

The retained P7.03 payload is a minimized JSON representation containing identifiers/references and safe governed metadata needed for UI1 inspection. It includes:

- distinct Subject and exact Version identities;
- semantic/schema identity;
- `External Reference` authority mode/scope;
- authoritative system and external object reference;
- approved manifest digest and member count;
- exact Product Contract reference;
- execution/event references;
- provenance references;
- governed Artifact integrity reference;
- explicit `raw_document_bytes_included=false`;
- explicit `reusable_secret_included=false`;
- explicit `external_actions=false`.

It does not persist the seven raw tender document bytes, credential secrets, SOAP/XML payloads, archive URLs, or raw owner-local evidence payloads.

`canonical_authority=true` in the P7.03 storage metadata means that the retained item is a canonical governed platform representation after admission; it does **not** replace ЕИС as authority for the externally sourced tender material. `authority_mode=External Reference` and the authoritative source remain explicit.

## 7. Idempotency and conflict behavior

The Subject/Version pair is deterministic from the actual Organization scope, notice and approved manifest digest.

First successful execution is expected to create exactly one governed item and one recovery checkpoint.

The required selected-Mac entrypoint is:

`reference/python/p7_06_ui1_real_state_admission_entrypoint.py`

Before an idempotent retry is accepted, it independently verifies the already-retained exact Subject/Version against:

- semantic/schema identity;
- External Reference authority mode/scope/source;
- exact approved source manifest digest;
- Product Contract `0.1.0`;
- complete CAP-001/RFC-0006/CAP-004 validation status;
- governed admission reference;
- bounded provenance chain;
- exact source release attribution;
- canonical/minimization/no-secret/no-external-effect flags.

Duplicate exact Subject/Version claims or any semantic drift fail closed. A successful retry must not create a second governed item or checkpoint.

## 8. Exact-release and operational boundary

The selected-Mac entrypoint must run from:

`<runtime-root>/releases/<current-exact-sha>/source/reference/python/p7_06_ui1_real_state_admission_entrypoint.py`

The implementation refuses a mutable working-tree invocation and verifies the active P7.06 release before protected execution.

No public/stable API, route, service topology, framework, browser matrix, persistence technology or remote-administration contract is introduced.

## 9. Selected-Mac exit evidence

Repository implementation alone does not create the real governed item. Selected-Mac closure must prove:

1. exact merged release deployed through P7.06;
2. existing owner context reused;
3. exact P7.04 admission grant established;
4. exact retained L7 manifest found and independently verified without refetch;
5. first hardened entrypoint run = admitted/persisted PASS;
6. P7.03 contains exactly the expected new real governed item and checkpoint;
7. second run = idempotent existing PASS with no duplicate item/checkpoint;
8. no network/external effect/raw-document platformization;
9. owner-local non-secret evidence retained;
10. UI1 then renders the real Subject, exact Version, External Reference/source, validation and provenance;
11. browsing leaves the governed-state digest unchanged.

Only after that evidence is reviewed may `P7.06-UI1` become `Complete / PASS`.

## 10. Non-claims

This bridge does not create:

- a standing canonical-write authority;
- general owner/admin authorization;
- Product Contract lifecycle promotion;
- Platform Capability lifecycle promotion;
- CAP-002/CAP-003 reliance;
- external/customer Production readiness;
- public/stable UI/API/SDK;
- SLA/support/browser compatibility commitments;
- a competing source of truth for ЕИС data.
