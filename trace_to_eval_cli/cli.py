from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .adapters import ingest_langgraph_jsonl
from .io import CliDataError, dump_json, load_json
from .paths import (
    DEFAULT_CASE_PATH,
    DEFAULT_MARKDOWN_REPORT_PATH,
    DEFAULT_REPORT_PATH,
    DEFAULT_TRACES_DIR,
)
from .runner import build_report, compare_reports, report_to_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trace-to-eval")
    subcommands = parser.add_subparsers(dest="command")

    validate = subcommands.add_parser("validate", help="validate the default or provided scenario")
    validate.add_argument("--case", type=Path, default=DEFAULT_CASE_PATH)
    validate.add_argument("--traces", type=Path, default=DEFAULT_TRACES_DIR)
    validate.add_argument("--report", type=Path, default=DEFAULT_REPORT_PATH)

    run = subcommands.add_parser("run", help="run eval cases and write a report")
    run.add_argument("--case", type=Path, default=DEFAULT_CASE_PATH)
    run.add_argument("--traces", type=Path, default=DEFAULT_TRACES_DIR)
    run.add_argument("--out", type=Path, default=DEFAULT_REPORT_PATH)
    run.add_argument("--md-out", type=Path, default=DEFAULT_MARKDOWN_REPORT_PATH)

    ingest = subcommands.add_parser("ingest", help="normalize a framework trace")
    ingest.add_argument("adapter", choices=["langgraph"])
    ingest.add_argument("input", type=Path)
    ingest.add_argument("--out", type=Path, required=True)

    regress = subcommands.add_parser("regress", help="compare baseline and current reports")
    regress.add_argument("--baseline", type=Path, required=True)
    regress.add_argument("--current", type=Path, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 2

    try:
        if args.command == "validate":
            return _validate(args.case, args.traces, args.report)
        if args.command == "run":
            return _run(args.case, args.traces, args.out, args.md_out)
        if args.command == "ingest":
            return _ingest(args.adapter, args.input, args.out)
        if args.command == "regress":
            return _regress(args.baseline, args.current)
    except CliDataError as exc:
        print(f"TTEC_VALIDATION_FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"TTEC_COMMAND_FAILED: unsupported command {args.command}", file=sys.stderr)
    return 2


def _validate(case_path: Path, traces_dir: Path, report_path: Path) -> int:
    built = build_report(case_path, traces_dir)
    expected = load_json(report_path)

    expected_cases = {
        item["case_id"]: item["status"] for item in expected.get("case_results", [])
    }
    built_cases = {item["case_id"]: item["status"] for item in built.get("case_results", [])}
    if built_cases != expected_cases:
        raise CliDataError(f"computed case statuses {built_cases} do not match {report_path}")
    if built["summary"] != expected.get("summary"):
        raise CliDataError(f"computed summary {built['summary']} does not match {report_path}")

    print(
        "TTEC_OK: validated "
        f"{len(built['case_results'])} case(s) against {report_path.as_posix()}"
    )
    return 0


def _run(case_path: Path, traces_dir: Path, out_path: Path, md_out_path: Path) -> int:
    report = build_report(case_path, traces_dir)
    dump_json(out_path, report)
    md_out_path.parent.mkdir(parents=True, exist_ok=True)
    md_out_path.write_text(report_to_markdown(report), encoding="utf-8")
    print(f"TTEC_OK: wrote {out_path.as_posix()} and {md_out_path.as_posix()}")
    return 0


def _ingest(adapter: str, input_path: Path, out_path: Path) -> int:
    if adapter != "langgraph":
        raise CliDataError(f"unsupported adapter: {adapter}")
    trace = ingest_langgraph_jsonl(input_path)
    dump_json(out_path, trace)
    print(f"TTEC_OK: wrote {out_path.as_posix()}")
    return 0


def _regress(baseline_path: Path, current_path: Path) -> int:
    regressions = compare_reports(load_json(baseline_path), load_json(current_path))
    if regressions:
        for regression in regressions:
            print(f"TTEC_REGRESSION: {regression}", file=sys.stderr)
        return 1
    print("TTEC_OK: no regressions")
    return 0

