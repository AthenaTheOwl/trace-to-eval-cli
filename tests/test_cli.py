from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_validate_no_args_succeeds() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "trace_to_eval_cli", "validate"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "TTEC_OK" in result.stdout


def test_regress_fails_when_prior_pass_fails_now() -> None:
    baseline = ROOT / "reports" / "ttec_v0_1_smoke.json"
    scratch = ROOT / "reports" / "local"
    scratch.mkdir(parents=True, exist_ok=True)
    current = scratch / "current-test.json"
    current.write_text(
        """
{
  "run_id": "current",
  "generated_at": "2026-06-22T00:00:00Z",
  "summary": {"passed": 0, "failed": 1, "skipped": 0},
  "case_results": [
    {
      "case_id": "TTEC-SMOKE-001",
      "suite": "canonical-smoke",
      "trace_id": "ttec-smoke-langgraph-001",
      "status": "failed",
      "check_results": []
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "trace_to_eval_cli",
                "regress",
                "--baseline",
                str(baseline),
                "--current",
                str(current),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        current.unlink(missing_ok=True)
    assert result.returncode == 1
    assert "TTEC_REGRESSION" in result.stderr
