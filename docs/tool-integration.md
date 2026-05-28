# Tool Integration Guide

This guide explains how existing tools can consume or emit PRI without changing
their native architecture.

PRI is a contract. A tool integrates by reading, writing, or translating PRI
documents.

## Integration Roles

| Role | Description | Minimum output |
|---|---|---|
| Validator | Checks PRI documents before storing or acting on them. | Schema validation result. |
| Emitter | Converts native promotion, release, deployment, or approval state into PRI records. | `PromotionRun` and optional `Evidence`. |
| Consumer | Reads `Promotion` intent and acts on it through the tool's native engine. | `PromotionRun` status. |
| Bridge | Translates between PRI and another API or file format in both directions where possible. | `Binding` document and translated records. |
| Policy agent | Evaluates policy, approvals, or checks for a promotion. | `CheckResult` and `Evidence`; not a PRI core component. |

## Minimal Adoption Path

1. Validate PRI documents with the JSON Schemas in `schemas/v0.1/`.
2. Choose an adoption mode: `native`, `emission`, or `bridge`.
3. Map native concepts to PRI objects.
4. Preserve portable required fields and phase values.
5. Preserve native phase names in `implementationPhase` when useful.
6. Emit `Evidence` records for approvals, scans, tests, audits, or policy
   decisions.
7. Publish a `Binding` document if the mapping is reusable.
8. Publish a `ConformanceProfile` describing what the integration supports.

## Mapping Native State

| Native concept | PRI target |
|---|---|
| Release request, deployment request, promotion request | `Promotion` |
| Run, execution, rollout, sync, deployment attempt | `PromotionRun` |
| Stage, environment, cluster, region, account | `Target` or `TargetResult` |
| Approval, policy, test, scan, quality gate | `Check` or `CheckResult` |
| Artifact, image, chart, package, manifest bundle | `Artifact` |
| Audit record, scan result, approval link, report | `Evidence` |
| Tool-specific integration mapping | `Binding` |
| Capability claim | `ConformanceProfile` |

## Consuming Promotion Intent

A consumer accepts a `Promotion` document as intent. It should:

1. validate the document against `promotion.schema.json`;
2. resolve any local `plan.ref`, `delivery.ref`, `policyRef`, or evidence
   references it understands;
3. create or persist a `PromotionRun`;
4. record check and target results with portable phases;
5. attach evidence references for decisions and outcomes;
6. expose the resulting `PromotionRun` and `Evidence` records.

PRI does not define how the tool performs delivery. Delivery remains native to
the consuming tool.

## Emitting From Existing Tools

An emitter does not need to consume PRI input. It observes native state and
exports PRI records.

An emission-only integration should:

- create stable PRI names for promotions and runs;
- set `spec.promotionRef` on `PromotionRun`;
- map native state into portable phases;
- preserve native phase values in `implementationPhase`;
- emit evidence URIs and digests when available;
- document unsupported PRI fields in a `Binding` document.

Emission-only integrations are valuable because they make existing promotion
history portable without forcing a platform migration.

## Binding Documents

A `Binding` document explains the mapping between PRI and another system. It
should say:

- which PRI versions are supported;
- whether the mapping is `lossless`, `lossy`, or `emission-only`;
- which adoption modes are supported;
- how objects and fields map;
- which PRI fields or behaviors are unsupported;
- which external specifications or APIs are authoritative.

## Contract Rules For Tools

Tools should follow these rules when producing PRI:

1. Required PRI fields must be present.
2. Portable phase enums must stay closed.
3. Native phase names belong in `implementationPhase`.
4. Tool-specific fields belong in native systems, bindings, labels, or
   annotations, not in the PRI core schema.
5. Evidence should be referenced with stable URIs and digests when available.
6. A tool should publish its adoption mode and conformance level.

The result is interoperability without requiring every tool to share the same
runtime, policy language, storage backend, or delivery engine.
