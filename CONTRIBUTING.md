# Contributing

PRI is early. Contributions should start with issues or small pull requests.

## Design Changes

Large contract changes should be proposed as a short RFC in `proposals/` before
implementation.

## Validation

Validate JSON files with:

```bash
for schema in schemas/v0.1/*.json; do
  python3 -m json.tool "$schema" >/dev/null
done
python3 scripts/validate-example.py schemas/v0.1/promotion.schema.json examples/00-hello-promotion.yaml
python3 scripts/validate-example.py schemas/v0.1/promotionrun.schema.json examples/01-promotion-run.yaml
python3 scripts/validate-example.py schemas/v0.1/evidence.schema.json examples/02-evidence.yaml
python3 scripts/validate-example.py schemas/v0.1/conformance-profile.schema.json examples/03-conformance-profile.yaml
python3 scripts/validate-example.py schemas/v0.1/binding.schema.json examples/04-binding.yaml
```
