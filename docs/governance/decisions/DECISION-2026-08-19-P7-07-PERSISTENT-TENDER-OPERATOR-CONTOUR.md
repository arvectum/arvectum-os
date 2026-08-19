# DECISION-2026-08-19 — P7.07 Persistent Tender Operator Operational Contour

Status: `Approved`
Date: `2026-08-19`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform` and `product_specific`
Constitution: `1.2.0`
Applicable Product Contract: `P6-02-FIRST-REAL-PRODUCT-CONTRACT.md` — `Provisional 0.1.0`
Decision assertion: `OWNER_APPROVES_P7_07_TENDER_OPERATOR_OPERATIONAL_ADMISSION`
Approval evidence: owner instruction to execute `P7.07 — Persistent Tender Operator operational contour` on `2026-08-19`; the consequential setup path still requires the exact assertion above at execution time.

## 1. Decision

The owner approves a bounded P7.07 operational contour that makes Arvectum Tender Operator a repeatable ongoing consumer of the existing `Persistent Internal / owner-operated` Arvectum OS runtime.

The contour MUST preserve the exact canonical P6.02 Product Contract `Provisional 0.1.0` boundary and SHALL NOT create a new Product Contract version merely to operationalize an already-declared CAP-001/CAP-004 reliance.

The contour is split into two deliberately different paths:

1. **one-time operational setup** — one exact governed `platform.document` External Reference Version MAY be admitted from the already-retained and already-approved P6.05-L7 exact EIS evidence manifest, persisted through P7.03 in a minimized but rehydratable CAP-001 representation, and bound to one exact persistent P7.04 local read grant;
2. **ordinary ongoing consumption** — repeated Tender Operator reads MUST be read-only, MUST rehydrate the exact admitted CAP-001 Document Version inside the platform boundary, and MUST reach CAP-001 through the product-owned `arvectum/tender-agent` `ArvectumOSBridge` under exact P6.02 `0.1.0`.

The already-retained P7.06-UI1 item is not silently repurposed for P7.07. It was intentionally minimized for workspace inspection and carries the UI1 admission handling purpose. P7.07 therefore creates a distinct operational exact Version whose handling purpose is `prebid-review`, matching the existing Tender Operator read path.

## 2. Exact source evidence

The one-time operational setup is limited to the already-retained P6.05-L7 exact EIS attachment-evidence manifest for notice:

`0344100006426000005`

Approved exact manifest SHA-256:

`74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`

The setup MUST independently verify the manifest body, exact digest, complete seven-document evidence set, retained external source version and retrieval provenance before any admission.

No new EIS/SOAP/network retrieval is authorized by this decision.

## 3. Authority and Product Contract boundary

The operational Document MUST remain:

- semantic type: `platform.document`;
- authority mode: `External Reference`;
- authoritative source: `ЕИС / zakupki.gov.ru`;
- authority scope: the existing P6.02 document External Reference scope;
- Product Contract: exact P6.02 `0.1.0`;
- product compatibility line: `restricted-paid-pilot/44fz-prebid-v1`;
- platform dependencies: only those already declared by P6.02 (`CAP-001` and `CAP-004`).

Arvectum OS MUST NOT become authoritative for the underlying procurement facts merely because it persists a governed reference/manifest representation.

The P7.03 filesystem store remains a private platform implementation detail. Tender Operator MUST NOT read P7.03 tables/files/directories as a product dependency. The platform-side operational adapter may hydrate the exact governed object internally, but product reliance MUST cross the existing declared IntegrationAdapters/CAP-001 seam through the product-owned bridge.

## 4. Separate governance bases

This approval does not collapse RFC-0003/RFC-0005 concepts.

For the one-time operational admission:

- **Authorization** MUST be proven independently by an exact P7.04 attributable-human local setup grant and credential verification;
- **Organizational Authority** MAY use this approved owner decision as its bounded basis;
- **Data Governance** MUST use exact P6.02 `0.1.0`, the retained P6.05-L7 evidence restrictions and the explicit `External Reference` authority mapping;
- **Consequential Approval** MAY use this approved owner decision as the exact approval for the one operational Document Version admission.

P7.04 authorization remains technical operational access only. It does not itself satisfy Organizational Authority or Consequential Approval.

After successful setup, the temporary setup grant MUST be revoked. The ongoing contour may retain only an exact local read grant for the exact P7.07 operational item and `p3.08.resolve-document` operation.

## 5. Rehydratable persistence boundary

The new P7.07 governed item MAY retain sufficient domain-neutral CAP-001 state to reconstruct the exact admitted `AdmittedDocumentVersion` after process restart, including:

- exact Subject and Version identities;
- exact Organization and attributable creation-actor identity references;
- semantic/schema version;
- External Reference authority mode/scope and full external-authority mapping;
- provenance and integrity metadata;
- exact governed Artifact identity, media type, rendition role and integrity reference;
- handling classification `restricted-pilot`, purpose `prebid-review`, right `read`, and inherited retention reference.

It MUST NOT persist raw tender-document bytes, reusable credentials, EIS secrets, product recommendations, bid decisions, procurement-domain analysis, arbitrary product state or external-effect payloads.

This representation is private/reversible operational storage. It is not a Stable/public persistence schema, SDK/API, DMS format or Product Contract wire format.

## 6. Ordinary operational consumption

Each ordinary P7.07 consumption MUST:

1. execute from the exact active P7.06 release;
2. verify P7.03 store/item integrity before use;
3. reuse the exact persistent P6.05-L4 Organization and attributable human owner-operated Principal;
4. authenticate/authorize through P7.04 for the exact item-scoped local read grant;
5. verify the canonical P6.02 source and exact `0.1.0` version pin;
6. rehydrate only the exact P7.07 operational `platform.document` inside the platform boundary;
7. preserve `External Reference` and ЕИС authority;
8. call the actual product-owned `arvectum/tender-agent` `ArvectumOSBridge.resolve_document(...)` path;
9. use the existing `prebid-review` / `read` / `restricted-pilot` access context;
10. preserve exact Subject, Version, Artifact and integrity reliance;
11. perform no canonical mutation, no EIS/SOAP retrieval and no product/external effect.

## 7. Restart-survivability proof

P7.07 is not complete merely because a single read succeeds.

The selected-Mac proof MUST:

1. consume the exact operational Document through the real Tender Agent product bridge;
2. record the exact P7.02 healthy runtime release/instance/generation;
3. record the P7.03 governed-state tree digest;
4. restart only through the already-established P7.02 supervised restart path;
5. prove the runtime instance changed, generation advanced and `previous_instance_id` preserves restart continuity;
6. prove P7.03 governed state is byte-stable across restart;
7. consume again through the real product bridge;
8. prove the second reliance is the same exact storage item, Subject, Version, Artifact, integrity reference, authority source and Product Contract version;
9. prove the two reads and restart produced no canonical mutation or external effect.

## 8. Explicit prohibitions

This decision does **not** authorize:

- new EIS/SOAP/network retrieval as part of P7.07 setup or read;
- tender submission, bid placement, signature, email, Telegram, payment or other external effect;
- AI or technical execution acting as organizational authority;
- Product Contract expansion beyond P6.02 `0.1.0`;
- CAP-002 or CAP-003 reliance;
- direct product access to P7.03 internal storage;
- procurement-domain schema/workflow/risk/recommendation logic moving into Arvectum OS;
- raw tender bytes or reusable secrets entering ordinary P7.03 payloads/logs/evidence;
- standing canonical-write permission after setup;
- capability lifecycle promotion;
- Product Contract lifecycle promotion;
- external/customer Production, public/stable API/SDK/persistence format, SLA/SLO/support or broader conformance claims.

## 9. ADR and stable-boundary disposition

No ADR is required for this bounded implementation because the P7.07 persistence/rehydration/configuration and selected-Mac process adapters remain private, owner-local, reversible and not externally relied upon.

Re-open the ADR/stable-boundary gate before any of the following becomes true:

- the persisted rehydratable representation becomes cross-product or externally relied upon;
- a stable/public persistence or transport schema is promised;
- the product consumes a network/service API rather than the current internal seam;
- a materially constraining long-lived topology or product-runtime deployment mechanism is selected.

## 10. Closure evidence

P7.07 may be marked `Complete / PASS` only after:

- repository implementation and focused tests pass;
- functional cross-review has no remaining material objection;
- CI passes on the merged implementation;
- the selected Mac activates the merged exact release through the existing P7.06 governed path;
- one-time setup/admission succeeds or is proven idempotent against the exact already-created P7.07 item;
- the temporary setup grant is revoked and exact persistent read grant is effective;
- the real `arvectum/tender-agent` product bridge succeeds before and after supervised runtime restart;
- exact reliance is unchanged across restart;
- P7.03 governed state is unchanged by ordinary reads/restart;
- bounded owner-local evidence is retained without credentials or raw tender bytes;
- roadmap/resulting canonical state is synchronized.

Until that selected-Mac/product proof passes, repository implementation alone is not P7.07 completion.