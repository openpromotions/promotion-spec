# Promotion Runtime Interface Specification

The Promotion Runtime Interface (PRI) is a draft open specification for safely
advancing versioned artifacts across explicit targets with auditable decisions.

Every delivery platform has to answer the same promotion questions:

- what is being promoted;
- which version or artifact is intended;
- which targets are eligible;
- which gates, approvals, and policies apply;
- what happened at runtime;
- what evidence proves the decision and result.

Today those answers are usually trapped inside individual CI/CD, GitOps, fleet,
and internal platform tools. PRI exists to define a shared promotion contract so
systems can exchange promotion intent, status, and evidence without adopting the
same implementation.

## Motivation

Cloud-native infrastructure has repeatedly benefited from small, clear
interoperability contracts. PRI follows that pattern for promotion workflows:
separate the contract from implementations, keep the core portable, and let many
tools implement or translate the same interface.

The goal is not to replace existing delivery systems. The goal is to make
promotion state understandable across them.

## Scope

PRI defines the portable shape of:

- promotion intent;
- targets and target metadata;
- rollout plans and stage ordering;
- gate and approval outcomes;
- runtime status;
- decision evidence;
- conformance expectations.

PRI does not define:

- cluster lifecycle;
- fleet inventory ownership;
- GitOps reconciliation;
- pipeline execution;
- cloud provisioning;
- a required implementation language.

## Example

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

The first draft centers on this runtime flow:

```text
Promotion -> PromotionRun -> TargetResult -> Evidence
```

## Repository Status

This repository is intentionally spec-driven. It should contain the contract,
schemas, examples, and conformance material. Reference engines, fleet managers,
delivery platforms, and SDKs should live outside this repository unless the
community later agrees otherwise.

PRI is experimental. Breaking changes are expected while the first
implementations prove the contract.

## Contributing

Promotion interoperability will only be useful if it reflects real-world
release, compliance, fleet, GitOps, pipeline, and platform needs.

Contributions are welcome in the form of:

- issue reports describing promotion workflows PRI should support;
- examples from existing tools and internal platforms;
- schema and terminology improvements;
- conformance ideas;
- pull requests that make the draft clearer and easier to implement.

If you work on delivery platforms, CI/CD, GitOps, fleet management, compliance,
security gates, or internal developer platforms, your feedback can materially
improve the outcome of this specification.

