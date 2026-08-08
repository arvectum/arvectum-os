# P4.02 — Organization Context, Identity and Scoped Navigation Shell

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P4.02 — Organization context, identity and scoped navigation shell`
Phase: `Phase 4 — Workspace / Operator Experience`
Milestone target: `M4 — Coherent governed workspace baseline`
Result: **`PASS — the bounded internal workspace shell makes Organization and attributable Actor context explicit, preserves Subject-versus-exact-Version navigation semantics, fails closed on unresolved or inconsistent Organization scope, keeps presentation state non-authoritative, and remains reversible without selecting a frontend/API/IAM/durable-read-model boundary.`**

## 1. Purpose and decision level

P4.02 makes the P4.01 workspace boundary executable through the smallest internal reversible navigation shell.

The implementation deliberately stops before record inspection, authorization policy implementation, product workflows, stable routes, public APIs or durable UI infrastructure. It exists to prove that an operator-facing shell can carry the already Accepted identity, Organization and version-reference semantics without becoming a second source of organizational authority.

This artifact is a subordinate implementation/review record. It does not amend the Constitution or an Accepted RFC, create a new Platform Capability, change CAP-001 through CAP-004 lifecycle, create or promote a Product Contract, select a frontend framework, establish an IAM/SSO integration, or create a stable public interface.

## 2. Canonical authority checked

P4.02 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral Kernel, governed state, product/platform separation, security/isolation invariants, technology independence and scoped conformance;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, Subject-versus-Version reference semantics, exact historical resolution and projection non-authority;
5. RFC-0003 — Principal/Actor semantics, Organization sovereignty scope, no ambient cross-Organization authority, deny-by-default/fail-closed behavior and separation of identity/authentication from authorization and Organizational Authority;
6. RFC-0004 — Product Contract as the explicit product/platform boundary and the rule that product/contract context does not itself grant permission or authority;
7. `docs/adrs/README.md` — no applicable Accepted ADR constrains this bounded reversible shell;
8. [`P4.01 operator journeys / workspace boundary / IA review`](P4-01-operator-journeys-workspace-boundary-information-architecture.md) — implementation handoff and executable evidence requirements;
9. canonical Roadmap `2.11.0` and Phase 4 roadmap `1.1.0` at task start.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was identified.

## 3. Implemented boundary

The bounded shell follows this invariant:

```text
ActorContext
  ├── actual Principal
  └── explicit Organization
          ↓
  open workspace shell
          ↓
┌───────────────────────────────────────┐
│ non-authoritative presentation state  │
│                                       │
│ Organization + Actor                  │
│ Discover / Records / Executions       │
│ Evidence / Documents / Knowledge      │
│ Subject OR exact Version reference    │
└───────────────────────────────────────┘
          ↓
