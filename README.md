# Promotion Runtime Interface Specification

The Promotion Runtime Interface (PRI) is an open specification for safely
advancing versioned artifacts across explicit targets with auditable decisions.

PRI defines a shared promotion contract. It lets CI/CD, GitOps, fleet,
compliance, release, and internal platform systems exchange promotion intent,
runtime status, and evidence without adopting the same implementation.

## Status

PRI v0.1 is a public draft for review and early implementation experiments.
The repository is ready for public discussion, examples, and prototype
adapters. The contract is intentionally small, but breaking changes can still
happen before a stable release.

## Why PRI Exists

Every delivery platform has to answer the same promotion questions:

- what is being promoted;
- which version or artifact is intended;
- which targets are eligible;
- which checks, approvals, and policies apply;
- what happened at runtime;
- what evidence proves the decision and result.

Today those answers are usually trapped inside individual tools. PRI makes the
answers portable.

The goal is not to replace existing delivery systems. The goal is to make
promotion state understandable across them.

## Architecture

PRI is a layered contract:

```text
Existing tools and platforms
        |
        v
Adapters and bindings
        |
        v
PRI documents and runtime semantics
        |
        +--> conformance scenarios
        +--> evidence and audit records
```

| Layer | What PRI defines | What stays outside core |
|---|---|---|
| Format | `Promotion`, `PromotionRun`, `Evidence`, `ConformanceProfile`, `Binding` documents and JSON Schemas | External storage, API envelopes, database schemas |
| Runtime | Semantic operations and portable state transitions | Required CLI, RPC, controller, workflow engine, or transport |
| Policy | Check references, required/advisory behavior, and result records | Policy language, policy agent, approval system, or rules engine |
| Bindings | How external systems map to PRI, including adoption mode and round-trip behavior | Tool-specific implementation details |
| Conformance | Levels, modes, examples, and scenarios | Product certification or signed attestation in v0.1 |

See [Architecture boundaries](docs/architecture-boundaries.md) for the strict
line between PRI core and implementation-specific integration.

## Core Flow

The v0.1 runtime flow is:

```text
Promotion -> PromotionRun -> CheckResult -> TargetResult -> Evidence
```

- `Promotion` records intent.
- `PromotionRun` records execution state for that intent.
- `CheckResult` records policy, test, approval, or verification outcomes.
- `TargetResult` records per-target delivery or verification outcomes.
- `Evidence` records why a decision or result is trustworthy.

## How Tools Use PRI

PRI is consumed as documents and semantics, not as a required service.

```text
Native tool state
        |
        v
validate / translate / emit / consume
        |
        v
PRI Promotion, PromotionRun, Evidence, Binding, ConformanceProfile
```

A tool can adopt PRI in one or more ways:

| Use | What the tool does |
|---|---|
| Validate | Accept PRI documents only when they pass the JSON Schemas and contract rules. |
| Emit | Export `PromotionRun` and `Evidence` records from native release or deployment state. |
| Consume | Read a `Promotion` document as intent, then record resulting `PromotionRun` status. |
| Bridge | Translate between a native model and PRI while documenting lossless, lossy, or emission-only behavior. |
| Claim conformance | Publish a `ConformanceProfile` that states supported PRI version, adoption mode, and conformance level. |

Tools do not have to implement every PRI object on day one. An existing system
can start by emitting portable `PromotionRun` and `Evidence` records. A deeper
integration can later consume `Promotion` intent directly.

## Minimal Example

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

More examples are in [examples/](examples/).

## Quick Start

Validate the repository examples locally:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install jsonschema pyyaml
python scripts/validate-all.py
```

Validate a single document:

```bash
python scripts/validate-example.py \
  schemas/v0.1/promotion.schema.json \
  examples/00-hello-promotion.yaml
```

The same validation runs in GitHub Actions.

## What PRI Is

- A portable promotion document model.
- A runtime semantic model with portable phases.
- A binding model for existing tools and platforms.
- A conformance starting point for implementations and adapters.

## What PRI Is Not

- Not a fleet manager.
- Not a cluster lifecycle system.
- Not a GitOps reconciler.
- Not a pipeline engine.
- Not a policy agent.
- Not a cloud provisioning API.
- Not a telemetry pipeline.
- Not tied to Kubernetes, OCI, Git, CI/CD, or any one runtime.

## Adoption Modes

Implementations can adopt PRI at different depths:

| Mode | Meaning |
|---|---|
| `native` | The implementation reads and writes PRI directly. |
| `emission` | The implementation emits PRI records from its native model but does not consume PRI as input. |
| `bridge` | An external adapter translates between a native model and PRI. |

Emission-only adoption is valid. Existing systems can participate by emitting
portable promotion records before they consume PRI as input.

## Repository Map

Core contract:

- [PRI v0.1 draft](spec/pri-v0.1.md)
- [PRI Runtime v0.1](spec/pri-runtime-v0.1.md)
- [PRI Bindings](spec/pri-bindings.md)
- [PRI Conformance](spec/pri-conformance.md)
- [Promotion JSON Schema](schemas/v0.1/promotion.schema.json)
- [PromotionRun JSON Schema](schemas/v0.1/promotionrun.schema.json)
- [Evidence JSON Schema](schemas/v0.1/evidence.schema.json)
- [ConformanceProfile JSON Schema](schemas/v0.1/conformance-profile.schema.json)
- [Binding JSON Schema](schemas/v0.1/binding.schema.json)

Adoption and interoperability:

- [Architecture boundaries](docs/architecture-boundaries.md)
- [Tool integration guide](docs/tool-integration.md)
- [CNCF path](docs/cncf-path.md)

Examples and project process:

- [Examples guide](examples/README.md)
- [Conformance notes](conformance/README.md)
- [Design proposals](proposals/README.md)
- [Governance](GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)

## Contributing

Promotion interoperability will only be useful if it reflects real-world
release, compliance, fleet, GitOps, pipeline, and platform needs.

Contributions are welcome in the form of:

- issue reports describing promotion workflows PRI should support;
- examples from existing tools and internal platforms;
- schema and terminology improvements;
- binding proposals for existing ecosystems;
- conformance ideas;
- pull requests that make the draft clearer and easier to implement.

If you work on delivery platforms, CI/CD, GitOps, fleet management, compliance,
security checks, or internal developer platforms, your feedback can materially
improve the outcome of this specification.
