# PRI Architecture Boundaries

PRI is a promotion contract first. It can interoperate with observability,
eventing, GitOps, pipeline, compliance, and storage systems, but those systems
do not define the PRI core.

## Layers

| Layer | Defined by PRI core | Optional compatibility surface |
|---|---|---|
| Format | `apiVersion`, `kind`, `metadata`, `spec`, `status`, JSON Schemas | External envelopes, storage formats, wire encodings |
| Runtime | Semantic operations and state transitions | CLI, API, controller, RPC, or job implementation |
| Bindings | Binding category, mapping, adoption mode, round-trip behavior | Tool-, platform-, format-, transport-, and evidence-specific rules |
| Signals | PRI signal attribute names and event names | OpenTelemetry spans, logs, metrics, CloudEvents, CDEvents, or other carriers |
| Collector | Receiver, processor, exporter roles for promotion data | OpenTelemetry Collector components, native collectors, or managed pipelines |
| Conformance | PRI documents, runtime semantics, binding claims | Product-specific test harnesses and certifications |

## Boundary Rules

1. Core PRI schemas MUST NOT require OpenTelemetry, Kubernetes, GitOps, OCI,
   CI/CD, or cloud-specific fields.
2. Core PRI runtime semantics define operations by meaning, not by transport,
   API, RPC, controller, CLI, or collector implementation.
3. Bindings absorb technology-specific mapping, naming, identity, transport,
   evidence, storage, and round-trip rules.
4. Optional signal bindings may reuse proven architectures such as
   OpenTelemetry's Resource/Scope context, semantic attribute naming, schema
   URLs, and receiver/processor/exporter pipeline shape.
5. Compatibility with a technology does not make that technology part of PRI
   conformance.

## OpenTelemetry Relationship

OpenTelemetry is an important compatibility target and architectural precedent,
not the PRI data model.

PRI derives these patterns:

- stable semantic attribute names for portable querying;
- schema URL style versioning for emitted signal conventions;
- resource/scope-like context for producer identity;
- receiver/processor/exporter collector pipelines;
- optional OTLP transport for telemetry observations.

PRI does not derive these as core requirements:

- OpenTelemetry governance;
- OpenTelemetry SDK usage;
- OpenTelemetry Collector runtime usage;
- OTLP as the only transport;
- spans, logs, or metrics as the source of truth for promotion state.

The source of truth remains PRI records and PRI runtime semantics. Telemetry
signals are observations of that state, not the state itself.
