# Promotion Runtime Interface Specification

The Promotion Runtime Interface (PRI) is a draft open specification for safely
advancing versioned artifacts across explicit targets with auditable decisions.

Every delivery platform has to answer the same promotion questions:

- what is being promoted;
- which version or artifact is intended;
- which targets are eligible;
- which checks, approvals, and policies apply;
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
- check and approval outcomes;
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
  artifacts:
    - name: checkout
      version: v1.2.3
  plan:
    ref: progressive
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
Promotion -> PromotionRun -> CheckResult -> TargetResult -> Evidence
```

## Repository Status

This repository is intentionally spec-driven. It should contain the contract,
schemas, examples, and conformance material. Reference engines, fleet managers,
delivery platforms, and SDKs should live outside this repository unless the
community later agrees otherwise.

PRI is experimental. Breaking changes are expected while the first
implementations prove the contract.

Current core draft material:

- [PRI v0.1 draft](spec/pri-v0.1.md)
- [PRI Runtime v0.1](spec/pri-runtime-v0.1.md)
- [PRI Bindings](spec/pri-bindings.md)
- [PRI Conformance](spec/pri-conformance.md)
- [Promotion JSON Schema](schemas/v0.1/promotion.schema.json)
- [PromotionRun JSON Schema](schemas/v0.1/promotionrun.schema.json)
- [Evidence JSON Schema](schemas/v0.1/evidence.schema.json)
- [ConformanceProfile JSON Schema](schemas/v0.1/conformance-profile.schema.json)
- [Binding JSON Schema](schemas/v0.1/binding.schema.json)

Optional interoperability and adoption material:

- [Architecture boundaries](docs/architecture-boundaries.md)
- [PRI OpenTelemetry Compatibility Binding](spec/pri-opentelemetry.md)
- [PRI Signal Semantic Conventions](spec/pri-semantic-conventions.md)
- [PRI Collector Architecture](spec/pri-collector.md)
- [Hello Promotion example](examples/00-hello-promotion.yaml)
- [Examples guide](examples/README.md)
- [Conformance notes](conformance/README.md)
- [Governance](GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)

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
security checks, or internal developer platforms, your feedback can materially
improve the outcome of this specification.
