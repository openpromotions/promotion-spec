# PRI Bindings

A PRI binding specifies how PRI core objects map to a specific technology,
platform, format, transport, evidence format, artifact system, or storage
backend.

Bindings are normative within their scope but optional for PRI core
conformance. The core PRI documents stay technology-neutral.

## Categories

| Category | Question it answers |
|---|---|
| `platform` | Where does the implementation run or integrate? |
| `event` | How are lifecycle transitions emitted? |
| `evidence` | How is evidence encoded at an evidence URI? |
| `artifact` | How are artifact identifiers, digests, and URIs interpreted? |
| `storage` | How are PRI records persisted and queried? |

## Precedent

PRI bindings follow the same general pattern used by standards such as
CloudEvents and AsyncAPI: a technology-neutral core model, with separate binding
documents for transport-, platform-, format-, or ecosystem-specific mapping
rules.

## Binding Document Requirements

Every binding document should include:

1. Scope and version compatibility.
2. Object mapping table.
3. Field mapping table.
4. Translation rules for missing fields and type mismatches.
5. Round-trip behavior: lossless, lossy, or emission-only.
6. Conformance tests or executable examples.
7. References to authoritative external specifications where applicable.

## Binding Documents

A Binding document records a machine-readable summary of a binding. It is not a
core Promotion object and does not make the binding mandatory.

Tools use Binding documents to explain how they consume or emit PRI. A binding
should make clear whether the tool validates PRI input, emits PRI from native
state, consumes `Promotion` intent, bridges PRI to another API, or only supports
a subset of the contract.

Required fields:

- `apiVersion`: `pri/v0.1`.
- `kind`: `Binding`.
- `metadata.name`: stable binding identifier.
- `spec.category`: one of `platform`, `event`, `evidence`, `artifact`, or
  `storage`.
- `spec.priVersions`: PRI versions the binding supports.
- `spec.adoptionModes`: supported adoption modes.
- `spec.roundTrip`: one of `lossless`, `lossy`, or `emission-only`.

Optional fields:

- `spec.summary`: short human-readable description.
- `spec.mappings`: object and field mappings.
- `spec.requiredConfiguration`: named configuration values the binding needs.
- `spec.unsupported`: PRI fields or behaviors the binding cannot support.
- `spec.references`: authoritative external references.

Example:

```yaml
apiVersion: pri/v0.1
kind: Binding
metadata:
  name: example-platform
spec:
  category: platform
  summary: Example platform binding shape.
  priVersions:
    - v0.1
  adoptionModes:
    - emission
    - bridge
  roundTrip: lossy
  mappings:
    objects:
      - pri: Promotion
        external: ExampleRelease
      - pri: PromotionRun
        external: ExampleReleaseStatus
    fields:
      - pri: spec.artifacts
        external: release.inputs
      - pri: spec.targets
        external: release.destinations
  requiredConfiguration:
    - name: endpoint
      description: API endpoint for the external system.
  unsupported:
    - spec.plan
  references:
    - title: Example external reference
      uri: https://example.com/spec
```

## Adoption Modes

Bindings often support one of the adoption modes defined by PRI conformance:

- `native`: the implementation reads and writes PRI directly.
- `emission`: the implementation emits PRI records from its native model but
  does not consume PRI as input.
- `bridge`: an external adapter translates between a native model and PRI.

## Repository Placement

The `promotion-spec` repository defines the binding model and schemas. Specific
technology bindings should live outside the core specification repository, for
example in dedicated binding or integration repositories.
