# PRI Examples

These examples are ordered as a learning path. Read them from `00` to `04`.
Each file is self-contained and validates against a v0.1 JSON Schema.

```text
00 Promotion intent
        |
        v
01 PromotionRun runtime record
        |
        v
02 Evidence record

03 ConformanceProfile describes an implementation
04 Binding describes an optional external mapping
```

| Example | Concept | Purpose |
|---|---|---|
| `00-hello-promotion.yaml` | Promotion | A complete promotion intent with artifacts, checks, targets, delivery, and evidence. |
| `01-promotion-run.yaml` | PromotionRun | Runtime status with attempts, check results, target results, and portable phases. |
| `02-evidence.yaml` | Evidence | A standalone evidence record linked to a promotion. |
| `03-conformance-profile.yaml` | ConformanceProfile | What an implementation claims to support. |
| `04-binding.yaml` | Binding | How an external platform can advertise a PRI mapping. |

## Run The Examples

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install jsonschema pyyaml
python scripts/validate-all.py
```

Validate one example:

```bash
python scripts/validate-example.py \
  schemas/v0.1/promotion.schema.json \
  examples/00-hello-promotion.yaml
```

The example URLs use `example.com` placeholders. They are intentionally not tied
to Kubernetes, GitOps, OCI, OpenTelemetry, or any one delivery platform.

## How To Read The Flow

1. `00-hello-promotion.yaml` says what should advance.
2. `01-promotion-run.yaml` says what happened when that intent ran.
3. `02-evidence.yaml` records why the result can be trusted.
4. `03-conformance-profile.yaml` says what a runtime or adapter supports.
5. `04-binding.yaml` says how an external system maps to PRI.

Bindings and conformance records are separate from promotions so existing tools
can adopt PRI incrementally. A tool can start by emitting `PromotionRun` and
`Evidence` records before it consumes `Promotion` intent.
