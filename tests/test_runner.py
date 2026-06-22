from __future__ import annotations

from pathlib import Path

from trace_to_eval_cli.adapters import ingest_langgraph_jsonl
from trace_to_eval_cli.paths import DEFAULT_CASE_PATH, DEFAULT_REPORT_PATH, DEFAULT_TRACES_DIR
from trace_to_eval_cli.runner import build_report, run_check
from trace_to_eval_cli.io import load_json


ROOT = Path(__file__).resolve().parent.parent


def test_build_report_matches_checked_artifact() -> None:
    assert build_report(DEFAULT_CASE_PATH, DEFAULT_TRACES_DIR) == load_json(DEFAULT_REPORT_PATH)


def test_text_present_failure_is_reported() -> None:
    trace = {
        "trace_id": "x",
        "framework": "passthrough",
        "input": "input",
        "output": "plain output",
    }
    result = run_check({"type": "text_present", "value": "missing"}, trace)
    assert result == {
        "type": "text_present",
        "status": "failed",
        "message": "output does not contain required text",
    }


def test_langgraph_fixture_ingests_to_canonical_shape() -> None:
    trace = ingest_langgraph_jsonl(ROOT / "examples" / "traces" / "langgraph" / "sample.jsonl")
    assert trace["trace_id"] == "ttec-smoke-langgraph-001"
    assert trace["tool_calls"][0]["name"] == "risk_lookup"
    assert trace["citations"][0]["span"] == "approved vendors policy"

