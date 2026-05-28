# PRI Proposals

Use this directory for substantial PRI contract changes. Proposals make design
discussion public before the specification changes.

Small editorial fixes can go directly to pull requests. Larger changes should
start with a short proposal.

All proposals must follow the [stability policy](../docs/stability-policy.md).
Breaking changes to v0.1 require a new minor version such as `v0.2`.

## Current Proposals

| Proposal | Status | Purpose |
|---|---|---|
| `0001-pri-v0.1-runtime-contract.md` | Accepted in v0.1 | Defines the runtime object set, semantic operations, state transitions, and retry behavior. |

## Proposal Template

New proposals should include:

- problem statement;
- proposed contract change;
- compatibility impact;
- examples or schema sketch when useful;
- alternatives considered;
- open questions;
- expected implementation or conformance impact.

## Review Standard

A proposal should preserve the main PRI architecture:

- core schemas stay technology-neutral;
- adapters and bindings absorb technology-specific mapping;
- runtime operations are semantic, not a required API shape;
- policy agents, controllers, and workflow engines remain implementations, not
  core PRI requirements;
- new fields should be justified by multiple plausible implementations.
