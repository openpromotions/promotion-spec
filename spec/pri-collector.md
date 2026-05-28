# PRI Collector Architecture v0.1

A PRI collector receives promotion records or native promotion events, processes
them into PRI records and/or interoperable promotion signals, and exports them
to one or more backends.

The collector is an adoption layer. It lets existing systems participate in PRI
without changing their native APIs.

The architecture mirrors the receiver/processor/exporter pipeline used by
OpenTelemetry Collector and similar data pipeline systems. Implementations may
build PRI components as OpenTelemetry Collector components where practical, but
PRI v0.1 does not require the OpenTelemetry Collector and does not define a
separate collector runtime or wire protocol.

## Pipeline Model

PRI collector pipelines follow this shape:

```text
receivers -> processors -> exporters
```

OpenTelemetry Collector also has connectors and extensions. PRI v0.1 derives
only the basic component roles and standardizes the promotion vocabulary for
receivers, processors, and exporters.

## Receivers

Receivers ingest data.

Examples of receiver categories:

- file receiver: reads PRI records or telemetry observations from files.
- webhook receiver: accepts HTTP POST payloads.
- native-tool receiver: watches or polls a native system and translates output
  into PRI records or interoperable promotion signals.

Receivers are trust boundaries. A receiver should validate input enough to
protect the rest of the pipeline.

## Processors

Processors transform, filter, or enrich data.

Common processors:

- validate: validate records against PRI schemas.
- normalize: convert native names and phases into PRI semantic conventions.
- correlate: connect Promotion, PromotionRun, CheckResult, TargetResult, and
  Evidence records.
- redact: remove sensitive attributes.
- deduplicate: suppress repeated observations.
- enrich: attach environment, source, or ownership metadata.

## Exporters

Exporters send PRI records, interoperable promotion signals, or both to another
system.

Example exporter categories:

- stdout/debug exporter.
- file or JSONL exporter.
- SQL or document-store exporter.
- event exporter.
- audit or compliance exporter.
- collector exporter for forwarding to another PRI collector.

Exporter-specific behavior belongs in binding documents.

## Collector Configuration Shape

This example is informative. It follows the receiver/processor/exporter shape
popularized by OpenTelemetry Collector configuration without standardizing a PRI
collector implementation or requiring OpenTelemetry Collector.

```yaml
receivers:
  pri_file:
    path: ./promotion-signals.jsonl
  pri_webhook:
    endpoint: :4319

processors:
  pri_validate: {}
  pri_correlate: {}

exporters:
  stdout: {}
  pri_file:
    path: ./normalized-promotions.jsonl

service:
  pipelines:
    promotion-signals:
      receivers: [pri_file, pri_webhook]
      processors: [pri_validate, pri_correlate]
      exporters: [stdout, pri_file]
```

## Relationship To Bindings

Bindings describe how a collector component maps between PRI and another
system. A binding can describe a receiver, processor, exporter, or native
runtime integration.

Collectors can use Binding documents to advertise supported mappings and to
explain whether a mapping is `lossless`, `lossy`, or `emission-only`.

## No Wire Protocol In v0.1

PRI v0.1 does not define a new wire protocol. OpenTelemetry OTLP can carry the
OpenTelemetry-compatible representation of promotion signals. PRI documents can
still be exchanged through files, webhooks, queues, APIs, or future bindings.
