# Bounded Reference Implementation — Phase 1

Status: `Provisional implementation harness`
Scope: `Phase 1 / P1.01–P1.02`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001, RFC-0002 and RFC-0003 `1.0.0`
Roadmap baseline: `1.3.0`

This directory contains the bounded executable reference implementation defined by `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`.

## P1.01 — Organization scope and attributable Actor / Principal

Implemented and merged:

1. one Organization scope is explicit and has no ambient/default fallback;
2. one acting Principal is attributable through a stable Subject Identity;
3. acting-on-behalf-of context preserves both actual and represented Principals;
4. Identity values remain immutable and do not encode roles, permissions or Organizational Authority;
5. authentication evidence is reference-only and is not authorization or Organizational Authority.

## P1.02 — Native subject + first immutable Canonical Record version

This work item adds one domain-neutral `Native` canonical subject with:

- stable Subject Identity;
- distinct first Version Identity;
- semantic record type and schema version;
- explicit Organization scope;
- explicit `Native` authority mode and authority scope;
- accountable architectural owner reference;
- attributable creation Actor and timezone-aware creation time;
- explicit provenance references;
- proportional integrity metadata for this bounded in-memory harness;
- immutable tuple payload representation;
- no predecessor for the initial version.

`External Reference` and `Governed Replica` are intentionally rejected by the P1.02 model. Their required external-authority, synchronization, freshness, ordering, conflict and failure contracts are not part of this work item.

The Python `frozen` value object and immutable tuple payload provide executable evidence of in-process semantic immutability for this bounded harness. They are **not** a claim of durable storage integrity, tamper evidence, database persistence, cryptographic sealing or production canonical-history guarantees.

## Deliberately not decided

This harness does **not** establish a permanent package layout, programming-language contract, database, API, event broker, IAM provider, policy engine, deployment topology, persistent lineage store, Canonical Head resolver or Product Contract.

Python and `unittest` are used only as a reversible, zero-dependency vehicle for executable architecture fitness evidence. No Platform Capability becomes `Active`, and no production-readiness or full-platform conformance claim is created by these tests.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next roadmap work item

After P1.02 is completed and roadmap evidence is synchronized, the next dependency-ordered item is `P1.03 — Versioned Workflow baseline`.
