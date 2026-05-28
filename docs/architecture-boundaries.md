# PRI Architecture Boundaries

PRI is a promotion contract first. It can interoperate with delivery, GitOps,
pipeline, compliance, storage, and internal platform systems, but those systems
do not define the PRI core.

## Layers

| Layer | Defined by PRI core | Outside the core |
|---|---|---|
| Format | `apiVersion`, `kind`, `metadata`, `spec`, `status`, JSON Schemas | External envelopes, storage formats, API resources, database schemas |
| Runtime | Semantic operations and state transitions | CLI, API, controller, RPC, workflow engine, or job implementation |
| Evidence | Evidence document shape and references from checks, targets, and runs | Evidence storage, signing, attestation formats, and dereference behavior |
| Policy | Check references, required/advisory behavior, and result records | Policy language, policy agent, approval system, or rules engine |
| Bindings | Binding category, mapping, adoption mode, and round-trip behavior | Tool-, platform-, format-, transport-, artifact-, and evidence-specific rules |
| Conformance | PRI documents, runtime semantics, binding claims, examples, and scenarios | Product certification or signed attestation in v0.1 |

## Boundary Rules

1. Core PRI schemas MUST NOT require Kubernetes, GitOps, OCI, CI/CD, cloud, or
   vendor-specific fields.
2. Core PRI runtime semantics define operations by meaning, not by transport,
   API, RPC, controller, CLI, or workflow engine.
3. PRI may record policy checks and outcomes, but policy evaluation belongs to
   implementations such as policy agents, approval systems, or rules engines.
4. Bindings absorb technology-specific mapping, naming, identity, transport,
   evidence, storage, and round-trip rules.
5. Evidence is portable as a record and reference. Evidence content, storage,
   signing, and verification formats belong in bindings or later focused specs.
6. Compatibility with a technology does not make that technology part of PRI
   conformance.

## Source Of Truth

The source of truth remains PRI records and PRI runtime semantics:

```text
Promotion -> PromotionRun -> CheckResult -> TargetResult -> Evidence
```

Implementations can expose those records through any platform shape they need.
The portable contract is the document model, state model, and evidence model.

## Tool Consumption Boundary

Tools consume PRI by validating documents, translating native state, emitting
portable records, or acting on `Promotion` intent. PRI does not prescribe the
tool's controller, policy agent, storage backend, delivery engine, approval
system, or API surface.

The contract between PRI and a tool is:

- input and output documents match the schemas;
- required fields are present;
- portable phase values are used;
- native differences are documented in a `Binding`;
- implementation capability is documented in a `ConformanceProfile`.
