#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate-example.py <schema.json> <document.yaml>", file=sys.stderr)
        return 2

    schema_path = Path(sys.argv[1])
    document_path = Path(sys.argv[2])
    schema = json.loads(schema_path.read_text())
    document = yaml.safe_load(document_path.read_text())

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda err: list(err.path))
    if errors:
        for err in errors:
            path = ".".join(str(part) for part in err.path) or "<root>"
            print(f"{document_path}:{path}: {err.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
