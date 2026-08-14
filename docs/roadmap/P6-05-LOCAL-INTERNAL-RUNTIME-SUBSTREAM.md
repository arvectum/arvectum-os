# P6.05 — Local Internal Runtime Substream

Status: `Active / In Progress`
Version: `0.1.7`
Created: `2026-08-09`
Updated: `2026-08-14`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_specific` and `product_contract`
Parent work item: `P6.05 — Platform-gap remediation from first real use`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Purpose

This substream makes the current P6.05 work executable in the real internal operating environment used by ООО «Арвектум», beginning with an owner-operated Mac mini.

The immediate purpose is not to define a general Arvectum OS deployment product, production topology, customer installation model or Stable/public runtime contract. The immediate purpose is to establish the minimum secure and reversible local runtime needed to:

1. run Arvectum OS as a real internal organizational workspace/runtime rather than only as repository/reference evidence;
2. connect the existing `ai-corporation` first real product through the already-declared P6.02 Product Contract boundary;
3. execute the bounded P6.05 real-evidence runner for notice `0344100006426000005`;
4. obtain truthful `7/7` exact tender attachment bytes + SHA-256 evidence if the existing authorized read-only EIS contour succeeds;
5. capture operator/deployment friction as evidence for later product/workspace work rather than speculating about a final UI or topology.

This substream exists because real product validation has now crossed from hosted/reference proof into owner-operated use. It is therefore part of P6.05 execution, not a claim that Phase 7 production readiness has begun.

## 2. Canonical boundaries

The substream MUST preserve the current accepted architecture and P6.02/P6.05 boundaries:

- Constitution `1.2.0` remains frozen;
- RFC-0001 through RFC-0008 remain the binding architecture baseline;
- only the existing CAP-001 + CAP-004 P6.02 product dependency set is relied on;
- CAP-002/CAP-003 remain omitted;
- external tender/EIS sources remain authoritative;
- procurement semantics and completeness judgment remain product-owned;
- consequential canonical mutation remains governed;
- no automated bid submission, supplier/customer contact, signature, payment or other external mutation is introduced;
- no Stable/public API, SDK, package, wire format, deployment topology, storage topology, SLA or support promise is created;
- no capability lifecycle promotion follows from successful local operation;
- secrets and credentials MUST NOT be committed to the repository or copied into canonical evidence.

The Mac mini is an **operational environment for bounded internal validation**, not an architectural commitment to macOS or single-host deployment.

## 3. Current implementation baseline

Already completed before this local-runtime substream:

- Arvectum OS bounded P6.05 CAP-001 admission implementation merged into platform `main` as `5dbbc7b3af1f0f3896301ef833de2214cb44e6f9`;
- `ai-corporation` PR `#142` merged into product `main` as `bf9a1c5438426031fce36370344ada969d2493dd`;
- product hosted standard CI and dedicated P6.05 exact-attachment evidence CI passed on the unchanged implementation head;
- the product live runner `scripts/p6_05_capture_real_attachment_evidence.py` exists and fails closed unless the existing EIS/getDocsIP contour is configured and the exact source-listed set is complete.

Local execution evidence now additionally establishes:

- P6.05-L1 host/runtime baseline — `Complete / PASS`;
- P6.05-L2 reproducible canonical checkout + reference runtime start — `Complete / PASS` under [`P6-05-L2-local-reference-runtime-start.md`](../reviews/P6-05-L2-local-reference-runtime-start.md);
- the successful L2 run used canonical `main` at `fb61889633b11875dc5e1cf92771a159024a5695`, CPython `3.14.6`, and passed `717/717` reference tests with a clean checkout before and after execution;
- no product, EIS, public ingress, external action or secret exposure occurred in L2.

Implementation readiness does **not** close P6.05. Real `7/7` evidence remains unobserved.

## 4. Subtasks

