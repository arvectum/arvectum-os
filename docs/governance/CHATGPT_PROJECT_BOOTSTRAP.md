# ChatGPT Project Bootstrap for Arvectum OS

Status: `Approved`
Version: `1.0.0`

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
4. Read only the accepted RFCs, ADRs, catalogs and standards relevant to the task.
5. Treat repository documents as authoritative over chat history, model memory and prior drafts.
6. Do not propose or implement anything that conflicts with the Constitution.
7. When a conflict is discovered, stop the conflicting path and identify whether a constitutional amendment RFC, architecture RFC or ADR is required.
8. Do not treat ideas discussed only in chat as accepted architecture until they are recorded in the repository.

## Source precedence

1. `docs/constitution/CONSTITUTION.md`
2. accepted RFCs
3. accepted ADRs
4. approved catalogs, standards and policies
5. implementation and tests
6. current task materials
7. chat history and model memory

A lower-priority source may add context, but it may not silently override a higher-priority source.

## Required response header for architecture work

For substantial architecture or implementation tasks, begin the working notes with:

```text
Constitution consulted: <version>
Task classification: platform | product_contract | product_specific | governance
Relevant RFCs/ADRs: <list or none>
Potential constitutional conflict: yes | no
```

This header may be omitted from casual discussion, but the startup protocol still applies.

## Product repositories

Every Arvectum product repository should contain a root `AGENTS.md` that:

- points to the canonical Arvectum OS Constitution;
- requires the Constitution to be consulted before cross-cutting work;
- forbids duplication of shared platform responsibilities;
- identifies product-specific domain boundaries;
- points to the product contract with Arvectum OS.

## Availability fallback

If the repository cannot be accessed:

1. do not rely on a remembered paraphrase as canonical;
2. clearly state that the Constitution could not be verified;
3. avoid irreversible architectural decisions;
4. request or use an attached current copy before proceeding.
