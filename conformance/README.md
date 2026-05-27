# PRI Conformance

PRI v0.1 includes a conformance skeleton: levels, adoption modes, schemas, and
scenario fixtures.

See [PRI Conformance v0.1](../spec/pri-conformance.md) for the normative
conformance model.

Initial scenarios live in [`scenarios/`](scenarios/):

- `00-happy-path.yaml`
- `01-failed-check.yaml`
- `02-cancelled-run.yaml`

The first executable suite should validate documents, run the semantic runtime
operations against an implementation, and compare resulting PromotionRun records
with expected portable phases.