| ID | Subtask | Status | Exit evidence |
|---|---|---|---|
| `P6.05-L1` | Local host/runtime baseline | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L1-local-host-runtime-baseline.md) | host prerequisites, repository locations, runtime versions and local-only network/port assumptions are inventoried; no final topology is declared |
| `P6.05-L2` | Reproducible Arvectum OS local checkout + reference runtime start | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L2-local-reference-runtime-start.md) | canonical `main` reproduced on the selected Mac mini; isolated stdlib-only reference runtime passed `717/717`; source checkout remained clean |
| `P6.05-L3` | Secure local configuration + secrets boundary | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md) | local configuration is separated from repository state; required credentials are detected without being printed/committed; fail-closed behavior is verified |
| `P6.05-L4` | Internal Organization + operator bootstrap | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L4-internal-organization-operator-bootstrap.md) | bounded ООО «Арвектум» Organization/operator context can execute the required local governed flow with least-privilege assumptions documented |
| `P6.05-L5` | First real product connection | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L5-first-real-product-connection.md) | `ai-corporation` connects through exact P6.02 Product Contract `0.1.0`, canonical source verified, CAP-001 + CAP-004 only, with Organization/Actor/Product/Product Contract continuity preserved; CAP-002/CAP-003 absent; no grants/delegations/Organizational Authority; no external actions |
| `P6.05-L6` | Local synthetic/redacted regression + negative-path smoke | 🟨 Current / next | relevant P6.03/P6.05 proof paths pass locally; missing config/gates/wrong versions fail closed |
| `P6.05-L7` | Real P6.05 exact-attachment live run | ⬜ Pending | the existing authorized read-only runner executes for `0344100006426000005`; success requires `PASS_EXACT_ATTACHMENT_EVIDENCE`, `exact_document_count = 7`, complete exact set and manifest SHA-256 |
| `P6.05-L8` | Governed evidence admission + canonical P6.05 closure package | ⬜ Pending | exact evidence is admitted/reconstructed through the bounded governed path; closure review records PASS or the truthful remaining blocker; roadmap is synchronized |
| `P6.05-L9` | Dogfooding friction capture | ⬜ Pending | concrete operator/setup/workspace friction observed during L1-L8 is recorded as evidence/backlog without silently expanding P6.05 scope |

Subtasks are sequential where dependencies require it, but reversible preparation may proceed in parallel when it cannot change canonical state or external systems.

## 5. Execution detail

### P6.05-L1 — Local host/runtime baseline

Record only what is required to run the current bounded contour:

- macOS/CPU architecture actually present;
- available Python/runtime/container tooling actually required by current code;
- local repository/work-data locations;
- ports/endpoints required for local-only interaction;
- available disk and permissions sufficient for exact document evidence;
- network/proxy constraints relevant to GitHub and EIS;
- rollback/removal locations.

Do not infer a general supported-hardware matrix from this host.

### P6.05-L2 — Reproducible local Arvectum OS start

Use canonical repository state and existing reference/runtime instructions where available. If a missing bootstrap/install mechanism is discovered, implement only the minimum reversible internal mechanism needed for this environment and record the friction.

A successful local start is internal validation evidence only. It does not establish production readiness.

**Completion:** `PASS` under [`P6-05-L2-local-reference-runtime-start.md`](../reviews/P6-05-L2-local-reference-runtime-start.md). The selected Mac mini reproduced canonical `main` at `fb61889633b11875dc5e1cf92771a159024a5695`, created the isolated stdlib-only environment outside the checkout, passed `717/717` tests, and remained clean after execution. The earlier cache-generating attempt was preserved as a truthful FAIL and remediated without weakening the clean-state gate.

### P6.05-L3 — Secure configuration + secrets

Verify local handling for configuration required by the selected workflow. Credentials MUST remain outside source control and canonical evidence. Diagnostics may report safe configured/not-configured state but MUST NOT print tokens or secret material.

**Completion:** `PASS` under [`P6-05-L3-secure-local-configuration-secrets-boundary.md`](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md). The initial fail-closed detection of divergent legacy copies led to an owner-approved in-memory diagnostic (5+2 distribution), owner decision [`DECISION-2026-08-14-P6-05-L3-DIVERGENT-EIS-SECRET-RECONCILIATION.md`](../governance/decisions/DECISION-2026-08-14-P6-05-L3-DIVERGENT-EIS-SECRET-RECONCILIATION.md), canonical reconciliation helper implementation via PR `#1`, and a clean owner-operated execution establishing the external owner-only credential while scrubbing all 7 legacy token assignments with all 69 targeted L3 tests passing.

### P6.05-L4 — Internal Organization/operator bootstrap

Establish the smallest Organization/operator context required by the existing governed boundary. Do not introduce a new general IAM architecture merely to make the local run convenient.

**Completion:** `PASS` under [`P6-05-L4-internal-organization-operator-bootstrap.md`](../reviews/P6-05-L4-internal-organization-operator-bootstrap.md). The real owner-operated bootstrap issued the opaque Organization and human Principal identities to external owner-only state under explicit authorization. The second canonical run proved idempotent reuse without state mutation. Both preflights passed, and all 62 targeted L4 tests (and 848 full reference tests) PASS with no authority, roles, permissions, product context or network invocation occurred.

