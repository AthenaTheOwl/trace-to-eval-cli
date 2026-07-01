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


def test_show_prints_ranked_readable_view() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "trace_to_eval_cli", "show"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    out = result.stdout
    # headline finding is present and the demo report's run id is shown
    assert "finding:" in out
    assert "ttec-v0.1-demo" in out
    # failing case is ranked first (before the passing cases)
    idx_fail = out.index("TTEC-DEMO-003")
    idx_pass = out.index("TTEC-DEMO-001")
    assert idx_fail < idx_pass, "failing case should rank above passing cases"


def test_summarize_report_ranks_failing_first() -> None:
    import json

    from trace_to_eval_cli.runner import summarize_report

    report = json.loads(
        (ROOT / "reports" / "ttec_v0_1_demo.json").read_text(encoding="utf-8")
    )
    view = summarize_report(report)
    assert view["summary"]["total"] == 3
    assert view["summary"]["failed"] == 1
    assert view["cases"][0]["status"] == "failed"
    assert view["cases"][0]["case_id"] == "TTEC-DEMO-003"
    # 2 passed of 3 -> 66.7. Computing from failed instead of passed yields 33.3.
    assert view["pass_rate_pct"] == 66.7


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


def test_show_directory_report_fails_cleanly() -> None:
    # A directory where a report file is expected must produce a clean error, not a
    # raw traceback. The read fails with IsADirectoryError/PermissionError (OSError).
    result = subprocess.run(
        [sys.executable, "-m", "trace_to_eval_cli", "show", "--report", str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "TTEC_VALIDATION_FAILED" in result.stderr


def test_ingest_directory_input_fails_cleanly() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trace_to_eval_cli",
            "ingest",
            "langgraph",
            str(ROOT),
            "--out",
            str(ROOT / "reports" / "local" / "ingest-dir-test.json"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "TTEC_VALIDATION_FAILED" in result.stderr


def test_regress_directory_baseline_fails_cleanly() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trace_to_eval_cli",
            "regress",
            "--baseline",
            str(ROOT),
            "--current",
            str(ROOT),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "TTEC_VALIDATION_FAILED" in result.stderr
