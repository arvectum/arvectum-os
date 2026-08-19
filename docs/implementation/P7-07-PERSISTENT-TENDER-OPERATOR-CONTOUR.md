# P7.07 — Persistent Tender Operator operational contour

Status: `Complete / PASS`
Date: `2026-08-19`
Task classification: `product_contract` with `platform` and `product_specific`
Canonical Product Contract: `P6-02-FIRST-REAL-PRODUCT-CONTRACT.md` — `Provisional 0.1.0`
Owner decision: `docs/governance/decisions/DECISION-2026-08-19-P7-07-PERSISTENT-TENDER-OPERATOR-CONTOUR.md`
Operational closure: `docs/reviews/P7-07-selected-mac-operational-closure.md`

## 1. Purpose

P7.07 converts the already-proved Tender Operator / Arvectum OS integration from a bounded one-shot proof into a repeatable `Persistent Internal / owner-operated` operational contour.

It does so without changing the P6.02 Product Contract, without moving procurement-domain logic into Arvectum OS and without making Arvectum OS authoritative for EIS procurement facts.

## 2. Runtime shape

The supported operator path is:

`P7.02 exact active release → P7.04 attributable human access → P6.02 exact 0.1.0 connection → P7.03 exact governed item → internal CAP-001 rehydration → guarded product-owned ArvectumOSBridge → CAP-001 resolve_document`

The P7.03 store is not a product contract surface. Tender Operator does not read P7.03 files directly. Loading and rehydration happen inside the platform-side private operational adapter; product reliance crosses only the already-declared CAP-001 seam through the product-owned bridge.

## 3. One-time setup

The one-time setup:

1. requires the exact active P7.06 release and approved P7.07 owner decision;
2. reuses the persistent P6.05-L4 Organization and attributable owner-operated human Principal;
3. independently verifies the already-retained P6.05-L7 EIS manifest for notice `0344100006426000005` and exact approved SHA-256;
4. uses a temporary exact P7.04 setup grant;
5. connects to exact P6.02 `0.1.0`;
6. performs one Governed Execution with distinct Authorization, Organizational Authority, Data Governance and Consequential Approval decisions;
7. admits an exact `platform.document` External Reference Version through CAP-001;
8. emits RFC-0006 admission provenance and proves CAP-004 reconstruction;
9. persists only a minimized but rehydratable CAP-001 representation through P7.03;
10. writes a private non-canonical item-routing config;
11. creates one exact item-scoped local `p3.08.resolve-document` read grant;
12. revokes the temporary setup grant.

The supported CLI for setup is `reference/python/p7_07_guarded_operational_entrypoint.py setup`, not direct low-level invocation of the semantic contour module.

The guarded entrypoint additionally rolls back newly-created read grants if setup does not complete and refuses a retry while a stale exact setup grant remains active.

## 4. Persisted representation

The P7.07 operational item stores only the minimum domain-neutral state needed to reconstruct the exact admitted CAP-001 `AdmittedDocumentVersion` after process restart:

- exact Subject and Version identities;
- Organization and attributable owner identity references;
- semantic/schema version;
- `External Reference` authority mode/scope;
- full external-authority mapping preserving `ЕИС / zakupki.gov.ru` authority;
- governed provenance and integrity metadata;
- one exact governed manifest Artifact identity, media type, rendition role and integrity reference;
- handling constraints `restricted-pilot / prebid-review / read`;
- inherited product/source retention reference.

It does not store raw tender bytes, reusable credentials, EIS secrets, procurement recommendations, bid decisions or arbitrary product state.

The representation is a private reversible storage shape, not a Stable/public schema or Product Contract wire format.

## 5. Repeatable consumption

Each ordinary read:

1. verifies exact active release and P7.03 integrity;
2. authenticates and authorizes the exact persistent human Principal through the exact item-scoped P7.04 local read grant;
3. verifies the canonical P6.02 source and exact `0.1.0` version pin;
4. loads and rehydrates only the configured exact P7.07 governed item inside the platform boundary;
5. structurally validates the product-owned `arvectum/tender-agent` `ArvectumOSBridge` before module execution;
6. invokes that bridge with `prebid-review / read / restricted-pilot` CAP-001 request semantics;
7. proves exact Subject, Version, Artifact and integrity reliance;
8. preserves EIS external authority;
9. performs no canonical mutation, EIS/SOAP retrieval or external effect.