### P6.05-L5 — First product connection

Connect `ai-corporation` without broadening the P6.02 contract:

- exact Product Contract `0.1.0`;
- CAP-001 + CAP-004 only;
- external source authority preserved;
- procurement logic remains product-owned;
- no external mutation.

**Completion:** `PASS` under [`P6-05-L5-first-real-product-connection.md`](../reviews/P6-05-L5-first-real-product-connection.md). The real owner-operated preflight successfully connected through exact P6.02 Product Contract `0.1.0` while maintaining strict Organization continuity and platform governance boundaries. Execution SHA `77233e798ce6a490035c457a97dfe03c04149df5`. 26/26 targeted L5 tests and 874/874 full reference tests PASS. The isolated worktree remained clean with `PYTHONDONTWRITEBYTECODE=1` and no grants, delegations, Organizational Authority or external actions occurred.

### P6.05-L6 — Local smoke

Before real-source execution, prove locally that the bounded path still behaves as expected under synthetic/redacted evidence and fails closed under material negative conditions.

This avoids using a real external request as the first signal that the local runtime is misconfigured.

### P6.05-L7 — Real exact-attachment run

Run the existing product command in the authorized local environment:

```bash
python scripts/p6_05_capture_real_attachment_evidence.py
```

The only successful real-evidence result for this subtask is a truthful complete seven-document set, including:

- `status = PASS_EXACT_ATTACHMENT_EVIDENCE`;
- `expected_document_count = 7`;
- `exact_document_count = 7`;
- no missing names;
- no duplicate source-listed names;
- manifest SHA-256;
- exact local evidence path;
- `external_actions = false`.

Any safe blocker/incomplete output remains evidence and MUST NOT be converted into PASS.

### P6.05-L8 — Governed admission + closure

Use the already-implemented bounded governed admission/reliance path. Record exact evidence/provenance and then perform the canonical P6.05 closure review. Only after a passing closure may R18 begin.

### P6.05-L9 — Dogfooding friction capture

During all local steps, record concrete friction such as:

- bootstrap/install complexity;
- configuration ambiguity;
- operator visibility gaps;
- inability to inspect Organization/Product Contract/execution/document state conveniently;
- missing local diagnostics;
- repeated manual steps;
- unsafe or confusing failure messages.

These observations may motivate later workspace/UI/runtime work. They are **evidence**, not automatic P6.05 implementation requirements and not automatic Platform Capability candidates.

## 6. Exit criteria for the local-runtime substream

The substream is complete only when:

1. the bounded Arvectum OS runtime is reproducibly runnable on the selected internal Mac mini;
2. credentials/configuration remain local and are not committed or exposed;
3. ООО «Арвектум» Organization/operator context is sufficient for the required governed flow;
4. `ai-corporation` relies through exact P6.02 Product Contract `0.1.0` with CAP-001 + CAP-004 only;
5. local synthetic/redacted and negative-path smoke passes;
6. the real P6.05 runner has executed in the authorized environment;
7. either real `7/7` exact evidence is obtained and governed, or a new truthful external/product/runtime blocker is canonically recorded;
8. rollback/removal instructions for the bounded local environment are known;
9. dogfooding friction is captured without inflating it into unapproved architecture or roadmap commitments.

If criterion 7 produces a new blocker rather than `7/7`, P6.05 remains open and the next action must be evidence-driven from that blocker.

## 7. Non-goals

This substream does not establish:

- Production environment status;
- Phase 7 operational readiness;
- HA, multi-node deployment or disaster recovery;
- enterprise SSO/IAM topology;
- a customer installer;
- a macOS support commitment;
- a container/Kubernetes/microservice architecture requirement;
- a persistent storage vendor/engine requirement;
- public ingress or internet-facing service exposure;
- Stable/public API/SDK/package compatibility;
- CAP-002/CAP-003 adoption;
- capability promotion to `Active`;
- a final Arvectum OS UI.

## 8. Rollback / containment

Until a later accepted decision says otherwise, this environment is bounded and removable:

- repository worktrees/checkouts can be removed and recreated from canonical Git history;
- local generated evidence/configuration remains separated from source-controlled code;
- product integration remains within the Provisional P6.02 contract;
- no external mutation is performed by this validation contour;
- any new durable/cross-cutting dependency discovered during setup must stop at the applicable ADR/RFC/Product Contract/policy gate before becoming an architectural commitment.

## 9. Immediate next action

Proceed with `P6.05-L6 — Local synthetic/redacted regression + negative-path smoke`. Keep P6.05 overall `Active / In Progress`.
