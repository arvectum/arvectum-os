# P7.04 — Persistent Access Implementation Cross-Review

Status: `Repository implementation PASS / selected-Mac closure pending`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Reviewed scope: `P7.04 — Persistent identity/operator/service access + least-privilege operations`
Implementation: [`P7.04 Persistent Identity / Operator / Service Access`](../implementation/P7-04-PERSISTENT-IDENTITY-ACCESS.md)
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Repository implementation PR: `#35`

## 1. Purpose

This functional cross-review evaluates the P7.04 repository implementation from architecture, identity/authority, security, operations and governance perspectives before selected-Mac operational proof.

It is not R22, not an ADR acceptance, not a Platform Capability lifecycle transition and not a production-readiness approval.

## 2. Authority baseline checked

Checked:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` per the canonical RFC Index;
- RFC-0002 opaque identity / canonical semantic boundary;
- RFC-0003 Identity, Authentication, Authorization, Organizational Authority, Organization scope, least privilege and secret-handling requirements;
- RFC-0005 Governed Execution and consequential approval boundary;
- RFC-0006 canonical evidence / non-canonical operational evidence distinction;
- P7.01 baseline `1.0.1`;
- P7.02 and P7.03 `Complete / PASS`;
- canonical Phase 7 roadmap and root roadmap;
- Accepted ADRs — none select IAM, SSO, RBAC, credential vault or remote-administration topology.

No higher-authority conflict was found.

## 3. Functional review iterations

### Iteration 1 — identity / authorization / authority semantics

Result: `REVISE`.

Material concern:

P7.04 must not solve persistent operational access by turning the RFC-0002/RFC-0003 `Identity` value into a mutable account/role/permission object. It also must not create a successful authentication path that implicitly becomes Organizational Authority.

Disposition:

- keep canonical `Identity` unchanged and opaque;
- introduce a separate operational registry keyed by principal identity;
- represent human/service kind in the operational principal record rather than in the identity value;
- make authentication credential verification separate from authorization grant matching;
- make every allowed access decision explicitly declare `operational_access_only=true`, `organizational_authority_satisfied=false` and `consequential_approval_satisfied=false`.

Result after revision: identity, authentication, authorization and authority remain separate.

### Iteration 2 — P6 continuity / persistent attribution

Result: `REVISE`.

Material concern:

A new P7 owner identity would break continuity with the real P6.05-L4 Organization/operator proof and create multiple competing owner identities for the same bounded contour.

Disposition:

- add an exact-shape P6.05-L4 continuity loader;
- require source Organization `ООО «Арвектум»` semantics and human `owner-operated` principal;
- reject P6 source context if it contains authorization grants, delegations, authority claims or authentication evidence not permitted by that bootstrap contract;
- reuse the exact existing Organization and human Principal identities;
- create at most one persistent service Principal when operationally significant machine execution needs attribution;
- make repeated bootstrap reuse that same service identity rather than regenerating it;
- issue zero credentials and zero grants merely from continuity bootstrap.

Result after revision: attributable human continuity is preserved and machine execution gains a separate persistent attributable identity without identity replacement.

### Iteration 3 — least privilege / secrets / revocation

Result: `REVISE`.

Material concerns:

1. role/wildcard semantics could accidentally create ambient admin;
2. reusable credential plaintext must not enter the registry, Git, ordinary logs or P7.03 governed backups;
3. rotation and revocation must be executable rather than documentary claims.

Disposition:

- fix registry invariant `default_access=deny`;
- reject wildcard `*` operation/resource scopes;
- provide no roles, superuser bit or ambient-admin bypass;
- require exact Organization + operation + resource + explicit access path matching;
- store reusable credential material only in owner-only `secrets/p7-04/*.secret` files;
- store only salted PBKDF2-SHA256 verifier material in `config/p7-04-access.json`;
- keep the P7.03 `secrets/` backup exclusion intact;
- implement credential issue/rotate/revoke, principal disablement and grant revocation;
- delete revoked/rotated active reusable secret files where the adapter owns them;
- fail closed if registry invariants or owner-only/symlink boundaries are violated.

Result after revision: no material least-privilege or secret-lifecycle objection remains at the current bounded owner-local scope.

### Iteration 4 — remote administration / hidden authority path

Result: `REVISE`.

Material concern:

Treating “remote admin” as an implicit trusted mode would create an undocumented bypass around ordinary authorization and could be confused with Organizational Authority.

Disposition:

- make `local` / `remote` an explicit grant dimension;
- selected-Mac proof grants human `runtime.status` on exact `runtime:p7-02` for local and remote paths;
- prove remote `runtime.restart` remains denied without a separate exact grant;
- prove the service Principal can observe exact runtime health but cannot restart the runtime absent its own explicit grant;
- avoid selecting SSH, Tailscale or another transport as a stable platform interface;
- keep host/OS administration an environment concern and never treat it as business/governance authority.

Result after revision: the operational access model has an explicit remote path without a hidden authority path.

### Iteration 5 — repository implementation / proof-contract review

Result: `PASS for repository implementation; selected-Mac proof remains required`.

Architecture:

- `Identity` semantics remain unchanged;
- no product/domain logic is introduced;
- no permanent IAM/SSO/RBAC/vault/remote-admin topology is selected;
- the adapter remains owner-local, single-Organization and reversible;
- no public/stable access API or wire contract is claimed.

Security/privacy:

- deny by default;
- exact Organization/operation/resource/path grants;
- wildcard/ambient-admin behavior rejected;
- credentials separated from verifier registry;
- owner-only file/directory boundaries and symlink checks;
- explicit rotation, credential revocation, grant revocation and principal disablement;
- raw owner/service identities and reusable credential values are excluded from selected-Mac attestation.

Operations:

- P6 human/Organization continuity is executable;
- service identity persists across bootstrap reuse;
- selected-Mac wrapper requires P7.02 `healthy` before and after proof;
- exact P7.02 runtime release must remain unchanged during proof;
- selected-Mac wrapper exercises local and remote paths, service attribution, rotation and grant revocation;
- wrapper declares `canonical_mutation=false` and `external_effects=false`.

Governance:

- allowed technical access never supplies Organizational Authority or consequential approval;
- residual owner/delegated authority and Governed Execution remain outside this adapter;
- no Product Contract, capability lifecycle, Production, SLA/support or conformance promotion occurs;
- ADR trigger remains `NO` at this bounded reversible scope.

Repository evidence:

- focused persistent-access tests: `14/14 PASS` in isolated preparation validation;
- selected-Mac proof-contract fixture tests: `2/2 PASS` in isolated preparation validation;
- GitHub `Reference Python CI` on final repository implementation head: `success`;
- final-head CI run: `32063442269`.

No material repository-side objection remains.

The remaining gate is operational, not architectural: execute the hardened proof on the selected ООО «Арвектум» Mac mini from a clean exact canonical `main`, with the existing healthy P7.02 runtime and the existing owner-local P6.05-L4 context.

Functional review iterations completed: `5 of maximum 7`.

## 4. Current disposition

Repository implementation: `PASS`.

Selected-Mac operational evidence: `PENDING`.

Therefore P7.04 MUST remain `Current` and MUST NOT yet be represented as `Complete / PASS`. P7.05 does not become the current canonical action until the selected-Mac proof, evidence review and roadmap synchronization close P7.04.

## 5. Closure conditions still required

P7.04 may close only after the selected-Mac proof records all required evidence:

- attributable existing human owner/operator identity;
- attributable persistent service identity;
- deny-by-default behavior;
- exact Organization/operation/resource scope;
- explicit local and remote paths;
- denied ungranted remote lifecycle administration;
- no service ambient admin;
- credential rotation fail-closed;
- grant revocation fail-closed;
- reusable credential values absent from registry/attestation;
- Organizational Authority not provided;
- consequential approval not provided;
- healthy P7.02 runtime before/after with unchanged exact runtime release;
- no canonical mutation;
- no external/product effect.

After successful evidence review, this cross-review can receive the final selected-Mac iteration and move to `Complete / PASS`; only then should roadmaps advance to P7.05.
