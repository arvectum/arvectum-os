# RFC-0007 Functional Cross-review

Status: `Complete`
Created: `2026-08-07`
Updated: `2026-08-07`
Subject: `RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`
Reviewed draft: `0.1.0`
Reviewed draft blob SHA: `686e6fc3fe720709773efb3b685f97b45d458b69`
Iterations completed: `4`
Maximum planned iterations: `7`
Result: `Pass after bounded reconciliation`

## 1. Purpose

This review tests RFC-0007 against Constitution `1.2.0` and Accepted RFC-0001 through RFC-0006 before owner approval is requested.

The review is functional rather than ceremonial. It evaluates whether the proposed lifecycle permits Arvectum OS to accumulate organizational intelligence without collapsing evidence, memory, knowledge, authority, rights or product boundaries into one another.

## 2. Review perspectives

The review considered the following functional perspectives:

- CEO / organizational-value and compounding-learning perspective;
- COO / operational learning and workflow perspective;
- CTO / platform architecture and Kernel compatibility perspective;
- CISO / security, tenant isolation and derived-data perspective;
- Privacy / minimization, retention and deletion perspective;
- Legal / rights, authority and cross-organization reuse perspective;
- Product / product-domain ownership and Product Contract perspective;
- Engineering / retrieval, indexing, migration and implementation feasibility perspective;
- AI Governance / automation, validation and authority-boundary perspective.

## 3. Iteration 1 — Semantic and Kernel consistency

### Finding 1.1 — Observation and Memory must not become new Kernel primitives

The draft correctly states that Observation, Memory, Knowledge Candidate, Improvement Proposal and Knowledge are semantic roles above the RFC-0002 Kernel metamodel.

This is required because RFC-0002 finalizes the Kernel primitives and explicitly leaves memory/knowledge promotion rules to RFC-0007 rather than authorizing a sixth primitive.

**Result:** Pass.

### Finding 1.2 — Knowledge Candidate must remain explicitly non-Knowledge

The Constitution defines Knowledge as validated organizational understanding. Therefore a pre-validation object cannot be described simply as a lower-confidence form of Knowledge.

The draft uses `Knowledge Candidate` for the pre-validation state and explicitly states that it is not Knowledge.

**Result:** Pass.

### Finding 1.3 — Organizational Memory must preserve epistemic status

Memory cannot turn a stored assertion into truth merely by retaining it. The draft explicitly separates the question “what did the organization preserve?” from “what has the organization validated?”.

This is compatible with Constitution Articles IV–VI and RFC-0001 Section 8.

**Result:** Pass.

## 4. Iteration 2 — Authority, privacy, rights and cross-organization learning

### Finding 2.1 — Native organizational interpretation must not steal external source authority

A significant risk exists when the organization validates guidance derived from an external authoritative fact. The Knowledge Record may be `Native` for the organization's adopted interpretation, but the underlying external fact must retain its RFC-0001/RFC-0002 authority mode.

The draft already establishes this distinction in Sections 7 and 20.

**Result:** Pass.

### Finding 2.2 — Cross-organization reuse must remain denied by default

Repeated customer patterns cannot become platform-global Knowledge merely because Arvectum OS processes multiple organizations. Explicit rights, classification, purpose and governance remain required.

The draft preserves this and explicitly rejects the idea that aggregation, anonymization, pseudonymization or model training automatically creates reuse rights.

**Result:** Pass.

### Finding 2.3 — Derived stores must obey later deletion/restriction changes

Embeddings, indexes, caches and summaries can leak restricted information after the source is deleted or reclassified unless derived-store invalidation is explicit.

The draft requires access/deletion/classification changes to propagate to retrieval and derived projections.

**Result:** Pass.

### Finding 2.4 — Memory minimization must prevent a “retain everything” interpretation

The Constitution requires organizational continuity but also privacy, minimization, retention and deletion. RFC-0007 must not be read as justification to retain every chat, prompt, telemetry item or personal detail.

The draft explicitly states this in Section 18.2 and permits governed references and minimum-sufficient evidence.

**Result:** Pass.

