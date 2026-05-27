# PRI v0.1 Draft

PRI, the Promotion Runtime Interface, defines a portable promotion contract for
advancing versioned artifacts across explicit targets with auditable decisions.

This draft defines the core document model. Runtime semantics, bindings, and
conformance are defined in companion documents:

- [PRI Runtime v0.1](pri-runtime-v0.1.md)
- [PRI Bindings](pri-bindings.md)
- [PRI Conformance](pri-conformance.md)

## Goals

PRI should let compatible systems answer the same core question:

> Can this set of artifacts advance to these explicit targets under this plan,
> with these check outcomes, and what evidence explains the result?

## Non-goals

PRI does not manage fleet inventory, join clusters, reconcile applications,
provision infrastructure, prescribe one delivery system, or require a
particular transport, controller model, RPC protocol, CLI, storage backend, or
implementation language.

## Core Rule

The core PRI schema stays strict. Adapters and bindings absorb implementation
messiness.

An implementation may derive PRI fields from native objects, but any emitted PRI
document MUST contain the required PRI fields and MUST use the portable PRI
phase values. Native implementation values can be preserved in explicit
implementation-specific fields where defined.

## Document Envelope

PRI documents use an `apiVersion` / `kind` / `metadata` envelope. The v0.1
Promotion document requires:

- `apiVersion`: `pri/v0.1`.
- `kind`: `Promotion`.
- `metadata.name`: stable document identifier.

The PRI `apiVersion` declares the PRI contract version of the document. Runtime
or platform wrappers may have their own versioning, but wrapper versions are
outside the PRI core contract.

Portable identifiers such as `metadata.name`, `spec.unit`, `spec.artifacts[].name`,
`spec.targets[].name`, `spec.checks[].name`, `spec.evidence[].name`, and
`delivery.ref` are DNS-1123 subdomain compatible in v0.1.

## Promotion

A Promotion is intent to advance one logical unit and one or more artifacts
across explicit targets.

Required `spec` fields:

- `unit`: logical workload, service, component, or artifact stream name.
- `artifacts`: non-empty list of artifacts being promoted.
- `targets`: non-empty list of explicit targets.

Optional `spec` fields:

- `plan`: named plan reference.
- `checks`: checks that must be recorded before or during promotion.
- `evidence`: evidence records or references known at authoring time.

Optional metadata fields:

- `metadata.labels`: classification metadata.
- `metadata.annotations`: additional metadata.

## Artifact

An Artifact identifies a promoted item.

Required fields:

- `name`: stable artifact identifier.

Optional fields:

- `version`: human-readable version or release label.
- `digest`: content digest in `algorithm:value` form.
- `uri`: URI for locating the artifact or artifact metadata.

PRI core does not assign registry-specific meaning to `digest` or `uri`.
Bindings may define stronger interpretation and dereference behavior.

## Plan

A Plan defines ordering or strategy by reference.

Required fields when `plan` is present:

- `ref`: named plan reference known to the implementation.

PRI v0.1 intentionally does not define a portable plan DAG. Future versions may
standardize richer plan structure after implementations prove the common shape.

## Check

A Check is a named decision point that can block or inform promotion.

Required fields:

- `name`: stable check identifier.

Optional fields:

- `required`: boolean. `true` means failure blocks the promotion. `false` means
  the check is recorded but does not block by itself. The default is `true`.
- `policyRef`: named policy reference. PRI core does not define the policy
  language.
- `evidenceRefs`: names of evidence records that support the check.

PRI v0.1 uses `required` as a boolean. More detailed enforcement modes can be
added in a later version if real implementations need them.

## Target

A Target is an explicit place where artifacts may advance.

Required fields:

- `name`: stable target identifier.

Optional fields:

- `labels`: selection and audit labels.
- `delivery`: delivery handoff configuration.

## Delivery

Delivery describes how an implementation hands work to its native delivery
system. PRI does not require a specific delivery engine.

Required fields when `delivery` is present:

- `ref`: local delivery binding name.
- `mode`: one of `push`, `pull`, or `manual`.

Delivery modes:

- `push`: the implementation writes desired state directly.
- `pull`: the implementation publishes desired state to a location the target
  reconciles from.
- `manual`: the implementation records a manual handoff, approval-only flow, or
  audit-only promotion without automated delivery.

Optional fields:

- `parameters`: implementation-specific string map.

## Evidence

Evidence records why a promotion, check, or target result is trustworthy.

Required fields:

- `name`: stable evidence identifier.
- `type`: one of `verification`, `approval`, `test`, `scan`, `audit`, or `other`.
- `uri`: URI for the evidence record.

Optional fields:

- `digest`: content digest in `algorithm:value` form.

PRI core treats `uri` as a generic URI. Bindings may define URI schemes,
dereference behavior, and evidence formats.

## Minimal Promotion Document

```yaml
apiVersion: pri/v0.1
kind: Promotion
metadata:
  name: checkout-v123
spec:
  unit: checkout
  artifacts:
    - name: checkout
      version: v1.2.3
  targets:
    - name: prod-eu
```

## Complete Promotion Document

```yaml
apiVersion: pri/v0.1
kind: Promotion
metadata:
  name: checkout-v123
  labels:
    team: payments
  annotations:
    example.com/source: release-request
spec:
  unit: checkout
  artifacts:
    - name: checkout
      version: v1.2.3
      digest: sha256:abc123
      uri: https://example.com/artifacts/checkout/v1.2.3
  plan:
    ref: progressive
  checks:
    - name: security
      required: true
      policyRef: security-release-policy
      evidenceRefs:
        - security-scan
  targets:
    - name: prod-eu
      labels:
        stage: production
        region: eu
      delivery:
        ref: default
        mode: push
        parameters:
          path: services/checkout
  evidence:
    - name: security-scan
      type: verification
      uri: https://example.com/evidence/security-scan
      digest: sha256:def456
```
