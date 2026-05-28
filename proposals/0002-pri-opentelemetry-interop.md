# Proposal 0002: PRI OpenTelemetry Interoperability

## Problem

OpenPromotions wants promotion data to work like OpenTelemetry works for
observability: many producers, common semantics, collectors, processors, and
many backends. At the same time, promotion is not only telemetry. Promotions
have durable intent, current runtime state, cancellation, retry, and auditable
evidence relationships.

PRI therefore needs OpenTelemetry interoperability without becoming an
OpenTelemetry extension or replacing the PRI data model.

## Proposal

Add three v0.1 documents:

- `spec/pri-opentelemetry.md`: maps PRI records to OpenTelemetry traces,
  logs/events, metrics, schema URL, resources, scope, and correlation.
- `spec/pri-semantic-conventions.md`: defines OpenPromotions semantic
  attributes for promotion telemetry.
- `spec/pri-collector.md`: defines a collector architecture aligned with
  OpenTelemetry Collector receivers, processors, and exporters.

PRI remains a separate standard. OpenTelemetry is a binding and an
implementation path for telemetry and collector infrastructure.

## Non-goals

- Do not define a new PRI wire protocol.
- Do not define a new collector runtime.
- Do not require OpenTelemetry for PRI core conformance.
- Do not claim upstream OpenTelemetry semantic-convention status.
- Do not place technology-specific tool mappings in `promotion-spec`.

## Compatibility

This proposal does not change existing PRI schemas. It adds an optional
interoperability layer.

## Alternatives Considered

- Extend OpenTelemetry directly. Rejected because promotion has control-plane
  state and lifecycle operations that are outside telemetry's role.
- Invent a PRI telemetry protocol. Rejected because OTLP and the OpenTelemetry
  Collector already provide mature telemetry transport and pipeline mechanics.
- Keep only descriptive Binding documents. Rejected as insufficient for the
  OpenTelemetry-for-promotions vision because semantic attributes and collector
  architecture need explicit guidance.

## Open Questions

- Which promotion metrics should become stable first.
- Whether the OpenPromotions semantic conventions should eventually be proposed
  upstream after independent implementations exist.
- Whether a future PRI runtime protocol is needed for control-plane operations.
