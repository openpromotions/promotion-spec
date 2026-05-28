# PRI Examples

Examples are ordered from basic authoring to runtime and conformance records:

| Example | Purpose |
|---|---|
| `00-hello-promotion.yaml` | Complete Promotion intent with artifacts, checks, targets, delivery, and evidence. |
| `01-promotion-run.yaml` | Runtime PromotionRun with attempts, check results, and target results. |
| `02-evidence.yaml` | Standalone Evidence record. |
| `03-conformance-profile.yaml` | ConformanceProfile with `adoptionMode`. |
| `04-binding.yaml` | Binding document that summarizes an optional external mapping. |

Validate examples from the repository root:

```bash
python3 scripts/validate-example.py schemas/v0.1/promotion.schema.json examples/00-hello-promotion.yaml
python3 scripts/validate-example.py schemas/v0.1/promotionrun.schema.json examples/01-promotion-run.yaml
python3 scripts/validate-example.py schemas/v0.1/evidence.schema.json examples/02-evidence.yaml
python3 scripts/validate-example.py schemas/v0.1/conformance-profile.schema.json examples/03-conformance-profile.yaml
python3 scripts/validate-example.py schemas/v0.1/binding.schema.json examples/04-binding.yaml
```
