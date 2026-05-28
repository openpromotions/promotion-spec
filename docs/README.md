# PRI Docs

This directory contains project-level architecture and ecosystem notes. The
normative specification documents live in [../spec](../spec/).

| Document | Purpose |
|---|---|
| [Architecture boundaries](architecture-boundaries.md) | Defines what belongs to PRI core and what belongs to implementation-specific integration. |
| [Tool integration guide](tool-integration.md) | Explains how existing tools validate, emit, consume, bridge, and claim conformance with PRI. |
| [Stability policy](stability-policy.md) | Defines v0.1 compatibility guarantees, breaking-change rules, extension points, and release criteria. |
| [CNCF path](cncf-path.md) | Describes the project practices and maturity milestones needed before any CNCF discussion. |

## Reading Order

For a first review:

1. Start with the repository [README](../README.md).
2. Read [PRI v0.1](../spec/pri-v0.1.md) for the core document model.
3. Read [PRI Runtime v0.1](../spec/pri-runtime-v0.1.md) for execution
   semantics.
4. Read [Architecture boundaries](architecture-boundaries.md) to understand
   how bindings and external tools fit around the core.
5. Read [Tool integration guide](tool-integration.md) to understand how tools
   consume and emit PRI.
6. Read [Stability policy](stability-policy.md) before proposing contract
   changes.
7. Validate the examples with `python scripts/validate-all.py`.

## Public Positioning

PRI should be presented as an interoperability interface for promotion state.
It is not a fleet manager, GitOps reconciler, VM deployment tool, pipeline
engine, cloud API, or telemetry pipeline.