The bridge guard permits only the narrow current product seam shape and rejects executable top-level behavior, imports outside the bounded seam or a `resolve_document` implementation that is not a pure keyword-for-keyword delegation to `self.adapters.capabilities.resolve_document(...)`.

This AST guard is private operational hardening, not a stable source-code ABI.

## 6. Restart survivability

`reference/python/p7_07_guarded_selected_mac_proof.py` is the closure launcher. It wraps the selected-Mac proof runner and ensures bridge validation immediately before each dynamic load.

The underlying proof:

- requires a clean local `main` checkout whose origin is canonical `arvectum/tender-agent`;
- records the product HEAD and platform release SHA;
- consumes once through the real product bridge;
- records P7.02 instance/generation and P7.03 state digest;
- restarts through the existing P7.02 supervised restart adapter;
- proves runtime instance replacement, generation advance and `previous_instance_id` continuity;
- proves P7.03 state did not change;
- consumes again through the same real product bridge;
- proves the same exact storage item, Subject, Version, Artifact, integrity reference, EIS authority and P6.02 version before and after restart.

## 7. Boundaries preserved

P7.07 creates none of the following:

- Product Contract `0.2.0` or lifecycle promotion;
- CAP-002/CAP-003 dependency;
- capability lifecycle promotion;
- public/stable API, SDK or persistence schema;
- product access to P7.03 internals;
- procurement-domain platform schema/workflow/approval logic;
- EIS mutation or competing source of truth;
- standing canonical-write authority;
- autonomous AI approval or organizational authority;
- SLA/SLO/support/conformance expansion.

## 8. Repository evidence

Repository-level coverage includes:

- exact manifest body/digest validation;
- governed admission and CAP-004 reconstruction;
- P7.03 rehydration and authority continuity;
- setup idempotency;
- exact read-grant enforcement and revocation fail-close behavior;
- actual CAP-001 product-bridge delegation;
- read-only P7.03 state behavior;
- product-bridge AST hardening;
- rollback of newly-created privileges on failed setup;
- selected-Mac restart-proof invariants and canonical product-origin checks;
- regression coverage for real dynamic loading of the product-owned `@dataclass(frozen=True, slots=True)` bridge after PR `#76`.

Initial implementation merged through PR `#75` at `bf1a3047aadf03384c9525eacd4e186a53092c11`. The selected-Mac Attempt 1 loader defect was remediated through PR `#76`, merged at `b0c18fba15de6b5abac83a4f583d89eedb5c03d1`; Reference Python CI `#157` completed with `success`.

## 9. Operational closure

P7.07 is `Complete / PASS` for the declared selected-Mac `Persistent Internal / owner-operated` scope.

Selected-Mac Attempt 2 activated exact release `b0c18fba15de6b5abac83a4f583d89eedb5c03d1` through the existing P7.06 governed update path, reused the existing exact governed item through `PASS_IDEMPOTENT_EXISTING`, retained zero active temporary setup grants and the exact item-scoped persistent read grant, then proved real CAP-001 reliance through the canonical product-owned bridge both before and after an actual supervised P7.02 restart.

The restart advanced generation `59 → 60`, replaced the runtime instance, preserved `previous_instance_id` continuity and left the P7.03 governed-state digest byte-stable at `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1`.

Before/after reliance preserved the same exact storage item, Document Subject, Document Version, Artifact, integrity reference, P6.02 `0.1.0`, `External Reference` authority and authoritative source `ЕИС / zakupki.gov.ru`. No EIS/SOAP retrieval, contour network action, ordinary-read canonical mutation, external product effect, raw tender-byte exposure or credential-secret exposure occurred.

Owner-local proof evidence remains outside Git. Canonical history records basename `selected-mac-restart-proof.json` and submitted SHA-256 `9613637b06c5d192311bda1eb3096a9cd0b49c016134af887697637a668cf0f8` through [`P7.07 — Selected-Mac Operational Closure`](../reviews/P7-07-selected-mac-operational-closure.md).

Completion does not promote P6.02 beyond `Provisional 0.1.0`, does not promote a Platform Capability, does not establish Production, public/stable API/SDK/persistence semantics, SLA/SLO/support or broader conformance.
