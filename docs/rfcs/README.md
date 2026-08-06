# Arvectum OS RFC Process

RFCs define cross-cutting architecture, public contracts and platform behavior before irreversible implementation.

## Statuses

- `Draft` — being written; no implementation authority.
- `Proposed` — ready for owner and architecture review.
- `Accepted` — normative and may be implemented.
- `Rejected` — considered and explicitly declined.
- `Superseded` — replaced by another RFC.
- `Withdrawn` — removed by its author before decision.

## When an RFC is required

An RFC is required for:

- changes to the Constitution;
- shared platform foundation responsibilities;
- entity, relation, event or workflow models;
- public product integration contracts;
- persistent storage semantics;
- permission and identity boundaries;
- learning and governance behavior;
- document generation and validation contracts;
- decisions that materially constrain multiple services or products.

An RFC is not required for a local refactor that preserves accepted contracts and behavior.

## Required sections

Every RFC must contain:

1. metadata and status;
2. summary;
3. motivation;
4. scope and non-goals;
5. terminology;
6. proposed model or contract;
7. invariants;
8. lifecycle and versioning;
9. security and privacy considerations;
10. observability and audit requirements;
11. compatibility and migration;
12. alternatives considered;
13. unresolved questions;
14. acceptance criteria;
15. consequences.

## Numbering

RFC files use four-digit identifiers:

```text
RFC-0000-constitution-1.1.md
RFC-0001-constitution-1.2.md
RFC-0002-architecture.md
RFC-0003-entity-model.md
```

Numbers are never reused, including rejected or withdrawn RFCs.

## Decision rule

An RFC becomes `Accepted` only after explicit owner approval. Implementation activity does not imply acceptance.

## Relationship to ADRs

RFCs define the intended architecture and contracts. ADRs record concrete choices made while implementing an accepted RFC, such as a serialization format, storage engine or deployment topology.
