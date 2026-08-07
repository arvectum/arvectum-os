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
