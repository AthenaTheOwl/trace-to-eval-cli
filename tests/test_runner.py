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
    # Pin the emitted span to the output length (69 here). The fixture input length
    # (46) differs, so this catches a swap of len(output) for len(input).
    assert trace["spans"] == [{"name": "answer", "start": 0, "end": len(trace["output"])}]
    assert trace["spans"][0]["end"] == 69


def test_refusal_required_matches_refusal_output() -> None:
    # Pins the positive-match path so each refusal term is exercised, not only the
    # value:false branch. Corrupting a refusal term makes this fail.
    refusal_trace = {
        "trace_id": "x",
        "framework": "passthrough",
        "input": "input",
        "output": "We cannot comply with that request.",
    }
    passed = run_check({"type": "refusal_required", "value": True}, refusal_trace)
    assert passed["status"] == "passed"

    plain_trace = {
        "trace_id": "x",
        "framework": "passthrough",
        "input": "input",
        "output": "Here is the answer you asked for.",
    }
    failed = run_check({"type": "refusal_required", "value": True}, plain_trace)
    assert failed["status"] == "failed"


def test_build_report_rolls_up_mixed_checks_to_failed() -> None:
    # A case with one passing and one failing check must roll up to failed.
    # all() yields failed here; any() would yield passed, catching that mutation.
    import json
    import tempfile

    trace = {
        "trace_id": "ttec-mixed-001",
        "framework": "passthrough",
        "input": "some input",
        "output": "the vendor was approved",
    }
    case_doc = {
        "cases": [
            {
                "id": "MIXED-001",
                "suite": "mixed",
                "trace_id": "ttec-mixed-001",
                "trace_file": "mixed.json",
                "checks": [
                    {"type": "text_present", "value": "approved"},
                    {"type": "text_present", "value": "absent-text"},
                ],
            }
        ]
    }
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "mixed.json").write_text(json.dumps(trace), encoding="utf-8")
        case_path = tmp_path / "cases.json"
        case_path.write_text(json.dumps(case_doc), encoding="utf-8")

        report = build_report(case_path, tmp_path)

    assert report["case_results"][0]["status"] == "failed"
    assert report["summary"]["failed"] == 1
    assert report["summary"]["passed"] == 0

