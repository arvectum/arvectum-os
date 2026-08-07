# ChatGPT Project Bootstrap for Arvectum OS

Status: `Approved`
Version: `1.1.3`
Updated: `2026-08-07`

Use this text in the instructions of every ChatGPT project or long-lived chat that works on Arvectum OS or an Arvectum product.

## Mandatory startup protocol

Before proposing architecture, implementation, product boundaries, standards, workflows, memory, learning, documents or integrations related to Arvectum OS:

1. Read the current canonical Constitution at `docs/constitution/CONSTITUTION.md` in `arutyunoveth/arvectum-os`.
2. State which Constitution version was consulted.
3. Determine whether the task concerns:
   - the Arvectum OS platform;
   - a shared product contract;
   - a specific domain product;
   - governance or documentation.
4. Read `docs/rfc/README.md`, then the Accepted RFCs, ADRs, catalogs and standards relevant to the task.
5. Read `docs/roadmap/ROADMAP.md` whenever the task asks what to do next, concerns sequencing or milestones, or may start a new architecture or implementation stage.
6. Treat repository documents as authoritative over chat history, model memory and prior drafts.
7. Do not propose or implement anything that conflicts with the Constitution or an Accepted RFC.
8. When a conflict is discovered, stop the conflicting path and identify whether a constitutional amendment RFC, architecture RFC, ADR or roadmap correction is required.
9. Do not treat ideas discussed only in chat as accepted architecture until they are recorded in the repository.
10. Do not infer the next architecture artifact from chat history when the canonical roadmap defines it.

## Continuity between project chats

When work continues in another chat of the same ChatGPT project:

1. use available project conversation context to recover the goal, current stage, prior user instructions, rationale and unfinished work;
2. recover the current factual state from the canonical GitHub repository;
3. do not ask the user to repeat another project chat when the task can be reconstructed from project context or repository state;
4. if a PR, issue, branch, RFC, ADR or repository file is mentioned, attempt to open it through the available GitHub connector before claiming it is unavailable;
5. incomplete conversational context is not a reason to stop when the canonical repository contains sufficient state to continue.

Use:

`project context → GitHub → Constitution → RFC Index → relevant Accepted RFC/ADR → current artifact → continue`

Repository state is authoritative for canonical work. Project conversation context is used for continuity, rationale and unfinished actions.

## Source precedence

1. `docs/constitution/CONSTITUTION.md`
2. Accepted RFCs
3. Accepted ADRs
4. approved catalogs, standards and policies
5. Product Contracts and approved product-specific decisions
6. implementation and tests
7. `docs/roadmap/ROADMAP.md` as the canonical planning source
8. current task materials
9. chat history and model memory

The roadmap coordinates sequence, status and milestones. It does not override a higher-authority architectural or governance source.

A lower-priority source may add context, but it may not silently override a higher-priority source.

## Iterative completion and functional cross-review

For every substantive new task, use the following default loop:

`execute → functional role cross-review → revise → functional role cross-review → revise → ...`

Continue until all functional roles materially relevant to the task agree that the result is sufficient for the current lifecycle stage and that further changes would be disproportionate, speculative or unnecessary at that stage, but never exceed seven cross-review iterations for the same task.

A cross-review iteration consists of one review of the current result by the materially relevant functional roles and incorporation of the material findings that can be resolved within that iteration. The initial execution before the first cross-review does not count toward the limit. Do not start an eighth cross-review iteration merely to continue refinement.

Choose review roles according to the task's actual scope and consequences. Include architecture, engineering, product, operations, security, privacy, governance, commercial, legal or domain perspectives when they are materially relevant; do not require irrelevant roles merely to satisfy process ceremony.

In each cycle, incorporate material findings that improve correctness, coherence, security, usability, operability, maintainability or stage-appropriate completeness, then repeat the review on the revised result while iterations remain.

Normally stop when relevant roles have no material objections and further refinement is not justified by the current lifecycle stage, evidence, risk or task scope. The objective is to produce, within one user request whenever practical, the strongest stage-appropriate final result rather than an avoidably preliminary draft.

Always stop after the seventh cross-review iteration even if material objections remain. At that hard limit, preserve the strongest result reached within the allowed iterations and explicitly report unresolved material objections, risks, disagreements, assumptions and any required decision authority or follow-up work. Reaching the iteration limit must not be presented as role consensus or as formal approval.

Functional cross-review is an execution-quality mechanism. It does not constitute formal governance approval, RFC or ADR acceptance, policy approval, decision-authority approval, lifecycle promotion or operational-readiness approval. Required canonical approvals remain mandatory.

Do not use iterative review to add speculative requirements, unnecessary enterprise ceremony or irreversible commitments that are not justified by the task and current lifecycle stage.

## Required response header for architecture work

For substantial architecture or implementation tasks, begin the working notes with:

```text
Constitution consulted: <version>
Task classification: platform | product_contract | product_specific | governance
Relevant RFCs/ADRs: <list or none>
Roadmap consulted: <version or not applicable>
Potential constitutional conflict: yes | no
```

This header may be omitted from casual discussion, but the startup protocol still applies.

## Product repositories

Every Arvectum product repository should contain a root `AGENTS.md` that:

- points to the canonical Arvectum OS Constitution;
- requires the Constitution to be consulted before cross-cutting work;
- forbids duplication of shared platform responsibilities;
- identifies product-specific domain boundaries;
- points to the product contract with Arvectum OS;
- points to the Arvectum OS canonical roadmap when platform sequencing or promotion work is involved.

## Roadmap rule

`docs/roadmap/ROADMAP.md` is the only canonical roadmap for Arvectum OS.

Chats, local notes, product repositories and model memory may discuss roadmap proposals, but they must not be treated as competing canonical roadmaps.

When a roadmap change is approved, update and version the canonical file in `arutyunoveth/arvectum-os`.

## Availability fallback

If the repository cannot be accessed:

1. first verify that access through the available GitHub connector was actually attempted;
2. do not rely on a remembered paraphrase as canonical;
3. clearly state that the Constitution, Accepted RFCs or roadmap could not be verified as applicable;
4. avoid irreversible architectural decisions;
5. request or use an attached current copy only when repository access genuinely fails.
