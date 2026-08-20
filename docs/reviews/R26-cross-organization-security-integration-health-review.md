# R26 — Cross-Organization Security / Integration Health Review

Status: `Complete / PASS`
Date: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` review
Trigger: after `P8.06`, before `P8.07`
Reviewed contour: `P8.01` through `P8.06`, with inherited P7 access/recovery evidence where Phase 8 depends on it
Operating scope: `Persistent Internal / owner-operated`, one governing Organization
Parent phase: [`Phase 8 — Ecosystem and External Integration`](../roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md)

## 1. Purpose

R26 is the cross-cutting security and integration-health gate after Phase 8 established the bounded EIS authoritative-source case, explicit authority/rights boundary, Provisional integration contract, real read-only external validation, external Event/replay/reconciliation semantics and one real separately maintained external product/extension consumer.

The gate asks whether those results compose without creating a hidden cross-Organization channel, ambient privilege, secret leakage, competing external authority, replay/duplicate risk, dependency inversion, stale-version acceptance or unsafe recovery behavior, and whether the current contour is healthy enough to proceed to `P8.07 — Portability/export/migration/customer-handover interoperability proof`.

The title intentionally does **not** mean that Phase 8 has already proved realistic multi-Organization tenant isolation. P8.01–P8.06 exercise one governing Organization only. R26 reviews the current one-Organization contour for cross-Organization leakage/bypass hazards and verifies that no current mechanism silently claims or requires a second Organization. Realistic multi-Organization isolation remains the explicit responsibility of P8.08 if and when a second Organization is actually activated into scope.

R26 is an engineering/governance review. It is not customer Production approval, full multi-tenant certification, Product Contract stabilization, Platform Capability activation, public/stable integration approval, SLA/support commitment, portability claim or broader conformance declaration.

## 2. Authority baseline checked

Checked before and during review:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with acceptance evidence;
- RFC-0001 — Organization sovereignty, explicit contracts, external authority/source-of-truth preservation, security/isolation, failure-closed behavior, reconstruction and stable-boundary constraints;
- RFC-0003 — Identity/Authentication/Authorization/Organizational Authority separation, Organization scope, deny-by-default, least privilege, Data Governance, cross-Organization transfer restrictions, secret handling and recovery/portability authority boundaries;
- RFC-0004 — Product Contract/extension boundary, no hidden coupling, no permission from contract/dependency presence and product/platform ownership separation;
- RFC-0005 — Governed Execution, exact version pinning, authorization/authority/data-governance gates, uncertain outcomes and side-effect-safe retry/recovery;
- RFC-0006 — canonical Event/provenance semantics, ingress/egress evidence, append-only history, duplicate/replay behavior and non-canonical telemetry distinction;
- RFC-0007/RFC-0008 where relevant to the prohibition on silently promoting transient/external material into validated Knowledge or portable governed artifacts beyond explicit rights;
- Accepted ADRs — none exist; `docs/adrs/` contains only the ADR process/index/template, so no permanent multi-tenant persistence, IAM, external transport, connector/plugin, registry or public integration technology has been canonically selected;
- canonical master and Phase 8 roadmap sequencing;
- P8.01–P8.06 canonical contracts/reviews/reference implementation and existing focused/full CI evidence;
- inherited P7.04 persistent-access and R23/P7.09 recovery evidence for temporary authorization, revocation, secret exclusion and recovery semantics.

No higher-authority conflict was found for the declared bounded scope.

## 3. Scope truth: what is and is not cross-Organization evidence

The currently activated Phase 8 contour contains:

- one governing Organization: `ООО «Арвектум»` / the bounded `arvectum` Organization scope used by the external consumer proof;
- one external authoritative system relationship: ЕИС / `zakupki.gov.ru`, read-only, with EIS remaining `External Reference` for source facts/documents;
- one separately maintained external product consumer: `arvectum/creative-test-agent`, still owned within the same governing Organization and connected only through an exact Provisional Product Contract and declared CAP-004 dependency;
- negative fail-closed checks against Organization mismatch, hidden/private coupling and excess access scope.

Therefore R26 may conclude that the existing integrations do not expose a demonstrated cross-Organization bypass, but it **must not** conclude that persistent tenant isolation, indexes/caches/search, support/admin paths, logs/metrics/errors, handover/import or real two-Organization operation are validated. Those are reserved for P8.07/P8.08 according to the roadmap.

This scope correction is a required part of the PASS rather than a caveat hidden after it.

## 4. Functional cross-review iterations

Functional review closed in five iterations of the maximum seven.

### Iteration 1 — scope / claim integrity

Result: `REVISE`.

Material objection:

The R26 name can be misread as a multi-Organization certification even though P8.01–P8.06 intentionally use one Organization, and P8.08 explicitly owns realistic multi-Organization validation.

Disposition:

- define R26 as a security/integration-health review of the current one-Organization contour with cross-Organization **bypass/leakage guard analysis**;
- treat Organization-mismatch negative tests as semantic fail-closed evidence, not as proof of tenant-storage isolation;
- preserve P8.08 as the only roadmap step that may establish realistic multi-Organization isolation when a second Organization is actually in scope;
- prohibit any Production, universal multi-tenancy or customer-isolation claim from this review.

Result after revision: `PASS` for scope/claim integrity.

### Iteration 2 — Organization isolation / least privilege / secrets / external authority

Result: `PASS`.

Findings:

- P8.02 keeps Identity, Authentication, Authorization, Organizational Authority and Data Governance distinct and deny-by-default;
- P8.03 permits only the exact owner-operated read-only EIS revalidation case and explicitly denies second-Organization/customer use, mutation, redistribution, secret persistence and TLS weakening;
- P8.04 reuses the real M7 Organization/operator continuity rather than minting a synthetic authority context;
- P8.04 uses the actual P7.04 least-privilege authorization path; the temporary exact grant is bound to the operation/resource/access path and is revoked after success and denial paths;
- reusable EIS credential material remains outside canonical history/evidence/logs and verified TLS is mandatory;
- EIS remains authoritative as `External Reference`; local comparison/evidence does not become a competing source of truth;
- P8.06 requires exact Organization equality across source declaration, Product Contract and capability request; Organization mismatch fails closed;
- P8.06 access is exactly `read` for purpose `creative-test-audit-reconstruction`, classification `internal`; Product Contract/dependency/install presence grants no Authorization or Organizational Authority;
- the external consumer declaration is disabled by default and does not activate reliance merely by existing.

No current path was found that turns identity, source possession, Product Contract existence, dependency resolution or restored evidence into ambient permission or Organizational Authority.

### Iteration 3 — provenance / duplicate / replay / uncertainty / recovery

Result: `PASS`.

Findings:

- P8.05 keeps transport delivery separate from canonical Event admission;
- repeat delivery of the same source occurrence does not create duplicate canonical truth, while a genuinely distinct occurrence is not collapsed merely because bytes match;
- occurrence time and recording time remain distinct;
- an unknown external outcome remains `Uncertain` and blocks blind retry;
- reconciliation is append-only and attributable; `ConfirmedSucceeded` blocks duplicate-risk retry, `StillUncertain` remains blocked and `ConfirmedNotApplied` permits only a new Governed Execution with a new retry token;
- historical reconstruction is pure and does not call live retrieval/effect paths;
- inherited P7.09/R23 recovery rules already prohibit restore/restart/rollback from granting authority or replaying historical external effects;
- reusable secrets are excluded from governed backup/handoff and must be reprovisioned separately after recovery;
- P8.04 reconstruction has zero additional EIS calls and its temporary technical grant is revoked, so recovery of the evidence cannot resurrect that grant.

No integration-health path was found where duplicate/replay/recovery silently converts old evidence into a new external effect or current authority.

### Iteration 4 — dependency direction / disable / downgrade / version drift

Result: `PASS with an explicit bounded downstream requirement`.

Findings:

- P8.06 accepts only `DeclaredPlatformContract` and rejects internal tables, private imports/modules, undocumented endpoints, private event streams and implicit shared mutable state;
- Creative Test Agent remains owner of creative schemas, workflows, scoring, reports/UX and model/prompt choices; platform dependency direction therefore remains product → declared platform contract, not platform → product business logic;
- source commit/blob, consumer version, Product Contract Version, CAP-004 identity/version/operation and current access scope are exact; semver inference and automatic fallback are absent;
- initial onboarding fails closed on missing, ambiguous, incompatible or undeclared provider evidence and on contract/request/source mismatch;
- operational reliance state is explicit: `Onboarded → Disabled → Removed`; disabled/removed receipts fail `require_external_consumer_enabled`; removal requires prior disable;
- upgrade requires a new immutable consumer version, new source commit and new Product Contract Version and reruns exact onboarding/dependency resolution.

Important interpretation required for health/recovery:

`ExternalConsumerOnboardingReceipt` is point-in-time **derived evidence**, explicitly not permission, authority, registry state, lifecycle state or canonical truth. Therefore an old `Onboarded` receipt must not be interpreted as proof that a provider/contract is still currently compatible after governance/version drift or after recovery. Any future runtime mechanism that turns this bounded proof into ongoing operational reliance must re-resolve the current effective Product Contract/provider evidence before use/resumption and fail closed on drift, deprecation/retirement, revocation or incompatibility.

No current production/runtime reliance service exists that makes the old receipt itself authoritative, so this is not an unclosed R26 implementation defect. It is a mandatory downstream design guard for any such activation. If P8.09/P8.11 introduces persistent integration state or automatic resumption, this requirement must become executable and tested there rather than being inferred from the P8.06 receipt.

### Iteration 5 — incident posture / stable-boundary / ADR and sequencing

Result: `PASS`.

Findings:

- Phase 8 adds no reusable secret to canonical recovery packages;
- incident recovery preserves the external-source-of-truth distinction and does not synthesize current EIS freshness from stale evidence;
- P8.05 uncertainty/reconciliation semantics compose with the existing P7 incident model rather than introducing a second retry/recovery model;
- P8.06 source/dependency evidence is immutable and version-specific, so recovery may reconstruct what was accepted historically without silently upgrading it;
- no public/stable API, multi-tenant datastore, external Event broker, connector registry/marketplace, customer export format, persistent third-party credential service or externally relied upon integration protocol has been selected;
- no concrete ADR trigger is crossed by R26 itself;
- P8.07 remains the correct next action; P8.08 remains the later multi-Organization isolation proof and must not be skipped by claiming R26 already covered it.

No material objection remains within the declared scope.

## 5. Security / integration-health evidence matrix

| Review property | Primary evidence | R26 result |
|---|---|---|
| explicit governing Organization | P8.02 / P8.03 / P8.04 / P8.06 | `PASS — one Organization only` |
| realistic two-Organization tenant isolation | not exercised yet | `NOT PROVEN — P8.08` |
| foreign Organization mismatch | P8.03 contract + P8.06 negative checks | `PASS — fail closed semantically` |
| least privilege / default denial | P8.02 + P7.04 + P8.04 + P8.06 | `PASS` |
| Authentication ≠ Authorization ≠ Organizational Authority | P8.02 / P8.04 / P8.06 | `PASS` |
| temporary live-read authorization cleanup | P8.04 remediation + P7.04 | `PASS — grant revoked` |
| reusable-secret exclusion | P8.02 / P8.03 / P8.04 + R23 | `PASS` |
| TLS downgrade | P8.02 / P8.03 / P8.04 | `DENIED / fail closed` |
| external source-of-truth preservation | P8.03 / P8.04 | `PASS — EIS remains External Reference` |
| duplicate ingress | P8.05 | `PASS — no duplicate canonical truth` |
| late/out-of-order occurrence semantics | P8.05 | `PASS` |
| uncertain external outcome | P8.05 + P7.09 | `PASS — reconciliation required` |
| blind retry after uncertain/succeeded outcome | P8.05 | `DENIED` |
| historical replay external effect | P8.05 + R23 | `DENIED` |
| hidden/private product-platform coupling | P8.06 | `DENIED` |
| shared mutable product/platform state | P8.06 | `DENIED` |
| exact contract/provider/version resolution | P8.06 | `PASS` |
| semver/automatic provider fallback | P8.06 | `ABSENT / correctly rejected` |
| explicit disable/remove | P8.06 | `PASS` |
| upgrade without new immutable version/contract | P8.06 | `DENIED` |
| stale historical onboarding receipt as current authority | RFC-0003/0004 + P8.06 receipt semantics | `DENIED BY INTERPRETATION; future runtime revalidation required` |
| recovery restoring reusable secrets/authority | R23 / P7.09 | `DENIED` |
| recovery/reconstruction making new live EIS call | P8.04 / P8.05 | `DENIED` |
| current ADR/stable-boundary trigger | R25 / P8.03 / P8.06 / R26 | `NONE` |

## 6. Cross-Organization leakage analysis

The reviewed contour has no second real Organization, so R26 limits its conclusion to paths that could accidentally erase Organization scope today.

No such material path was found in the reviewed Phase 8 surface:

- source, Product Contract and request Organization must match in P8.06;
- consumer Identity is scoped to its Organization;
- dependency identity remains platform-scoped rather than being mistaken for consumer authority;
- Product Contract/dependency presence does not grant data access;
- P8.03 denies second-Organization and customer use by contract;
- P8.04 binds the live run to the existing owner Organization and exact temporary technical grant;
- P8.05 evidence/reconciliation does not create a transfer primitive;
- no current shared mutable table/index/cache/search surface is introduced by P8.06;
- no external callback path may redefine Organization authority merely by supplying an identifier.

What remains intentionally unproven until P8.08 includes real storage/query/index/cache/log/error isolation across two Organizations, same external identifier collision, admin/support isolation, cross-org import/handover, revocation across tenant boundaries and callback/ingress spoofing under realistic second-Organization evidence.

## 7. Incident / recovery impact

Phase 8 does not require a new recovery architecture before P8.07.

The composed rule is:

1. recover/reconstruct immutable historical governed state and evidence;
2. do not restore reusable secrets or expired/revoked technical authority from canonical backup/handoff;
3. do not infer current external freshness from historical EIS evidence;
4. do not replay historical external effects;
5. preserve `Uncertain` as reconciliation-required;
6. re-establish current credentials/Authorization/Data Governance through their current governed procedures;
7. treat historical Product Contract/provider/onboarding evidence as historical version evidence, not automatic current compatibility;
8. if future operational reliance is resumed automatically, re-resolve current dependency/contract state before use and fail closed on drift.

This composes with R23/P7.09 and introduces no competing recovery model.

## 8. Contract/version drift and integration downgrade disposition

Current protection is deliberately exact rather than dynamic:

- P8.03 EIS contract remains `Provisional 0.1.0` and `PROVISIONAL_INTERNAL_ONLY / NO_STABLE_SURFACE`;
- P8.06 Creative Test Agent Product Contract remains `Provisional 0.1.0`;
- CAP-004 remains `Incubating / Provisional`, exact contract version `1.0.0` in the P8.06 proof;
- nearby provider versions and undeclared operations are not accepted;
- a consumer upgrade cannot reuse the old consumer version/source commit/Product Contract Version;
- disable/remove are explicit and fail closed for the bounded receipt state.

R26 does not create an automatic provider-discovery or background revalidation service. Such a service would be new operational behavior and may create a stable-boundary/ADR/security decision depending on its scope. Until then, point-in-time receipts remain evidence only.

## 9. ADR / stable-boundary disposition

`ADR required by R26 itself: NO`.

The reviewed Phase 8 mechanisms remain bounded, private/provisional and reversible. No permanent implementation choice is made for:

- multi-Organization persistence/isolation topology;
- external identity federation/IAM/trust protocol;
- Event broker/transport/inbox/outbox infrastructure;
- public connector/plugin packaging/discovery;
- external consumer registry/marketplace;
- customer-facing export/migration format;
- persistent third-party secret vault;
- automatic dependency discovery/update service;
- public/stable SDK/API/wire protocol.

Reopen ADR/stable-boundary review if later Phase 8 work makes one of those mechanisms cross-product, externally relied upon, materially constraining or expensive to reverse.

## 10. Bounded downstream requirements

R26 leaves no blocker before P8.07, but the following requirements must remain visible downstream:

1. **P8.07:** any activated export/handover must preserve Organization, rights/classification/retention/provenance and explicit omissions; reusable secrets remain excluded; handover must not grant Organizational Authority or create competing authoritative systems.
2. **P8.08:** do not claim realistic multi-Organization isolation unless a second Organization is genuinely activated and the roadmap’s cross-tenant storage/query/index/log/support/callback tests are exercised. Do not fabricate a second Organization merely to close the task.
3. **P8.09/P8.11:** if integration onboarding becomes persistent runtime reliance or auto-resumes after restart/recovery, current Product Contract/provider/access governance must be revalidated before use. A historical `Onboarded` receipt alone is insufficient.
4. **P8.09/P8.11:** any new privileged support/admin path must remain explicit, attributable, least-privilege and non-ambient with respect to customer/content access.
5. **P8.10:** no security, compatibility, lifecycle, Production, support or conformance claim may exceed the exact evidence above.
6. **P8.11/R28:** re-check concrete ADR/stable-boundary triggers and accidental public surface after the later portability/multi-org/operator integration work exists.

These are sequencing constraints, not deferred permission to bypass existing controls.

## 11. Gate result

**R26 result: `Complete / PASS`.**

P8.01–P8.06 compose into a healthy bounded external-integration contour for the declared one-Organization `Persistent Internal / owner-operated` scope. The reviewed paths preserve explicit Organization scope, least privilege/default denial, secret boundaries, external source authority, append-only provenance, duplicate/replay/uncertainty rules, declared product/platform dependency direction, exact version resolution and fail-closed disable/upgrade behavior. Existing incident/recovery rules do not resurrect secrets, authority, stale freshness or historical external effects.

The PASS is deliberately narrower than the review title might suggest: **realistic multi-Organization tenant isolation is not yet proven** and remains P8.08 work when a second Organization is genuinely in scope. Likewise, an old P8.06 onboarding receipt is historical derived evidence, not a current compatibility/permission token; any future persistent runtime reliance must revalidate current governance before use/resumption.

No current defect requires another P8.01–P8.06 implementation step, and no R26-specific ADR is required.

Next canonical action:

> **P8.07 — Portability/export/migration/customer-handover interoperability proof.**
