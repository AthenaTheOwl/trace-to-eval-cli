from __future__ import annotations

from pathlib import Path
from typing import Any

from .adapters import load_canonical_trace
from .io import CliDataError, load_case_file
from .paths import DEFAULT_GENERATED_AT, DEFAULT_RUN_ID


CheckResult = dict[str, str]


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = load_case_file(path)
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise CliDataError(f"{path} must contain at least one case")

    for case in cases:
        validate_case_shape(case, path)
    return cases


def validate_case_shape(case: dict[str, Any], path: Path) -> None:
    for field in ("id", "suite", "trace_id", "trace_file"):
        if not isinstance(case.get(field), str) or not case[field]:
            raise CliDataError(f"{path} case missing required string field: {field}")
    checks = case.get("checks")
    if not isinstance(checks, list) or not checks:
        raise CliDataError(f"{path} case {case['id']} must contain checks")
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get("type"), str):
            raise CliDataError(f"{path} case {case['id']} has an invalid check")


def build_report(
    case_path: Path,
    traces_dir: Path,
    *,
    run_id: str = DEFAULT_RUN_ID,
    generated_at: str = DEFAULT_GENERATED_AT,
) -> dict[str, Any]:
    cases = load_cases(case_path)
    case_results: list[dict[str, Any]] = []

    for case in cases:
        trace_path = traces_dir / case["trace_file"]
        trace = load_canonical_trace(trace_path)
        if trace["trace_id"] != case["trace_id"]:
            raise CliDataError(
                f"case {case['id']} expected trace_id {case['trace_id']} "
                f"but {trace_path} has {trace['trace_id']}"
            )

        check_results = [run_check(check, trace) for check in case["checks"]]
        status = "passed" if all(item["status"] == "passed" for item in check_results) else "failed"
        case_results.append(
            {
                "case_id": case["id"],
                "suite": case["suite"],
                "trace_id": case["trace_id"],
                "status": status,
                "check_results": check_results,
            }
        )

    summary = {
        "passed": sum(1 for item in case_results if item["status"] == "passed"),
        "failed": sum(1 for item in case_results if item["status"] == "failed"),
        "skipped": sum(1 for item in case_results if item["status"] == "skipped"),
    }
    return {
        "run_id": run_id,
        "generated_at": generated_at,
        "summary": summary,
        "case_results": case_results,
    }


def run_check(check: dict[str, Any], trace: dict[str, Any]) -> CheckResult:
    check_type = check["type"]
    value = check.get("value", check.get("pattern", ""))

    if check_type == "text_present":
        return _result(
            check_type,
            str(value) in trace["output"],
            "output contains required text",
            "output does not contain required text",
        )
    if check_type == "text_absent":
        return _result(
            check_type,
            str(value) not in trace["output"],
            "output omits forbidden text",
            "output contains forbidden text",
        )
    if check_type == "citation_span_present":
        spans = [item.get("span", "") for item in trace.get("citations", []) if isinstance(item, dict)]
        return _result(
            check_type,
            any(str(value) in span for span in spans),
            "citation span is present",
            "citation span is missing",
        )
    if check_type == "tool_call_allowed":
        names = [item.get("name", "") for item in trace.get("tool_calls", []) if isinstance(item, dict)]
        return _result(
            check_type,
            str(value) in names,
            "tool call is allowed",
            "tool call is missing",
        )
    if check_type == "refusal_required":
        refusal_terms = ("cannot comply", "I can't", "I cannot", "unable to")
        has_refusal = any(term.lower() in trace["output"].lower() for term in refusal_terms)
        expected = bool(value)
        return _result(
            check_type,
            has_refusal is expected,
            "refusal is present" if expected else "refusal was not required",
            "refusal expectation was not met",
        )

    raise CliDataError(f"unsupported check type: {check_type}")


def report_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Trace To Eval CLI Report",
        "",
        f"Run: `{report['run_id']}`",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Passed: {report['summary']['passed']}",
        f"- Failed: {report['summary']['failed']}",
        f"- Skipped: {report['summary']['skipped']}",
        "",
        "## Cases",
        "",
    ]
    for result in report["case_results"]:
        lines.append(f"- `{result['case_id']}` (`{result['suite']}`): {result['status']}")
    return "\n".join(lines) + "\n"


def compare_reports(baseline: dict[str, Any], current: dict[str, Any]) -> list[str]:
    current_by_case = {item["case_id"]: item for item in current.get("case_results", [])}
    regressions: list[str] = []
    for old in baseline.get("case_results", []):
        if old.get("status") != "passed":
            continue
        new = current_by_case.get(old["case_id"])
        if new is None:
            regressions.append(f"{old['case_id']} passed before and is missing now")
        elif new.get("status") != "passed":
            regressions.append(f"{old['case_id']} passed before and is {new.get('status')} now")
    return regressions


def _result(check_type: str, passed: bool, ok_message: str, fail_message: str) -> CheckResult:
    return {
        "type": check_type,
        "status": "passed" if passed else "failed",
        "message": ok_message if passed else fail_message,
    }

