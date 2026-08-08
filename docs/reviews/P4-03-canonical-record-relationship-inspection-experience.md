# P4.03 — Canonical Record / Relationship Inspection Experience

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P4.03 — Canonical Record / Relationship inspection experience`
Phase: `Phase 4 — Workspace / Operator Experience`
Milestone target: `M4 — Coherent governed workspace baseline`
Result: **`PASS — the bounded internal inspection surface preserves stable Subject Identity, exact immutable Version Identity, Canonical Head versus Effective Version, typed Relationship direction/reference-role semantics, authority/owner/scope/lifecycle meaning and immutable history while independently re-checking current source authorization before governed source or exact-Version disclosure.`**

## 1. Purpose and decision level

P4.03 makes the first governed-object inspection journey from P4.01 executable on top of the P4.02/R9 workspace boundary.

The implementation is deliberately read-only and internal. It resolves a current workspace Subject or exact-Version reference against caller-supplied current governed source lineages and independently supplied current source-authorization evidence, then renders the resulting Canonical Record or Typed Relationship semantics without creating canonical state, mutation authority, a public API, a route contract or a durable read model.

This artifact is subordinate implementation/review evidence. It does not amend Constitution or an Accepted RFC, create a new Platform Capability, change CAP-001 through CAP-004 lifecycle, create or promote a Product Contract, establish an IAM/entitlement model, select a frontend framework, or make a production/conformance claim.

## 2. Canonical authority checked

P4.03 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral Kernel, governed state, source-of-truth/authority semantics, security/isolation invariants, technology independence and scoped conformance;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, Canonical Head, Effective Version, exact historical resolution, first-class Typed Relationship identity/versioning, explicit relationship direction and SubjectIdentity/VersionIdentity endpoint roles, authority modes and the rule that a relationship grants neither Authorization nor Organizational Authority;
5. RFC-0003 — identity/authentication/Authorization/Organizational Authority separation, Organization sovereignty and fail-closed/no-ambient cross-Organization access semantics;
6. `docs/adrs/README.md` — no applicable Accepted ADR constrains this bounded reversible presentation/resolution layer;
7. [`P4.01 operator journeys / workspace boundary / IA review`](P4-01-operator-journeys-workspace-boundary-information-architecture.md) — inspection journey and presentation-authority requirements;
8. [`P4.02 Organization context / identity / scoped navigation shell review`](P4-02-organization-context-identity-scoped-navigation-shell.md) — explicit Actor/Organization and Subject/exact-Version reference shell;
9. [`R9 Workspace Boundary Review`](R9-workspace-boundary-review.md) — mandatory handoff requiring source-owned Organization scope and current authorization to be re-checked independently at dereference rather than inferred from presentation state or identifier syntax;
10. canonical Roadmap `2.13.0` and Phase 4 roadmap `1.3.0` at task start.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was identified.

RFC-0006/Event provenance and reconstruction were intentionally not pulled into this slice because the canonical Phase 4 plan assigns them to P4.04. Governed action/approval mutation remains P4.05 scope.

## 3. Implemented boundary

The P4.03 resolution path is intentionally ordered as follows:

```text
WorkspaceShellState
  ├── explicit ActorContext
  ├── explicit OrganizationScope
  └── Subject OR exact-Version reference
              ↓
current source authorization for Actor + Organization + stable Subject
              ↓
resolve current governed source by source-owned Organization + stable identity
              ↓
resolve Subject→Canonical Head OR preserve exact historical Version
              ↓
resolve Effective Version independently at explicit evaluation time
              ↓
read-only non-authoritative inspection DTO
              ↓
