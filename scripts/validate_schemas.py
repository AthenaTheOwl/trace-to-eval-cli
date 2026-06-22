from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SCHEMA_KEYS = {"$schema", "$id", "title", "type", "properties"}


def main() -> int:
    errors: list[str] = []
    for path in sorted((ROOT / "schemas").glob("*.json")):
        data = _load_json(path, errors)
        if isinstance(data, dict):
            missing = REQUIRED_SCHEMA_KEYS - data.keys()
            if missing:
                errors.append(f"{path}: missing schema keys {sorted(missing)}")

    for path in sorted((ROOT / "examples" / "traces" / "canonical").glob("*.json")):
        data = _load_json(path, errors)
        if isinstance(data, dict):
            for field in ("trace_id", "framework", "input", "output"):
                if not isinstance(data.get(field), str) or not data[field]:
                    errors.append(f"{path}: missing required trace field {field}")

    for path in sorted((ROOT / "reports").glob("*.json")):
        data = _load_json(path, errors)
        if isinstance(data, dict):
            for field in ("run_id", "generated_at", "summary", "case_results"):
                if field not in data:
                    errors.append(f"{path}: missing report field {field}")

    if errors:
        for error in errors:
            print(f"TTEC_SCHEMA_FAILED: {error}", file=sys.stderr)
        return 1
    print("TTEC_OK: schema and fixture files are structurally valid")
    return 0


def _load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc.msg}")
        return None


if __name__ == "__main__":
    raise SystemExit(main())

