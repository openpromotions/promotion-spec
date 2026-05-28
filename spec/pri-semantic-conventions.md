# PRI Signal Semantic Conventions v0.1

PRI signal semantic conventions define common attribute names for promotion
signals, records, bindings, and collectors. They make promotion data queryable
across tools without forcing those tools to use the same promotion runtime.

These conventions intentionally follow OpenTelemetry-style attribute naming so
the same data can be carried as OpenTelemetry spans, log records, and metrics.
They are defined by OpenPromotions, are not part of the PRI core schema, and are
not upstream OpenTelemetry semantic conventions.

The convention namespace is intentionally plain:

- `promotion.*` for promotion intent and runs.
- `artifact.*` for promoted artifacts.
- `target.*` for promotion targets.
- `check.*` for checks and check results.
- `evidence.*` for evidence.
- `delivery.*` for delivery handoff.
- `binding.*` for binding metadata.
- `source.*` for native source systems and adapters.
- `collector.*` for generic collector pipeline metadata.

## Requirement Levels

| Level | Meaning |
|---|---|
| Required | Must be present when the concept exists in the signal or record. |
| Recommended | Should be present when available. |
| Optional | Useful for correlation or diagnostics, but not required. |

## Promotion Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `promotion.name` | string | Required | Promotion `metadata.name`. |
| `promotion.unit` | string | Required | Logical unit being promoted. |
| `promotion.plan.ref` | string | Optional | Plan reference. |
| `promotion.run.name` | string | Recommended | PromotionRun `metadata.name`. |
| `promotion.run.phase` | string | Recommended | Portable PromotionRun phase. |
| `promotion.run.implementation_phase` | string | Optional | Native implementation phase. |
| `promotion.attempt.id` | string | Optional | Attempt identifier within a PromotionRun. |
| `promotion.event.name` | string | Recommended | Promotion event name such as `promotion.run.state.changed`. |

## Artifact Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `artifact.name` | string | Required | Artifact name. |
| `artifact.version` | string | Recommended | Human-readable artifact version. |
| `artifact.digest` | string | Recommended | Content digest in `algorithm:value` form. |
| `artifact.uri` | string | Optional | URI for locating artifact metadata or content. |

## Target Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `target.name` | string | Required | Target name. |
| `target.phase` | string | Recommended | Portable TargetResult phase. |
| `target.implementation_phase` | string | Optional | Native implementation phase. |

## Check Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `check.name` | string | Required | Check name. |
| `check.required` | boolean | Recommended | Whether failure blocks promotion. |
| `check.phase` | string | Recommended | Portable CheckResult phase. |
| `check.policy.ref` | string | Optional | Policy reference. |
| `check.implementation_phase` | string | Optional | Native implementation phase. |

## Evidence Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `evidence.name` | string | Required | Evidence name. |
| `evidence.type` | string | Required | Evidence type. |
| `evidence.uri` | string | Recommended | Evidence URI. |
| `evidence.digest` | string | Optional | Evidence digest. |

## Delivery Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `delivery.ref` | string | Recommended | Delivery binding reference. |
| `delivery.mode` | string | Recommended | `push`, `pull`, or `manual`. |

## Binding Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `binding.name` | string | Required | Binding document name. |
| `binding.category` | string | Required | Binding category. |
| `binding.round_trip` | string | Recommended | `lossless`, `lossy`, or `emission-only`. |
| `binding.adoption_mode` | string | Recommended | `native`, `emission`, or `bridge`. |

## Source And Collector Attributes

| Attribute | Type | Level | Meaning |
|---|---|---|---|
| `source.system` | string | Recommended | Native source system or runtime name. |
| `source.kind` | string | Recommended | Source role such as `runtime`, `receiver`, `bridge`, or `adapter`. |
| `source.version` | string | Optional | Native source version. |
| `collector.receiver` | string | Optional | Collector receiver name. |
| `collector.processor` | string | Optional | Collector processor name. |
| `collector.exporter` | string | Optional | Collector exporter name. |
| `collector.pipeline` | string | Optional | Collector pipeline name. |

## Event Names

| Event name | Required attributes |
|---|---|
| `promotion.intent.observed` | `promotion.name`, `promotion.unit` |
| `promotion.run.state.changed` | `promotion.name`, `promotion.run.name`, `promotion.run.phase` |
| `promotion.check.result.recorded` | `promotion.name`, `promotion.run.name`, `check.name`, `check.phase` |
| `promotion.target.result.recorded` | `promotion.name`, `promotion.run.name`, `target.name`, `target.phase` |
| `promotion.evidence.recorded` | `promotion.name`, `evidence.name`, `evidence.type` |
| `promotion.binding.capability.observed` | `binding.name`, `binding.category` |

## Naming Rules

Attribute names are lowercase, dot-separated, and stable once published.
Technology-specific attributes belong in binding documents, not in the core PRI
semantic conventions. OpenTelemetry compatibility bindings may map these
attributes into OTel signals, but PRI core documents do not import OTel semantic
convention groups.
