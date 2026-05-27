# PRI Bindings

A PRI binding specifies how PRI core objects map to a specific technology,
platform, format, transport, evidence format, artifact system, or storage
backend.

Bindings are normative within their scope but optional for PRI core
conformance. The core PRI documents stay technology-neutral.

## Categories

| Category | Question it answers |
|---|---|
| Platform | Where does the implementation run or integrate? |
| Event | How are lifecycle transitions emitted? |
| Evidence | How is evidence encoded at an evidence URI? |
| Artifact | How are artifact identifiers, digests, and URIs interpreted? |
| Storage | How are PRI records persisted and queried? |

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

## Adoption Modes

Bindings often support one of the adoption modes defined by PRI conformance:

- `native`: the implementation reads and writes PRI directly.
- `emission`: the implementation emits PRI records from its native model but
  does not consume PRI as input.
- `bridge`: an external adapter translates between a native model and PRI.
