# PRI Stability Policy

This policy defines what "stable" means for PRI v0.1.

PRI v0.1 is the first public contract. It is stable for early adopters who want
to validate, emit, consume, or bridge promotion records. This is a contract
stability claim, not a claim that the ecosystem is complete.

## Stability Scope

The v0.1 stability promise covers:

- document kinds: `Promotion`, `PromotionRun`, `Evidence`, `Binding`,
  `ConformanceProfile`;
- required fields in `schemas/v0.1/`;
- closed portable phase enums;
- evidence type enum values;
- adoption mode values;
- binding category and round-trip values;
- semantic runtime operation names and their meanings;
- example order and validation commands.

## Compatibility Rules

Within v0.1, changes must be backward-compatible.

Allowed changes:

- clarify prose without changing meaning;
- add examples;
- add optional fields when older documents remain valid;
- add non-normative guidance;
- strengthen validation tooling without rejecting valid v0.1 documents.

Breaking changes require a new minor version such as `v0.2`.

Breaking changes include:

- removing or renaming a field;
- making an optional field required;
- changing enum values;
- changing the meaning of a portable phase;
- changing the meaning of a semantic runtime operation;
- changing identifier rules in a way that rejects previously valid names;
- changing evidence mapping between inline and standalone Evidence;
- changing adoption mode or conformance level semantics.

## Wire Format

PRI v0.1 does not define a required wire format. YAML examples are for humans.
JSON Schemas define the object contract. Implementations may use any
serialization that preserves required fields, enum values, and semantics.

## Extension Points

Implementations should use these extension points instead of changing core
schemas:

- `metadata.labels` and `metadata.annotations` for metadata;
- `implementationPhase` for native phase names;
- `delivery.parameters` for delivery-specific string configuration;
- `Binding` documents for platform, event, evidence, artifact, storage,
  transport, VM deployment, and other mapping details;
- external evidence formats referenced by `Evidence.spec.uri`.

## Release Criteria

A v0.1 release is publishable only when:

- all JSON Schemas parse;
- all bundled examples validate against their schemas;
- conformance scenarios validate against their schema;
- negative URI, timestamp, and semantic-operation checks fail as expected;
- required public files exist;
- no removed or renamed example paths are referenced by docs;
- CI is green on `main`.

## Stability Boundary

PRI stability covers the contract, not any one implementation. A tool can be
conformant without using a PRI-specific runtime, controller, policy agent,
storage backend, delivery engine, or wire protocol.
