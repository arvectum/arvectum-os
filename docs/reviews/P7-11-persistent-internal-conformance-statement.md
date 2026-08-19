# P7.11 — Persistent Internal Scoped Conformance Statement

Status: `Scoped`
Version: `1.0.0`
Date: `2026-08-20`
Owner: `ООО «Арвектум»`
Assessment owner: `ООО «Арвектум»`
Decision authority: `Owner of Arvectum OS` under residual authority
Task classification: `platform` with `governance` and `product_contract`
Parent work item: `P7.11 — Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition`
Operating classification: `Persistent Internal / owner-operated`

## 1. Statement

Arvectum OS is assessed as **`Scoped` conformant for the declared Persistent Internal / owner-operated contour only**.

The claim is intentionally narrow. It does not state or imply full-platform conformance, external/customer Production readiness, a supported operating-system matrix, an `Active` Platform Capability, a `Stable` Product Contract, a public/stable API or recovery format, or any SLA/SLO/RPO/RTO/support commitment.

## 2. RFC-0001 conformance axes

The three RFC-0001 axes are recorded separately:

| Axis | Disposition | Rationale |
|---|---|---|
| Subject lifecycle | `Not Applicable` | The assessed subject is an operational deployment contour, not a Platform Capability or Product Experiment. Capability and Product Contract lifecycles are recorded separately in Section 8. |
| Operational environment | `Local` | The assessed environment is a private owner-operated Arvectum deployment. `Persistent Internal / owner-operated` is the operating classification used by Phase 7; it is not an RFC-0001 lifecycle value and is not `Production`. |
| Conformance maturity | `Scoped` | Applicable invariants have been assessed and evidenced for the declared contour. Out-of-scope capabilities, environments and commitments are not included in the claim. |

## 3. Subject and deployment scope

Subject:

- Arvectum OS Phase 7 persistent internal operating contour;
- one Organization: `ООО «Арвектум»`;
- one owner-operated primary runtime on the selected Mac mini;
- private operator access and private runtime/network surfaces only;
- current Phase 7 mechanisms proven through P7.02–P7.10 and R21–R23;
- exact historical release identity preserved where required for governed reconstruction and recovery.

Tenant/Organization scope:

- one Organization sovereignty boundary;
- no ambient or undifferentiated multi-Organization authority context;
- cross-Organization access and customer-tenant operation are outside this statement.

## 4. Workflows and capabilities in scope

In-scope operational surfaces are limited to:

1. supervised persistent runtime lifecycle proven by P7.02;
2. durable governed state, integrity verification and tested backup/restore proven by P7.03;
3. attributable owner/service access, explicit least privilege, credential rotation/revocation and authority separation proven by P7.04;
4. health, minimized non-canonical telemetry, audit visibility and bounded retention proven by P7.05;
5. exact governed deploy/update/rollback/re-update path proven by P7.06;
6. private operator workspace and bounded governed preflight proven by P7.06-UI;
7. Tender Operator reliance under P6.02 `Provisional 0.1.0`, using the declared CAP-001 boundary and retained reconstruction evidence, proven by P7.07;
8. Discount Parser cross-host evidence/reconstruction under P6.06 `Provisional 0.1.0`, using the declared CAP-004 boundary, proven by P7.08;
9. operator incident, uncertain-outcome and recovery behavior proven by P7.09;
10. governed-state host-loss portability and clean-secondary reconstruction proven by P7.10 and reviewed by R23.

CAP-002 and CAP-003 are not materially relied upon by the Phase 7 real-product operational contours and are not included in this operational claim merely because they exist in the capability catalog.

## 5. Data classes, authority and external systems

The contour keeps at least these classes distinct:

- canonical governed state and canonical Events/evidence;
- governance-significant execution/checkpoint state;
- non-canonical telemetry and diagnostics;
- cache, projections and Transient Outputs;
- owner-local configuration and reusable secrets;
- product-owned state reached only through declared Product Contract boundaries;
- external-authority references and product external effects.

Authority handling within the evidence includes:

- `Native` authority for applicable Arvectum OS governed records;
- `External Reference` where an external source remains authoritative, including the EIS evidence retained by the Tender Operator contour;
- product-owned Telegram mutation/outcome semantics under the P6.06 Product Contract rather than a platform claim of Telegram authority.

No recovery, authentication, technical access, Product Contract possession or capability contract creates Organizational Authority or consequential approval.

## 6. Applicable normative basis

This statement assesses the declared contour against the applicable requirements of:

- Constitution `1.2.0`;
- RFC-0001 `1.0.0`, especially Canonical Records, capability/product boundaries, commercial-commitment integrity, decision authority, security/privacy/isolation, portability, scoped conformance and architectural fitness tests;
- RFC-0002 `1.0.0` for stable identity/version, authority and immutable governed-history semantics;
- RFC-0003 `1.0.0` for identity/authentication/authorization/Organizational Authority separation, least privilege, Organization isolation, secrets, portability, migration and failure-closed behavior;
- RFC-0004 `1.0.0` for Product Contract boundaries and lifecycle separation;
- RFC-0005 `1.0.0` for Governed Execution, consequential change, uncertainty and side-effect-safe retry/recovery;
- RFC-0006 `1.0.0` for canonical Events, provenance, evidence and reconstruction;
- RFC-0007 `1.0.0` where Memory/Knowledge non-promotion and transient/observation boundaries apply;
- RFC-0008 `1.0.0` for Document/Artifact identity, exact-version reliance and portable governed meaning.

Accepted ADRs applicable to this contour: `None`.

## 7. Manual and provisional controls

The following controls are deliberately manual, private or provisional and are acceptable within this scoped internal claim:

- owner-operated runtime administration and escalation;
- owner-local credentials and secret reprovisioning;
- private `launchd`-based primary-host supervision;
- private filesystem/tar-based durable-state and handoff mechanisms;
- manual recovery/bootstrap of a clean secondary environment;
- owner-controlled exact-release source retrieval;
- private browser/operator workspace and local access path;
- private cross-host Discount Parser dispatch/evidence handoff;
- bounded local telemetry/alerting rather than external paging or an enterprise monitoring service.

These mechanisms are implementation adapters beneath the governed semantics. They are not stable public interfaces or customer promises.

## 8. Independent lifecycle dispositions

This conformance result does not change lifecycle state.

Platform Capabilities remain:

- `CAP-001 — Document & Artifact Governance`: `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance`: `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection`: `Incubating / Provisional`;
- `CAP-004 — Audit / Reconstruction Support`: `Incubating / Provisional`.

Real Product Contracts remain:

- P6.02 Tender Operator Product Contract: `Provisional 0.1.0`;
- P6.06 Discount Parser Product Contract: `Provisional 0.1.0`.

No `Active` or `Stable` transition is part of this statement.

## 9. Operational-readiness evidence

The accumulated evidence is sufficient to treat the declared contour as operationally fit for ongoing owner-operated internal use:

- supervised restart and host restart behavior are proven;
- governed state survives ordinary recovery and selected-host loss;
- backup/restore and handoff integrity fail closed on invalid evidence;
- exact update/rollback/re-update is proven;
- attributable least-privilege operation and credential lifecycle are proven;
- health and operator-visible failure/alert paths are proven;
- two materially distinct real Product Contract contours have repeatable operational evidence;
- unknown external outcomes remain `RECONCILIATION_REQUIRED` rather than being retried blindly;
- historical reconstruction does not replay an external effect;
- technical recovery does not restore or grant Organizational Authority.

This is an **internal contour readiness disposition**. It is not the RFC-0001 operational-readiness approval required for promotion of a capability to `Active`.

## 10. Dependency and continuity assumptions

### 10.1 Release-source availability

Exact-release recovery is supported within this statement only when the exact canonical release can be obtained from canonical Git history or another owner-controlled, integrity-verifiable copy of that history/source.

Current evidence proves exact-release restore while source is available. It does not prove indefinite availability of the GitHub service or independent off-provider retention of every historical release.

GitHub is therefore a current source-delivery dependency, not a permanent platform architecture contract. A stronger provider-loss or independent-source-retention promise requires a separate bounded operational decision and evidence before the conformance scope is broadened.

