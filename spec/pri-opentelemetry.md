# PRI OpenTelemetry Compatibility Binding v0.1

PRI has its own document format, runtime semantics, binding model, and
conformance model. This document defines how PRI observations can be exported in
an OpenTelemetry-compatible form without making OpenTelemetry part of the PRI
core contract.

The binding reuses proven OpenTelemetry patterns: traces, log records, metrics,
semantic attribute naming, schema URLs, and receiver/processor/exporter
pipelines. Those patterns are compatibility surfaces and implementation
shortcuts, not PRI concepts.

This document defines the v0.1 mapping from PRI records to OpenTelemetry
signals. It is a binding, not a replacement for the core PRI records.

## Relationship To OpenTelemetry

PRI does not extend OpenTelemetry governance, require upstream OpenTelemetry
acceptance, or force promotion state into OpenTelemetry's data model.

Promotion state has control-plane behavior that telemetry alone does not model:

- Promotions and PromotionRuns are queried by stable identity.
- Runtime operations can cancel, pause, retry, or inspect a run.
- Current state matters, not only emitted observations.
- Evidence and checks form a document graph that can be audited outside a
  telemetry backend.

The OpenTelemetry binding is therefore one interoperability path. It lets
promotion observations flow through OpenTelemetry traces, logs/events, metrics,
OTLP, and Collector pipelines while PRI remains the promotion contract.

OpenTelemetry terms MUST NOT appear in PRI core schemas unless they are part of
an explicit optional binding. Core PRI documents remain valid and complete
without this binding.

## Design Principles

1. PRI records remain the source of truth for promotion semantics.
2. When this binding is used, OpenTelemetry carries promotion observations as
   traces, logs/events, and metrics.
3. PRI does not require OpenTelemetry for core conformance.
4. PRI does not define a new telemetry wire protocol in v0.1; OTLP MAY carry
   the OpenTelemetry representation of PRI observations.
5. The receiver/processor/exporter collector shape is an architectural pattern,
   not a required OpenTelemetry runtime.
6. Technology-specific mappings belong in binding documents.

## Schema URL

OpenTelemetry exporters that support schema URLs SHOULD use:

```text
https://openpromotions.org/schemas/otel/pri/v0.1
```

The schema URL identifies the version of the PRI signal semantic conventions
used by emitted OpenTelemetry-compatible telemetry. It is not a PRI document
`apiVersion`. It is also separate from any OpenTelemetry Resource or
Instrumentation Scope schema URL a specific SDK or exporter may set for its own
telemetry schema.

## Compatibility Signal Mapping

| PRI concept | OpenTelemetry signal | Purpose |
|---|---|---|
| `Promotion` | Log/event | Promotion intent was observed or changed. |
| `PromotionRun` | Trace span and log/event | Runtime execution state and lifecycle transitions. |
| `CheckResult` | Child span or log/event | Check evaluation result. |
| `TargetResult` | Child span or log/event | Per-target delivery or verification result. |
| `Evidence` | Log/event with links | Evidence was recorded or attached. |
| `ConformanceProfile` | Log/event | Runtime or adapter capability was observed. |
| `Binding` | Log/event | Binding capability or mapping metadata was observed. |

## Traces

A PromotionRun MAY be represented as a trace. The PromotionRun span should cover
the execution window from `status.startedAt` to `status.completedAt` when those
timestamps are known.

Recommended span names:

| Span | Name |
|---|---|
| PromotionRun span | `promotion.run` |
| CheckResult span | `promotion.check` |
| TargetResult span | `promotion.target` |

Recommended span attributes are defined in
[PRI Semantic Conventions](pri-semantic-conventions.md).

Portable phase mapping:

| PRI phase | Suggested span status |
|---|---|
| `Succeeded` | OK |
| `Failed` | ERROR |
| `Cancelled` | UNSET with `promotion.run.phase=Cancelled` |
| `Pending`, `Running`, `Paused`, `Delivering`, `Verifying`, `Skipped` | UNSET with phase attribute |