escaped inert HTML presentation
```

Authorization is checked before source existence, source multiplicity or exact-Version resolution so different error states cannot be used as an unauthorized object/version discovery oracle.

The authorization handoff is not treated as evidence that the source belongs to the Organization. The source's own governed `OrganizationScope` is checked independently. `Identity.scope` remains opaque identifier text and is never interpreted as permission, canonical Organization membership or Organizational Authority.

## 4. Executable implementation

### 4.1 `canonical_inspection.py`

`reference/python/arvectum_os_ref/canonical_inspection.py` introduces an internal immutable inspection boundary:

- `CurrentSourceAuthorization` — bounded caller-supplied evidence of one current source-access decision, bound to Organization, actual/represented Actor identity and stable resource Subject Identity;
- `GovernedInspectionSourceSet` — caller-supplied current Canonical Record and Typed Relationship lineages from their owning runtime boundaries;
- `CanonicalRecordInspection` — stable Subject, displayed exact Version, Canonical Head, Effective Version state, semantic type/schema, owner, Organization, lifecycle, authority, payload, immutable history and authorized relationship context;
- `RelationshipInspection` — stable Relationship Identity, displayed exact Relationship Version, Relationship Head, Effective Version, exact Relationship Type Version, source/target endpoint roles and identities, owner, lifecycle, authority and immutable history;
- `CanonicalInspectionBlockedState` — fail-closed no-content presentation state for absent reference, denied access, unavailable/ambiguous source or unavailable exact Version;
- `inspect_current_workspace_reference()` — ordered authorization/source/version/effective-resolution boundary;
- `render_canonical_inspection_html()` — escaped inert HTML presentation with textual semantics and no links/forms/routes/actions.

The inspection module remains unexported from the package root and imports no mutation, Governed Execution, gate, Product Contract, network, persistence, web-framework, database or serialization infrastructure.

### 4.2 Head, Effective and exact historical Version

A Subject reference deliberately displays the Canonical Head, but Effective Version is resolved independently at a required timezone-aware evaluation instant.

Therefore a future-effective Head can be visible as Head while an older immutable Version remains Effective. A missing effective interval returns `Missing`; overlapping effective intervals return `Ambiguous`. Neither state silently falls back to Head.

An exact-Version reference remains exact. If that Version does not exist after access has been authorized, the inspector returns `VERSION_UNAVAILABLE`; it never redirects to Head.

### 4.3 Typed Relationship graph context

Relationship graph context is generated only from current governed Typed Relationship lineages whose relationship Subject has its own matching current authorization decision.

For every visible edge the inspection preserves:

- stable Relationship Identity;
- Relationship Head Version Identity;
- independently resolved Effective Relationship Version state;
- exact Relationship Type Identity and Type Version Identity;
- traversal direction;
- matched endpoint role and identity;
- opposite endpoint role and identity;
- lifecycle, owner and authority meaning.

Subject-pinned and Version-pinned endpoints remain distinct. A Version-pinned relationship appears only when the displayed record Version matches that exact endpoint identity.

An unauthorized relationship is omitted without exposing its identifier, type, edge marker or hidden count. Relationship visibility itself creates no permission or Organizational Authority. The opposite endpoint identity is presented only as part of an already-authorized relationship assertion; P4.03 does not dereference opposite-endpoint content, and any later navigation must perform its own source resolution and authorization.

### 4.4 Static visible demo

`reference/python/examples/p4_03_canonical_inspection_demo.py` renders one exact historical Canonical Record inspection and one Relationship-Head inspection into a standalone static HTML document.

From `reference/python`:

```sh
python examples/p4_03_canonical_inspection_demo.py > /tmp/arvectum-p4-03.html
```

The demo is presentation evidence only. It establishes no server, route/deep-link schema, public API/BFF, frontend framework, browser session, IAM mechanism or durable read-model topology.

## 5. P4.03 evidence matrix

| P4.03 requirement | Executable evidence |
|---|---|
| stable Subject Identity and exact Version Identity visible | `test_subject_reference_explicitly_distinguishes_head_from_effective`; `test_exact_historical_version_is_preserved_without_head_redirect` |
| Head versus Effective Version distinct | `test_subject_reference_explicitly_distinguishes_head_from_effective`; relationship equivalent `test_relationship_subject_reference_shows_head_even_when_effective_differs` |
| authority mode / authoritative source visible | `test_authority_owner_scope_lifecycle_and_validation_meaning_are_visible`; renderer test |
| typed relationship direction and endpoint-role visible | `test_authorized_relationship_context_exposes_direction_roles_and_effective_state`; `test_direct_relationship_inspection_preserves_type_roles_and_exact_history` |
| lifecycle/validation state and owner/scope visible | `test_authority_owner_scope_lifecycle_and_validation_meaning_are_visible` |
| immutable historical versions inspectable | exact-history record and relationship tests |
| missing Effective Version explicit, no Head fallback | `test_missing_effective_version_is_explicit_and_never_defaults_to_head` |
| ambiguous Effective Version explicit, no guessed choice | `test_ambiguous_effective_version_is_explicit_and_never_guessed` |
| exact unknown Version does not fall back to Head | `test_unknown_exact_version_fails_closed_without_head_fallback` |
| source Organization comes from governed source rather than `Identity.scope` | `test_governed_source_organization_not_identity_scope_controls_resolution` |
| current authorization re-checked and Actor-bound | `test_current_authorization_is_fail_closed_and_actor_bound` |
| authorization precedes exact-Version existence disclosure | `test_authorization_is_checked_before_exact_version_existence_is_disclosed` |
| authorization precedes source-existence disclosure | `test_unauthorized_unknown_subject_does_not_become_source_existence_oracle`; `test_source_unavailability_is_reached_only_after_explicit_current_allow` |
| hidden relationships do not leak metadata/counts | `test_unauthorized_relationship_is_omitted_without_relationship_metadata` |
| Version-pinned relationship semantics preserved | `test_version_endpoint_relationship_only_appears_for_matching_displayed_version` |
| presentation remains inert/read-only/internal | `test_renderer_is_readable_inert_and_escapes_governed_values`; `test_inspection_layer_remains_internal_read_only_and_technology_neutral` |
| blocked presentation reveals no governed metadata | `test_blocked_renderer_exposes_no_governed_metadata` |

## 6. Validation-state honesty

The current generic RFC-0002 `CanonicalRecord` reference implementation carries lifecycle state and structural lineage invariants, but it does not define one universal business-validation/approval field applicable to every record type.

P4.03 therefore does not fabricate a generic `Validated` or `Approved` status. `SourceValidationState.STRUCTURALLY_VALIDATED` means only that the displayed object comes from a Canonical/Relationship lineage whose structural invariants were admitted by the existing runtime model. The UI states textually that this is not business approval and not Organizational Authority.

Capability- or product-specific validation semantics remain owned by their respective governed sources and later workspace surfaces. If such semantics are displayed later, they must be derived from that source's canonical contract rather than retrofitted into the P4.03 generic inspector.

## 7. Authorization and data-governance disposition

`CurrentSourceAuthorization` is a bounded reference-harness handoff from an owning current authorization/data-governance boundary; it is not an IAM, PDP/PEP, entitlement store, policy language or new stable authorization contract.

The P4.03 inspector consumes exactly one explicit allow decision for the requested Actor/represented Actor, Organization and stable Subject. Missing, deny, duplicate or actor-mismatched decisions fail closed.

Purpose, permitted-use right, classification, minimization and other source-specific constraints remain the responsibility of the applicable source-access boundary (for example the P3.07 composition semantics where those constraints exist). P4.03 does not invent generic handling constraints for Canonical Records that do not possess them.

This bounded split satisfies R9's required independent current-authorization check without prematurely designing a universal authorization mechanism.

## 8. Functional role cross-review

Cross-review followed the repository iterative-completion rule. These reviews are execution-quality evidence, not formal approval or delegated decision authority.

### Iteration 1 — Architecture / canonical semantics

Finding: a presentation inspector could accidentally collapse Subject, Head, Effective and exact historical Version into one notion of "current", or flatten Typed Relationships into unversioned graph links.

Disposition:

- Subject references resolve to Head explicitly while Effective Version is resolved separately at an explicit evaluation time;
- exact-Version references remain exact and immutable;
- missing/ambiguous Effective states remain explicit;
- Relationship Identity, Relationship Version and Relationship Type Version are all preserved;
- endpoint SubjectIdentity/VersionIdentity roles and direction remain explicit;
- no Event/provenance/action semantics were pulled forward from P4.04/P4.05.

### Iteration 2 — Security / tenant sovereignty / authority

Finding: the first implementation checked current authorization before exact-Version disclosure but resolved source candidates before authorization. Although content stayed hidden, `SOURCE_UNAVAILABLE` versus `SOURCE_AMBIGUOUS` could still become an object/source multiplicity oracle for an unauthorized caller.

Disposition:

- reordered the boundary to require one current Actor/Organization/Subject allow decision before governed source existence or multiplicity is evaluated;
- added dedicated regression tests for unauthorized unknown-subject discovery;
- source membership is still independently checked from source-owned `OrganizationScope`, never from the authorization handoff or `Identity.scope`;
- relationship edges require separate relationship authorization and omitted edges expose no metadata/count;
- exact-Version existence is checked only after source access is authorized.

### Iteration 3 — Operator UX / accessibility / semantic honesty

Finding: raw object DTOs would not prove that an operator can distinguish Head from Effective Version, identify authority/owner/scope, understand an exact historical selection, or recognize blocked/ambiguous states without visual inference.

Disposition:

- renderer emits textual Subject/Relationship identity, displayed Version basis, Head, Effective status/evaluation time, Organization, owner, lifecycle and authority/source/scope;
- history uses a captioned semantic table and explicit `Displayed` / `Head` / `Effective` labels;
- blocked state uses `role="alert"` and carries no governed source metadata;
- empty relationship context says only that no authorized context is available and does not expose hidden counts;
- all governed display values are HTML escaped;
- static demo makes both record and relationship inspection visibly reviewable without selecting an application framework.

### Iteration 4 — Engineering / governance / regression integrity

Finding: P4.03 must not turn the P4.02 semantic navigation layer into a public resolver/service contract, select a durable graph/read-model stack, create a new capability, or overstate validation/approval semantics.

Disposition:

- kept `canonical_inspection.py` internal and unexported;
- selected no HTTP/API/wire/frontend/database/network/storage/graph technology;
- added no mutation/gate/Product Contract dependency;
- used existing CanonicalLineage and TypedRelationshipLineage semantic owners rather than cloning Kernel semantics;
- limited generic validation wording to structural lineage validation and explicitly disclaimed business approval/Organizational Authority;
- no RFC, ADR, capability-lifecycle or Product Contract change is required on current evidence;
- complete reference CI remains green after the security remediation and static demo addition.

No material objection remained after iteration 4. Further expansion now belongs to P4.04+ rather than speculative generalization of P4.03.

## 9. Technology / ADR disposition

The implementation uses only existing reference-model modules plus Python dataclasses/enums and standard-library HTML escaping.

It establishes no:

- public/stable package surface;
- frontend framework or design-system contract;
- HTTP route/deep-link or API/BFF topology;
- stable wire/serialization format;
- IAM/session/authentication mechanism;
- authorization policy language or entitlement store;
- graph database;
- durable workspace/read-model/cache persistence;
- service/deployment topology.

The Phase 4 ADR gate is therefore not crossed and no new ADR is required for P4.03.

## 10. Validation

GitHub Actions `Reference Python CI` run `#123` passed on PR `#47` after the source-resolution security remediation and static demo addition.

