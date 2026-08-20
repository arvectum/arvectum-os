# P8.07 — Portability / Export / Migration / Customer-Handover Interoperability Proof

Status: `Complete / PASS — bounded interoperability proof; external customer transfer NOT ACTIVATED`
Date: `2026-08-20`
Task classification: `platform` with `product_contract` boundary implications
Constitution: `1.2.0` (`Ratified`, frozen)
Checked Accepted RFC: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0008 (`1.0.0`)
Checked ADR: no Accepted ADR applies; `docs/adrs/README.md` contains no permanent portability/customer-handover topology decision
Roadmap source: `docs/roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`

## 1. Decision and exact scope

P8.07 is closed only as a **bounded interoperability proof**.

The canonical Phase 8 scope still contains one governing Organization, `ООО «Арвектум»`, and no concrete permitted external portability/customer-handover recipient. The roadmap explicitly prohibits exercising organization control beyond the owner-operated deployment without such a recipient/scope. Therefore this task does **not** fabricate a customer, second Organization, redistribution right, access grant or handover authorization.

The proof instead demonstrates that a machine-readable governed package can be created and independently interpreted by an isolated same-Organization receiver process while preserving the required semantics and remaining fail-closed on any attempt to activate external transfer.

Actual customer/cross-Organization transfer is `NOT ACTIVATED` and remains unproven until a concrete permitted recipient/scope exists and a fresh governed implementation/evidence path is executed.

## 2. Canonical compatibility

The proof follows the authority hierarchy without changing a higher-level contract:

- RFC-0001 portability/organizational-control requirements remain intact;
- RFC-0002 Subject/Version identity and relationship endpoint semantics remain explicit;
- RFC-0003 portability package, integrity, handling-constraint, authority, termination and migration requirements are exercised in bounded form;
- RFC-0004 hidden product/platform coupling is not introduced;
- RFC-0005 consequential state/effect authority is not inferred from export/import;
- RFC-0006 historical reconstruction never replays an external effect;
- RFC-0008 document/artifact portability semantics are preserved without promoting the proof package into a universal artifact/customer format.

No Constitution amendment, RFC amendment, ADR, Product Contract lifecycle transition or Platform Capability lifecycle transition is required.

## 3. Executable evidence

Reference harness:

- `reference/python/p8_07_handover_interoperability.py`

Regression coverage:

- `reference/python/tests/test_p8_07_handover_interoperability.py`

The harness emits only transient proof material:

- `package.json` — deterministic machine-readable bounded proof document;
- `package.sha256` — independent package-integrity sidecar;
- receiver receipt — emitted by verification and not committed as canonical state.

The proof format is task-local reference evidence. It is **not** a public/stable API, SDK, wire format, customer export standard, compatibility promise or Product Contract surface.

Focused local execution before repository write: `11 tests / OK`.

Repository `Reference Python CI` is the merge gate for the complete reference suite.

## 4. Requirement-to-evidence mapping

| P8.07 requirement | Evidence |
|---|---|
| preserve identities and versions | explicit `subject_id` + immutable `version_id` with receiver validation |
| preserve authority semantics | proof fixture authority is scoped; package explicitly records no Organizational Authority transfer |
| preserve provenance/history | immutable Event identity/timestamps and selected historical outcome are exported |
| preserve relationships | typed relationship with resolvable Subject/Version source and explicit external-reference target |
| explicit omissions | secret and ephemeral-runtime omissions are declared with reasons and reprovisioning instructions |
| classification/rights/retention survive | `Internal` classification, purpose, denied redistribution/customer/cross-Organization rights, retention and deletion instructions are receiver-validated |
| non-exportable secrets omitted | credentials are represented only as an omission descriptor; secret/credential material fields are rejected |
| receiver validates integrity and metadata | exact schema/version/Organization/scope/receiver checks plus SHA-256 verification |
| selected historical outcome reconstructable | outcome digest and source Event references are revalidated by the receiver without external-effect replay |
| no implicit Organizational Authority/access | package requires `organizational_authority_transferred=false`, `technical_access_granted=false`, `credentials_exported=false` |
| termination/revocation explicit | separate credential revocation, receiver-access revocation, retention/deletion instruction and handover/deletion evidence requirements are mandatory |
| no competing authoritative systems | simultaneous source+receiver authority fails closed; receiver authority without an explicit governed transition authorization fails closed |

