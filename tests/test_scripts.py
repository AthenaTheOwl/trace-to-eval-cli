from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_validate_schemas_script() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_schemas.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_voice_lint_script() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/voice_lint.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