no authorization minted
no Organizational Authority minted
no Product Contract validity minted
no canonical mutation path
no route/API schema stabilized
```

If the Organization context cannot be resolved or an optional entry context is inconsistent with the Actor Organization, the shell returns a blocked state with no governed content and no enabled navigation rather than choosing a default Organization.

## 4. Executable implementation

### 4.1 `workspace_shell.py`

`reference/python/arvectum_os_ref/workspace_shell.py` introduces only internal presentation semantics:

- `WorkspaceDestination` — exactly the P4.01 domain-neutral IA destinations: `Discover`, `Records`, `Executions`, `Evidence`, `Documents`, `Knowledge`;
- `WorkspaceShellState` — immutable disposable presentation state carrying explicit Organization, attributable Actor, current destination and optional governed navigation reference;
- `WorkspaceBlockedState` — textual fail-closed state with governed content and navigation disabled;
- `SubjectNavigationReference` — navigation to one logical Subject without claiming an exact current version;
- `ExactVersionNavigationReference` — navigation to one exact immutable Version Identity;
- `WorkspaceProductContext` — optional future entry context whose presence grants no permission, Organizational Authority or Product Contract validity;
- `open_workspace_shell()` — resolves an explicit Actor-scoped shell or returns blocked state; it never invents a default Organization;
- `navigate_workspace()` — changes presentation/navigation state only and preserves Actor/Organization attribution;
- `render_workspace_shell_html()` — a zero-dependency inert HTML adapter with textual Organization/Actor/reference/blocked-state semantics and HTML escaping.

The module intentionally does not expose authorization decisions, permissions, approval state, canonical mutation methods, Head resolution, Effective-Version inference, counts/facets/results inventories, network access, persistence, HTTP routes or a frontend framework.

### 4.2 Standalone visible demo

`reference/python/examples/p4_02_workspace_shell_demo.py` renders the bounded shell into a standalone static HTML document using only the Python standard library.

It exists as visual reference evidence, not as a server or UI architecture decision. It establishes no route/deep-link contract, client framework, BFF/API, session mechanism or public package surface.

From `reference/python`:

```sh
python examples/p4_02_workspace_shell_demo.py > /tmp/arvectum-p4-02.html
```

The resulting file can be opened locally in a browser.

## 5. P4.01 handoff evidence matrix

| P4.01 P4.02 requirement | Executable evidence |
|---|---|
| unresolved Organization fails closed | `test_unresolved_organization_fails_closed_without_default` |
| wrong-Organization navigation cannot expose protected object metadata | `test_wrong_organization_navigation_reference_is_rejected`; exception text omits foreign object/Organization identifiers |
| Actor attribution and Organization survive navigation | `test_navigation_preserves_actor_and_organization_context` |
| domain-neutral navigation only | `test_open_shell_exposes_only_p4_01_domain_neutral_destinations` |
| Subject and exact Version references remain distinct | `test_subject_and_exact_version_references_remain_distinct` |
| exact historical Version is not redirected to Head | `test_exact_historical_version_is_preserved_without_head_redirect` |
| presentation state cannot create authorization or Organizational Authority | `test_presentation_state_cannot_create_authorization_or_authority` |
| shell navigation does not expose derived counts/inventories that could leak inaccessible objects | `test_shell_navigation_has_no_counts_or_protected_content_inventory` |
| optional Product context is context only | `test_product_entry_context_is_scope_checked_and_non_authoritative` |
| critical context/blocked meaning is textual, not color-only | `test_rendered_shell_has_textual_context_and_no_route_contract`; `test_blocked_render_has_text_meaning_and_no_navigation` |
| presentation rendering does not inject raw identity values into HTML | `test_renderer_escapes_identity_values` |

## 6. Authority and security disposition

### 6.1 Identity is not permission

The shell reuses `ActorContext` and `OrganizationScope`; it does not add roles, entitlements, permission flags or Organizational Authority to `Identity`, `Principal`, `ActorContext` or presentation state.

Authentication/identity presence therefore remains attribution/context, not authorization.

### 6.2 Organization scope fails closed

An absent/unresolved Actor context produces `WorkspaceBlockCode.ORGANIZATION_UNRESOLVED` with:

- no governed content;
- no navigation;
- no fallback Organization.

An optional product entry context from another Organization produces `CONTEXT_SCOPE_MISMATCH` and the same fail-closed disposition.

A foreign navigation reference raises `WorkspaceScopeViolation`; the error surface deliberately omits foreign object and Organization identifiers so the scope failure is not converted into an existence/metadata disclosure channel.

### 6.3 Exact Version remains exact

`ExactVersionNavigationReference` carries its Version Identity as immutable presentation input. `navigate_workspace()` does not resolve it to Canonical Head or Effective Version and contains no such inference mechanism.

A `SubjectNavigationReference` remains explicitly less precise. Later consequential surfaces must still resolve and pin exact governed versions through the applicable runtime semantics.

### 6.4 Presentation remains non-authoritative

`PresentationAuthority.NON_AUTHORITATIVE` is the only presentation-authority value admitted by the bounded shell.

The shell contains no canonical mutation operation and no authorization/approval state. The HTML renderer also states textually that presentation state is not authorization, Organizational Authority, approval or canonical organizational state.

## 7. Technology and boundary disposition

P4.02 uses Python dataclasses/enums and the standard-library HTML escaping utility only as reversible reference-implementation vehicles.

The implementation does **not** establish:

- a frontend framework;
- a stable URL/deep-link schema;
- REST/GraphQL/gRPC or another public API;
- BFF/service topology;
- browser session or authentication protocol;
- IAM/SSO provider;
- durable workspace/read-model/cache persistence;
- a design-system package contract;
- a stable frontend SDK/package root surface;
- a production deployment topology.

Therefore the existing Phase 4 ADR gate is not crossed and no new ADR is required for P4.02.

## 8. Product Contract and capability disposition

No Product Contract is created by P4.02.

`WorkspaceProductContext` is deliberately context-only preparation for future composition and is not contract admission, validation, permission or authority. The real bounded Product Contract-backed product entry point remains P4.08 scope.

P4.02 does not create `CAP-005 Workspace` and does not promote CAP-001 through CAP-004. They remain `Incubating / Provisional`; visible workspace progress does not imply lifecycle `Active`, production readiness, Stable Product Contract status, SLA/support or full-platform conformance.

## 9. Functional role cross-review

Cross-review followed the repository iterative-completion rule. These reviews are execution-quality evidence, not formal approval or delegated authority.

### Iteration 1 — Architecture / product / governance

Finding: a shell implementation could accidentally stabilize a public route/API model, become a fifth capability, or turn future product-entry context into a hidden Product Contract substitute.

Disposition:

- kept the implementation internal and unexported from the provisional package root;
- used semantic destination/reference types rather than URL routes;
- kept product context optional and explicitly non-authoritative;
- added no product-domain screen, queue, role or workflow taxonomy;
- created no new capability or lifecycle claim.

### Iteration 2 — Security / privacy / tenant sovereignty

Finding: rejecting a cross-Organization reference could still leak the foreign target through exception details, and renderer output could expose an injection surface if identity display values were treated as trusted markup.

Disposition:

- cross-scope errors intentionally omit candidate identifiers;
- unresolved/mismatched scope blocks all governed content/navigation;
- no counts/facets/object inventory exists at shell level;
- all rendered identity/reference values are HTML escaped;
- executable negative tests cover these properties.

### Iteration 3 — Operations / UX / accessibility

Finding: a technically correct shell was insufficient if critical context and blocked state were visible only as internal dataclasses or visual styling.

Disposition:

- Organization, Actor and Subject/exact-Version reference kind are emitted as text;
- blocked state uses explicit textual meaning and `role="alert"`;
- current navigation uses `aria-current` and a labeled navigation region;
- a standalone static HTML demo was added so the boundary is visibly inspectable without selecting an application framework or route contract.

### Iteration 4 — Engineering / regression integrity

Finding: the first PR CI run exposed two stale P3.12 closure tests that still hard-coded Roadmap `2.9.0` and required Phase 4 to remain `Draft`, contradicting the already-canonical P4.01 activation state. All P4.02 tests themselves passed.

Disposition:

- repaired the P3.12 guards to preserve the actual historical invariant — M3 scope and lifecycle distinction — while allowing later phases to progress canonically;
- did not weaken M3 closure/capability-lifecycle checks;
- reran the complete reference Python CI successfully.

No material objections remained after iteration 4; further refinement would be disproportionate before R9 and the P4.03–P4.07 workspace surfaces provide additional evidence.

## 10. Validation

GitHub Actions `Reference Python CI` run `#109` passed on PR `#45` after the regression-guard repair.

The full reference suite passed, including all P4.02 shell tests and the retained Phase 1–3 architecture fitness/regression evidence.

The earlier run `#107` failed only because two historical P3.12 tests encoded obsolete later-phase state (`ROADMAP 2.9.0` / Phase 4 `Draft`); P4.02's new tests were green in that run. The repair changes those tests from later-phase state freezing to historical M3 invariant checks.

## 11. Exit decision

**P4.02 = PASS / Complete.**

The required Organization/identity shell semantics are executable and bounded enough to proceed to the mandatory engineering gate:

> **`R9 — Workspace Boundary Review`.**

R9 should review the accumulated P4.01 + P4.02 boundary before P4.03–P4.05 expand the shell into governed record, provenance and execution surfaces. In particular, R9 should confirm that the internal navigation types/render adapter have not become an accidental public interface and that no authority, tenant, product or technology boundary has drifted.
