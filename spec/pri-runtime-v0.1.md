# PRI Runtime v0.1

PRI runtime semantics describe how a compatible implementation records promotion
execution. They do not require a specific transport, controller model, RPC
protocol, CLI, storage backend, or implementation language.

## Runtime Objects

The runtime flow is:

```text
Promotion -> PromotionRun -> CheckResult -> TargetResult -> Evidence
```

`Promotion` is the authored intent. `PromotionRun` is a runtime record for
executing that intent. `CheckResult` and `TargetResult` record outcomes inside a
run. `Evidence` records why outcomes are trustworthy.

## PromotionRun

A PromotionRun records one runtime identity for executing a Promotion.

Required `spec` fields:

- `promotionRef`: name of the Promotion.

Required `status` fields:

- `phase`: one of `Pending`, `Running`, `Paused`, `Succeeded`, `Failed`, or
  `Cancelled`.

Optional `status` fields:

- `implementationPhase`: native implementation phase value, preserved for audit
  fidelity. The portable `phase` value remains closed and normative.
- `startedAt`: RFC 3339 timestamp for run start.
- `completedAt`: RFC 3339 timestamp for terminal completion.
- `attempts`: retry attempt history.
- `checkResults`: check outcomes.
- `targetResults`: target outcomes.

## Attempt

An Attempt records retry history within a PromotionRun.

Required fields:

- `id`: attempt identifier unique within the PromotionRun.
- `startedAt`: RFC 3339 timestamp for attempt start.

Optional fields:

- `completedAt`: RFC 3339 timestamp for attempt completion.
- `phase`: portable PromotionRun phase for this attempt.
- `implementationPhase`: native implementation phase value.

## CheckResult

CheckResult phases are:

- `Pending`
- `Running`
- `Succeeded`
- `Failed`
- `Skipped`

Each CheckResult references a check by name and may include evidence references.

## TargetResult

TargetResult phases are:

- `Pending`
- `Delivering`
- `Verifying`
- `Succeeded`
- `Failed`
- `Skipped`

Each TargetResult references a target by name and may include evidence
references.

## Semantic Operations

PRI v0.1 defines semantic operations. Implementations may expose them through
any interface.

| Operation | Meaning |
|---|---|
| `ValidatePromotion` | Validate that a Promotion document conforms to PRI. |
| `CreatePromotionRun` | Create a PromotionRun for a Promotion. |
| `StartPromotionRun` | Transition a pending PromotionRun into execution. |
| `GetPromotionRun` | Read the current PromotionRun state. |
| `CancelPromotionRun` | Request cancellation of a non-terminal PromotionRun. |
| `RetryPromotionRun` | Append a new attempt to an existing PromotionRun. |
| `RecordCheckResult` | Record a check outcome. |
| `RecordTargetResult` | Record a target outcome. |
| `RecordEvidence` | Record or attach evidence. |
| `GetRuntimeInfo` | Return implementation capabilities and supported PRI versions. |

These operations are semantic, not a required API. PRI v0.1 does not reserve or
require a remote operation protocol.

## State Transitions

PromotionRun portable transitions:

```text
Pending -> Running
Pending -> Cancelled
Running -> Paused
Paused -> Running
Running -> Succeeded
Running -> Failed
Running -> Cancelled
```

TargetResult portable transitions:

```text
Pending -> Delivering
Pending -> Skipped
Delivering -> Verifying
Delivering -> Failed
Verifying -> Succeeded
Verifying -> Failed
```

CheckResult portable transitions:

```text
Pending -> Running
Pending -> Skipped
Running -> Succeeded
Running -> Failed
```

## Retry Semantics

`RetryPromotionRun(id)` appends a new entry to `status.attempts[]` on the same
PromotionRun. The PromotionRun identity does not change.

Retry resets transient check and target result state as defined by the
implementation and re-enters `Running`. Terminal attempt history MUST remain
auditable. To create a fresh runtime identity, call `CreatePromotionRun` again.
