# Arvectum OS — Agent Rules

This repository is the canonical architecture and implementation source for Arvectum OS.

## Mandatory startup

Before any substantive work:

1. Read `docs/constitution/CONSTITUTION.md` in full.
2. Record the Constitution version consulted.
3. Classify the task.
4. Read `docs/rfc/README.md` and the relevant Accepted RFCs, ADRs, catalogs, standards and policies.
5. Read `docs/roadmap/ROADMAP.md` when the task concerns sequencing, next work, milestones, roadmap status, or implementation readiness.
6. Treat repository sources as authoritative over chat history, model memory and prior drafts.
7. Do not continue with a proposal or implementation that conflicts with the Constitution or an Accepted RFC.
8. Do not infer the next architecture artifact from chat history when the canonical roadmap defines it.

For ChatGPT project instructions, use `docs/governance/CHATGPT_PROJECT_BOOTSTRAP.md`.

## Project-chat continuity

When this repository is used from a ChatGPT project, use available project conversation context to recover the goal, current stage, prior user instructions, rationale and unfinished work, but restore the factual current state from this repository.

Do not require the user to paste or repeat another project chat when the task can be reconstructed from project context and repository state.

If a PR, issue, branch, RFC, ADR or repository file is referenced, attempt access through the available GitHub connector before claiming that artifact is unavailable.

Incomplete conversational context is not a reason to stop when the canonical repository contains sufficient state to continue.

For continued canonical work, use:

`project context → repository → Constitution → RFC Index → relevant Accepted RFC/ADR → current artifact → continue`

## Mandatory classification

Classify every task as one of:

- `platform`: reusable, domain-neutral capability of Arvectum OS;
- `product_contract`: interface used by one or more domain products;
- `product_specific`: business-domain logic that does not belong here;
- `governance`: Constitution, RFC, ADR, catalog, standard, policy or roadmap work.

If a task is `product_specific`, do not implement its domain logic in this repository. Describe or implement only the required platform contract.

## Architecture precedence

1. `docs/constitution/CONSTITUTION.md`
2. Accepted RFCs in `docs/rfc/`
3. Accepted ADRs in `docs/adr/` or the repository's canonical ADR location
4. approved catalogs, standards and policies
5. Product Contracts and approved product-specific decisions
6. implementation and tests
7. `docs/roadmap/ROADMAP.md` as the canonical planning source
8. task-specific materials
9. chat history and model memory

A lower-priority source may add context, but it may not silently override a higher-priority source.

Code must not silently override architecture documents. The roadmap coordinates sequence and status but must not redefine an Accepted architectural contract.

## Change rules

- New cross-cutting architecture requires an RFC.
- Constitutional changes require a dedicated amendment RFC.
- Concrete implementation choices require an ADR when they constrain future work.
- Every persistent object, record, workflow, contract and significant state transition must have stable identity and versioning appropriate to its role.
- No consequential action may occur without an observable record.
- Generated outputs must preserve sufficient provenance to identify inputs, applied rules, versions, warnings, initiator and result.
- Learning mechanisms may propose changes but must not silently mutate approved standards or production behavior.
- External products, vendors, model providers, editors and storage engines must not be named in the Constitution.
- Domain concepts such as tenders, advertising campaigns, suppliers or procurement law belong in product modules, not in the platform kernel.
- Ideas discussed only in chat are not accepted architecture until recorded through the repository governance process.
- Do not maintain a competing roadmap in chat, local notes or another repository; update `docs/roadmap/ROADMAP.md` instead.

## Iterative completion and functional cross-review

For every substantive new task, the default execution model is an iterative completion loop:

`execute → functional role cross-review → revise → functional role cross-review → revise → ...`

The agent must continue this loop until all functional roles relevant to the task agree that the result is sufficient for the current lifecycle stage and that additional changes would be disproportionate, speculative or otherwise unnecessary at that stage, subject to a hard maximum of seven cross-review iterations per task.

A cross-review iteration is one review of the current result by the materially relevant functional roles together with incorporation of the material findings that can be resolved within that iteration. The initial execution before the first cross-review is not counted as an iteration. No eighth cross-review iteration may be started for the same task merely to continue refinement.

Functional role selection must be based on the actual scope and consequences of the task. It must include the perspectives materially needed to evaluate the work, such as architecture, engineering, product, operations, security, privacy, governance, commercial, legal or domain expertise where applicable. The loop does not require review by roles that have no material relevance to the task.

Each cross-review must evaluate the result against the concerns of the selected roles and against the current project lifecycle, accepted architecture, applicable governance, delivery value, reversibility and risk. Review findings that materially improve correctness, coherence, security, usability, operability, maintainability or stage-appropriate completeness must be incorporated before the next review cycle.

The normal stopping condition is reached when the relevant roles have no remaining material objections and further refinement would exceed what is justified by the current lifecycle stage, evidence, risk or task scope. The goal is to deliver, within one user request whenever practical, the strongest stage-appropriate final result rather than an avoidably preliminary draft.

The hard stopping condition is reached after the seventh cross-review iteration even if material objections remain. In that case, the agent must stop the iterative improvement loop, preserve the strongest result reached within the seven-iteration limit, and explicitly report unresolved material objections, risks, disagreements, assumptions and any decision authority or follow-up work required. Reaching the limit must not be represented as role consensus or successful formal approval.

Functional cross-review is an execution-quality mechanism. It does not itself constitute formal approval, acceptance, delegation of authority or promotion of lifecycle status. Any change that requires owner approval, decision-authority approval, RFC acceptance, ADR acceptance, policy approval, operational-readiness approval or another canonical governance action remains subject to that action.

Cross-review must not be used to create speculative requirements, unnecessary enterprise ceremony or irreversible commitments beyond the current task and lifecycle stage.

## Initial implementation boundary

Until the relevant architecture RFCs are accepted:

- do not implement an irreversible production kernel;
- do not introduce a database or event broker as a platform commitment without the applicable architectural decision;
- do not create speculative microservices;
- prefer precise contracts, schemas, catalogs and executable validation tests;
- keep early reference implementation bounded, reversible, migration-friendly and clearly provisional where required;
- parallel implementation is permitted only when it does not prejudge unresolved higher-level architecture.

## Required working header

For substantial architecture or implementation work, include:

```text
Constitution consulted: <version>
Task classification: platform | product_contract | product_specific | governance
Relevant RFCs/ADRs: <list or none>
Roadmap consulted: <version or not applicable>
Potential constitutional conflict: yes | no
```

## Required completion report

For each change, report:

- Constitution version consulted;
- task classification;
- architecture documents consulted;
- roadmap version consulted when relevant;
- files changed;
- decisions introduced;
- unresolved questions;
- validation performed.