## 5. Iteration 3 — AI governance, validation and operational mutation

### Finding 3.1 — AI validation must not collapse into approval

RFC-0005 permits bounded AI validation but prohibits AI from becoming final consequential approver or Organizational Authority. RFC-0007 must preserve that split.

The draft separates validation from approval and states that a successful validator is not automatically an organizational approver.

**Result:** Pass.

### Finding 3.2 — Automated promotion wording requires tightening

Draft Section 13 states that a fully automated promotion path may exist if governance explicitly delegates bounded promotion authority. This is directionally compatible with approved governance mechanisms, but the wording could be misread as allowing AI output itself to satisfy the final promotion gate.

**Required reconciliation:** clarify that automated execution may carry out a pre-approved promotion policy, but AI-generated judgement alone cannot constitute the Organizational Authority or final approval predicate unless a higher-authority approved governance mechanism explicitly defines a non-AI or independently controlled objective gate for the bounded scope. Preserve the rule that AI does not turn observations into validated Knowledge by itself.

**Result:** Bounded change required.

### Finding 3.3 — Learning-driven operational changes must remain separate from Knowledge promotion

Knowledge that a Workflow, Policy, Standard or Product Contract should change is not itself authorization to change it.

The draft clearly routes such changes through Improvement Proposals and the existing governed version/change process.

**Result:** Pass.

## 6. Iteration 4 — Product boundary, freshness and implementation feasibility

### Finding 4.1 — Product Contract access must not imply write authority

A Product Contract can declare an operation boundary, but contract declaration/registration cannot itself grant Organizational Authority under RFC-0003/RFC-0004.

Draft Section 16 lists read/write/propose operations but should explicitly state that declaring a write/propose operation does not grant authority to promote or approve Knowledge.

**Required reconciliation:** add an explicit sentence preserving separation between declared contract surface, technical authorization, Organizational Authority and promotion approval.

**Result:** Bounded change required.

### Finding 4.2 — Knowledge freshness is operationally necessary but must not create one universal TTL

Knowledge can decay, but stable knowledge may not need time-based expiry. The draft correctly allows review-by, source freshness, event-triggered invalidation, source-version dependency or explicit no-expiry rationale.

**Result:** Pass.

### Finding 4.3 — Retrieval technology must remain replaceable

Vector stores, search engines and embeddings must remain projections, not canonical authorities. Consequential reliance must resolve to governed source versions.

The draft satisfies this and is compatible with technology independence.

**Result:** Pass.

### Finding 4.4 — Migration must not bulk-promote legacy memory

Existing chats, notes, vector stores and analytics should not become canonical Memory/Knowledge merely to satisfy the new architecture.

The draft defines incremental, evidence-driven migration and explicit handling when provenance cannot be established.

**Result:** Pass.

## 7. Bounded reconciliation required for reviewed proposal

The reviewed proposal should incorporate exactly the following material clarifications without changing the core architecture:

1. tighten Section 13 so automated promotion execution cannot be read as AI self-approval or AI-only validation-to-Knowledge promotion;
2. tighten Section 16 so Product Contract declarations do not create Organizational Authority or Knowledge-promotion approval;
3. update status/version to `Proposed 0.2.0` and reference this cross-review.

No Constitution amendment, earlier RFC modification or new Kernel primitive is required.

## 8. Compatibility result

After the bounded reconciliation above, RFC-0007 is compatible with:

- Constitution `1.2.0`;
- RFC-0001 `1.0.0`;
- RFC-0002 `1.0.0`;
- RFC-0003 `1.0.0`;
- RFC-0004 `1.0.0`;
- RFC-0005 `1.0.0`;
- RFC-0006 `1.0.0`.

No material contradiction was found.

## 9. Review conclusion

**Result: `Pass after bounded reconciliation`.**

Four review iterations were sufficient. Further review up to the maximum of seven iterations is not justified unless owner review identifies a new material concern.

After the bounded edits are published as RFC-0007 `0.2.0`, the proposal is suitable for explicit owner approval. It MUST remain `Proposed` until independent owner approval exists and the acceptance publication transition is completed under the approved RFC State Transition Procedure.
