# P1.10 — Portable Semantic Fixture

Status: `Provisional bounded reference format`
Scope: `Phase 1 / P1.01–P1.10`
Public compatibility contract: `No`
Canonical authority source: `No`
Serialization: `UTF-8 JSON`

## 1. Purpose

This document describes the implementation-neutral semantic fixture emitted by
`export_p1_10_semantic_fixture` for the bounded Phase 1 reference scenario.

The fixture proves that the organizational meaning exercised by P1.01–P1.09 can
be represented outside the Python in-memory object graph while preserving the
identities, immutable versions, Organization scope, authority, exact version
reliance, provenance, causation and Observation non-promotion semantics required
by the Accepted architecture.

The fixture is a **derived portability representation**. It is not a Canonical
Record, not an independent source of authority, not a durable persistence format,
not a production export endpoint and not a stable cross-product/public wire
contract.

## 2. Architecture basis

The bounded format implements already-Accepted semantics from:

- Constitution `1.2.0`, especially organizational control, portability,
  reproducibility, versioning and technology independence;
- RFC-0001 `1.0.0` — Canonical Record, graph/context, Governed Execution,
  portability and technology-independence laws;
- RFC-0002 `1.0.0` — stable Subject Identity, immutable Version Identity,
  Canonical Record envelope, version-aware references and technology-independent
  representation;
- RFC-0003 `1.0.0` — Organization sovereignty and governed portability packages;
- RFC-0005 `1.0.0` — exact Workflow/input/gate/effect version reliance and sealed
  execution history;
- RFC-0006 `1.0.0` — Event, provenance, correlation and causation semantics;
- RFC-0007 `1.0.0` — Observation remains distinct from validated Knowledge;
- RFC-0008 `1.0.0` — manifest-based governed export, explicit omissions and
  Artifact portability semantics.

This bounded JSON choice remains below the current ADR gate because it is local
to the reference harness, reversible, non-public and does not create a durable
cross-product dependency. A later stable public/cross-product serialization
contract, durable migration format or portability standard must cross the
applicable ADR/standard/governance gate before reliance.

## 3. Representation rules

### 3.1 Semantic mapping, not Python serialization

The exporter constructs every JSON member explicitly. It does not use Python
`repr`, pickle, dataclass field dumping, module/class names or another runtime
object serialization mechanism as the semantic contract.

The JSON therefore preserves organizational semantics rather than incidental
Python object layout.

### 3.2 Identity

Every exported Identity is represented as:

```json
{
  "namespace": "...",
  "value": "...",
  "scope": "..."
}
```

The three components are carried separately. The fixture does not concatenate
an Identity into a vendor/runtime key and does not infer permissions, authority
or mutable business meaning from identifier syntax.

### 3.3 Canonical Record envelope

Each exported Canonical Record version contains an explicit semantic envelope:

- Subject Identity;
- Version Identity;
- semantic type;
- schema version;
- Organization Identity;
- authority mode and authority scope;
- accountable owner Identity;
- attributable creation Actor;
- timezone-aware creation time;
- provenance references;
- proportional integrity metadata already present in the bounded harness;
- bounded payload entries;
- lifecycle status;
- predecessor Version Identity where applicable.

The fixture does not strengthen the evidentiary meaning of the existing
`frozen-in-memory-reference` integrity metadata and does not add a cryptographic
integrity claim.

### 3.4 Type-specific semantics

The common envelope is supplemented by explicit semantic sections where needed:

- `workflow` — semantic operations, target Subject reference and side-effect
  classes;
- `gate` — gate kind/outcome, governed basis, initiating Principal, exact
  evaluated Execution/Workflow/target references;
- `execution` — exact Workflow pin, operation, material inputs, gate decisions
  and canonical effects;
- `event` — Event type/schema, source, times, actor attribution, exact execution
  and related references, correlation, causation, classification and access
  scope;
- `observation` — explicit `Unvalidated` epistemic status, exact Event,
  Execution and effect pins, evidence references and `not-performed` Knowledge
  promotion state.

### 3.5 Subject references versus Version references

Where the distinction is material, the fixture declares `reference_role` as one
of:

- `subject` — stable logical governed subject reference;
- `version` — exact immutable Canonical Record version reference;
- `governed-identity` — an Identity reference whose P1 bounded fixture does not
  claim to be a Subject or Version role, such as the supplied gate basis.

The exporter never silently treats a Subject Identity as an exact Version
Identity or the reverse.

## 4. Fixture sections