### 10.2 Recovery environment boundary

The supported operational primary environment in this statement is the selected owner-operated Mac mini contour.

P7.10 proves governed-state reconstruction on one distinct clean secondary macOS environment. GitHub Actions Linux evidence additionally proves mechanism portability across an independent runner. Neither result creates a general macOS, Linux or hardware support matrix.

A recovery environment is eligible only when the owner can re-establish the required exact source/runtime and the P7.03/P7.10 security/integrity prerequisites. Full automatic replacement-host service activation is outside this statement.

### 10.3 Separately reprovisioned host prerequisites

The portability package deliberately does not carry reusable machine-local prerequisites. A recovered host must re-establish, as applicable:

- current credentials and reusable secrets through governed identity/credential procedures;
- service-manager registration/configuration;
- runtime installation and runtime roots;
- network, proxy, DNS and TLS trust/configuration;
- OS-specific filesystem paths, ownership and permissions;
- product-host credentials/integration configuration needed for an actual product effect.

Their exclusion is a security and portability boundary, not evidence that the restored governed state may bypass them.

## 11. Requirements not applicable within this claim

The following are not applicable because the declared subject does not provide the addressed external or multi-tenant behavior:

- external/customer Production operation;
- public multi-tenant service operation;
- public ingress or public control plane;
- cross-Organization sharing or customer-to-customer learning;
- public/stable API, SDK, wire or serialization compatibility;
- customer-facing support/SLA/SLO/RTO/RPO obligations;
- `Active` capability support obligations;
- `Stable` Product Contract support obligations;
- general supported OS/browser/hardware matrices.

Declaring them not applicable to this claim does not assert that Arvectum OS could satisfy them without further work.

## 12. Architectural exceptions

Approved architectural exceptions for this statement: `None`.

No known in-scope material violation is being waived to obtain `Scoped` status.

## 13. Known boundaries and unproven stronger claims

The following remain deliberately unproven or uncommitted:

- external/customer Production readiness;
- public multi-Organization tenancy and customer isolation operations;
- Stable Product Contract compatibility/deprecation/support policy;
- Active Platform Capability supported public contracts and capability-level operational readiness;
- public/stable backup/export/recovery/migration formats or APIs;
- full replacement-host service activation from one self-contained package;
- independent long-term source mirror/provider-loss recovery;
- supported OS/browser/hardware matrix;
- contractual availability, response, recovery or data-loss objectives;
- enterprise on-call, remote paging, 24x7 support or customer escalation commitments;
- jurisdiction- or certification-specific compliance claims.

These are boundaries of the claim, not silently accepted exceptions.

## 14. Customer-facing commitments

Applicable customer-facing operational commitments created by this statement: `None`.

No SLA, SLO, RPO, RTO, support, compatibility, portability, archival, hosting or Production promise is created.

## 15. Review and reassessment triggers

Owner of gaps/reassessment: `ООО «Арвектум»`.

Reassess this statement before any of the following:

1. external/customer Production reliance;
2. public ingress or externally reachable control plane;
3. new Organization/customer tenant operation;
4. `Stable` Product Contract proposal;
5. `Active` Platform Capability proposal;
6. stable/public/cross-product API, SDK, wire, serialization, backup/export or recovery boundary;
7. a concrete infrastructure mechanism becoming materially constraining, cross-product or expensive to reverse;
8. a customer-facing SLA/SLO/RPO/RTO/support or portability commitment;
9. material change to persistence, IAM, service supervision, key management, event transport or deployment topology;
10. inability to reproduce exact-release recovery because required source history is unavailable;
11. material security, privacy, authority, portability or reconstruction finding from R24 or later operation.

Scheduled lifecycle review dates in the capability catalog remain independently applicable.

## 16. Result

**Conformance maturity: `Scoped`.**

This statement confirms conformance only for the declared `Local` / `Persistent Internal / owner-operated` Arvectum contour and only for the workflows, evidence and boundaries described above.

It intentionally preserves the distinction among operating readiness, conformance maturity, Platform Capability lifecycle, Product Contract lifecycle and external Production/customer commitments.