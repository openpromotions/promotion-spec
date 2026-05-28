# PRI Examples

These examples are ordered as a learning path. Read them from `00` to `05`.
Each file is self-contained and validates against a v0.1 JSON Schema. The
examples use YAML because it is easy to read. YAML is not the PRI wire format.
PRI defines the object contract and schemas; tools can exchange JSON, YAML,
database records, API resources, or another serialization that preserves the
same fields and semantics.

The first example is intentionally tiny. It teaches the whole base contract:

```text
promote this unit
with this artifact version
to this target
```

Everything after that adds one concept at a time.

```text
00 Hello-world Promotion contract
        |
        v
01 Promotion with checks, delivery, and inline evidence
        |
        v
02 PromotionRun runtime record
        |
        v
03 Standalone Evidence record

04 Binding describes an external mapping
05 ConformanceProfile describes an implementation
```

| Example | Concept | Purpose |
|---|---|---|
| `00-hello-promotion.yaml` | Promotion | The smallest valid promotion contract: unit, artifact, target. |
| `01-promotion-with-check.yaml` | Promotion | Adds checks, delivery handoff, labels, annotations, and inline evidence. |
| `02-promotion-run.yaml` | PromotionRun | Runtime status with attempts, check results, target results, and portable phases. |
| `03-evidence.yaml` | Evidence | A standalone evidence record linked to a promotion. |
| `04-binding.yaml` | Binding | How an external platform can advertise a PRI mapping. |
| `05-conformance-profile.yaml` | ConformanceProfile | What an implementation claims to support. |

## Why This Matters

Without a small shared contract, every tool describes promotion differently.
One tool may say release, another rollout, another sync, another approval, and
another deployment. PRI gives those systems a neutral record they can exchange
without changing their native architecture.

The hello-world contract is useful because it is the minimum stable question:

```text
what moved, which version moved, and where did it go?
```

That same shape can later be enriched with runtime state, checks, evidence,
bindings, and conformance claims.

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
to Kubernetes, GitOps, OCI, cloud, or any one delivery platform.

## How To Read The Flow

1. `00-hello-promotion.yaml` says what should advance.
2. `01-promotion-with-check.yaml` adds gates, delivery handoff, and evidence.
3. `02-promotion-run.yaml` says what happened when that intent ran.
4. `03-evidence.yaml` records why the result can be trusted.
5. `04-binding.yaml` says how an external system maps to PRI.
6. `05-conformance-profile.yaml` says what a runtime or adapter supports.

Bindings and conformance records are separate from promotions so existing tools
can adopt PRI incrementally. A tool can start by emitting `PromotionRun` and
`Evidence` records before it consumes `Promotion` intent.

## Tool Consumption Example

A tool that consumes `00-hello-promotion.yaml` should validate it, translate
`spec.unit`, `spec.artifacts[]`, and `spec.targets[]` into its native execution
model, then emit a `PromotionRun` like `02-promotion-run.yaml`. Evidence
produced during checks or delivery can be emitted as `03-evidence.yaml`.
