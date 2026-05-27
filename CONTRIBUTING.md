# Contributing

PRI is early. Contributions should start with issues or small pull requests.

## Design Changes

Large contract changes should be proposed as a short RFC in `proposals/` before
implementation.

## Validation

Validate JSON files with:

```bash
python3 -m json.tool schemas/v0.1/promotion.schema.json >/dev/null
```

