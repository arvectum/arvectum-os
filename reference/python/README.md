# Bounded Reference Implementation — Step 1

Status: `Provisional implementation harness`
Scope: `First executable slice / scenario step 1`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001, RFC-0002 and RFC-0003 `1.0.0`

This directory starts the first bounded executable reference implementation defined by `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`.

The implemented step proves only:

1. one Organization scope is explicit and has no ambient/default fallback;
2. one acting Principal is attributable through a stable Subject Identity;
3. acting-on-behalf-of context preserves both the actual and represented Principals;
4. Identity values remain immutable and do not encode roles, permissions or Organizational Authority;
5. authentication evidence is carried only by reference and is not authorization or Organizational Authority.

Tenant partition mapping, mutable principal lifecycle/role state and concrete authorization/approval mechanisms are intentionally deferred to later bounded steps or adapters. This avoids implementing partial semantics that would look like a stable contract before their executable scenario requires them.

## Deliberately not decided

This harness does **not** establish a permanent package layout, programming-language contract, database, API, event broker, IAM provider, policy engine, deployment topology or Product Contract. Python and `unittest` are used only as a reversible, zero-dependency vehicle for executable architecture fitness evidence.

No Platform Capability becomes `Active`, and no production-readiness or full-platform conformance claim is created by these tests.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next scenario step

Create one `Native` canonical subject with a stable Subject Identity and its first immutable Version Identity, preserving the Organization scope established here.