Implementations MAY map `Cancelled` to ERROR when cancellation should count
toward operational error-rate views, or keep it as UNSET when cancellation is a
normal control-plane outcome. The chosen mapping should be documented by the
implementation or binding.

## Logs And Events

Point-in-time promotion observations SHOULD be represented as OpenTelemetry log
records or events. The event name should be one of the PRI event names below.

In this binding, references to events mean OpenTelemetry log records that carry
an event name attribute. Implementations should prefer log records for
point-in-time promotion observations unless their OpenTelemetry SDK exposes a
dedicated event API with equivalent log-record semantics.

| Event name | Meaning |
|---|---|
| `promotion.intent.observed` | A Promotion intent was observed. |
| `promotion.run.state.changed` | A PromotionRun phase changed or was observed. |
| `promotion.check.result.recorded` | A CheckResult was recorded. |
| `promotion.target.result.recorded` | A TargetResult was recorded. |
| `promotion.evidence.recorded` | Evidence was recorded or attached. |
| `promotion.binding.capability.observed` | A Binding or ConformanceProfile capability was observed. |

When a backend does not support first-class events, the event name can be stored
as a log attribute.

## Baggage

PRI does not use OpenTelemetry Baggage to carry mutable promotion state. Baggage
MAY carry correlation hints such as a promotion name or run name when an
implementation already uses Baggage, but PRI state MUST remain in PRI records or
telemetry attributes.

## Metrics

PRI metrics are derived from records and lifecycle observations. Metrics are
optional in v0.1.

Recommended metric names:

| Metric | Type | Meaning |
|---|---|---|
| `promotion.run.count` | counter | Number of PromotionRuns observed, labeled by phase. |
| `promotion.run.duration` | histogram | PromotionRun duration. |
| `promotion.check.result.count` | counter | Number of check results observed, labeled by phase. |
| `promotion.target.result.count` | counter | Number of target results observed, labeled by phase. |
| `promotion.evidence.count` | counter | Number of evidence records observed, labeled by type. |

Metric labels should use PRI semantic conventions.

## Resource And Scope

When emitting OpenTelemetry signals, Resource attributes describe the system
that produced or observed the signal. Instrumentation scope describes the
adapter, receiver, runtime, or collector component that emitted it.

Recommended resource attributes:

- `service.name`
- `service.version`
- `source.system`
- `source.kind`

Recommended scope name:

- the adapter, runtime, receiver, or collector component name.

## Correlation

Promotion observations should be correlated with these attributes when
available:

- `promotion.name`
- `promotion.unit`
- `promotion.run.name`
- `promotion.attempt.id`
- `artifact.name`
- `target.name`
- `check.name`
- `evidence.name`

For traces, child spans for checks and targets should share the PromotionRun
trace. For logs and events, the same identifiers should be attached as
attributes.

## Collector Use

A promotion collector can be implemented as PRI-native components, as
OpenTelemetry Collector components, or as an OpenTelemetry Collector
distribution where practical. The normative PRI idea is the component role, not
the underlying collector runtime:

- receivers ingest native promotion data or PRI records;
- processors validate, normalize, enrich, redact, deduplicate, or correlate;
- exporters send OpenTelemetry-compatible signals, PRI records, or both.

This keeps the project aligned with the existing telemetry ecosystem instead of
inventing a parallel collector protocol, while preserving PRI as the promotion
contract.

## Runtime Operations

PRI runtime operations such as `CancelPromotionRun`, `RetryPromotionRun`, and
`GetPromotionRun` are not OpenTelemetry operations. They remain part of PRI
runtime semantics. OpenTelemetry can observe those operations, but it does not
replace the runtime API or state model.

## Stability

This binding is part of the v0.1 public draft. Future versions may refine the
mapping as multiple independent implementations prove which signal shapes are
useful.
