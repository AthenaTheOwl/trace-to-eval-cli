from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CliDataError(ValueError):
    """Raised when an input file is present but invalid for the CLI contract."""


def load_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    # OSError covers a directory or unreadable path passed where a file is expected
    # (IsADirectoryError on POSIX, PermissionError on Windows) as well as missing files.
    except OSError as exc:
        raise CliDataError(f"could not read file {path}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise CliDataError(f"invalid JSON in {path}: {exc.msg}") from exc


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def load_case_file(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CliDataError(f"could not read file {path}: {exc}") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise CliDataError(
                f"{path} is not JSON-compatible YAML and PyYAML is not installed"
            ) from exc
        data = yaml.safe_load(text)

    if not isinstance(data, dict):
        raise CliDataError(f"{path} must contain an object with a cases list")
    return data