The top-level JSON object contains:

- `fixture` — format identity/version, bounded scope and explicit non-authority,
  non-public and non-production declarations;
- `organization` — explicit Organization Identity and the bounded tenant field;
- `actors` — initiating Actor and gate-decision Actor attribution;
- `manifest` — exported Canonical Record Version list, record/link counts and
  included semantic concerns;
- `records` — the ten governed Canonical Record versions exercised by P1.02–P1.09;
- `semantic_links` — derived reference links preserving relationship/reference
  meaning without fabricating Typed Relationship Canonical Records;
- `reconstruction` — the P1.08 read-only reconstruction manifest marked
  `derived-non-canonical`;
- `portability` — portability boundary, explicit omissions and non-exportable
  dependency declaration for this bounded fixture.

## 5. Exported governed state

The bounded fixture exports exactly these Canonical Record versions:

1. material input v1;
2. Workflow v1;
3. Authorization decision;
4. Organizational Authority decision;
5. `AwaitingGate` Execution Context;
6. `Ready` Execution Context;
7. resulting target v2;
8. terminal `Succeeded` Execution Context;
9. admitted canonical Event;
10. captured Observation.

The fixture preserves the stable target Subject Identity across v1/v2 and the
stable Execution Subject Identity across its three governance-significant
Execution Context versions.

## 6. Semantic links are not new canonical relationships

`semantic_links` is a derived export aid. Every link contains:

```json
"canonical_typed_relationship": false
```

The links preserve relationship/reference meaning already present in the source
records and type-specific fields, including predecessor lineage, exact Workflow
and material-input reliance, gate-decision reliance, canonical effects, Event
execution/result linkage, correlation, causation and Observation source/effect
references.

P1.10 does **not** create or fabricate `platform.relationship` Canonical Records.
A later need for governed Typed Relationship instances must use the RFC-0002
Canonical Record lifecycle rather than promote these derived manifest links by
implication.

## 7. Observation non-promotion

The exported Observation remains:

- semantic type `platform.observation`;
- lifecycle `Captured`;
- epistemic status `Unvalidated`;
- `knowledge_promotion = not-performed`;
- pinned to the exact admitted Event, terminal Execution Context and observed
  canonical effect versions.

No `platform.knowledge` record is introduced by export. Portability does not
upgrade evidence into validated Knowledge.

## 8. Authority and disclosure boundary

The fixture preserves source authority metadata but is itself explicitly
`canonical_authority = false`.

The P1.10 exporter operates only on the predetermined domain-neutral reference
scenario and is **not an authorization mechanism for real organizational data
export**. A production or customer-data export remains a security/privacy-
sensitive disclosure and must pass the applicable RFC-0003 authorization,
Organizational Authority, purpose, classification, rights and contractual gates.

No administrator, caller or fixture consumer receives additional permission or
Organizational Authority merely because the JSON can be produced or parsed.

## 9. Explicit omissions

The bounded fixture explicitly omits or declines to claim:

- reusable secrets, private keys, provider tokens and credentials;
- product-domain semantics and Product Contract state;
- durable persistence, cache, projection or index implementation state;
- validated Knowledge, Knowledge promotion or Improvement Proposal state;
- production, SLA, support, archival or compatibility commitments.

`non_exportable_dependencies` is empty for the synthetic bounded scenario. A
real portability package must list applicable non-exportable dependencies rather
than silently omit them.

## 10. Determinism and verification

The exporter:

1. re-validates the supplied P1.08 reconstruction evidence from the exact
   P1.02–P1.07 governed objects;
2. re-validates the exact P1.09 Observation from that evidence;
3. rejects mismatch rather than exporting a mixed or stale semantic state;
4. requires one Organization scope across all exported Canonical Record versions;
5. rejects duplicate exported Version Identities;
6. emits deterministic, sorted, human-readable JSON;
7. does not mutate or replay the source governed state.

The P1.10 fitness tests parse the resulting JSON through the standard JSON data
model and verify semantic values rather than Python object identity.

## 11. Conformance boundary

P1.10 is executable architecture evidence for the bounded Phase 1 reference
slice. It does not claim:

- full RFC-0003 portability conformance for a production deployment;
- a complete service-termination/handover package;
- a stable organization-wide portability standard;
- a public API or wire-format compatibility commitment;
- an `Active` Platform Capability;
- production readiness.

Those claims require their own declared scope, operational evidence and any
applicable subordinate ADRs, standards, policies and approvals.
