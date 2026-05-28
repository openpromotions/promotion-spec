# PRI Conformance

PRI conformance describes what an implementation can do with PRI documents and
runtime records. v0.1 includes the conformance model, example profile, and
scenario fixtures. It does not yet include certification or signed attestations.

See [PRI Conformance v0.1](../spec/pri-conformance.md) for the normative
conformance model.

## Levels

| Level | Meaning |
|---|---|
| Document | Can parse and validate PRI documents against schemas. |
| Runtime | Can produce or persist `PromotionRun` records with portable phases. |
| Decision | Can consume `Promotion` intent and drive deterministic promotion decisions. |

## Adoption Modes

| Mode | Meaning |
|---|---|
| `native` | The implementation reads and writes PRI directly. |
| `emission` | The implementation emits PRI records from its native model but does not consume PRI. |
| `bridge` | An external adapter translates between a native model and PRI. |

Emission-only conformance is valid. It lets an existing platform expose
portable promotion records without restructuring around PRI as its native API.

## Scenarios

Initial scenarios live in [scenarios/](scenarios/):

| Scenario | Purpose |
|---|---|
| `00-happy-path.yaml` | Successful validation, run creation, check result, target result, evidence, and final state. |
| `01-failed-check.yaml` | Required check failure before target delivery succeeds. |
| `02-cancelled-run.yaml` | Running promotion transitions to terminal `Cancelled`. |

The scenario fixtures are intentionally small. They define semantic operations
and expected portable phases, not a required API or protocol.

## Validate Locally

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install jsonschema pyyaml
python scripts/validate-all.py
```

`validate-all.py` checks:

- JSON schema syntax;
- all bundled examples against their schemas;
- negative URI and timestamp validation;
- conformance scenario YAML parsing;
- required public launch files.

## What An Implementation Should Prove

A v0.1 implementation should publish a `ConformanceProfile` and enough evidence
for its claimed level:

- document conformance: examples validate against PRI schemas;
- runtime conformance: `PromotionRun`, `CheckResult`, and `TargetResult`
  records use portable phases;
- decision conformance: the implementation can consume `Promotion` intent and
  produce deterministic outcomes for the scenarios.

Future versions can add an executable test harness and signed profiles after
multiple independent implementations exercise the current model.
