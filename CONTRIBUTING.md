# Contributing

PRI is early. Contributions should start with issues or small pull requests.

## Design Changes

Large contract changes should be proposed as a short RFC in `proposals/` before
implementation.

## Validation

Validate the repository with:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install jsonschema pyyaml
python scripts/validate-all.py
```

To validate one example, pass a schema and document:

```bash
python scripts/validate-example.py \
  schemas/v0.1/promotion.schema.json \
  examples/00-hello-promotion.yaml
```
