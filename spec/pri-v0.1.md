# PRI v0.1 Draft

PRI, the Promotion Runtime Interface, defines a portable promotion contract.

This document is a draft. Normative language is intentionally light until early
implementations prove the shape of the contract.

## Goals

PRI should let compatible systems answer the same core question:

> Can this versioned artifact advance to these explicit targets under this
> plan, with these gate and approval outcomes, and what evidence explains the
> result?

## Non-goals

PRI does not manage fleet inventory, join clusters, reconcile GitOps
applications, provision infrastructure, or prescribe one delivery system.

## Core Objects

### Promotion

A Promotion is intent to advance one versioned artifact through a plan across
explicit targets.

PRI documents use an `apiVersion` / `kind` / `metadata` envelope. The v0.1
Promotion document requires:

- `apiVersion`: PRI version for the document.
- `kind`: `Promotion`.
- `metadata.name`: stable promotion identifier.

Required `spec` fields:

- `unit`: logical workload or artifact stream name.
- `version`: desired version or artifact reference.
- `targets`: explicit non-empty list of targets.

Optional fields:

- `spec.plan`: named rollout plan.
- `metadata.labels`: implementation-neutral classification metadata.
- `metadata.annotations`: implementation-neutral metadata.

### Target

A Target is an explicit place where a version may advance.

Required fields:

- `name`: stable target identifier.

Optional fields:

- `labels`: selection and audit labels.
- `delivery`: delivery handoff configuration.

### Delivery

Delivery describes how an implementation hands work to the native delivery
system. PRI does not require a specific delivery engine.

Common fields:

- `ref`: local delivery binding name.
- `mode`: `push` or `pull`.
- `parameters`: implementation-specific string map.

### Plan

A Plan defines stage ordering and promotion strategy. PRI v0.1 treats `plan` as
a named reference. A later draft can define the full portable plan shape.

### Evidence

Evidence records why a promotion advanced, paused, or failed.

Evidence should include:

- decision timestamp;
- implementation identity;
- target name;
- gate and approval outcomes;
- delivery handoff identity;
- native status links when available.

## Runtime Contract

The draft runtime shape is:

```text
Promotion -> PromotionRun -> TargetResult -> Evidence
```

`PromotionRun` is an informative v0.1 term for one attempt to execute a
Promotion. `TargetResult` is an informative v0.1 term for the outcome recorded
for one target in that attempt. Their portable document shapes are intentionally
left to a later draft.

PRI-compatible implementations may store these records in Kubernetes resources,
files, databases, CI artifacts, or another durable store.

## Minimal Promotion Document

```yaml
apiVersion: pri/v0.1
kind: Promotion
metadata:
  name: checkout-v123
spec:
  unit: checkout
  version: v1.2.3
  plan: progressive
  targets:
    - name: prod-eu
      labels:
        stage: production
        region: eu
      delivery:
        ref: delivery-system
        mode: push
```

## Draft Conformance Levels

| Level | Meaning |
|---|---|
| Document | Can parse and validate PRI documents. |
| Decision | Can evaluate plan, gate, and approval state into deterministic next actions. |
| Runtime | Can persist promotion attempts, target results, and evidence. |

The conformance suite is not implemented in v0.1.