## 5. External transfer activation gate

Current proof behavior is deliberately stricter than a generic handover utility:

- `external_transfer_activated=false` is part of the package;
- the activation gate states that a concrete permitted external recipient and scope are required;
- calling the harness with `external_transfer_activated=True` fails closed;
- no caller-supplied string, synthetic grant identifier or test recipient can convert the harness into permission;
- any future real external handover requires fresh canonical rights/recipient scope and a new governed implementation/evidence path.

This prevents a test helper from becoming accidental authorization or a hidden stable customer-transfer interface.

## 6. Migration / source-of-truth safety

The bounded package represents `NO_AUTHORITY_TRANSFER`:

- source authority remains active for the proof fixture;
- receiver authority remains inactive;
- a simultaneous source+receiver authoritative state is rejected;
- receiver authority without explicit governed transition authorization is rejected;
- package import/verification alone never changes source-of-truth authority.

Therefore a failed or partial migration cannot silently establish two competing authoritative systems through this proof path.

## 7. Historical reconstruction boundary

The selected historical outcome in this proof is a synthetic domain-neutral fixture used only to validate interoperable reconstruction mechanics.

It is **not** represented as a customer record, EIS redistribution package, real customer handover, or new evidence that external data may be redistributed. P7.10 remains the earlier owner-operated clean-host recovery proof; P8.07 adds the explicit receiver/rights/authority/termination/migration interoperability envelope without broadening those rights.

## 8. Functional cross-review

### Iteration 1

Material objection:

> A draft activation branch accepted caller-provided recipient/scope/grant strings, which could be mistaken for a sufficient authorization mechanism.

Revision:

- removed any pseudo-grant activation path;
- current harness fails closed on every external-transfer activation attempt;
- no external permission can be synthesized inside the reference helper.

Disposition: `resolved`.

### Iteration 2

Material objections checked:

1. task-local package might be mistaken for a universal/stable customer export format;
2. synthetic reconstruction might be overstated as a real customer handover;
3. migration verification might validate integrity but still permit authority ambiguity.

Revisions / controls:

- package is deliberately minimal (`package.json` + SHA-256 sidecar) and explicitly marked task-local/non-stable;
- review and harness state that customer transfer is `NOT ACTIVATED`;
- synthetic outcome is described only as reconstruction-mechanics evidence;
- dual-active authority and receiver activation without governed transition authorization fail closed.

Disposition: `resolved`; no remaining material functional objection identified.

Functional review is not formal architecture approval, lifecycle promotion or customer authorization.

## 9. PASS statement and non-claims

`P8.07 = Complete / PASS` only for the bounded interoperability mechanics actually exercised:

- deterministic machine-readable package;
- independent receiver-process validation;
- semantic identity/version/relationship/history preservation;
- classification/rights/retention/deletion propagation;
- secret omission/reprovisioning semantics;
- authority/access non-transfer;
- historical reconstruction without effect replay;
- explicit termination/revocation controls;
- fail-closed migration authority conflict;
- fail-closed external-transfer activation.

Not proven or claimed:

- actual customer handover;
- cross-Organization transfer;
- customer-facing redistribution rights;
- universal export/import compatibility;
- public/stable package format or API;
- receiver Production readiness;
- Stable Product Contract;
- Active Platform Capability;
- SLA/support/certification/full-platform conformance.

## 10. Next canonical action

After canonical merge/CI closure, the next roadmap action is:

> `P8.08 — Multi-Organization isolation + cross-organization security validation`.

P8.08 must not fabricate a second Organization merely to satisfy sequencing; its own conditional scope must be dispositioned from the actual canonical activation state.
