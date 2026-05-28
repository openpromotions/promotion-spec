# PRI Conformance v0.1

PRI conformance describes what an implementation can do with PRI documents and
runtime records.

## Conformance Levels

| Level | Meaning |
|---|---|
| Document | Can parse and validate PRI documents against schemas. |
| Runtime | Can produce or persist PromotionRun records with portable phases. |
| Decision | Can consume PRI intent and drive deterministic promotion decisions. |

An implementation may support some levels without supporting all of them.

## Adoption Modes

| Mode | Meaning |
|---|---|
| `native` | Implementation reads and writes PRI directly. |
| `emission` | Implementation emits PRI records from its native model but does not consume PRI. |
| `bridge` | External adapter translates between a native model and PRI. |

Emission-only conformance is valid. It lets existing systems expose portable PRI
records without restructuring around PRI as their native model.

## ConformanceProfile

A ConformanceProfile records the supported PRI version, adoption mode, and
conformance levels for an implementation.

Conformance is a claim about a tool's PRI behavior. It does not imply that the
tool is a PRI-specific runtime. Existing release, VM deployment, GitOps,
approval, policy, and audit systems can publish ConformanceProfiles for the
parts of PRI they consume or emit.

```yaml
apiVersion: pri/v0.1
kind: ConformanceProfile
metadata:
  name: example-runtime
spec:
  priVersion: v0.1
  adoptionMode: emission
  conformance:
    document: true
    runtime: true
    decision: false
```

The v0.1 ConformanceProfile is unsigned. Signing and attestation can be added
after the conformance suite is exercised by independent implementations.
