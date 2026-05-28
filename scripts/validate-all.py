#!/usr/bin/env python3
import json
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

EXAMPLES = [
    ("schemas/v0.1/promotion.schema.json", "examples/00-hello-promotion.yaml"),
    ("schemas/v0.1/promotionrun.schema.json", "examples/01-promotion-run.yaml"),
    ("schemas/v0.1/evidence.schema.json", "examples/02-evidence.yaml"),
    (
        "schemas/v0.1/conformance-profile.schema.json",
        "examples/03-conformance-profile.yaml",
    ),
    ("schemas/v0.1/binding.schema.json", "examples/04-binding.yaml"),
]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "CODE_OF_CONDUCT.md",
    "docs/README.md",
    "docs/architecture-boundaries.md",
    "docs/tool-integration.md",
    "docs/cncf-path.md",
    "spec/pri-v0.1.md",
    "spec/pri-runtime-v0.1.md",
    "spec/pri-bindings.md",
    "spec/pri-conformance.md",
    "examples/README.md",
    "examples/00-hello-promotion.yaml",
    "examples/01-promotion-run.yaml",
    "examples/02-evidence.yaml",
    "examples/03-conformance-profile.yaml",
    "examples/04-binding.yaml",
    "schemas/v0.1/promotion.schema.json",
    "schemas/v0.1/promotionrun.schema.json",
    "schemas/v0.1/evidence.schema.json",
    "schemas/v0.1/conformance-profile.schema.json",
    "schemas/v0.1/binding.schema.json",
    "scripts/validate-example.py",
    "scripts/validate-all.py",
]

format_checker = FormatChecker()


@format_checker.checks("uri")
def is_absolute_uri(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if any(char.isspace() for char in value):
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme)


@format_checker.checks("date-time")
def is_rfc3339_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return "T" in value


def validate_document(schema_path: Path, document_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text())
    document = yaml.safe_load(document_path.read_text())
    validator = Draft202012Validator(schema, format_checker=format_checker)
    errors = sorted(validator.iter_errors(document), key=lambda err: list(err.path))
    messages = []
    for err in errors:
        path = ".".join(str(part) for part in err.path) or "<root>"
        try:
            display_path = document_path.relative_to(ROOT)
        except ValueError:
            display_path = document_path
        messages.append(f"{display_path}:{path}: {err.message}")
    return messages


def check_json_schemas() -> list[str]:
    messages = []
    for schema_path in sorted((ROOT / "schemas/v0.1").glob("*.json")):
        try:
            json.loads(schema_path.read_text())
        except json.JSONDecodeError as exc:
            messages.append(f"{schema_path.relative_to(ROOT)}: invalid JSON: {exc}")
    return messages


def check_examples() -> list[str]:
    messages = []
    for schema, document in EXAMPLES:
        messages.extend(validate_document(ROOT / schema, ROOT / document))
    return messages


def check_negative_formats() -> list[str]:
    messages = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)

        bad_evidence = tmpdir / "bad-evidence.yaml"
        bad_evidence.write_text(
            (ROOT / "examples/02-evidence.yaml")
            .read_text()
            .replace("https://example.com/evidence/security-scan", "not a uri")
        )
        if not validate_document(ROOT / "schemas/v0.1/evidence.schema.json", bad_evidence):
            messages.append("negative check failed: invalid evidence URI was accepted")

        bad_run = tmpdir / "bad-promotion-run.yaml"
        bad_run.write_text(
            (ROOT / "examples/01-promotion-run.yaml")
            .read_text()
            .replace("2026-05-27T17:00:00Z", "not a timestamp", 1)
        )
        if not validate_document(ROOT / "schemas/v0.1/promotionrun.schema.json", bad_run):
            messages.append("negative check failed: invalid date-time was accepted")

    return messages


def check_conformance_scenarios() -> list[str]:
    messages = []
    for path in sorted((ROOT / "conformance/scenarios").glob("*.yaml")):
        try:
            yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            messages.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
    return messages


def check_required_files() -> list[str]:
    messages = []
    for path in REQUIRED_FILES:
        if not (ROOT / path).is_file():
            messages.append(f"{path}: required file is missing")
    return messages


def main() -> int:
    checks = [
        ("JSON schemas", check_json_schemas),
        ("examples", check_examples),
        ("negative format checks", check_negative_formats),
        ("conformance scenarios", check_conformance_scenarios),
        ("required files", check_required_files),
    ]

    failed = False
    for name, check in checks:
        messages = check()
        if messages:
            failed = True
            print(f"FAIL {name}")
            for message in messages:
                print(f"  {message}")
        else:
            print(f"OK   {name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