The full reference suite passed under Python `3.12.13`:

```text
Ran 436 tests in 1.013s
OK
```

The first P4.03 CI run exposed one incorrect new test assertion: the test forbade the literal phrase `hidden relationship count` even though the renderer stated the safe negative meaning `No hidden relationship count is disclosed.` The assertion was corrected to verify the actual security invariant — absence of unauthorized relationship identity/type/edge metadata — without changing runtime behavior.

Subsequent cross-review then found and fixed the more material pre-authorization source-status oracle described in Iteration 2. Dedicated regression tests cover the corrected ordering.

## 11. Deferred scope and exit decision

Current bounded reference records are admitted as `AuthorityMode.NATIVE`; P4.03 therefore proves the authority/source presentation shape with Native authority and does not fabricate an external authoritative-source integration merely to exercise the other RFC-0002 authority modes.

P4.03 intentionally does not provide:

- Event timeline, causation/correlation, provenance or reconstruction — P4.04;
- Governed Execution actions, approval/gate UX or canonical mutation — P4.05;
- Document/Artifact handling specifics — P4.06;
- Knowledge/Search discovery semantics — P4.07;
- broad cross-capability rights/minimization UX hardening — P4.09;
- final Phase 4 accessibility/usability fitness baseline — P4.10.

**P4.03 = PASS / Complete.**

The bounded Canonical Record / Relationship inspection experience satisfies the declared roadmap behavior without crossing a new RFC/ADR/public-contract/lifecycle boundary.

The next canonical work item is:

> **`P4.04 — Version, Event, provenance and reconstruction experience`.**
